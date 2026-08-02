from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_reports() -> list[dict]:
    text = (ROOT / "assets/data-6.js").read_text(encoding="utf-8")
    match = re.search(r"\.concat\((.*)\);\s*$", text, re.S)
    if not match:
        raise AssertionError("data-6.js does not contain a JSON concat payload")
    return json.loads(match.group(1))


class DailyEditionIntegrityTests(unittest.TestCase):
    def test_august_2_contains_31_complete_reports(self) -> None:
        reports = load_reports()
        self.assertEqual(31, len(reports))
        self.assertEqual(31, len({report["slug"] for report in reports}))
        for report in reports:
            self.assertEqual("2026-08-02", report["editionDate"])
            self.assertGreaterEqual(len(report["body"]), 4)
            self.assertGreaterEqual(len(report["summary"]), 60)
            self.assertTrue(report["categories"])
            self.assertTrue(report["tags"])
            self.assertTrue(report["sources"])
            self.assertTrue((ROOT / f"2026/08/02/reports/{report['slug']}.html").exists())
            self.assertTrue((ROOT / f"content/ja/2026-08-02/{report['slug']}.md").exists())

    def test_grouped_layout_renders_every_august_2_report_once(self) -> None:
        script = r"""
const fs = require('fs');
global.window = {XNEWS_ARTICLES: []};
const raw = fs.readFileSync('assets/data-6.js', 'utf8');
eval(raw);
delete global.window;
const {arrangeEdition} = require('./assets/site.js');
const result = arrangeEdition(globalThis.__unused || []);
const reports = JSON.parse(raw.match(/\.concat\((.*)\);\s*$/s)[1]);
const layout = arrangeEdition(reports);
const slugs = [layout.lead.slug, ...layout.featured.map(x => x.slug), ...layout.groups.flatMap(g => g.items.map(x => x.slug))];
console.log(JSON.stringify({count: slugs.length, unique: new Set(slugs).size, featured: layout.featured.length, groups: layout.groups.filter(g => g.items.length).length}));
"""
        result = subprocess.run(["node", "-e", script], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(31, payload["count"])
        self.assertEqual(31, payload["unique"])
        self.assertEqual(4, payload["featured"])
        self.assertGreaterEqual(payload["groups"], 5)

    def test_august_1_mapping_remains_29(self) -> None:
        renderer = (ROOT / "assets/site.js").read_text(encoding="utf-8")
        match = re.search(r'"2026-08-01":(\[.*?\]),\n"2026-08-02"', renderer, re.S)
        self.assertIsNotNone(match)
        self.assertEqual(29, len(json.loads(match.group(1))))

    def test_wordpress_manifest_contains_all_posts_and_index(self) -> None:
        reports = load_reports()
        manifest = (ROOT / "wordpress/ja/2026-08-02/wordpress.yml").read_text(encoding="utf-8")
        for report in reports:
            self.assertIn(f"  - {report['slug']}.md", manifest)
        self.assertIn("  - index.md", manifest)
        self.assertEqual(32, len(re.findall(r"^  - .*\.md$", manifest, re.M)))

    def test_japanese_index_no_longer_says_eight(self) -> None:
        index = (ROOT / "content/ja/2026-08-02/index.md").read_text(encoding="utf-8")
        self.assertIn("31件", index)
        self.assertNotIn("8件", index)


if __name__ == "__main__":
    unittest.main()
