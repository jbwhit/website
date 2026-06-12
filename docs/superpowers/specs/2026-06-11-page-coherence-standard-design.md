# Site-Wide Page Coherence Standard — Design

**Status:** Implemented 2026-06-12 (PR #12, squash-merged to main; Codex xhigh on the final diff: READY TO MERGE)
**Date:** 2026-06-11
**Author:** Jonathan Whitmore (with Claude)
**Trigger:** The `projects/checklists/` index page renders a blue `title-block-banner` that no other page on the site uses — surfaced during a review of jonathanwhitmore.com.

**Review provenance:** Codex xhigh, 2 rounds. Round 1: NOT SOUND — caught that `_quarto.yml` sets `toc: true` globally, so the original "no TOC on landing pages" rule was unsound and the audit's TOC column was wrong. Revised to keep the global TOC and treat left-placement as the only TOC inconsistency; added removal of the duplicate body title. Round 2: **SOUND ENOUGH TO IMPLEMENT** (two cosmetic wording nits, fixed inline).

---

## Goal

Establish and document a two-archetype page styling standard for the Quarto site, then bring every page into compliance. The concrete result: the checklists section stops being a visual outlier, and future pages have a written rule to follow.

## Background / Audit findings

The theme foundation is already coherent and is **not** changing:

- Gruvbox Light Hard palette; `$primary` = gruvbox blue `#076678`; dark mode mirrors via `custom-dark.scss`.
- Fonts: Fraunces (headings), Source Sans Pro (body), Source Code Pro (mono), loaded globally via `includes/fonts.html`.
- The navbar is filled with `$primary` (blue) site-wide.

The incoherence is entirely at the **page-frontmatter** level and traces to one root cause: the checklists *index* is dressed like an article when it is actually a section-landing page.

Current state (TOC column verified against rendered `_site` HTML — `_quarto.yml` sets `toc: true` **globally**, so every page with headings gets a right-side TOC by default):

| Page | Role | Banner | Date/Categories | TOC (actual) |
|------|------|--------|-----------------|-----|
| `index.qmd` (home) | landing | none | none | global default; not displayed (page-layout: full) |
| `about.qmd` | landing | none | none | right, 1 item |
| `blog.qmd` | landing | none | none | none rendered (year `##` headings come from the listing layout) |
| `projects/talks/index.qmd` | landing | none | none | right, 9 items |
| `projects/physics-quals/index.qmd` | landing | none | none | right, 3 items |
| `projects/checklists/index.qmd` | landing | **banner** | **date + categories** | **left**, 3 items (page-layout: full) |
| `projects/checklists/investing.qmd` | article | none | dated | **left** |
| `projects/checklists/did.qmd` | article | none | dated | **left** |
| blog posts (`posts/**`) | article | none | dated | right (margin notes via `_metadata.yml`) |

`title-block-banner: true` renders in `$primary` — the *same blue as the navbar* — stacked directly beneath it, producing a doubled blue header that appears on the checklists index and nowhere else. The banner is the visible symptom; the `date`, `categories`, and `page-layout: full` on that index page are the same article-vs-landing confusion.

**The only TOC inconsistency is placement:** the checklists subtree forces `toc-location: left`; every other page uses the default right. The global `toc: true` is left as-is — a short right-side TOC on landing pages is the existing, consistent behavior and is not in scope to suppress.

## The standard

**Two page archetypes. Keep frontmatter consistent with the archetype.**

### Landing pages (navigational / index)
Home, blog, about, and every `projects/*/index.qmd`.
- Plain title block: **no `title-block-banner`**.
- **No `date`, no `categories`** (these signal "article" and render a dated byline).
- `page-layout: full` **only** for the home page (`index.qmd`), for its hero. All other landing pages use the default article width.
- Body should not repeat the frontmatter `title` as a top-level `#` heading.

### Article pages (long-form, dated)
Blog posts and individual checklists (`investing.qmd`, `did.qmd`).
- Keep `date` and `categories`.
- Per-page `toc-title` is allowed (a content label, not a placement choice).

### TOC rule (both archetypes)
Keep Quarto's global `toc: true` default — a TOC renders on the **right** for any page with headings. **Never set `toc-location: left`.** Do not add per-page `toc: false`; suppressing short TOCs on landing pages is intentionally out of scope (it would touch pages that are otherwise compliant, and a short right-side TOC is the existing consistent behavior).

## Changes required

The audit confirms checklists is the sole outlier, so the changes are surgical — **three files in the checklists subtree, plus a documentation edit to `CLAUDE.md`.** Everything else is already compliant.

### 1. `projects/checklists/index.qmd` → clean landing page
Remove from frontmatter: `title-block-banner: true`, `date: 2024-07-04`, the `categories:` line, `toc: true`, `toc-location: left`, and `page-layout: full`.
Keep: `title`, `description`, `aliases`, and the full `listing:` block (including `id: listing-listing`).
Also remove the **duplicate body `# Checklists for Decision Making and Analysis` heading** (line ~25) — with the banner gone the frontmatter `title` is the page heading, so the body `#` would render a second identical title. The intro paragraph becomes the first body content. The `## Available Checklists` / `## Using These Checklists` / `## Contributing` sections stay, producing a 3-item right-side TOC from the global default — identical to the physics-quals page.

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
- `about.qmd`, `blog.qmd`: plain landings — correct. (About keeps its 1-item right TOC from the global default; not worth suppressing.)
- `projects/talks/index.qmd`: plain landing with a right-side TOC (9 year-sections) — correct.
- `projects/physics-quals/index.qmd`: plain landing, right-side TOC (3 sections) — correct. This is exactly the target shape for the checklists index after the change.
- Blog posts and `posts/_metadata.yml` (margin notes, `reference-location: margin`, `grid.margin-width`) — correct.
- The global `toc: true` in `_quarto.yml` stays.

## Verification
1. `QUARTO_PYTHON=.venv/bin/python quarto render` succeeds with no errors.
2. Rendered checklists index: no blue banner, no dated byline, no duplicate title, listing renders at article width directly under the (frontmatter) heading, and a 3-item TOC appears on the **right** (grep `_site/projects/checklists/index.html` for `<nav id="TOC"` and confirm it is not the left/sidebar variant — matches `_site/projects/physics-quals/index.html`).
3. Rendered investing/did pages: TOC appears on the right, not left.
4. Confirm the `/checklists.html` and `/checklists/*.html` aliases still resolve (frontmatter `aliases` retained → check for the generated redirect stubs in `_site`).
5. Confirm the listing still renders its two items with category tags (the listing's own `categories: true` is independent of the index page's removed `categories`).

## Out of scope (explicit)
- **Theme/SCSS changes.** The palette, fonts, navbar, and dark mode are not modified.
- **External project microsites.** `clocks`, `discoverneptune`, and `habitable-zone-black-holes` live in separate repositories with their own themes. Establishing a shared visual identity across the main site and those microsites (shared theme extraction, cross-repo branding, cross-links) is a **separate effort** that warrants its own brainstorming cycle and spec. This spec covers only the `website` repo's internal page consistency.
