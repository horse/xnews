#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import mistune
import yaml

REQUIRED_META = ("title", "slug", "categories", "tags")


def parse_markdown_file(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML front matter")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError(f"{path}: malformed YAML front matter")
    meta_text = parts[0][4:]
    meta = yaml.safe_load(meta_text) or {}
    if not isinstance(meta, dict):
        raise ValueError(f"{path}: front matter must be a mapping")
    body = parts[1]
    if body.startswith("\n"):
        body = body[1:]
    for key in REQUIRED_META:
        if key not in meta:
            raise ValueError(f"{path}: missing required field {key}")
    if not isinstance(meta["categories"], list) or not meta["categories"]:
        raise ValueError(f"{path}: categories must be a non-empty list")
    if not isinstance(meta["tags"], list):
        raise ValueError(f"{path}: tags must be a list")
    return meta, body


def wordpress_dates(publish_at: str) -> tuple[str, str]:
    dt = datetime.fromisoformat(publish_at)
    if dt.tzinfo is None:
        raise ValueError("publish_at must include a UTC offset")
    local = dt.replace(tzinfo=None).isoformat(timespec="seconds")
    gmt = dt.astimezone(timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")
    return local, gmt


def normalize_application_password(value: str) -> str:
    """Remove display whitespace from a WordPress application password."""
    return "".join(value.split())


def rewrite_internal_markdown_links(body: str, published_links: dict[str, str]) -> str:
    pattern = re.compile(r"\(\./([A-Za-z0-9_-]+)\.md\)")

    def replace(match: re.Match[str]) -> str:
        slug = match.group(1)
        return f"({published_links.get(slug, match.group(0)[1:-1])})"

    return pattern.sub(replace, body)


def markdown_to_html(body: str) -> str:
    renderer = mistune.HTMLRenderer(escape=False)
    markdown = mistune.create_markdown(renderer=renderer, plugins=["strikethrough", "table"])
    return markdown(body)


def build_post_payload(
    *,
    meta: dict[str, Any],
    html: str,
    publish_at: str,
    category_ids: list[int],
    tag_ids: list[int],
    default_status: str,
    comment_status: str,
    ping_status: str,
    author_id: int | None = None,
) -> dict[str, Any]:
    local, gmt = wordpress_dates(publish_at)
    payload: dict[str, Any] = {
        "title": meta["title"],
        "slug": meta["slug"],
        "status": default_status,
        "content": html,
        "excerpt": meta.get("excerpt", ""),
        "date": local,
        "date_gmt": gmt,
        "categories": category_ids,
        "tags": tag_ids,
        "format": "standard",
        "comment_status": comment_status,
        "ping_status": ping_status,
        "sticky": False,
    }
    if author_id is not None:
        payload["author"] = author_id
    return payload


@dataclass
class WordpressClient:
    site_url: str
    username: str
    application_password: str

    def __post_init__(self) -> None:
        self.site_url = self.site_url.rstrip("/")
        self.application_password = normalize_application_password(
            self.application_password
        )
        token = base64.b64encode(
            f"{self.username}:{self.application_password}".encode("utf-8")
        ).decode("ascii")
        self.auth_header = f"Basic {token}"

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        query: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self.site_url}/wp-json/wp/v2/{endpoint.lstrip('/')}"
        if query:
            url += "?" + urlencode(query, doseq=True)
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": self.auth_header,
                "Accept": "application/json",
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "XNEWS-WordPress-Publisher/1.0",
            },
        )
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"WordPress API {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"WordPress connection failed: {exc.reason}") from exc

    def ensure_term(self, taxonomy: str, name: str) -> int:
        results = self.request("GET", taxonomy, query={"search": name, "per_page": 100})
        for item in results:
            if item.get("name") == name:
                return int(item["id"])
        created = self.request("POST", taxonomy, payload={"name": name})
        return int(created["id"])

    def find_post_by_slug(self, slug: str) -> dict[str, Any] | None:
        results = self.request(
            "GET",
            "posts",
            query={"slug": slug, "status": "any", "context": "edit", "per_page": 1},
        )
        return results[0] if results else None

    def upsert_post(self, payload: dict[str, Any]) -> dict[str, Any]:
        existing = self.find_post_by_slug(str(payload["slug"]))
        if existing:
            return self.request("POST", f"posts/{existing['id']}", payload=payload)
        return self.request("POST", "posts", payload=payload)


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    required = (
        "content_dir",
        "publish_at",
        "status",
        "comment_status",
        "ping_status",
        "posts",
    )
    for key in required:
        if key not in manifest:
            raise ValueError(f"{path}: missing manifest field {key}")
    if not isinstance(manifest["posts"], list) or not manifest["posts"]:
        raise ValueError(f"{path}: posts must be a non-empty list")
    publish_at = manifest["publish_at"]
    if isinstance(publish_at, datetime):
        manifest["publish_at"] = publish_at.isoformat(timespec="seconds")
    else:
        manifest["publish_at"] = str(publish_at)
    wordpress_dates(manifest["publish_at"])
    return manifest


