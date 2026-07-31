# XNEWS Static Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Publish a mobile-friendly static Japanese X trend news site at GitHub Pages with one page per article and a daily archive.

**Architecture:** Plain static HTML and one shared CSS file are stored on the main branch. GitHub Actions uploads the repository root as a Pages artifact. Each daily edition lives under YYYY/MM/DD and links to independent article pages.

**Tech Stack:** HTML5, CSS, GitHub Actions, GitHub Pages.

## Global Constraints

- Publication window will be 06:00 JST to 06:00 JST.
- Target publication time is 07:00 JST.
- Trend popularity is not represented as a population opinion poll.
- News prose must not expose collection or clustering implementation details.

---

### Task 1: Create shared site shell
- Create `assets/style.css`, `index.html`, `about.html`, and `.nojekyll`.
- Verify all internal links include the `/xnews/` project prefix.

### Task 2: Create first daily edition
- Create `2026/08/01/index.html`.
- Create one HTML page per article.
- Verify every article links back to the daily index.

### Task 3: Configure deployment
- Create `.github/workflows/pages.yml` using the official Pages actions.
- Push to main and verify the Pages workflow.
