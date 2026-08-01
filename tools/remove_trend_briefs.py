#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/superpowers/plans/2026-08-01-remove-trend-briefs.md"
WORKFLOW = ROOT / ".github/workflows/remove-trend-briefs.yml"
SCRIPT = Path(__file__).resolve()

DELETE_PATHS = [
    ROOT / "content/ja/2026-08-01/briefs.md",
    ROOT / "2026/08/01/briefs.html",
    ROOT / "ja/2026/08/01/briefs.html",
]

BANNED_TERMS = [
    "briefs.html",
    "briefs.md",
    "renderBriefs",
    "トレンド短報",
    "趋势简讯",
    "短報26件",
    "26条简讯",
    "条趋势简讯",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected_files() -> list[Path]:
    paths: list[Path] = []
    for index in range(1, 6):
        paths.append(ROOT / f"assets/data-{index}.js")
        paths.append(ROOT / f"assets/ja-data-{index}.js")

    article_dir = ROOT / "content/ja/2026-08-01"
    article_markdown = sorted(
        path for path in article_dir.glob("*.md")
        if path.name not in {"index.md", "briefs.md"}
    )
    if len(article_markdown) != 29:
        raise RuntimeError(f"expected 29 Japanese article Markdown files, found {len(article_markdown)}")
    paths.extend(article_markdown)

    chinese_pages = sorted((ROOT / "2026/08/01/reports").glob("*.html"))
    if len(chinese_pages) != 29:
        raise RuntimeError(f"expected 29 Chinese article pages, found {len(chinese_pages)}")
    paths.extend(chinese_pages)

    japanese_pages = sorted((ROOT / "ja/2026/08/01").glob("*/index.html"))
    if len(japanese_pages) != 29:
        raise RuntimeError(f"expected 29 Japanese article pages, found {len(japanese_pages)}")
    paths.extend(japanese_pages)
    return paths


def snapshot(paths: list[Path]) -> dict[str, str]:
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.exists()]
    if missing:
        raise RuntimeError(f"protected files missing: {missing}")
    return {str(path.relative_to(ROOT)): digest(path) for path in paths}


def remove_meta_briefs(path: Path, variable: str) -> None:
    text = path.read_text(encoding="utf-8").strip()
    prefix = f"window.{variable}="
    if not text.startswith(prefix) or not text.endswith(";"):
        raise RuntimeError(f"unexpected metadata wrapper: {path}")
    payload = json.loads(text[len(prefix):-1])
    if "briefs" not in payload:
        raise RuntimeError(f"briefs key missing before removal: {path}")
    del payload["briefs"]
    path.write_text(
        prefix + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";",
        encoding="utf-8",
    )


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return result


def update_chinese_site() -> None:
    path = ROOT / "assets/site.js"
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "const D=window.XNEWS_META, S=D.site, A=window.XNEWS_ARTICLES||[], B=D.briefs;",
        "const D=window.XNEWS_META, S=D.site, A=window.XNEWS_ARTICLES||[];",
        "remove Chinese briefs variable",
    )
    text = replace_once(
        text,
        "${A.length}篇独立报道与${B.length}条简讯，覆盖",
        "${A.length}篇独立报道，覆盖",
        "remove Chinese home brief count",
    )
    text = replace_once(
        text,
        '<a href="${S.base}/2026/08/01/">8月1日完整日报</a><a href="${S.base}/2026/08/01/briefs.html">趋势简讯</a>',
        '<a href="${S.base}/2026/08/01/">8月1日完整日报</a>',
        "remove Chinese home brief link",
    )
    text = replace_once(
        text,
        "以下日报将能够核实的事件整理为独立新闻，并把较分散的话题集中列入简讯。",
        "以下日报将能够核实的事件整理为独立新闻。",
        "remove Chinese edition brief copy",
    )
    text = replace_once(
        text,
        '<span>${B.length}条简讯</span>',
        "",
        "remove Chinese edition brief statistic",
    )
    text = regex_once(
        text,
        r'\n <h2 class="section-title">趋势简讯</h2><article class="story"><h2><a href="\$\{S\.base\}/2026/08/01/briefs\.html">\$\{B\.length\}条趋势简讯</a></h2>\n <p>汇集当天受到关注、但适合以短篇形式记录的作品、人名、活动和社群话题。</p></article>',
        "",
        "remove Chinese edition brief section",
    )
    text = regex_once(
        text,
        r'\nfunction renderBriefs\(\)\{.*?\n\}\nfunction renderCategories\(\)\{',
        "\nfunction renderCategories(){",
        "remove Chinese brief renderer",
    )
    text = replace_once(
        text,
        "article:renderArticle,briefs:renderBriefs,categories:renderCategories",
        "article:renderArticle,categories:renderCategories",
        "remove Chinese brief route",
    )
    path.write_text(text, encoding="utf-8")


