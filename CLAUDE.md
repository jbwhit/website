# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal website and blog for Jonathan Whitmore, built with **Quarto** and deployed to GitHub Pages at jonathanwhitmore.com.

## Workflow

Commit early and often, and push to GitHub after each logical chunk of work.

## Build & Development Commands

```bash
# Preview site locally (live reload)
quarto preview

# Render full site (output goes to _site/)
quarto render
```

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

- **Landing pages** (home, blog, about, every `projects/*/index.qmd`): plain title block — never `title-block-banner` (renders in `$primary`, stacking a second blue band directly under the already-blue navbar); no `date` or `categories` (those signal "article" and render a dated byline); `page-layout: full` only on the home page (hero); body must not repeat the frontmatter `title` as a `#` heading.
- **Article pages** (blog posts, individual checklists like `projects/checklists/investing.qmd`): keep `date` and `categories`; per-page `toc-title` is allowed.
- **TOC rule (both archetypes):** global `toc: true` in `_quarto.yml` stays — TOC renders on the right for any page with headings. Never set `toc-location: left`; don't add per-page `toc: false`.

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
