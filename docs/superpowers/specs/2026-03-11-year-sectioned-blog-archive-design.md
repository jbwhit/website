# Design: Year-Sectioned Blog Archive

**Date:** 2026-03-11
**Status:** Approved
**PR scope:** `blog.qmd` + SCSS — no post content changes

## Problem

The blog listing at `/blog` is a flat chronological list of 6 published posts spanning
2010–2026 (34 additional posts remain drafts). There is no visual grouping by era, and
as more drafts are published across different years the list will grow across many
distinct periods. Year headers add useful orientation with minimal friction.

## Implementation Approach

Quarto does **not** have a native `group-by: year` option. The correct approach (used by
andrewheiss.com) is **multiple listing blocks with year-based content globs**, combined
with explicit year headings in the page body. One listing block per year filters to posts
from that year via glob: `"posts/YYYY-*/index.qmd"`.

**Currently published years:** 2010, 2018, 2024, 2026

Publishing additional 2010 drafts does not require updating `blog.qmd` — the 2010 listing
block will pick them up automatically. Only publishing the first post in a *new* year
requires adding a new listing block.

## RSS Feed and Categories

With multiple listing blocks, `feed: true` and `categories: true` must be handled carefully:

- **RSS feed**: A separate hidden master listing block covers all posts and generates
  the RSS feed. It is defined in frontmatter but has no corresponding div in the body,
  so it produces no visible output. This preserves a complete cross-year RSS feed.
- **Categories sidebar**: `categories: true` goes on the master listing block, so the
  sidebar shows categories from all published posts rather than just the current year.

## Files Changed

### `blog.qmd`

Replace the single flat listing with year-sectioned listing blocks plus a hidden master
listing for RSS and categories:

```yaml
---
title: "Blog"
listing:
  # Hidden master listing: drives RSS feed and category sidebar only (no div in body)
  - id: all-posts
    contents: posts
    sort: "date desc"
    type: default
    categories: true
    feed: true

  # Year-scoped visible listings
  - id: posts-2026
    contents: "posts/2026-*/index.qmd"
    sort: "date desc"
    type: default

  - id: posts-2024
    contents: "posts/2024-*/index.qmd"
    sort: "date desc"
    type: default

  - id: posts-2018
    contents: "posts/2018-*/index.qmd"
    sort: "date desc"
    type: default

  - id: posts-2010
    contents: "posts/2010-*/index.qmd"
    sort: "date desc"
    type: default
---
```

Body:
```markdown
## 2026
:::{#posts-2026}
:::

## 2024
:::{#posts-2024}
:::

## 2018
:::{#posts-2018}
:::

## 2010
:::{#posts-2010}
:::
```

The `all-posts` listing block has a corresponding div in the body that is immediately
hidden with CSS. Quarto requires every listing `id` to have a matching div target —
omitting it may cause a render error or warning. Include the div and suppress it:

```markdown
:::{#all-posts style="display:none"}
:::
```

### `custom.scss` and `custom-dark.scss`

The existing `h2` rule already adds `border-bottom` and appropriate styling via Fraunces.
Inspect the rendered output to confirm the year headings look intentional.

If the hidden `all-posts` listing block renders visibly, suppress it:
```scss
#all-posts { display: none; }
```

If `h2` style conflicts with other heading uses on the blog page (e.g., inside post
description previews), scope the year heading rule:
```scss
// Quarto wraps listing page content in .quarto-listing-container
// If needed, add spacing above year headings
.quarto-listing h2 {
  margin-top: 2.5rem;
}
.quarto-listing h2:first-child {
  margin-top: 0;
}
```
Exact selectors depend on the rendered DOM — inspect before writing rules.

### `index.qmd`

No changes. The home page recent-posts listing shows only 3 posts and benefits from
staying compact.

## Non-Goals

- No `group-by` config hack (not a valid Quarto option)
- No custom EJS templates
- No changes to post content or frontmatter
- No changes to the home page listing

## Success Criteria

- Blog page shows `## 2026`, `## 2024`, `## 2018`, `## 2010` headings, each followed
  by their respective posts
- Year headings use Fraunces font (inherited from existing `h2` rule) and match Gruvbox palette
- Light and dark modes both look intentional
- Category sidebar shows categories from all published posts (not just 2026)
- RSS feed (`blog.xml`) includes all published posts across all years
- Hidden `all-posts` listing block produces no visible output on the page
- Mobile layout at 375px: year headings not clipped, no horizontal scroll
- No layout regressions on the home page

## Risks

- The `all-posts` div uses inline `style="display:none"` — if Quarto strips inline
  styles, add `#all-posts { display: none; }` to SCSS as a fallback
- Year-glob `posts/2026-*/index.qmd` depends on the post directory naming convention
  (`YYYY-MM-DD-slug`) being consistent — it is, for all current posts
- The existing global `h2` SCSS rule may need scoping if post description previews
  contain `h2` elements

## Maintenance Note

When the first post of a new year (e.g., 2027) is published, add to `blog.qmd`:
1. `## 2027` heading and `:::{#posts-2027}:::` div at the top of the body
2. A new listing block: `id: posts-2027`, `contents: "posts/2027-*/index.qmd"`
Do NOT add `feed: true` or `categories: true` to new year blocks — those stay on
the `all-posts` master listing only.
