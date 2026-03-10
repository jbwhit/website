# Theme Bugfixes & Design Improvements Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix three theme bugs (missing fonts, incomplete dark mode, duplicate import) then improve matplotlib figure colors and the home page.

**Architecture:** All changes are to existing files — SCSS themes, the font HTML include, the talent-vs-luck post, and the home page QMD. No new files except this plan.

**Tech Stack:** Quarto, SCSS, Google Fonts, matplotlib (Python)

---

## Task 1: Load Source Sans Pro and Source Code Pro

Both SCSS files declare these fonts but they're never loaded. Only Fraunces is in the `<link>` tag.

**Files:**
- Modify: `includes/fonts.html`

- [ ] **Step 1: Add Source Sans Pro and Source Code Pro to font include**

Replace the contents of `includes/fonts.html` with:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&family=Source+Sans+Pro:ital,wght@0,400;0,600;0,700;1,400&family=Source+Code+Pro:wght@400;600&display=swap" rel="stylesheet">
```

This loads all three font families in a single request.

- [ ] **Step 2: Verify with quarto preview**

Run: `quarto preview`
Expected: Body text renders in Source Sans Pro (check with browser dev tools). Code blocks render in Source Code Pro. Headings still use Fraunces.

- [ ] **Step 3: Commit**

```bash
git add includes/fonts.html
git commit -m "Fix: load Source Sans Pro and Source Code Pro fonts

Both were declared in SCSS but never loaded — site was falling back to system fonts."
git push
```

---

## Task 2: Remove duplicate Fraunces import from dark SCSS

`custom-dark.scss` has an `@import url(...)` for Fraunces that duplicates the `<link>` in `includes/fonts.html`.

**Files:**
- Modify: `custom-dark.scss`

- [ ] **Step 1: Remove the @import line**

Delete line 23 from `custom-dark.scss`:

```scss
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&display=swap');
```

The `/*-- scss:rules --*/` comment should be immediately followed by the `h1, h2, h3` rule.

- [ ] **Step 2: Verify dark mode still loads Fraunces**

Run: `quarto preview`, toggle to dark mode.
Expected: Headings still render in Fraunces (loaded via includes/fonts.html).

- [ ] **Step 3: Commit**

```bash
git add custom-dark.scss
git commit -m "Fix: remove duplicate Fraunces import from dark SCSS

Font is already loaded via includes/fonts.html."
git push
```

---

## Task 3: Sync dark mode SCSS with light mode rules

`custom-dark.scss` is missing most styling rules that `custom.scss` has: hero sizing, heading optical sizing, blog listing card styles, cell output styles.

**Files:**
- Modify: `custom-dark.scss`

- [ ] **Step 1: Add all missing rules to dark mode**

After removing the `@import` (Task 2), the `/*-- scss:rules --*/` section of `custom-dark.scss` should become:

```scss
/*-- scss:rules --*/

// Fraunces — expressive optical-size variable serif for headings
h1, h2, h3 {
  font-family: 'Fraunces', Georgia, serif;
  font-optical-sizing: auto;
  letter-spacing: -0.02em;
  color: $gb-fg0;
}

// Home page hero — give the title/subtitle more presence
.quarto-title h1.title {
  font-size: clamp(2.4rem, 6vw, 4rem);
  font-weight: 600;
  line-height: 1.1;
  margin-bottom: 0.4rem;
}

.quarto-title .quarto-title-subtitle {
  font-family: 'Fraunces', Georgia, serif;
  font-style: italic;
  font-weight: 300;
  font-size: 1.25rem;
  opacity: 0.7;
  margin-top: 0;
  color: $gb-gray;
}

// Section headings — subtle rule accent
h2 {
  padding-bottom: 0.4rem;
  border-bottom: 1px solid $gb-dark2;
  margin-bottom: 1.25rem;
}

// Blog listing cards — breathing room + styled date
.quarto-listing-default .quarto-post {
  padding: 1.25rem 0;
  border-bottom: 1px solid $gb-dark2;
}

