# Remove Trend Briefs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Permanently remove the public trend-brief layer from XNEWS while preserving all 29 bilingual news articles, the bilingual daily editions, taxonomy, sources, slugs, and publication timestamps.

**Architecture:** Delete the brief source files and generated pages, remove all brief data and rendering branches from both language sites, remove the brief item from the WordPress publication manifest, and use the existing authenticated WordPress REST workflow to permanently delete only the `2026-08-01-briefs` post. Trend collection remains private editorial input; unpromoted topics stay private as hold/noise/unconfirmed.

**Tech Stack:** Static HTML/JavaScript, YAML, Markdown, Python WordPress REST publisher, GitHub Actions.

## Global Constraints

- Preserve all 29 Chinese and 29 Japanese news articles without title, body, slug, category, tag, source, or timestamp changes.
- Preserve both daily-edition posts and pages.
- Permanently delete the WordPress post with slug `2026-08-01-briefs`.
- Remove public short-brief pages, links, counts, data, and publication steps.
- Keep raw trend collection and rejected/unconfirmed signals private in `xnews-editorial`.

---

### Task 1: Remove public brief data and rendering

- Delete `content/ja/2026-08-01/briefs.md`, `2026/08/01/briefs.html`, and `ja/2026/08/01/briefs.html`.
- Remove brief arrays and brief-related copy from the Chinese and Japanese metadata files.
- Remove brief render functions, links, counts, and sections from `assets/site.js` and `assets/ja-site.js`.
- Remove the trend-brief section from `content/ja/2026-08-01/index.md`.

### Task 2: Remove briefs from publishing workflow

- Remove `briefs.md` from `wordpress/ja/2026-08-01/wordpress.yml`.
- Add a one-time authenticated deletion action for the WordPress slug `2026-08-01-briefs`, with `force=true`.
- Verify the manifest validates exactly 30 publication sources: 29 articles plus the daily edition.

### Task 3: Update editorial process

- Record in `xnews-editorial` that public briefs are discontinued.
- Keep trend capture private; classify non-article items only as hold, noise, unconfirmed, or merged.
- Remove any instruction that generates a public briefs file or page.

### Task 4: Verify preservation and deletion

- Confirm 29 Chinese and 29 Japanese article slugs remain identical.
- Confirm the daily edition remains and no brief link/count/text remains in public source.
- Confirm the WordPress deletion workflow returns deletion of `2026-08-01-briefs` and does not update or delete other posts.
- Confirm the old GitHub Pages brief files no longer exist.
