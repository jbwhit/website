# Design: TIL Section

**Date:** 2026-03-16
**Status:** Approved
**PR scope:** `til/`, `til.qmd`, `_quarto.yml`, move `posts/2024-07-11-cname-fix/` — no changes to blog

## Problem

Short tech-note posts (e.g., the CNAME fix) don't fit comfortably alongside longer essay-style blog posts. A dedicated TIL (Today I Learned) section gives lightweight reference notes their own home in the nav, keeps the blog listing focused on substantive content, and signals to readers what kind of content to expect in each section.

## Approach

Standalone `til/` directory with directory-per-post structure (matching `posts/`). A `til.qmd` listing page with a flat date-descending layout. No RSS feed — TIL is display-only. Blog RSS and listing are unchanged. The existing CNAME fix post is moved from `posts/` to `til/` with alias redirects preserving both old URLs.

## Files Changed

### New: `til/` directory

```
til/
├── _metadata.yml
└── 2024-07-11-cname-fix/
    ├── index.qmd
    └── githubsettings.png
```

Each TIL post lives at `til/YYYY-MM-DD-slug/index.qmd`. The directory-per-post structure allows images and data files alongside the post.

### New: `til/_metadata.yml`

Shared defaults for all TIL posts — mirrors `posts/_metadata.yml`:

```yaml
format:
  html:
    grid:
      margin-width: 350px
    toc-depth: 2
reference-location: margin
citation-location: margin
execute:
  echo: false
  warning: false
```

### New: `til.qmd`

```yaml
---
title: "TIL"
listing:
  id: til-posts
  contents: "til/*/index.qmd"
  sort: "date desc"
  type: default
  categories: true
  fields: [image, date, title, description, categories]
  image-height: "120px"
  image-placeholder: assets/images/post-placeholder.svg
---

:::{#til-posts}
:::
```

Flat listing — no year sections yet. Add year-sectioning (same pattern as `blog.qmd`) when the volume warrants it.

### Modified: `_quarto.yml`

Add to the render list:
```yaml
- "til/**/*.qmd"
- "til/**/*.ipynb"
```

Add navbar entry between Blog and Projects:
```yaml
- text: TIL
  href: til.qmd
```

### Moved: `posts/2024-07-11-cname-fix/` → `til/2024-07-11-cname-fix/`

Update frontmatter:
- Add `til` to categories
- Expand aliases to cover both old URLs:

```yaml
aliases:
  - /posts/2024-07-11-cname-github-pages/
  - /posts/2024-07-11-cname-fix/
```

## Non-Goals

- No RSS feed for TIL (blog RSS unchanged)
- No changes to `blog.qmd`, `index.qmd`, or any existing posts
- No year-sectioning of the TIL listing at launch
- No content edits to the moved CNAME post

## Success Criteria

- `/til` renders a listing of TIL posts with thumbnails and category filter
- "TIL" appears in the navbar between Blog and Projects
- `/posts/2024-07-11-cname-fix/` and `/posts/2024-07-11-cname-github-pages/` both redirect to `/til/2024-07-11-cname-fix/`
- Blog listing and RSS are unchanged
- Light and dark modes both render cleanly

## Maintenance Note

When publishing the first TIL post of a new year, the flat listing handles it automatically — no `til.qmd` changes needed. Add year-sectioning only if the listing grows long enough that year headings add meaningful orientation (rough threshold: 15+ posts).