.quarto-listing-default .quarto-post .listing-title a {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 600;
  font-size: 1.15rem;
  letter-spacing: -0.01em;
}

.quarto-listing-default .quarto-post .listing-date {
  font-size: 0.8rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  opacity: 0.5;
}

// Navbar styling
.navbar {
  background-color: $gb-blue !important;
}

.navbar .navbar-brand, .navbar .navbar-title {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 600;
  color: $gb-bg0-hard !important;
}

.navbar .nav-link, .navbar .quarto-navigation-tool {
  color: $gb-bg0-hard !important;
}

.navbar .nav-link:hover, .navbar .navbar-brand:hover {
  color: #282828 !important; // Gruvbox Dark 0 Hard
}

// Cell output styling
.cell {
  margin-bottom: 1rem;
}

.cell > .sourceCode {
  margin-bottom: 0;
}

.cell-output > pre {
  margin-bottom: 0;
}

.cell-output > pre,
.cell-output > .sourceCode > pre,
.cell-output-stdout > pre {
  margin-left: 0.8rem;
  margin-top: 0;
  background: none;
  border-left: 2px solid $gb-orange;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.cell-output > .sourceCode {
  border: none;
  background: none;
  margin-top: 0;
}
```

- [ ] **Step 2: Verify dark mode rendering**

Run: `quarto preview`, toggle to dark mode.
Expected: Hero title is large and responsive. Blog listing cards have padding, Fraunces titles, small-caps dates. Cell output has orange left border with no background. All matches light mode behavior but with dark palette.

- [ ] **Step 3: Commit**

```bash
git add custom-dark.scss
git commit -m "Fix: sync dark mode SCSS with all light mode styling rules

Dark mode was missing hero sizing, heading optical sizing, blog listing
card styles, date formatting, and cell output styling."
git push
```

---

## Task 4: Update matplotlib figures to Gruvbox colors

The three figures in the talent-vs-luck post use Material Design colors that clash with the Gruvbox theme.

**Files:**
- Modify: `posts/2018-03-12-talent-vs-luck/index.qmd`

**Color mapping:**
- `#2196F3` (MD Blue) → `#076678` (Gruvbox Dark Blue)
- `#F44336` (MD Red) → `#cc241d` (Gruvbox Dark Red)
- `#9E9E9E` (MD Gray) → `#a89984` (Gruvbox Gray)
- `"red"` (named) → `#cc241d` (Gruvbox Dark Red)

- [ ] **Step 1: Update Figure 1 (probability bands) — lines 138-140**

Replace:
```python
ax.fill_between(quantiles, p_halve + p_same, 1.0,   color="#2196F3", alpha=0.8, label="Doubles")
ax.fill_between(quantiles, p_halve,           p_halve + p_same, color="#9E9E9E", alpha=0.35, label="Stays the same")
ax.fill_between(quantiles, 0,                 p_halve,          color="#F44336", alpha=0.8, label="Halves")
```

With:
```python
ax.fill_between(quantiles, p_halve + p_same, 1.0,   color="#076678", alpha=0.8, label="Doubles")
ax.fill_between(quantiles, p_halve,           p_halve + p_same, color="#a89984", alpha=0.35, label="Stays the same")
ax.fill_between(quantiles, 0,                 p_halve,          color="#cc241d", alpha=0.8, label="Halves")
```

- [ ] **Step 2: Update Figure 2 (mean vs geometric-mean) — lines 194-195**

Replace:
```python
ax.plot(quantiles, evs, ls="--", lw=2, color="#2196F3", label="Mean (expected value)")
ax.plot(quantiles, gms, ls="-", lw=2, color="#F44336", label="Geometric-mean path")
```

With:
```python
ax.plot(quantiles, evs, ls="--", lw=2, color="#076678", label="Mean (expected value)")
ax.plot(quantiles, gms, ls="-", lw=2, color="#cc241d", label="Geometric-mean path")
```

- [ ] **Step 3: Update Figure 3 (p_event estimation) — lines 250, 252**

Replace:
```python
    ax.plot(p_events, max_unlucky, lw=0.4, color="#2196F3", alpha=0.5)
```
With:
```python
    ax.plot(p_events, max_unlucky, lw=0.4, color="#076678", alpha=0.5)
```

Replace:
```python
ax.axhline(15, color="red", lw=2, label="Observed max unlucky events (paper Fig. 5b)")
```
With:
```python
ax.axhline(15, color="#cc241d", lw=2, label="Observed max unlucky events (paper Fig. 5b)")
```

- [ ] **Step 4: Clear cache and verify**

Run:
```bash
rm -rf posts/2018-03-12-talent-vs-luck/*_cache
quarto preview
```

Navigate to the talent-vs-luck post. Expected: all three figures use warm Gruvbox blue/red/gray instead of bright Material Design colors.

- [ ] **Step 5: Commit**

```bash
git add posts/2018-03-12-talent-vs-luck/index.qmd
git commit -m "Update matplotlib figures to Gruvbox color palette

Replace Material Design blue/red/gray with Gruvbox equivalents
for visual cohesion with the site theme."
git push
```

---

## Task 5: Redesign home page for more presence

The current home page is minimal — one welcome sentence, three recent posts, three project links. For a site with 15+ years of content, talks at PyCon/Grace Hopper/Stanford, and a generative art practice, the landing page should do more.

**Files:**
- Modify: `index.qmd`

- [ ] **Step 1: Rewrite home page content**

Replace the full contents of `index.qmd` with:

```markdown
---
title: "Jonathan Whitmore"
subtitle: "Physics, data science, and learning systems"
page-layout: full
listing:
  id: recent-posts
  contents: posts
  sort: "date desc"
  type: default
  max-items: 3
  fields: [date, title, description]
---

::: {.lead}
I'm a physicist and data scientist who builds things at the intersection of machine learning, causal inference, and education. I studied physics at UC San Diego, gave talks at PyCon, Grace Hopper, and Stanford, and make [generative art](https://www.jbwhitmoreart.com/) on the side.
:::

## Recent Posts

::: {#recent-posts}
:::

Browse all posts on the [Blog](blog.qmd) page.

## Projects

- [Checklists](projects/checklists/index.qmd) — Decision-making checklists for investing and causal inference
- [UCSD Physics Qualifying Exams](projects/physics-quals/index.qmd) — Archive of physics PhD qualifying exams (1987–2019)
- [Talks](projects/talks/index.qmd) — Conference talks, tutorials, and public lectures (2011–2019)
- [Generative Art](https://www.jbwhitmoreart.com/) — Algorithmic explorations of motion, form, and color
```

Changes:
- The `.lead` div replaces the generic welcome sentence with a confident, specific intro that names credentials
- Adds the Talks page to the Projects list (it exists but wasn't linked from the home page)

- [ ] **Step 2: Style the .lead class**

Add to `custom.scss`, after the `.quarto-title .quarto-title-subtitle` rule (after line 47):

```scss
// Home page lead paragraph
.lead {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.2rem;
  font-weight: 300;
  line-height: 1.6;
  color: $gb-fg1;
  max-width: 40em;
  margin-bottom: 2rem;
}
```

Add the same rule to `custom-dark.scss`, after the `.quarto-title .quarto-title-subtitle` rule:

```scss
// Home page lead paragraph
.lead {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.2rem;
  font-weight: 300;
  line-height: 1.6;
  color: $gb-fg1;
  max-width: 40em;
  margin-bottom: 2rem;
}
```

- [ ] **Step 3: Verify in both themes**

Run: `quarto preview`
Expected: Home page has a Fraunces-set intro paragraph below the title. Talks link appears in Projects. Light and dark modes both render the lead paragraph correctly.

- [ ] **Step 4: Commit**

```bash
git add index.qmd custom.scss custom-dark.scss
git commit -m "Redesign home page with stronger intro and complete project links

Add confident lead paragraph naming specific credentials. Link to Talks
page which existed but wasn't on the home page."
git push
```
