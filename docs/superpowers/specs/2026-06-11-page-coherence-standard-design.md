# Site-Wide Page Coherence Standard — Design

**Status:** Approved design, pending spec review
**Date:** 2026-06-11
**Author:** Jonathan Whitmore (with Claude)
**Trigger:** The `projects/checklists/` index page renders a blue `title-block-banner` that no other page on the site uses — surfaced during a review of jonathanwhitmore.com.

**Review provenance:** (to be appended — Codex xhigh review per the project Review & Approval Protocol)

---

## Goal

Establish and document a two-archetype page styling standard for the Quarto site, then bring every page into compliance. The concrete result: the checklists section stops being a visual outlier, and future pages have a written rule to follow.

## Background / Audit findings

The theme foundation is already coherent and is **not** changing:

- Gruvbox Light Hard palette; `$primary` = gruvbox blue `#076678`; dark mode mirrors via `custom-dark.scss`.
- Fonts: Fraunces (headings), Source Sans Pro (body), Source Code Pro (mono), loaded globally via `includes/fonts.html`.
- The navbar is filled with `$primary` (blue) site-wide.

The incoherence is entirely at the **page-frontmatter** level and traces to one root cause: the checklists *index* is dressed like an article when it is actually a section-landing page.

Current state:

| Page | Role | Banner | Date/Categories | TOC |
|------|------|--------|-----------------|-----|
| `index.qmd` (home) | landing | none | none | none (page-layout: full) |
| `about.qmd` | landing | none | none | none |
| `blog.qmd` | landing | none | none | none |
| `projects/talks/index.qmd` | landing | none | none | right (9 year-sections) |
| `projects/physics-quals/index.qmd` | landing | none | none | none (3 headings) |
| `projects/checklists/index.qmd` | landing | **banner** | **date + categories** | **left** (page-layout: full) |
| `projects/checklists/investing.qmd` | article | none | dated | **left** |
| `projects/checklists/did.qmd` | article | none | dated | **left** |
| blog posts (`posts/**`) | article | none | dated | right (margin notes via `_metadata.yml`) |

`title-block-banner: true` renders in `$primary` — the *same blue as the navbar* — stacked directly beneath it, producing a doubled blue header that appears on the checklists index and nowhere else. The banner is the visible symptom; the `date`, `categories`, `toc-location: left`, and `page-layout: full` on that index page are the same article-vs-landing confusion.

## The standard

**Two page archetypes. Keep frontmatter consistent with the archetype.**

### Landing pages (navigational / index)
Home, blog, about, and every `projects/*/index.qmd`.
- Plain title block: **no `title-block-banner`**.
- **No `date`, no `categories`** (these signal "article" and render a dated byline).
- `page-layout: full` **only** for the home page (`index.qmd`), for its hero. All other landing pages use the default article width.
- TOC only when the page has several (~4+) navigable sections.

### Article pages (long-form, dated)
Blog posts and individual checklists (`investing.qmd`, `did.qmd`).
- Keep `date` and `categories`.
- TOC on the **right** (Quarto default). **Never set `toc-location: left`.**
- Per-page `toc-title` is allowed (a content label, not a placement choice).

### TOC rule (both archetypes)
Include a TOC when the page has ~4+ navigable sections; placement is always default/right; `toc-location: left` is never used.

## Changes required

The audit confirms checklists is the sole outlier, so the changes are surgical — **three files, all in the checklists subtree.** Everything else is already compliant.

### 1. `projects/checklists/index.qmd` → clean landing page
Remove from frontmatter: `title-block-banner: true`, `date: 2024-07-04`, the `categories:` line, `toc: true`, `toc-location: left`, and `page-layout: full`.
Keep: `title`, `description`, `aliases`, and the full `listing:` block (including `id: listing-listing`).

Target frontmatter:
```yaml
---
title: "Checklists for Decision Making and Analysis"
description: "A collection of curated checklists for various domains including investing and research methodologies."
aliases:
  - /checklists.html
listing:
  id: listing-listing
  contents:
    - "investing.qmd"
    - "did.qmd"
  type: default
  sort: "title"
  categories: true
  sort-ui: false
  filter-ui: false
  fields: [title, description, categories]
  feed: false
---
```

### 2. `projects/checklists/investing.qmd` → TOC to default right
Remove only `toc-location: left`. Keep `date`, `categories`, `toc: true`, `toc-title: Checklist Sections`, the `aliases`, and the `format.html` block.

Target frontmatter:
```yaml
---
title: "Investment Evaluation Checklist"
description: "A systematic checklist to evaluate potential investments by assessing key financial, operational, and strategic factors."
date: 2024-07-04
categories: [Investing, Finance]
aliases:
  - /checklists/investing.html
toc: true
toc-title: Checklist Sections
format:
  html:
    code-fold: true
    code-summary: "Show the code"
---
```

### 3. `projects/checklists/did.qmd` → TOC to default right
Remove only `toc-location: left`. Keep everything else (parallel to investing.qmd).

Target frontmatter:
```yaml
---
title: "Difference-in-Differences (DiD) Checklist"
description: "A comprehensive checklist for conducting Difference-in-Differences analysis in econometrics and causal inference."
date: 2024-07-04
categories: [Econometrics, Causal Inference, Research Methods]
aliases:
  - /checklists/difference-in-differences.html
toc: true
toc-title: Checklist Sections
format:
  html:
    code-fold: true
    code-summary: "Show the code"
---
```

### 4. Document the standard in `CLAUDE.md`
Add a `### Page archetypes & styling` subsection under "Content Conventions" in the project `CLAUDE.md`, codifying the landing-vs-article rules and the explicit warning not to add `title-block-banner` (it stacks a second blue band under the navbar).

## Non-changes (already compliant — do not touch)
- `index.qmd` (home): plain title, no banner/date, `page-layout: full` for hero — correct.
- `about.qmd`, `blog.qmd`: plain landings — correct.
- `projects/talks/index.qmd`: plain landing with a right-side TOC justified by 9 year-sections — correct.
- `projects/physics-quals/index.qmd`: plain landing, no TOC (3 headings) — correct.
- Blog posts and `posts/_metadata.yml` (margin notes, `reference-location: margin`, `grid.margin-width`) — correct.

## Verification
1. `QUARTO_PROFILE=drafts QUARTO_PYTHON=.venv/bin/python quarto render` (or full `quarto render`) succeeds with no errors.
2. Visual check of the rendered checklists index: no blue banner, no dated byline, listing renders at article width directly under its heading.
3. Visual check of investing/did pages: TOC appears on the right.
4. Confirm the `/checklists.html` and `/checklists/*.html` aliases still resolve (frontmatter `aliases` retained).
5. Confirm the listing still renders its two items with category tags (the listing's own `categories: true` is independent of the index page's removed `categories`).

## Out of scope (explicit)
- **Theme/SCSS changes.** The palette, fonts, navbar, and dark mode are not modified.
- **External project microsites.** `clocks`, `discoverneptune`, and `habitable-zone-black-holes` live in separate repositories with their own themes. Establishing a shared visual identity across the main site and those microsites (shared theme extraction, cross-repo branding, cross-links) is a **separate effort** that warrants its own brainstorming cycle and spec. This spec covers only the `website` repo's internal page consistency.
