# Left-Image Post Listing Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add thumbnail images to the blog listing and home page recent-posts listing, using Quarto's auto-extraction of the first local image in each post as the thumbnail source.

**Architecture:** Add `fields`, `image-height`, and `image-placeholder` to the Quarto listing configs in `blog.qmd` and `index.qmd`. Create a single shared SVG placeholder for posts with no images. Add `object-fit: cover` SCSS to ensure consistent thumbnail cropping. This PR is independent of PR 1 (year-sectioned) but includes notes for both orderings.

**Tech Stack:** Quarto 1.8.27, SVG, SCSS. No JavaScript. No per-post changes.

---

## Chunk 1: Create the placeholder SVG

**Files:**
- Create: `assets/images/post-placeholder.svg`

### Task 1: Create the placeholder SVG

- [ ] **Step 1: Create the SVG file**

  Write `assets/images/post-placeholder.svg`:

  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120" width="160" height="120">
    <rect width="160" height="120" fill="#a89984"/>
    <line x1="0" y1="20" x2="20" y2="0" stroke="#928374" stroke-width="1.5"/>
    <line x1="0" y1="40" x2="40" y2="0" stroke="#928374" stroke-width="1.5"/>
    <line x1="0" y1="60" x2="60" y2="0" stroke="#928374" stroke-width="1.5"/>
    <line x1="0" y1="80" x2="80" y2="0" stroke="#928374" stroke-width="1.5"/>
    <line x1="0" y1="100" x2="100" y2="0" stroke="#928374" stroke-width="1.5"/>
    <line x1="0" y1="120" x2="120" y2="0" stroke="#928374" stroke-width="1.5"/>
    <line x1="20" y1="120" x2="140" y2="0" stroke="#928374" stroke-width="1.5"/>
    <line x1="40" y1="120" x2="160" y2="0" stroke="#928374" stroke-width="1.5"/>
    <line x1="60" y1="120" x2="160" y2="20" stroke="#928374" stroke-width="1.5"/>
    <line x1="80" y1="120" x2="160" y2="40" stroke="#928374" stroke-width="1.5"/>
    <line x1="100" y1="120" x2="160" y2="60" stroke="#928374" stroke-width="1.5"/>
    <line x1="120" y1="120" x2="160" y2="80" stroke="#928374" stroke-width="1.5"/>
    <line x1="140" y1="120" x2="160" y2="100" stroke="#928374" stroke-width="1.5"/>
  </svg>
  ```

  This is a 4:3 rectangle in Gruvbox gray (`#a89984`) with subtle diagonal hatching
  in a slightly darker gray (`#928374`). Purely decorative, no text or icons.

- [ ] **Step 2: Verify the SVG opens correctly**

  ```bash
  open assets/images/post-placeholder.svg
  ```

  Expected: a gray rectangle with diagonal lines. Confirm it looks neutral and
  unobtrusive — not like a broken image icon.

- [ ] **Step 3: Commit**

  ```bash
  git add assets/images/post-placeholder.svg
  git commit -m "feat: add Gruvbox-toned placeholder SVG for posts without images

  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
  ```

---

## Chunk 2: Update listing configs in `blog.qmd` and `index.qmd`

**Files:**
- Modify: `blog.qmd`
- Modify: `index.qmd`

### Task 2: Update `blog.qmd`

**Two scenarios depending on whether PR 1 (year-sectioned) has been merged first.**
Check by running: `grep "posts-2026" blog.qmd` — if it matches, PR 1 is already merged.

- [ ] **Step 1a (if PR 1 NOT yet merged): Add image fields to the single flat listing**

  Current `blog.qmd` listing block:
  ```yaml
  listing:
    contents: posts
    sort: "date desc"
    type: default
    categories: true
    feed: true
  ```

  Replace with:
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

- [ ] **Step 1b (if PR 1 IS already merged): Add image fields to each year listing block**

  Add `fields`, `image-height`, and `image-placeholder` to each of the four year-scoped
  listing blocks (`posts-2026`, `posts-2024`, `posts-2018`, `posts-2010`). Do NOT add
  these to the hidden `all-posts` master listing.

  Each year block becomes:
  ```yaml
  - id: posts-YYYY
    contents: "posts/YYYY-*/index.qmd"
    sort: "date desc"
    type: default
    fields: [image, date, title, description, categories]
    image-height: "120px"
    image-placeholder: assets/images/post-placeholder.svg
  ```

### Task 3: Update `index.qmd`

- [ ] **Step 1: Add image fields to the recent-posts listing**

  Current listing in `index.qmd`:
  ```yaml
  listing:
    id: recent-posts
    contents: posts
    sort: "date desc"
    type: default
    max-items: 3
    fields: [date, title, description]
  ```

  Replace with:
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

- [ ] **Step 2: Render both pages to check for YAML errors**

  ```bash
  QUARTO_PYTHON=.venv/bin/python quarto render blog.qmd
  QUARTO_PYTHON=.venv/bin/python quarto render index.qmd
  ```

  Expected: both render without errors or YAML validation warnings.
  If you see a warning about `image-height`, change `"120px"` to `120` (integer, no quotes)
  in both files and re-render.

