#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import json
import re
import shutil
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS_DIR = ROOT / ".upgrade"
WORKFLOW = ROOT / ".github/workflows/apply-bilingual-upgrade.yml"
SCRIPT = ROOT / "tools/apply_bilingual_upgrade.py"


def safe_extract(data: bytes) -> None:
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            target = (ROOT / member.name).resolve()
            if ROOT.resolve() not in target.parents and target != ROOT.resolve():
                raise RuntimeError(f"unsafe archive path: {member.name}")
        archive.extractall(ROOT)


def parse_js(path: Path, variable: str) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    pattern = rf"window\.{re.escape(variable)}=\(window\.{re.escape(variable)}\|\|\[\]\)\.concat\((\[.*\])\);$"
    match = re.fullmatch(pattern, text, flags=re.S)
    if not match:
        raise RuntimeError(f"invalid JS wrapper: {path}")
    value = json.loads(match.group(1))
    if not isinstance(value, list):
        raise RuntimeError(f"invalid JS payload: {path}")
    return value


def validate() -> None:
    zh: list[dict] = []
    ja: list[dict] = []
    for index in range(1, 6):
        zh.extend(parse_js(ROOT / f"assets/data-{index}.js", "XNEWS_ARTICLES"))
        ja.extend(parse_js(ROOT / f"assets/ja-data-{index}.js", "XNEWS_JA_ARTICLES"))
    if len(zh) != 29 or len(ja) != 29:
        raise RuntimeError(f"article count mismatch: zh={len(zh)}, ja={len(ja)}")
    zh_slugs = [item["slug"] for item in zh]
    ja_slugs = [item["slug"] for item in ja]
    if len(set(zh_slugs)) != 29 or len(set(ja_slugs)) != 29:
        raise RuntimeError("duplicate slug")
    if set(zh_slugs) != set(ja_slugs):
        raise RuntimeError("bilingual slug mismatch")
    for item in zh:
        if len(item.get("summary", "")) < 70:
            raise RuntimeError(f"Chinese summary too short: {item['slug']}")
        if len(item.get("body", [])) < 4:
            raise RuntimeError(f"Chinese body too short: {item['slug']}")
    for item in ja:
        summary = item.get("summary", "")
        body = item.get("body", [])
        body_chars = sum(len(paragraph) for paragraph in body)
        if len(summary) < 90:
            raise RuntimeError(f"Japanese summary too short: {item['slug']}")
        if item.get("level") == "focus":
            if len(body) < 5 or body_chars < 480:
                raise RuntimeError(f"Japanese focus article too short: {item['slug']}")
        else:
            if len(body) < 4 or body_chars < 350:
                raise RuntimeError(f"Japanese standard article too short: {item['slug']}")
    content_dir = ROOT / "content/ja/2026-08-01"
    article_files = sorted(path for path in content_dir.glob("*.md") if path.name not in {"index.md", "briefs.md"})
    if len(article_files) != 29:
        raise RuntimeError(f"Japanese Markdown count mismatch: {len(article_files)}")
    for path in article_files:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            raise RuntimeError(f"missing front matter: {path}")
        if f"slug: {path.stem}\n" not in text:
            raise RuntimeError(f"slug mismatch: {path}")
        if "date: 2026-08-01T06:00:00+09:00" not in text:
            raise RuntimeError(f"publish time mismatch: {path}")
        if "excerpt:" not in text or "## 出典" not in text:
            raise RuntimeError(f"missing excerpt or sources: {path}")
    index = (content_dir / "index.md").read_text(encoding="utf-8")
    if index.count("./") < 30:
        raise RuntimeError("daily index links incomplete")
    print(json.dumps({
        "validated": 29,
        "chinese_summary_min": min(len(item["summary"]) for item in zh),
        "japanese_summary_min": min(len(item["summary"]) for item in ja),
        "japanese_markdown": len(article_files),
    }, ensure_ascii=False, indent=2))


def main() -> int:
    parts = sorted(PARTS_DIR.glob("part-*.txt"))
    if len(parts) != 6:
        raise RuntimeError(f"expected 6 archive parts, found {len(parts)}")
    values = []
    for path in parts:
        value = path.read_text(encoding="ascii").strip()
        values.append(value)
        print(f"PART {path.name} length={len(value)} sha256={hashlib.sha256(value.encode()).hexdigest()}")
    encoded = "".join(values)
    print(f"TOTAL length={len(encoded)}")
    safe_extract(base64.b64decode(encoded, validate=True))
    validate()
    shutil.rmtree(PARTS_DIR)
    SCRIPT.unlink(missing_ok=True)
    WORKFLOW.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
