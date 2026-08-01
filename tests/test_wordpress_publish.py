import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.wordpress_publish import (
    build_post_payload,
    load_manifest,
    normalize_application_password,
    parse_markdown_file,
    rewrite_internal_markdown_links,
    wordpress_dates,
)


class WordpressPublishTests(unittest.TestCase):
    def test_parse_markdown_file_reads_front_matter_and_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.md"
            path.write_text(
                "---\n"
                'title: "見出し"\n'
                "slug: sample\n"
                "status: publish\n"
                "categories:\n  - 国際\n"
                "tags:\n  - 円相場\n"
                "---\n\n本文です。\n",
                encoding="utf-8",
            )
            meta, body = parse_markdown_file(path)
        self.assertEqual(meta["title"], "見出し")
        self.assertEqual(meta["slug"], "sample")
        self.assertEqual(body, "本文です。\n")

    def test_wordpress_dates_convert_tokyo_six_am_to_utc(self):
        local, gmt = wordpress_dates("2026-08-01T06:00:00+09:00")
        self.assertEqual(local, "2026-08-01T06:00:00")
        self.assertEqual(gmt, "2026-07-31T21:00:00")

    def test_normalize_application_password_removes_all_whitespace(self):
        self.assertEqual(
            normalize_application_password("abcd efgh\nijkl\tmnop"),
            "abcdefghijklmnop",
        )

    def test_rewrite_internal_markdown_links_uses_published_links(self):
        body = "[記事](./yen-intervention.md) と [短報](./briefs.md)"
        links = {
            "yen-intervention": "https://example.jp/yen-intervention/",
            "briefs": "https://example.jp/briefs/",
        }
        rewritten = rewrite_internal_markdown_links(body, links)
        self.assertEqual(
            rewritten,
            "[記事](https://example.jp/yen-intervention/) と [短報](https://example.jp/briefs/)",
        )

    def test_load_manifest_normalizes_yaml_timestamp_to_string(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "wordpress.yml"
            path.write_text(
                "content_dir: content\n"
                "publish_at: 2026-08-01T06:00:00+09:00\n"
                "status: publish\n"
                "comment_status: closed\n"
                "ping_status: closed\n"
                "posts: [sample.md]\n",
                encoding="utf-8",
            )
            manifest = load_manifest(path)
        self.assertEqual(manifest["publish_at"], "2026-08-01T06:00:00+09:00")

    def test_build_post_payload_maps_publish_fields(self):
        meta = {
            "title": "見出し",
            "slug": "sample",
            "excerpt": "要約",
            "status": "publish",
        }
        payload = build_post_payload(
            meta=meta,
            html="<p>本文</p>",
            publish_at="2026-08-01T06:00:00+09:00",
            category_ids=[3],
            tag_ids=[8, 9],
            default_status="publish",
            comment_status="closed",
            ping_status="closed",
        )
        self.assertEqual(payload["date"], "2026-08-01T06:00:00")
        self.assertEqual(payload["date_gmt"], "2026-07-31T21:00:00")
        self.assertEqual(payload["status"], "publish")
        self.assertEqual(payload["categories"], [3])
        self.assertEqual(payload["tags"], [8, 9])
        self.assertEqual(payload["comment_status"], "closed")
        self.assertEqual(payload["ping_status"], "closed")
        self.assertFalse(payload["sticky"])


if __name__ == "__main__":
    unittest.main()
