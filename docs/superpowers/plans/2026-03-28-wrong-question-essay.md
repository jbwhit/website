# "The Wrong Question" Essay — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write and publish a draft essay arguing that the "individual rights vs. collective obligations" framing of vaccination policy is a false dichotomy, using ergodicity economics, Rawls, Taleb, and game theory — with Python simulations embedded in a Quarto blog post.

**Architecture:** The work has four phases: (0) scaffold, (1) deep research, (2) exploratory simulation to test the ergodicity claim (branching point), (3) build production simulations, (4) write essay prose section by section. Research and exploratory coding happen first because they inform the argument. Simulations use numpy/matplotlib (static plots, no JS dependencies). Essay is a Quarto `.qmd` post with code-folded Python cells and margin notes.

**Tech Stack:** Quarto, Python (numpy, matplotlib), uv for package management

**Spec:** `docs/superpowers/specs/2026-03-28-wrong-question-essay-design.md`

**Reference post:** `posts/2010-11-26-monty-hall-monte-carlo-python/index.qmd` — follow this pattern for code cells, figure labels, and frontmatter.

---

## Phase 0: Scaffold

### Task 1: Create post directory and scaffold

**Files:**
- Create: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Create the post directory**

```bash
mkdir -p posts/2026-03-28-the-wrong-question
```

- [ ] **Step 2: Write the scaffold file**

```qmd
---
title: "The Wrong Question"
date: 2026-03-28
author: Jonathan Whitmore
draft: true
categories: [ergodicity, game-theory, philosophy, policy, simulation]
description: "The individual rights vs. collective obligations debate is a false dichotomy — here's the math that shows why."
execute:
  echo: true
  cache: true
---

<!-- Placeholder: essay content will be built section by section -->
```

- [ ] **Step 3: Add `.superpowers/` to `.gitignore`**

Check `.gitignore` — if `.superpowers/` is not already listed, add it.

- [ ] **Step 4: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd .gitignore
git commit -m "chore: scaffold 'The Wrong Question' essay as draft"
git push
```

---

## Phase 1: Deep Research

Research produces markdown files in a `research/` subdirectory of the post. These are reference material, not published content. Each research task can be delegated to deep research tools (Gemini Deep Research, Codex) or done interactively.

### Task 2: Research — Epidemiological data

**Files:**
- Create: `posts/2026-03-28-the-wrong-question/research/epidemiology.md`

**Research questions:**
- Measles: R0, case fatality rate, vaccine efficacy (1-dose, 2-dose), adverse event rates (serious and mild), herd immunity threshold, historical coverage data
- Smallpox: R0, case fatality rate, vaccine efficacy, adverse event rates, herd immunity threshold, timeline of eradication campaign
- General: How does herd immunity threshold relate to R0? (formula: 1 - 1/R0). What does the non-linear benefit curve actually look like empirically?
- Plausible parameter ranges for hypothetical archetypes (Gray Threat, Black Swan Pandemic)

- [ ] **Step 1: Delegate to deep research tool or research interactively**

Provide the research questions above. Request sourced data with citations.

- [ ] **Step 2: Save results to `research/epidemiology.md`**

Include: data tables, key numbers, source citations, any surprising findings.

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/research/epidemiology.md
git commit -m "research: epidemiological data for essay archetypes"
```

### Task 3: Research — Philosophy and political theory

**Files:**
- Create: `posts/2026-03-28-the-wrong-question/research/philosophy.md`

**Research questions:**
- Rawls: How does the veil of ignorance apply to public health? Has Rawls or Rawlsian scholars written about vaccination specifically? What does the "maximin" principle imply for vaccination policy?
- Mill: How does the harm principle apply to vaccination? Where is the line between self-regarding and other-regarding actions for infectious disease?
- Communitarian vs. libertarian arguments on vaccination mandates — key thinkers and positions
- Historical precedent: Jacobson v. Massachusetts (1905) and the legal/philosophical foundation for vaccine mandates in liberal democracies

- [ ] **Step 1: Delegate to deep research tool or research interactively**