def update_japanese_site() -> None:
    path = ROOT / "assets/ja-site.js"
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "const M=window.XNEWS_JA_META,S=M.site,A=window.XNEWS_JA_ARTICLES||[],B=M.briefs;",
        "const M=window.XNEWS_JA_META,S=M.site,A=window.XNEWS_JA_ARTICLES||[];",
        "remove Japanese briefs variable",
    )
    text = replace_once(
        text,
        "主要ニュース10本、その他19本、短報26件。",
        "主要ニュース10本、その他19本。",
        "remove Japanese home brief count",
    )
    text = replace_once(
        text,
        '<span>短報26件</span>',
        "",
        "remove Japanese edition brief statistic",
    )
    text = regex_once(
        text,
        r'<h2 class="section-title">トレンド短報</h2><article class="story"><h2><a href="\$\{S\.jaBase\}/2026/08/01/briefs\.html">26件の短報</a></h2><p>人物、作品、活動、コミュニティーの話題を短く整理した。</p></article>',
        "",
        "remove Japanese edition brief section",
    )
    text = regex_once(
        text,
        r'\nfunction briefs\(\)\{.*?\}\nfunction cats\(\)\{',
        "\nfunction cats(){",
        "remove Japanese brief renderer",
    )
    text = replace_once(
        text,
        "({home,edition,article,briefs,categories:cats,tags}",
        "({home,edition,article,categories:cats,tags}",
        "remove Japanese brief route",
    )
    path.write_text(text, encoding="utf-8")


def update_daily_markdown() -> None:
    path = ROOT / "content/ja/2026-08-01/index.md"
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'\n## トレンド短報\n\n短報は \[`briefs\.md`\]\(\./briefs\.md\) にまとめた。\n?$',
        "\n",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"daily Markdown brief section: expected one match, found {count}")
    path.write_text(updated, encoding="utf-8")


def update_wordpress_manifest() -> None:
    path = ROOT / "wordpress/ja/2026-08-01/wordpress.yml"
    text = path.read_text(encoding="utf-8")
    text = replace_once(text, "  - briefs.md\n", "", "remove WordPress brief source")
    post_lines = [line for line in text.splitlines() if line.startswith("  - ")]
    if len(post_lines) != 30:
        raise RuntimeError(f"expected 30 WordPress sources after removal, found {len(post_lines)}")
    if post_lines[-1] != "  - index.md":
        raise RuntimeError("daily edition must remain the final WordPress source")
    path.write_text(text, encoding="utf-8")


def remove_files() -> None:
    for path in DELETE_PATHS:
        if not path.exists():
            raise RuntimeError(f"expected public brief file missing before deletion: {path.relative_to(ROOT)}")
        path.unlink()


def scan_for_residue() -> None:
    matches: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for term in BANNED_TERMS:
            if term in text:
                matches.append(f"{path.relative_to(ROOT)}: {term}")
    if matches:
        raise RuntimeError("public brief residue remains:\n" + "\n".join(matches))


def validate_metadata() -> None:
    for path, variable in [
        (ROOT / "assets/data-meta.js", "XNEWS_META"),
        (ROOT / "assets/ja-meta.js", "XNEWS_JA_META"),
    ]:
        text = path.read_text(encoding="utf-8").strip()
        prefix = f"window.{variable}="
        payload = json.loads(text[len(prefix):-1])
        if "briefs" in payload:
            raise RuntimeError(f"briefs metadata remains: {path}")


def main() -> int:
    protected = protected_files()
    before = snapshot(protected)

    remove_meta_briefs(ROOT / "assets/data-meta.js", "XNEWS_META")
    remove_meta_briefs(ROOT / "assets/ja-meta.js", "XNEWS_JA_META")
    update_chinese_site()
    update_japanese_site()
    update_daily_markdown()
    update_wordpress_manifest()
    remove_files()

    for temporary in [PLAN, WORKFLOW, SCRIPT]:
        temporary.unlink(missing_ok=True)

    after = snapshot(protected)
    if before != after:
        changed = sorted(key for key in before if before[key] != after[key])
        raise RuntimeError(f"protected news content changed unexpectedly: {changed}")

    validate_metadata()
    scan_for_residue()

    print(json.dumps({
        "preserved_chinese_articles": 29,
        "preserved_japanese_articles": 29,
        "wordpress_sources": 30,
        "deleted_repository_files": [str(path.relative_to(ROOT)) for path in DELETE_PATHS],
        "public_brief_residue": 0,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
