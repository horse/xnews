from __future__ import annotations

import json
import re
import subprocess
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DailyEditionIntegrityTests(unittest.TestCase):
    def test_frontend_renderer_is_date_aware(self) -> None:
        renderer = (ROOT / "assets/site.js").read_text(encoding="utf-8")
        self.assertNotIn("/2026/08/02/", renderer)
        self.assertIn('"2026-08-01"', renderer)
        self.assertIn('"2026-08-02"', renderer)

    def test_august_1_grouped_layout_renders_every_report_once(self) -> None:
        script = textwrap.dedent(
            """
            global.window = {XNEWS_ARTICLES: []};
            for (const name of ['data-1.js','data-2.js','data-3.js','data-4.js','data-5.js']) {
              require('./assets/' + name);
            }
            const layout = require('./assets/site.js');
            const slugs = layout.EDITIONS['2026-08-01'];
            const bySlug = Object.fromEntries(window.XNEWS_ARTICLES.map(article => [article.slug, article]));
            const articles = slugs.map(slug => bySlug[slug]).filter(Boolean);
            const arranged = layout.arrangeEdition(articles);
            const rendered = [arranged.lead, ...arranged.featured, ...arranged.groups.flatMap(group => group.items)].filter(Boolean);
            const unique = new Set(rendered.map(article => article.slug));
            if (articles.length !== 29) throw new Error(`expected 29 source articles, got ${articles.length}`);
            if (rendered.length !== 29) throw new Error(`expected 29 rendered articles, got ${rendered.length}`);
            if (unique.size !== 29) throw new Error(`expected 29 unique articles, got ${unique.size}`);
            if (arranged.featured.length !== 4) throw new Error(`expected 4 featured articles, got ${arranged.featured.length}`);
            if (arranged.groups.filter(group => group.items.length).length < 4) throw new Error('expected at least four non-empty editorial groups');
            """
        )
        result = subprocess.run(
            ["node", "-e", script],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)

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
