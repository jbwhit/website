# Year-Sectioned Blog Archive Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the flat blog listing with year-sectioned groups (2026, 2024, 2018, 2010) using multiple Quarto listing blocks and a hidden master listing for RSS/categories.

**Architecture:** `blog.qmd` is rewritten to contain one listing block per published year plus a hidden `all-posts` master block. Each year block uses a content glob `"posts/YYYY-*/index.qmd"` to filter posts. Year headings are `h2` elements styled by the existing Fraunces/Gruvbox SCSS rules. The hidden master block drives the RSS feed and category sidebar.

**Tech Stack:** Quarto 1.8.27, SCSS (compiled by Quarto), no JavaScript required.

---

## Chunk 1: Rewrite `blog.qmd` with year-sectioned listing blocks

**Files:**
- Modify: `blog.qmd`

### Task 1: Rewrite `blog.qmd`

- [ ] **Step 1: Read the current `blog.qmd`**

  Current content:
  ```yaml
  ---
  title: "Blog"
  listing:
    contents: posts
    sort: "date desc"
    type: default
    categories: true
    feed: true
  ---
  ```
  Note: no body content currently.

- [ ] **Step 2: Replace `blog.qmd` with year-sectioned structure**

  Write the following complete file:

  ```yaml
  ---
  title: "Blog"
  listing:
    # Hidden master listing: drives RSS feed and category sidebar only
    - id: all-posts
      contents: posts
      sort: "date desc"
      type: default
      categories: true
      feed: true

    # Year-scoped visible listings (add new block when first post of a new year is published)
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

  :::{#all-posts style="display:none"}
  :::

  <!-- MAINTENANCE: when first post of a new year is published, add a new ## YYYY heading,
       :::{#posts-YYYY}::: div, and a new listing block (contents: "posts/YYYY-*/index.qmd").
       Keep feed: true and categories: true on the all-posts block only. -->

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

- [ ] **Step 3: Render the blog page to verify structure**

  ```bash
  QUARTO_PYTHON=.venv/bin/python quarto render blog.qmd
  ```

  Expected: `_site/blog.html` created with no errors. Open `_site/blog.html` in a browser
  (or run `quarto preview blog.qmd`) and verify:
  - Four `## YEAR` headings appear: 2026, 2024, 2018, 2010
  - Posts appear under the correct year
  - The `all-posts` block is not visible on the page
  - `_site/blog.xml` exists (RSS feed generated)

- [ ] **Step 4: Check that the hidden `all-posts` block is truly hidden**

  ```bash
  python3 -c "
  with open('_site/blog.html') as f:
      content = f.read()
  import re
  # Find all-posts div
  match = re.search(r'id=\"all-posts\"[^>]*>(.*?)</div>', content, re.DOTALL)
  if match:
      inner = match.group(1).strip()
      print('all-posts inner content length:', len(inner))
      print('First 200 chars:', inner[:200])
  else:
      print('all-posts div not found in rendered HTML')
  "
  ```

  Expected: `all-posts` div is present but contains only the listing markup hidden by
  `display:none`. If it renders visibly (i.e., a duplicate post list appears on the page),
  add to `custom.scss` and `custom-dark.scss`:
  ```scss
  #all-posts { display: none !important; }
  ```

- [ ] **Step 5: Verify RSS feed covers all published posts**

  ```bash
  python3 -c "
  import re
  with open('_site/blog.xml') as f:
      content = f.read()
  titles = re.findall(r'<title>([^<]+)</title>', content)
  print('RSS titles found:', titles)
  "
  ```

  Expected: All 6 published post titles appear in the RSS feed (not just 2026 posts).
  Published posts: military-strategy, mathacademy, cname-fix, talent-vs-luck,
  monty-hall-monte-carlo, making-money-with-monty-hall.

- [ ] **Step 6: Commit**

  ```bash
  git add blog.qmd
  git commit -m "feat: replace flat blog listing with year-sectioned blocks

  Use multiple Quarto listing blocks (one per published year) with year-based
  content globs. Hidden all-posts master listing preserves RSS feed and
  cross-year category sidebar.

  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
  ```

---

## Chunk 2: Style year headings in SCSS

**Files:**
- Modify: `custom.scss`
- Modify: `custom-dark.scss`

### Task 2: Inspect rendered output and add targeted SCSS

