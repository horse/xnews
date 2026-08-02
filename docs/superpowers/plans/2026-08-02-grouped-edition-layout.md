# Grouped Edition Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restore the August 1 edition's layered visual organization while displaying all 29 reports exactly once.

**Architecture:** Keep article data unchanged. Add a pure layout function in `assets/site.js` that selects one lead, four additional focus reports, and assigns every remaining report to one ordered editorial group. Use the same function in the edition renderer and expose it to Node for verification.

**Tech Stack:** ES6 JavaScript, Python unittest, Node.js.

## Global Constraints

- Every August 1 report must appear exactly once.
- Do not expose selection or scoring data.
- Preserve existing article URLs and content.
- Use the existing card and section CSS classes.

### Task 1: Add a failing layout integrity test

**Files:**
- Modify: `tests/test_daily_edition_integrity.py`

- [ ] Add a Node-backed test that loads the five August 1 data files and calls `arrangeEdition` from `assets/site.js`.
- [ ] Assert 29 rendered items, 29 unique slugs, one lead, four featured reports, and non-empty editorial sections.
- [ ] Run the test and confirm it fails because `arrangeEdition` is not exported.

### Task 2: Implement grouped edition layout

**Files:**
- Modify: `assets/site.js`

- [ ] Add ordered editorial group rules.
- [ ] Add and export `arrangeEdition(articles)`.
- [ ] Replace the edition long-list renderer with lead, focus grid, and grouped sections.
- [ ] Ensure every report is consumed once through a `Set`.
- [ ] Run all tests and Node syntax checks.

### Task 3: Refresh the August 1 page cache key

**Files:**
- Modify: `2026/08/01/index.html`

- [ ] Update asset version query strings.
- [ ] Verify the page still loads all six data files and the renderer.