- [ ] **Step 2: Save results to `research/philosophy.md`**

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/research/philosophy.md
git commit -m "research: philosophy and political theory for essay"
```

### Task 4: Research — Ergodicity economics

**Files:**
- Create: `posts/2026-03-28-the-wrong-question/research/ergodicity.md`

**Research questions:**
- Ole Peters' core argument: ensemble average vs. time average. Key papers (especially "The ergodicity problem in economics," Nature Physics 2019). What is the simplest example that illustrates the divergence?
- How does ergodicity economics apply to repeated decisions under risk (like annual vaccination)? Is health/disease a non-ergodic process?
- Kelly criterion: how does it relate to ergodicity? What does "growth-rate optimal" mean for health decisions?
- Has anyone applied ergodicity economics to public health or vaccination specifically? If not, what's the closest application?
- What are the main criticisms of ergodicity economics? (Important for intellectual honesty)

- [ ] **Step 1: Delegate to deep research tool or research interactively**

- [ ] **Step 2: Save results to `research/ergodicity.md`**

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/research/ergodicity.md
git commit -m "research: ergodicity economics literature for essay"
```

### Task 5: Research — Taleb and fat tails

**Files:**
- Create: `posts/2026-03-28-the-wrong-question/research/fat-tails.md`

**Research questions:**
- Taleb's precautionary principle: what is the formal argument? When does it apply (multiplicative/systemic risk) vs. not (additive/local risk)?
- How does Taleb distinguish thin-tailed and fat-tailed risk domains? Where do pandemics sit?
- "Skin in the game" applied to vaccination: what does Taleb actually argue about collective risk?
- Correlated tail risk: why does everyone's ruin happening together change the calculation?
- Key papers: "The Precautionary Principle" (with co-authors), relevant sections of Antifragile and Skin in the Game

- [ ] **Step 1: Delegate to deep research tool or research interactively**

- [ ] **Step 2: Save results to `research/fat-tails.md`**

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/research/fat-tails.md
git commit -m "research: Taleb and fat tails literature for essay"
```

### Task 6: Research — Institutional design and legitimacy

**Files:**
- Create: `posts/2026-03-28-the-wrong-question/research/institutional-design.md`

**Research questions:**
- How do liberal democracies actually operationalize vaccination mandates? (School-entry requirements, military, healthcare workers)
- Vaccine-injury compensation programs (e.g., US VICP, UK Vaccine Damage Payment Scheme) — how do they work and why do they exist?
- Exemption frameworks: medical, religious, philosophical — how do different jurisdictions handle them?
- The policy ladder in practice: recommend → subsidize → require → mandate — real-world examples of each level
- What makes a mandate politically legitimate vs. perceived as authoritarian?

This research grounds the policy ladder (section 9) in real institutional mechanisms rather than pure theory.

- [ ] **Step 1: Delegate to deep research tool or research interactively**

- [ ] **Step 2: Save results to `research/institutional-design.md`**

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/research/institutional-design.md
git commit -m "research: institutional design and mandate mechanisms"
```

---

## Phase 2: Exploratory Coding (Branching Point)

This phase tests the central claim *before* the essay commits to it. The ergodicity claim — that the individual/collective tension dissolves under time-average reasoning — is the essay's highest-risk assertion. Test it with simulation first.

### Task 7: Build basic herd immunity model

**Files:**
- Create: `posts/2026-03-28-the-wrong-question/research/explore_herd_immunity.py`

This is exploratory code, not the final simulation. Goal: build a reusable model of herd immunity dynamics that the later simulations can build on.

- [ ] **Step 1: Implement basic SIR-inspired herd immunity function**

The herd immunity threshold for a disease with basic reproduction number R0 is approximately `1 - 1/R0`. The effective reproduction number at vaccination coverage `v` with vaccine efficacy `e` is `R0 * (1 - v*e)`. When this drops below 1, herd immunity is achieved.

Write a Python script that:
- Defines the four archetypes with their parameters (R0, severity, vaccine efficacy, adverse event rate)
- Computes effective R at different coverage levels
- Computes a "population disease burden" function (infections as a function of coverage) — this is the S-curve
- Plots the S-curve for each archetype

- [ ] **Step 2: Run and verify the curves look right**

```bash
cd posts/2026-03-28-the-wrong-question/research
uv run --with numpy --with matplotlib explore_herd_immunity.py
```

Verify: measles herd threshold near 93-95%, smallpox near 80-85%, Gray Threat lower, Black Swan uncertain.

- [ ] **Step 3: Commit exploratory code**

```bash
git add posts/2026-03-28-the-wrong-question/research/explore_herd_immunity.py
git commit -m "explore: basic herd immunity model for four archetypes"
```

### Task 8: Test the ergodicity claim

**Files:**
- Create: `posts/2026-03-28-the-wrong-question/research/explore_ergodicity.py`

**This is the branching point.** The essay claims that under ergodicity economics, the individual/collective tension dissolves. Test this with a concrete model.

- [ ] **Step 1: Design the model**

