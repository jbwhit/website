# Monty Hall Blog Posts Polish — Design

## Goal

Polish and modernize two Monty Hall blog posts, combining the Python simulation draft and "play at home" draft into one executable Quarto post.

## Post 1: "Making Money with Monty Hall"

- **Path:** `posts/2010-11-24-making-money-with-monty-hall/index.qmd`
- Anonymize "adolthitler" → "a YouTube commenter" throughout (callout titles, body text)
- Update bottom link to point to the new combined post path
- Add categories (e.g., `[probability, python]`)
- Light copy-editing pass

## Post 2 (combined): "Monty Hall Monte Carlo — Python"

- **Path:** `posts/2010-11-26-monty-hall-monte-carlo-python/index.qmd` (reuse post 3's date, new slug)
- **Date:** 2010-11-26, draft: false
- Merge narrative: recap the bet from post 3, then walk through the simulation
- Modernize Python 3: drop `pylab`, `locale` hacks, use `numpy` + `matplotlib`
- Quarto executable Python with `code-fold: true`
- Generate convergence plot showing win ratios approaching 1/3 and 2/3
- Print summary stats (win percentages, net payouts)
- Remove Zemanta image link

## Deletions

- Delete `posts/2010-11-25-monty-hall-monte-carlo-python/` (old post 2, content merged)
- Delete `posts/2010-11-26-monty-hall-bet-monte-carlo-play-at-home/` (old post 3, content merged)

## GitHub Issue

- Create issue: "Audit all posts for dead Zemanta links and remove them"