- [ ] **Step 3: Commit**

  ```bash
  git add blog.qmd index.qmd
  git commit -m "feat: add image fields to blog and home page listing configs

  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
  ```

---

## Chunk 3: SCSS for consistent thumbnail cropping

**Files:**
- Modify: `custom.scss`
- Modify: `custom-dark.scss`

### Task 4: Add thumbnail CSS

- [ ] **Step 1: Inspect rendered HTML to find the thumbnail image selector**

  ```bash
  python3 -c "
  with open('_site/blog.html') as f:
      content = f.read()
  import re
  # Find img tags in listing context
  matches = re.findall(r'<div class=\"[^\"]*thumbnail[^\"]*\">.*?</div>', content, re.DOTALL)
  for m in matches[:2]:
      print(m[:300])
      print('---')
  "
  ```

  Note the exact class hierarchy around the `<img>` tag in listing post cards.
  Common Quarto selectors: `.quarto-post .thumbnail img` or `.listing-item .thumbnail img`.

- [ ] **Step 2: Add thumbnail CSS to `custom.scss`**

  Add after the existing `.cell-output-stdout` rule at the bottom of `custom.scss`:

  ```scss
  // Listing thumbnails — consistent crop, prevent stretch
  .quarto-post .thumbnail img {
    object-fit: cover;
    width: 100%;
    height: 100%;
  }
  ```

  If Step 1 revealed a different selector, use that instead.

- [ ] **Step 3: Mirror to `custom-dark.scss`**

  Add the identical rule to `custom-dark.scss` (same location, after `.cell-output-stdout`).

- [ ] **Step 4: Commit**

  ```bash
  git add custom.scss custom-dark.scss
  git commit -m "style: add object-fit: cover to listing thumbnails

  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
  ```

---

## Chunk 4: Full render verification and push

### Task 5: Full render, visual check, and push

- [ ] **Step 1: Full site render**

  ```bash
  QUARTO_PYTHON=.venv/bin/python quarto render 2>&1 | grep -E 'ERROR|WARN'
  ```

  Expected: no ERRORs. Investigate any warnings.

- [ ] **Step 2: Verify thumbnail extraction for each published post**

  ```bash
  python3 -c "
  import re, os

  posts = {
      'military-strategy': '_site/posts/2026-02-08-military-strategy-reading-program/index.html',
      'mathacademy': '_site/posts/2024-09-10-MathAcademy-after-2000-points/index.html',
      'cname-fix': '_site/posts/2024-07-11-cname-github-pages/index.html',
      'talent-vs-luck': '_site/posts/2018-03-12-talent-vs-luck/index.html',
      'monty-hall-monte-carlo': '_site/posts/2010-11-26-monty-hall-monte-carlo-python/index.html',
      'making-money-monty-hall': '_site/posts/2010-11-24-making-money-with-monty-hall/index.html',
  }

  for name, path in posts.items():
      if os.path.exists(path):
          content = open(path).read()
          imgs = re.findall(r'<img[^>]+src=\"([^\"]+)\"', content)
          local = [i for i in imgs if not i.startswith('http')]
          print(f'{name}: first local img = {local[0] if local else \"NONE\"}')
      else:
          print(f'{name}: rendered file not found at {path}')
  "
  ```

  Then check that the blog listing HTML references those same images as thumbnails:

  ```bash
  python3 -c "
  with open('_site/blog.html') as f:
      content = f.read()
  import re
  # Find all img src values in listing cards
  imgs = re.findall(r'<img[^>]+src=\"([^\"]+)\"[^>]*class=\"[^\"]*thumbnail[^\"]*\"', content)
  if not imgs:
      # Try other order of attributes
      imgs = re.findall(r'class=\"[^\"]*thumbnail[^\"]*\"[^>]*src=\"([^\"]+)\"', content)
  print('Thumbnail images in blog listing:', imgs)
  "
  ```

  Expected: 6 thumbnail paths, none being the placeholder SVG (all current posts have images).
  If any post shows the placeholder, the post likely wasn't fully rendered — run
  `QUARTO_PYTHON=.venv/bin/python quarto render posts/<post-slug>/index.qmd` for that
  post first, then re-render `blog.qmd`.

- [ ] **Step 3: Visual check in browser**

  Open `_site/blog.html`. Verify:
  - Each post shows a thumbnail on the left, text on the right
  - Thumbnails are consistently sized (not stretched or distorted)
  - Toggle dark mode — thumbnails still look clean
  - Open `_site/index.html` — home page recent-posts also shows thumbnails
  - Resize to ~375px width — layout remains usable (Quarto default type is responsive)

- [ ] **Step 4: Push and verify CI**

  ```bash
  git push
  gh run watch --exit-status
  ```

  Expected: GitHub Actions publish workflow completes. Visit the live site to confirm
  thumbnails appear on the deployed blog page.