- [ ] **Step 1: Inspect the rendered HTML to find exact heading structure**

  ```bash
  python3 -c "
  with open('_site/blog.html') as f:
      content = f.read()
  import re
  # Find the h2 year headings and surrounding context
  matches = re.finditer(r'<h2[^>]*>.*?</h2>', content, re.DOTALL)
  for m in matches:
      start = max(0, m.start() - 50)
      print(content[start:m.end() + 50])
      print('---')
  "
  ```

  Note the exact class and surrounding element structure of the year `h2` headings.
  The existing `h2` SCSS rule already applies `border-bottom` and Fraunces font.
  Determine if the spacing looks correct or needs adjustment.

- [ ] **Step 2: Open the rendered page in a browser and assess visually**

  ```bash
  quarto preview blog.qmd --no-browser
  ```

  Open the URL shown (typically `http://localhost:4444`) in a browser. Toggle light/dark
  mode. Check:
  - Year headings clearly separate post groups
  - Spacing above each year heading feels comfortable (not cramped against previous section)
  - First year heading (2026) does not have excessive space above it
  - Year headings do not visually compete with post titles

- [ ] **Step 3: Add spacing adjustments to `custom.scss` if needed**

  Add after the existing `h2` rule in `custom.scss`:
  ```scss
  // Year section headings on blog listing page — extra breathing room above each year
  .quarto-listing-container h2 {
    margin-top: 3rem;
  }
  .quarto-listing-container h2:first-of-type {
    margin-top: 1rem;
  }
  ```

  If the rendered `h2` elements are not inside `.quarto-listing-container`, adjust the
  selector based on what Step 1 revealed. Only add this rule if the default spacing
  looks insufficient — do not add it if the default is already correct.

- [ ] **Step 4: Mirror any changes to `custom-dark.scss`**

  Any SCSS rules added to `custom.scss` in Step 3 must be added identically to
  `custom-dark.scss`. The rules are layout/spacing only so the same values apply in
  both themes.

- [ ] **Step 5: Add hidden-block suppression to both SCSS files if needed**

  If Step 4 of Task 1 revealed that `#all-posts` renders visible content, add to
  both `custom.scss` and `custom-dark.scss`:
  ```scss
  // Suppress the hidden all-posts listing block (RSS/categories only)
  #all-posts { display: none !important; }
  ```

- [ ] **Step 6: Render and do a final visual check**

  ```bash
  QUARTO_PYTHON=.venv/bin/python quarto render blog.qmd
  ```

  Open `_site/blog.html` in a browser. Verify:
  - Light mode: year headings look intentional, spaced, Fraunces font
  - Dark mode: year headings match the dark palette, same spacing
  - No duplicate post list from `all-posts` block
  - Category sidebar renders (if using a browser that triggers the JS)
  - Mobile at narrow width (resize browser to ~375px): no clipping or horizontal scroll

- [ ] **Step 7: Commit**

  ```bash
  git add custom.scss custom-dark.scss
  git commit -m "style: adjust year heading spacing on blog listing page

  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
  ```

  (If no SCSS changes were needed, skip this commit.)

---

## Chunk 3: Final verification and push

### Task 3: Full site render and push

- [ ] **Step 1: Full site render to catch any cross-page regressions**

  ```bash
  QUARTO_PYTHON=.venv/bin/python quarto render 2>&1 | grep -E 'ERROR|WARN'
  ```

  Expected: no ERRORs. WARN about blog.xml missing a post is acceptable only if the
  RSS feed check in Task 1 Step 5 passed. Any other warnings should be investigated.

- [ ] **Step 2: Spot-check home page and a blog post**

  Open `_site/index.html` and `_site/posts/2018-03-12-talent-vs-luck/index.html` in a
  browser. Confirm no layout regressions.

- [ ] **Step 3: Push and verify CI passes**

  ```bash
  git push
  gh run watch --exit-status
  ```

  Expected: GitHub Actions publish workflow completes successfully.

---

## Maintenance Note (add as comment in `blog.qmd`)

When the first post of a new year (e.g., 2027) is published:
1. Add `## 2027` heading and `:::{#posts-2027}:::` div at the top of the body (above `## 2026`)
2. Add a new listing block in frontmatter:
   ```yaml
   - id: posts-2027
     contents: "posts/2027-*/index.qmd"
     sort: "date desc"
     type: default
   ```
3. Do NOT add `feed: true` or `categories: true` to new year blocks.
