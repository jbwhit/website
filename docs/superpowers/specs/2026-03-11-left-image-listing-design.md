# Design: Left-Image Post Listing

**Date:** 2026-03-11
**Status:** Approved
**PR scope:** `blog.qmd`, `index.qmd`, `assets/images/`, SCSS — no post content changes

## Problem

The blog listing and home page recent-posts listing show posts as text-only rows
(date, title, description). Posts that contain figures or images have a natural visual
asset that is currently invisible in the listing. Adding thumbnails makes the listing
more scannable and visually engaging, consistent with silviacanelon.com's image-left +
text-right card layout.

## How Quarto Finds Thumbnail Images

Quarto's listing image extraction (`findPreviewImgEl`) uses the following priority order:

1. `image:` frontmatter field (explicit path)
2. `img.preview-image` class on an element in the post
3. `div.preview-image div.cell-output-display img` (code cell with that class)
4. Any local image whose filename matches `preview|feature|cover|thumbnail`
5. **Last-resort fallback**: the first local `<img>` in `#quarto-document-content`
   that does not start with `http:` or `https:`

**Currently published posts and expected thumbnail behavior:**

| Post | Image in post | Expected thumbnail source |
|---|---|---|
| military-strategy (2026) | `uccello-san-romano.jpg` (frontmatter) | Rule 1: explicit `image:` field |
| mathacademy (2024) | `tradeoff.png` (inline) | Rule 5: first local img fallback |
| cname-fix (2024) | `githubsettings.png` (inline) | Rule 5: first local img fallback |
| talent-vs-luck (2018) | matplotlib figures (generated) | Rule 5: first rendered figure (requires full render) |
| monty-hall-monte-carlo (2010) | matplotlib figures (generated) | Rule 5: first rendered figure (requires full render) |
| making-money-monty-hall (2010) | `monty_open_door.svg` (inline) | Rule 5: first local img fallback |

All 6 currently published posts have images. The placeholder will apply to future
posts published without any images.

**Important**: posts with generated matplotlib figures (talent-vs-luck, monty-hall-monte-carlo)
only have their figures available after a full `quarto render`. The listing will not
find their thumbnails on a single-page or incremental render. See Risks.

## Files Changed

### `blog.qmd`

Add image-related fields and options to each listing block.

**If this PR lands before PR 1 (year-sectioned)**, the single flat listing becomes:
```yaml
listing:
  contents: posts
  sort: "date desc"
  type: default
  categories: true
  feed: true
  fields: [image, date, title, description, categories]
  image-height: "120px"
  image-placeholder: assets/images/post-placeholder.svg
```

**If this PR lands after PR 1 (year-sectioned)**, add `fields`, `image-height`, and
`image-placeholder` to each per-year listing block. Use this `fields` list for all
year blocks: `[image, date, title, description, categories]`. Do NOT add `fields` to
the hidden `all-posts` master listing — it drives RSS and categories only and should
not change its output format.

### `index.qmd`

Add `image` to fields and set image options on the recent-posts listing:

```yaml
listing:
  id: recent-posts
  contents: posts
  sort: "date desc"
  type: default
  max-items: 3
  fields: [image, date, title, description]
  image-height: "100px"
  image-placeholder: assets/images/post-placeholder.svg
```

### `assets/images/post-placeholder.svg`

Create a minimal SVG for posts without any images. Specifications:
- `viewBox="0 0 160 120"` (4:3 ratio)
- Background rect: Gruvbox gray `#a89984`
- Subtle foreground pattern in `#928374` (e.g., diagonal lines spaced 20px apart)
- No text, no icons — purely decorative
- Neutral enough to work against both the light page background (`#f9f5d7`) and
  dark page background (`#1d2021`) — the gray mid-tone achieves this

### `custom.scss` and `custom-dark.scss`

Add listing image styling to ensure consistent crop:

```scss
// Listing thumbnail — prevent stretch, ensure consistent crop
.quarto-post .thumbnail img {
  object-fit: cover;
  width: 100%;
  height: 100%;
}
```

Exact selector should be confirmed against rendered output. No border-radius changes.

## Non-Goals

- No manual `image:` frontmatter additions to existing posts
- No per-post image creation beyond the single shared placeholder SVG
- No changes to post content
- `image-height` values are starting points — tune after visual inspection

## Success Criteria

- Blog listing renders each post with an image on the left and text on the right
- military-strategy shows `uccello-san-romano.jpg`
- mathacademy shows `tradeoff.png`, cname-fix shows `githubsettings.png`
- making-money-monty-hall shows `monty_open_door.svg`
- talent-vs-luck and monty-hall-monte-carlo show their first matplotlib figure
  (verified after a full `quarto render`, not an incremental render)
- Home page recent-posts listing also shows thumbnails
- Thumbnails are consistently sized; no visible stretch or letterboxing
- The placeholder SVG renders cleanly against both light and dark page backgrounds
- Light and dark modes both render cleanly
- No YAML validation warnings from `image-height` string value
- Mobile layout is not broken (Quarto's default type is responsive)

## Risks

- **Generated figure availability**: talent-vs-luck and monty-hall-monte-carlo require
  a full `quarto render` to populate `index_files/figure-html/`. In CI (GitHub Actions
  publish workflow), the full render runs before deploy, so production will be correct.
  Local incremental renders may show the placeholder instead — this is expected and
  not a bug.
- **`image-height` type**: Quarto schema allows both string (`"120px"`) and number
  (`120`) in different contexts. If YAML validation warns, switch to the integer form.
- **First matplotlib figure quality**: The first generated figure may be a small
  diagnostic plot rather than the main figure. If this happens for a specific post,
  add `{.preview-image}` to the desired image in that post's source. This does not
  change the spec — it is a per-post adjustment.
- **PR ordering**: If PR 1 (year-sectioned) is merged first, apply image fields to
  each per-year listing block in `blog.qmd`. The spec covers both orderings above.
