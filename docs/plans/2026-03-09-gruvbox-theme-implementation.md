# Gruvbox Hard Theme Implementation Plan

> **For Gemini:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement a site-wide Gruvbox Hard theme for both light and dark modes, replacing the current Bootstrap `flatly` and `darkly` themes while maintaining existing typography.

**Architecture:** Custom SCSS implementation that maps the Gruvbox Hard palette to Bootstrap variables in `custom.scss` (Light) and `custom-dark.scss` (Dark).

**Tech Stack:** Quarto, Bootstrap 5 (via SCSS), Gruvbox Hard palette.

---

### Task 1: Update Global Quarto Configuration

**Files:**
- Modify: `_quarto.yml`

**Step 1: Update theme and highlight-style**

Change the `theme` and `highlight-style` in `_quarto.yml`.

```yaml
format:
  html:
    theme:
      light: [custom.scss]
      dark: [custom-dark.scss]
    highlight-style: gruvbox
    # ... rest of format settings
```

**Step 2: Commit**

```bash
git add _quarto.yml
git commit -m "feat: set custom gruvbox theme and highlight-style in _quarto.yml"
```

---

### Task 2: Implement custom.scss (Light Mode)

**Files:**
- Modify: `custom.scss`

**Step 1: Replace defaults with Gruvbox Light Hard variables**

```scss
/*-- scss:defaults --*/

// Gruvbox Light Hard Palette
$gb-bg0-hard: #f9f5d7;
$gb-fg0: #282828;
$gb-fg1: #3c3836;
$gb-blue: #076678;
$gb-orange: #af3a03;
$gb-gray: #a89984;
$gb-light2: #d5c4a1;

// Bootstrap Overrides
$body-bg: $gb-bg0-hard;
$body-color: $gb-fg1;
$primary: $gb-blue;
$link-color: $gb-blue;

$font-family-sans-serif: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
$font-family-monospace: "Source Code Pro", SFMono-Regular, Menlo, Monaco, monospace;

/*-- scss:rules --*/

// (Maintain existing Fraunces headings and home page hero rules, but update colors)
h1, h2, h3 {
  font-family: 'Fraunces', Georgia, serif;
  color: $gb-fg0;
}

h2 {
  border-bottom: 1px solid $gb-light2;
}

.quarto-title .quarto-title-subtitle {
  color: $gb-gray;
}

.quarto-listing-default .quarto-post {
  border-bottom: 1px solid rgba(0, 0, 0, 0.07); // Adjusted for light background
}

.cell-output > pre,
.cell-output > .sourceCode > pre,
.cell-output-stdout > pre {
  border-left: 2px solid $gb-orange;
}
```

**Step 2: Commit**

```bash
git add custom.scss
git commit -m "feat: implement Gruvbox Light Hard theme in custom.scss"
```

---

### Task 3: Implement custom-dark.scss (Dark Mode)

**Files:**
- Modify: `custom-dark.scss`

**Step 1: Replace defaults with Gruvbox Dark Hard variables**

```scss
/*-- scss:defaults --*/

// Gruvbox Dark Hard Palette
$gb-bg0-hard: #1d2021;
$gb-fg0: #fbf1c7;
$gb-fg1: #ebdbb2;
$gb-blue: #83a598;
$gb-orange: #fe8019;
$gb-gray: #a89984;
$gb-dark2: #504945;

// Bootstrap Overrides
$body-bg: $gb-bg0-hard;
$body-color: $gb-fg1;
$primary: $gb-blue;
$link-color: $gb-blue;

$font-family-sans-serif: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
$font-family-monospace: "Source Code Pro", SFMono-Regular, Menlo, Monaco, monospace;

/*-- scss:rules --*/

@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&display=swap');

h1, h2, h3 {
  font-family: 'Fraunces', Georgia, serif;
  color: $gb-fg0;
}

h2 {
  border-bottom: 1px solid $gb-dark2;
}

.quarto-title .quarto-title-subtitle {
  color: $gb-gray;
}

.quarto-listing-default .quarto-post {
  border-bottom: 1px solid $gb-dark2;
}

.cell-output > pre,
.cell-output > .sourceCode > pre,
.cell-output-stdout > pre {
  border-left: 2px solid $gb-orange;
}
```

**Step 2: Commit**

```bash
git add custom-dark.scss
git commit -m "feat: implement Gruvbox Dark Hard theme in custom-dark.scss"
```

---

### Task 4: Verify and Refine Implementation

**Files:**
- Test: `index.qmd`, `posts/2010-11-26-monty-hall-monte-carlo-python/index.qmd`

**Step 1: Render site**

```bash
source .venv/bin/activate && quarto render
```

**Step 2: Check light and dark mode in a browser**
(Note: This requires manual verification or checking the generated HTML for correct classes/styles)

**Step 3: Refine Navbar styling if needed**
The navbar might need explicit styling if `$primary` doesn't cover everything.

**Step 4: Commit any refinements**

```bash
git add custom.scss custom-dark.scss
git commit -m "fix: refine gruvbox theme styling based on render"
```

---

### Task 5: Final Cleanup

**Step 1: Set `draft: false` if any posts were being used for testing**

**Step 2: Push changes**

```bash
git push origin feature/gruvbox-theme
```
