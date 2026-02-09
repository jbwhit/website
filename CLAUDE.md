# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal website and blog for Jonathan Whitmore, deployed to GitHub Pages at jonathanwhitmore.com.

**Active migration:** On branch `quarto-redesign`, migrating from nbdev+Quarto to a clean **pure Quarto** website. Design inspiration: Mickaël Canouil's site (https://mickael.canouil.fr) — clean, minimal aesthetic. See `TODO.md` for the detailed migration plan and task checklist.

## Workflow

Commit early and often, and push to GitHub after each logical chunk of work.

## Build & Development Commands

```bash
# Preview site locally (live reload)
quarto preview

# Render full site
quarto render
```

## Target Architecture (quarto-redesign branch)

```
├── _quarto.yml              # Main Quarto config (navbar, theme, blog listings)
├── index.qmd                # Home page
├── about.qmd                # About page
├── blog.qmd                 # Blog listing page
├── posts/                   # Blog posts (YYYY-MM-DD-slug/index.qmd or .ipynb)
├── projects/
│   ├── checklists/          # Investment & DID checklists
│   └── physics-quals/       # UCSD physics qualifying exam archive
├── assets/images/           # Images and media
├── CNAME                    # Custom domain (jonathanwhitmore.com) — lives in root
└── .github/workflows/       # GitHub Pages deployment
```

## Legacy Architecture (main branch, being replaced)

- **`nbs/`** — Old source directory. Content files, `_quarto.yml`, and `CNAME` all lived here because nbdev required it.
- **`website/`** — Auto-generated Python package from nbdev. Not needed in pure Quarto.
- **`_proc/`** — Old build output directory (gitignored).
- **`settings.ini`** — nbdev configuration. Not needed in pure Quarto.

## Key Requirements

- Preserve all existing content (blog posts, checklists, physics quals)
- Jupyter notebooks are supported natively by Quarto — `.ipynb` files can be used directly as posts
- `CNAME` file goes in the **root** directory (not inside `nbs/` like the old setup)
- Navbar sections: Home, Blog, Projects, About
- Social links: Twitter/X, LinkedIn, YouTube, GitHub
- RSS feed for blog
- Blog posts use Quarto frontmatter with title, description, author, date, categories

## Deployment

Push to `main` triggers GitHub Actions deploying to `gh-pages` branch. Workflow config in `.github/workflows/`.

## Theming

Target: clean, minimal aesthetic inspired by Mickaël Canouil. Consider cosmo or flatly base theme with custom SCSS. Dual light/dark mode support.
