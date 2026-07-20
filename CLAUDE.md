# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal website and blog for Jonathan Whitmore, built with **Quarto** and deployed to GitHub Pages at jonathanwhitmore.com.

## Workflow

Commit early and often, and push to GitHub after each logical chunk of work.

## Build & Development Commands

**Freeze is on, so most work needs no Python.** `execute: freeze: auto` is set in `_quarto.yml`
and `_freeze/` is committed, so `quarto preview` / `quarto render` reuse frozen computational
output — a jupyter post (`.ipynb` / `.qmd` with code cells) re-executes only when its **own**
source changes. Writing or editing markdown posts (the common case) needs no Python at all:

```bash
quarto preview                        # live preview; reuses _freeze/, no Python needed
QUARTO_PROFILE=drafts quarto preview  # same, including draft posts
quarto render                         # full render to _site/
```

**You only need Python when you edit or add a computational (jupyter) post** — it must
re-execute, and Quarto's jupyter engine otherwise grabs the system `python3` (no jupyter) and
dies with `ModuleNotFound: yaml`. Deps live in `requirements.txt`, installed into a **uv-managed
`.venv`** (Python 3.13, matching CI); the `Makefile` points Quarto at it via **`QUARTO_PYTHON`**:

```bash
make setup      # uv venv (Python 3.13) + install requirements.txt  (one-time / after dep changes)
make preview    # live preview incl. drafts, using the venv python
make render     # full render, using the venv python
```

- After a computational post re-executes, **commit the updated `_freeze/`** so CI and other
  clones reuse it (don't re-ignore `_freeze/`).
- An explicit single-file `quarto render posts/…/index.qmd` always re-executes *that* file
  (freeze is bypassed for an explicit target), so it needs the venv only if that post has code.
- `uv run quarto …` does **not** work (no `pyproject.toml` → uv builds an ephemeral env missing
  the deps); use the Makefile / `QUARTO_PYTHON`.
- `quarto preview` serves at `http://localhost:<port>/` and opens your browser; a post appears in
  the full-site build only once its branch is on `main` (or when run from that post's worktree).

## Architecture

```
├── _quarto.yml              # Main Quarto config (navbar, theme, blog listings)
├── index.qmd                # Home page (with recent posts listing)
├── about.qmd                # About page
├── blog.qmd                 # Blog listing page (RSS feed via blog.xml)
├── posts/                   # Blog posts (YYYY-MM-DD-slug/index.qmd or .ipynb)
├── projects/
│   ├── checklists/          # Investment & DiD checklists (with downloadable .md files)
│   └── physics-quals/       # UCSD physics qualifying exam archive (1987–2019)
├── assets/images/           # Images and media (favicon lives here)
├── custom.scss              # Light theme overrides (flatly base)
├── custom-dark.scss         # Dark theme overrides (darkly base)
├── styles.css               # Additional CSS
├── CNAME                    # Custom domain (jonathanwhitmore.com)
└── .github/workflows/
    └── publish.yml          # GitHub Actions: Quarto render + deploy-pages
```

## Content Conventions

### Page archetypes & styling

- **Landing pages** (home, blog, about, every `projects/*/index.qmd`):
  - Plain title block — never `title-block-banner` (renders in `$primary`, stacking a second blue band directly under the already-blue navbar)
  - No `date` or `categories` (those signal "article" and render a dated byline)
  - `page-layout: full` only on the home page (hero)
  - Body must not repeat the frontmatter `title` as a `#` heading
- **Article pages** (blog posts, individual checklists like `projects/checklists/investing.qmd`): keep `date` and `categories`; per-page `toc-title` is allowed.
- **TOC rule (both archetypes):** global `toc: true` in `_quarto.yml` stays — TOC renders on the right for any page with headings. Never set `toc-location: left`; don't add per-page `toc: false`.

### Posts & files

- Blog posts go in `posts/YYYY-MM-DD-slug/index.qmd` (or `.ipynb` for notebook posts)
- Posts need frontmatter: title, description, author, date, categories
- Draft posts use `draft: true` in frontmatter — by default Quarto renders them as empty pages everywhere (even in `quarto preview`). To preview drafts locally, use the drafts profile: `QUARTO_PROFILE=drafts quarto preview` (defined in `_quarto-drafts.yml`). Never flip `draft: false` just to preview.
- Quarto `aliases` in frontmatter provide redirects from old URLs (e.g., `/checklists.html` → `/projects/checklists/`)
- Downloadable files (like checklist `.md` files) live alongside their pages but are excluded from rendering via `projects/**/*.qmd` glob in `_quarto.yml`

## Deployment

Push to `main` triggers `.github/workflows/publish.yml`:
1. Quarto renders the site to `_site/`
2. `actions/deploy-pages` deploys to GitHub Pages

GitHub Pages source must be set to "GitHub Actions" (not "Deploy from a branch").

After pushing, verify the deploy succeeded:
```bash
gh run watch --exit-status
```

## Theming

Dual light/dark mode using flatly (light) and darkly (dark) Bootstrap themes, with custom SCSS overrides. Navbar sections: Home, Blog, Projects, Courses, About. Social icons: art portfolio, Twitter/X, YouTube, LinkedIn, GitHub, RSS.