Model a population of agents over many "years." Each year:
- Each agent decides whether to vaccinate (cost: small certain health risk from adverse event)
- Unvaccinated agents face disease risk based on population coverage and herd immunity curve
- Disease has a health cost (severity × probability of infection given coverage)
- Track each agent's cumulative health over time (time average) AND the population average health at each timestep (ensemble average)

Key question: does the individually optimal vaccination decision (maximizing personal time-average health) match the collectively optimal decision (maximizing ensemble-average health)?

- [ ] **Step 2: Implement and run for each archetype**

Run the simulation. Compare:
- Ensemble-optimal vaccination rate (the rate that maximizes population average health)
- Time-optimal vaccination rate (the rate that maximizes an individual's long-run health trajectory)

If they converge → strong claim holds (essay sections 8-9 work as designed).
If they diverge → weaker claim. The essay should say "the dichotomy is less sharp than it appears" rather than "it dissolves."

- [ ] **Step 3: Document findings**

Write results to `posts/2026-03-28-the-wrong-question/research/ergodicity-findings.md`:
- For each archetype: do time-average and ensemble-average optimal decisions converge?
- Under what parameters do they converge vs. diverge?
- What's the magnitude of the gap, if any?

- [ ] **Step 4: Decision point — adjust essay framing if needed**

If the strong claim doesn't hold, update the spec's Open Questions section (`docs/superpowers/specs/2026-03-28-wrong-question-essay-design.md`) documenting the finding, then proceed with the weaker framing in subsequent tasks:
- Section 8: change from "dissolves" to "narrows" or "reframes"
- Section 9: acknowledge the remaining gap and what it means
- This is fine — intellectual honesty strengthens the essay

- [ ] **Step 5: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/research/explore_ergodicity.py
git add posts/2026-03-28-the-wrong-question/research/ergodicity-findings.md
git commit -m "explore: test ergodicity claim — [RESULT: converges/diverges]"
```

---

## Phase 3: Production Simulations

Build the four simulations that will appear in the essay. These use matplotlib (static plots), code-folded in Quarto, with labeled cells and figure captions. Follow the pattern in `posts/2010-11-26-monty-hall-monte-carlo-python/index.qmd`.

### Task 9: Simulation 1 — Herd immunity S-curve (section 2)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

Build on the exploratory model from Task 7. This simulation shows the non-linear relationship between vaccination coverage and disease burden for a single archetype (measles-like, to keep the dial one-dimensional).

- [ ] **Step 1: Write the simulation code cell**

Add to `index.qmd` in the section 2 area. Use Quarto code cell syntax:

```python
#| label: fig-herd-immunity
#| fig-cap: "The herd immunity curve is sharply non-linear. Small changes in coverage near the threshold produce dramatic changes in disease burden."
```

Plot: x-axis = vaccination coverage (0–100%), y-axis = expected disease burden (infections per 1000). Show the S-curve with the herd immunity threshold marked. Use sourced measles parameters from research.

- [ ] **Step 2: Verify the plot renders in Quarto**

```bash
cd /Users/jonathan/projects/website
quarto preview posts/2026-03-28-the-wrong-question/index.qmd
```

Check: plot renders, code is folded, figure caption shows.

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "feat: add herd immunity S-curve simulation (section 2)"
```

### Task 10: Simulation 2 — Monte Carlo free-rider model (section 5)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

Agent-based Monte Carlo: a population where each agent makes an individually "rational" vaccination decision. Show how collective outcomes degrade as free-riding increases.

- [ ] **Step 1: Write the simulation**

Model:
- N agents (e.g., 10,000)
- Each agent has a "rationality threshold" — they skip vaccination if current coverage is "high enough" that their individual risk is low
- Run multiple rounds. In each round, agents observe last round's coverage and decide
- Track: equilibrium coverage, disease burden, individual outcomes

Run for each archetype. Show that:
- Measles-like: free-riding near threshold is catastrophic
- Gray Threat: individually rational to free-ride, but collective outcome degrades

```python
#| label: fig-free-rider
#| fig-cap: "When agents make individually rational vaccination decisions, collective outcomes degrade — but the severity depends dramatically on disease parameters."
```

Plot: multi-panel or overlaid, showing equilibrium coverage and disease burden for each archetype.

- [ ] **Step 2: Verify renders correctly**

```bash
quarto preview posts/2026-03-28-the-wrong-question/index.qmd
```

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "feat: add Monte Carlo free-rider simulation (section 5)"
```

### Task 11: Simulation 3 — Ensemble vs. time-average divergence (section 8)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

The key ergodicity economics visualization. Show that population-average outcomes differ from individual-over-time outcomes.

- [ ] **Step 1: Write the simulation**

Adapt the exploratory model from Task 8. Show:
- Left panel: ensemble average — average health across many agents at each timestep (looks fine)
- Right panel: time average — one agent's cumulative health over many timesteps (reveals the real story)

The exact design depends on Task 8's findings. If the strong claim holds, show convergence of optimal decisions. If not, show the gap and what it means.

```python
#| label: fig-ergodicity
#| fig-cap: "The population average hides what matters: your personal trajectory through time. These two perspectives can recommend different actions."
```

- [ ] **Step 2: Verify renders correctly**

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "feat: add ensemble vs time-average simulation (section 8)"
```

### Task 12: Simulation 4 — Framework comparison table (section 9)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

A visual summary: framework × archetype → policy ladder level. This can be a styled table or a heatmap.

- [ ] **Step 1: Build the comparison**

Create a matplotlib heatmap or styled table showing:
- Rows: Expected Value, Game Theory, Rawls, Taleb, Ergodicity
- Columns: Measles-like, Smallpox-like, Gray Threat, Black Swan
- Cells: Policy ladder level (1-5: Recommend, Subsidize, School-entry, Outbreak-triggered, Universal)

Values are the essay's argued positions based on each framework's logic applied to each archetype. These are interpretive, not computed — but presenting them visually makes the disagreements concrete.

```python
#| label: fig-framework-comparison
#| fig-cap: "Different frameworks recommend different policy responses — and they disagree most on the hard cases."
```

- [ ] **Step 2: Verify renders correctly**

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "feat: add framework comparison visual (section 9)"
```

---

## Phase 4: Essay Prose

Write the essay section by section, integrating the simulations. Each task writes one or two sections. Use margin notes (`::: {.column-margin}` blocks) for sidenotes. Keep the core argument lean.

### Task 13: Write sections 1-2 (Opening + Single Dial)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Write section 1 — The Pharmacy Moment**

The opening hook. Personal moment (pharmacy flu shot), acknowledge it's low-stakes, then zoom out: this is the accessible end of a harder policy class. What if the consequences ranged from trivial to catastrophic?

Tone: conversational, draws the reader in. ~200-300 words.

- [ ] **Step 2: Write section 2 — The Single Dial**

Introduce the single-dial intuition: fix measles-like parameters, vary only coverage. The herd immunity S-curve simulation (from Task 9) goes here. Narrate what the curve shows — small changes near the threshold matter enormously.

~300-400 words (excluding simulation output).

- [ ] **Step 3: Preview and verify flow**

```bash
quarto preview posts/2026-03-28-the-wrong-question/index.qmd
```

- [ ] **Step 4: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "draft: write sections 1-2 (opening hook, single dial)"
```

### Task 14: Write section 3 (Parameter Space)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Write section 3 — The Real Complexity**

Reveal the parameter space. Coverage was just one axis — now introduce severity, R0, vaccine efficacy, adverse event rate, epistemic uncertainty. Present the four archetypes as named clusters in this space.

Use sourced data from `research/epidemiology.md` for measles and smallpox parameters. Explicitly label the hypothetical archetypes as toy values.

~400-500 words. Consider a small table or list for the four archetypes with key parameters.

- [ ] **Step 2: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "draft: write section 3 (parameter space and archetypes)"
```

### Task 15: Write section 4 (Expected Value as Foil)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Write section 4 — The Default Answer**

Present the naive cost-benefit calculation. Work through it with actual numbers for measles-like (sourced) and Gray Threat (toy values, labeled as such). Then expose the cracks.

Use margin notes for the mathematical details so the main text stays readable.

~400-500 words.

- [ ] **Step 2: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "draft: write section 4 (expected value as foil)"
```

### Task 16: Write sections 5-6 (Game Theory + Rawls)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Write section 5 — The Free-Rider Trap**

Game theory framing. Non-linear payoffs, shifting Nash equilibria. The Monte Carlo simulation (Task 10) goes here. Narrate what it shows for each archetype.

Use research from `research/philosophy.md` for any relevant game-theoretic framing of vaccination in the literature.

~400-500 words.

- [ ] **Step 2: Write section 6 — Behind the Veil**

Rawls' veil of ignorance. Enumerate the four uncertainty sets (immune status, contact network, family, population coverage). Argue that behind a sufficiently thick veil, you'd consent to mandates earlier.

**Margin note:** The Rawlsian case strengthening non-linearly with population uncertainty.

Use research from `research/philosophy.md` for Rawlsian sources.

~400-500 words + margin note.

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "draft: write sections 5-6 (game theory, Rawls)"
```

### Task 17: Write sections 7-8 (Taleb + Ergodicity)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Write section 7 — When the Tail Wags the Dog**

Taleb's precautionary principle. Distinguish thin-tailed (seasonal flu) from fat-tailed (novel pandemic) risk. The precautionary principle as *policy* — maintaining infrastructure against the distribution of possible pandemics. Correlated tail risk.

Use research from `research/fat-tails.md`.

~400-500 words.

- [ ] **Step 2: Write section 8 — You Are Not the Average**

The ergodicity economics section. Core mathematical insight: ensemble ≠ time average. The simulation (Task 11) goes here. Frame carefully based on Task 8's findings — if the strong claim holds, say so; if not, say what actually happens.

**Clearly differentiate from section 5:** This is about one agent's path through time, not strategic interaction among many agents.

**Margin note:** Kelly criterion connection.

Use research from `research/ergodicity.md`.

~500-600 words + margin note.

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "draft: write sections 7-8 (Taleb, ergodicity economics)"
```

### Task 18: Write sections 9-10 (Synthesis + Coda)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Write section 9 — The Right Question**

Synthesis. The framework comparison visual (Task 12) goes here. Present the policy ladder. Show where frameworks agree (extremes) and disagree (Gray Threat). Articulate the "right question."

Use research from `research/institutional-design.md` to ground the policy ladder in real institutional mechanisms.

~500-600 words.

- [ ] **Step 2: Write section 10 — Coda**

Return to the pharmacy. Brief, grounded. The flu shot decision reframed. The "selfish" and "selfless" calculations, done properly, point the same direction (or nearly so, depending on Task 8 findings).

~150-200 words.

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "draft: write sections 9-10 (synthesis, coda)"
```

---

## Phase 5: Polish and Review

### Task 19: Add remaining margin notes and sidenotes

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Add margin notes not yet written**

Review the spec's sidenote list:
- Kelly criterion connection to ergodicity (may already be in section 8)
- Historical context on smallpox eradication campaign (use `research/epidemiology.md`)
- Technical details on simulation parameters and assumptions
- Adverse event rate data and how to interpret it

Use Quarto syntax:
```
::: {.column-margin}
Content here.
:::
```

- [ ] **Step 2: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "draft: add margin notes and sidenotes"
```

### Task 20: Full review and tighten

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd`

- [ ] **Step 1: Read the full essay end-to-end**

Check for:
- Argument flow: does each section motivate the next?
- Repetition: cut redundant points
- Data provenance: are sourced numbers cited and toy values labeled?
- Tone consistency: conversational but rigorous
- Simulation narration: does the prose explain what each plot shows?

- [ ] **Step 2: Tighten prose**

The spec says "lean and concise." Cut aggressively. Push detail to margin notes.

- [ ] **Step 3: Preview full post in Quarto**

```bash
quarto preview posts/2026-03-28-the-wrong-question/index.qmd
```

Verify: all plots render, code folds work, margin notes appear correctly, light/dark theme both look right.

- [ ] **Step 4: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "draft: review and tighten full essay"
git push
```

---

## Task Dependency Summary

```
Task 1 (scaffold) → all other tasks

Tasks 2-6 (research) → can run in parallel, all must complete before Phase 4

Task 7 (explore herd immunity) → Task 8 (test ergodicity claim)
Task 8 (test ergodicity claim) → Tasks 9-12 (production sims) and Tasks 13-18 (prose)

Tasks 9-12 (production sims) → can run in parallel once Task 8 is done
Tasks 13-18 (prose) → sequential, each builds on the last

Task 19 (margin notes) → after Tasks 13-18
Task 20 (review) → after everything
```

## Notes for the Implementer

- **Research files** in `research/` are working material, not published. Exclude them from Quarto rendering if needed (they're `.md` not `.qmd`, so Quarto should ignore them by default).
- **The Monty Hall post** (`posts/2010-11-26-monty-hall-monte-carlo-python/index.qmd`) is your template for code cell syntax, figure labels, and frontmatter.
- **Matplotlib colors:** Use colors that work with both Gruvbox light and dark themes. The existing post uses `#e74c3c` (red) and `#2ecc71` (green). Check both themes. For multi-line plots and the heatmap, use a colorblind-safe palette (e.g., the Okabe-Ito palette or matplotlib's `tab10` with verified distinguishability).
- **`execute: cache: true`** is set in the frontmatter — simulations only re-run when code changes.
- **Post is `draft: true`** — it renders locally but is excluded from listings and RSS.
- **Static plots only.** No plotly, no JS widgets. Matplotlib is the standard in this codebase.
- **uv** for any Python package management. No pip, no conda.
