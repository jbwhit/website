# Design: Full Gruvbox Hard Theme

**Date:** 2026-03-09
**Status:** Validated
**Goal:** Implement a site-wide Gruvbox Hard theme for both light and dark modes, replacing the current Bootstrap `flatly` and `darkly` themes while maintaining the "Literary" typography.

## Architecture

The site will use Quarto's multi-theme capability with two custom SCSS files that provide a full implementation of the Gruvbox Hard palette.

- **`custom.scss` (Light Mode):** A "Hybrid" Gruvbox Light Hard implementation. It maintains a clean, airy feel but uses warmer, parchment-like backgrounds and softer ink-colored text.
- **`custom-dark.scss` (Dark Mode):** A full Gruvbox Dark Hard implementation designed for high readability and low eye strain.

Both files will map Gruvbox-specific colors to standard Bootstrap variables (`$primary`, `$body-bg`, `$body-color`, etc.) in their respective `/*-- scss:defaults --*/` sections.

## Color Palette

**Primary Brand Color:** Gruvbox Blue (Professional)
- Light Mode: `#076678` (Dark Blue)
- Dark Mode: `#83a598` (Light Blue)

### Light Mode (Gruvbox Light Hard)
- **Background (`$body-bg`):** `#f9f5d7` (Hard Background)
- **Foreground (`$body-color`):** `#3c3836` (Dark 0)
- **Headings:** `#282828` (Dark 0 Hard)
- **Secondary Accents:** `#d5c4a1` (Light 2)
- **Code Output Border:** `#af3a03` (Gruvbox Orange)

### Dark Mode (Gruvbox Dark Hard)
- **Background (`$body-bg`):** `#1d2021` (Hard Background)
- **Foreground (`$body-color`):** `#ebdbb2` (Light 1)
- **Headings:** `#fbf1c7` (Light 0)
- **Secondary Accents:** `#504945` (Dark 2)
- **Code Output Border:** `#fe8019` (Gruvbox Orange)

## Typography

The "Literary" typography stack is preserved but color-tuned for the Gruvbox backgrounds.

- **Headings:** `Fraunces` (Expressive optical-size serif).
- **Body:** `Source Sans Pro`.
- **Monospace:** `Source Code Pro`.

## Components

- **Navbar:** Solid Gruvbox Blue background in both modes.
- **Home Page Hero:** Enhanced by the parchment (Light) or deep charcoal (Dark) backgrounds, with the subtitle using mid-tone Gruvbox "Gray" variants (`#a89984`).
- **Syntax Highlighting:** Quarto's built-in `gruvbox` theme will be used for all code blocks.
- **Rules/Borders:** Subtle, low-contrast etched look using Gruvbox Light 2 (Light mode) and Dark 2 (Dark mode).

## Implementation Steps

1. Update `_quarto.yml` to point only to `custom.scss` and `custom-dark.scss`.
2. Define the full Gruvbox color scale as SCSS variables.
3. Map these variables to Bootstrap defaults in `/*-- scss:defaults --*/`.
4. Update `/*-- scss:rules --*/` to handle custom component styling (Hero, Code Output, Navbar).
5. Set `highlight-style: gruvbox` in the global `format: html` configuration.

## Validation

- **Accessibility:** Verify text/background contrast ratios meet WCAG AA standards.
- **Consistency:** Ensure Gruvbox Blue remains the primary "action" color across both modes.
- **Code Integration:** Verify that `gruvbox` syntax highlighting integrates seamlessly with the site-wide theme.