def load_entries(manifest_path: Path) -> list[tuple[Path, dict[str, Any], str]]:
    manifest = load_manifest(manifest_path)
    root = manifest_path.parents[3]
    content_dir = root / str(manifest["content_dir"])
    entries: list[tuple[Path, dict[str, Any], str]] = []
    seen_slugs: set[str] = set()
    for item in manifest["posts"]:
        path = content_dir / str(item)
        if not path.is_file():
            raise ValueError(f"missing Markdown file: {path}")
        meta, body = parse_markdown_file(path)
        slug = str(meta["slug"])
        if slug in seen_slugs:
            raise ValueError(f"duplicate slug: {slug}")
        seen_slugs.add(slug)
        entries.append((path, meta, body))
    return entries


def publish(manifest_path: Path, *, dry_run: bool) -> int:
    manifest = load_manifest(manifest_path)
    entries = load_entries(manifest_path)
    if dry_run:
        print(
            json.dumps(
                {
                    "validated": len(entries),
                    "publish_at": manifest["publish_at"],
                    "status": manifest["status"],
                    "slugs": [meta["slug"] for _, meta, _ in entries],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    site_url = os.environ.get("WP_SITE_URL", "").strip()
    username = os.environ.get("WP_USERNAME", "").strip()
    password = normalize_application_password(
        os.environ.get("WP_APPLICATION_PASSWORD", "")
    )
    if not site_url or not username or not password:
        raise RuntimeError(
            "WP_SITE_URL, WP_USERNAME and WP_APPLICATION_PASSWORD are required"
        )
    author_id_text = os.environ.get("WP_AUTHOR_ID", "").strip()
    author_id = int(author_id_text) if author_id_text else None
    client = WordpressClient(site_url, username, password)
    published_links: dict[str, str] = {}

    for _, meta, body in entries:
        category_ids = [client.ensure_term("categories", str(x)) for x in meta["categories"]]
        tag_ids = [client.ensure_term("tags", str(x)) for x in meta["tags"]]
        rewritten = rewrite_internal_markdown_links(body, published_links)
        payload = build_post_payload(
            meta=meta,
            html=markdown_to_html(rewritten),
            publish_at=str(manifest["publish_at"]),
            category_ids=category_ids,
            tag_ids=tag_ids,
            default_status=str(manifest["status"]),
            comment_status=str(manifest["comment_status"]),
            ping_status=str(manifest["ping_status"]),
            author_id=author_id,
        )
        result = client.upsert_post(payload)
        published_links[str(meta["slug"])] = str(result.get("link", ""))
        print(f"published {meta['slug']}: {result.get('link', '')}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Publish XNEWS Markdown to WordPress")
    parser.add_argument(
        "manifest",
        type=Path,
        nargs="?",
        default=Path("wordpress/ja/2026-08-01/wordpress.yml"),
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="send posts to WordPress; without this flag only validate and print a plan",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return publish(args.manifest, dry_run=not args.publish)
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
