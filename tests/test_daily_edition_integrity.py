from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DailyEditionIntegrityTests(unittest.TestCase):
    def test_frontend_renderer_is_date_aware(self) -> None:
        renderer = (ROOT / "assets/site.js").read_text(encoding="utf-8")
        self.assertNotIn("/2026/08/02/", renderer)
        self.assertIn('"2026-08-01"', renderer)
        self.assertIn('"2026-08-02"', renderer)

    def test_august_2_public_data_contains_eight_complete_reports(self) -> None:
        text = (ROOT / "assets/data-6.js").read_text(encoding="utf-8")
        match = re.search(r"\.concat\((.*)\);\s*$", text, re.S)
        self.assertIsNotNone(match)
        reports = json.loads(match.group(1))
        self.assertEqual(8, len(reports))
        self.assertEqual(8, len({report["slug"] for report in reports}))
        for report in reports:
            self.assertEqual("2026-08-02", report["editionDate"])
            self.assertGreaterEqual(len(report["body"]), 4)
            self.assertGreaterEqual(len(report["summary"]), 60)
            self.assertTrue(report["sources"])

    def test_august_2_wordpress_manifest_replaces_failed_five_story_edition(self) -> None:
        manifest = (ROOT / "wordpress/ja/2026-08-02/wordpress.yml").read_text(encoding="utf-8")
        for stale in ("july-heat-low-rain.md", "water-day-2026.md", "treasure-ig-arena.md", "metopoli-summer-festival.md"):
            self.assertNotIn(stale, manifest)
        for slug in ("fgo-fes-2026-day1", "engei8-2026", "sakura-miko-8th-anniversary",
                     "vnl-men-semifinal-2026", "koshien-draw-2026", "srw-35th-stream",
                     "liella-tutorial-live-2026", "tif2026-august1"):
            self.assertIn(f"{slug}.md", manifest)
            self.assertTrue((ROOT / f"content/ja/2026-08-02/{slug}.md").exists())

    def test_august_1_archive_no_longer_advertises_briefs(self) -> None:
        archive = (ROOT / "2026/08/01/index.html").read_text(encoding="utf-8")
        self.assertNotIn("简讯", archive)


if __name__ == "__main__":
    unittest.main()
