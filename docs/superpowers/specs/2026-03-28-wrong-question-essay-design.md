# The Wrong Question — Essay Design Spec

**Date:** 2026-03-28
**Type:** Draft blog post with simulations
**Status:** Design approved

## Overview

A long-form essay arguing that the "individual rights vs. collective obligations" framing of public health policy (vaccination specifically) is a false dichotomy. The tension dissolves when examined through the right mathematical and philosophical lenses — particularly ergodicity economics, which shows that ensemble averages and time averages diverge for non-ergodic systems, collapsing the apparent conflict between self-interest and collective welfare.

## Audience

Mixed: accessible core argument for educated general readers, with quantitative depth (code-folded simulations, sidenotes) for those who want to dig in. Written for the blog at jonathanwhitmore.com using Quarto.

## Central Thesis

The "individual rights vs. public good" debate around vaccination policy is mal-posed. It arises from a framing error — specifically, from treating non-ergodic systems as ergodic (using ensemble averages where time averages are what matter). Multiple frameworks (game theory, Rawls, Taleb, ergodicity economics) each expose different flaws in the standard framing. Under the correct mathematical treatment, the "selfish" and "selfless" calculations converge.

## Core Device

A **parameter space** of disease/vaccine/population characteristics, introduced first as a single intuitive dial (0–100% vaccination with consequences from trivial to catastrophic), then expanded to the full multi-dimensional reality. Four archetypal scenarios anchor the analysis:

1. **Measles-like:** R0 ~15, severe, excellent vaccine, herd threshold ~95%. Historical anchor. Strong mandate case.
2. **Smallpox-like:** R0 ~5-7, devastating severity, effective vaccine, eradication achieved. Historical proof of concept.
3. **"Gray Threat" (hypothetical):** Moderate R0, moderate severity, decent but imperfect vaccine with non-trivial adverse rate, uncertain herd threshold. The hard case where frameworks disagree.
4. **"Black Swan Pandemic" (hypothetical):** Novel pathogen, high uncertainty on all parameters, fat-tailed severity. Taleb's territory.

## Essay Structure

### 1. The Pharmacy Moment (Opening Hook)
You're standing in a pharmacy. "Want a flu shot today?" Simple personal question — zoom out to the policy question: what if the consequences of low vaccination ranged from trivial to catastrophic? At what point does coercion become justified, and how do you decide?

### 2. The Single Dial (Intuition Builder)
Introduce the spectrum: 0–100% vaccination, consequence from negligible to societal collapse. At the extremes, the answer is obvious. The essay lives in the middle. Introduce the non-linear herd immunity S-curve.

**Simulation:** Interactive plot of the herd immunity benefit curve (S-curve).

### 3. The Real Complexity (Parameter Space)
Reveal the multi-dimensional reality: severity, R0, incubation period, vaccine effectiveness, adverse event rate, epistemic uncertainty. Introduce the four archetypal clusters.

### 4. The Default Answer (Expected Value as Foil)
The naive utilitarian cost-benefit calculation. Show it with actual numbers for each archetype. Then expose the cracks: insensitive to non-linearity, treats individuals as interchangeable with population averages, gives the same recommendation regardless of current vaccination rate.

### 5. The Free-Rider Trap (Game Theory)
Vaccination as a public goods game with non-linear payoffs. The payoff matrix shifts along the herd immunity curve. Individual rationality produces collective irrationality — but severity depends on position in parameter space.

**Simulation:** Monte Carlo population model. Agents make individually "rational" decisions. Show how collective outcomes degrade non-linearly as free-riding increases. Apply to each archetype.

### 6. Behind the Veil (Rawls)
Behind the veil of ignorance — unknown immune status, age, population vaccination state — what policy would you design? Key insight: you'd consent to mandates earlier than revealed preferences suggest, because you'd weight worst-case positions.

**Sidenote:** The Rawlsian case strengthens non-linearly with population uncertainty. If you don't know the vaccination rate, the marginal value of your contribution has higher variance, and Rawlsian reasoning is risk-averse.

### 7. When the Tail Wags the Dog (Taleb / Fat Tails)
Under fat-tailed pandemic risk, you don't optimize expected value — you avoid ruin. The precautionary principle as policy: maintaining vaccination infrastructure/readiness is about the distribution of possible pandemics, not any single disease. The individual-vs-collective framing is especially bankrupt here because tail risk is correlated.

### 8. You Are Not the Average (Ergodicity Economics)
The core mathematical insight. Ensemble average ≠ time average for non-ergodic processes. What looks rational for "the population" can be irrational for any individual, and vice versa. The "individual vs. collective" framing assumes ergodicity. Drop that assumption and the dichotomy dissolves.

**Simulation:** Side-by-side ensemble vs. time-average divergence for a health/vaccination model.

### 9. The Right Question (Synthesis)
Bring frameworks together. Show where each draws the mandate threshold for each archetype (table or visual). They disagree informatively. The right question: "What policy would I design for the sequence of decisions a society faces over time, under uncertainty about disease parameters, population state, and individual vulnerability?" This is simultaneously self-interested and pro-social — not as moral compromise, but as mathematical consequence.

### 10. Coda
Return to the pharmacy. The flu shot decision, seen correctly, isn't about your rights vs. society's claim on you. It's about understanding the system you're embedded in.

## Simulations

All simulations in Python, code-folded in Quarto, results prominent. Code is secondary — documented for those who care, but not the star.

1. **Herd immunity S-curve** (section 2) — Non-linear benefit of vaccination as a function of population coverage.
2. **Monte Carlo free-rider model** (section 5) — Population of agents making individually rational vaccination decisions. Shows collective degradation under free-riding across archetypes.
3. **Ensemble vs. time-average divergence** (section 8) — Demonstrates that population-average outcomes differ from individual-over-time outcomes in a vaccination/health model.
4. **Framework comparison** (section 9) — Table or heatmap showing where each framework draws the mandate threshold for each archetype.

## Deep Research Tasks

To be delegated to deep research tools (Gemini/Codex):

1. **Epidemiological data:** Real herd immunity thresholds, R0 values, vaccine efficacy rates, adverse event rates for measles and smallpox vaccines. Historical vaccination coverage data.
2. **Philosophy / political theory:** Rawls on public health obligations and the veil of ignorance applied to health policy. Mill's harm principle applied to vaccination. Communitarian vs. libertarian arguments.
3. **Ergodicity economics:** Ole Peters' key papers and arguments. Ensemble vs. time-average distinction. Applications to policy decisions. Kelly criterion connection.
4. **Taleb / fat tails:** Precautionary principle papers. Fat-tail arguments applied to pandemic policy. Distinction between thin-tailed and fat-tailed risk domains.

## Sidenotes / Margin Content

- Rawlsian herd-immunity-under-ignorance result (the non-linear marginal contribution under population uncertainty)
- Kelly criterion connection to ergodicity economics
- Historical context on smallpox eradication campaign
- Technical details on simulation parameters and assumptions
- Adverse event rate data and how to interpret it

## Format

- Quarto blog post (`posts/YYYY-MM-DD-the-wrong-question/index.qmd`)
- Draft mode (`draft: true`) until ready
- Code-folded Python simulations
- Margin notes / sidenotes for depth
- Lean core argument with detail pushed to notes

## Design Decisions

- **Avoid COVID:** Use measles, smallpox, and hypothetical pandemics to avoid political gravity.
- **Policy framing over personal framing:** The central question is "when should society mandate?" not "should I get vaccinated?" — though the personal angle opens and closes the essay.
- **Single dial first, then parameter space:** Build intuition before revealing complexity.
- **Expected value as foil:** The framework everyone defaults to, shown to be insufficient from multiple angles.
- **Ergodicity as resolution, not just critique:** The essay doesn't just tear down framings — it offers a mathematically grounded alternative that dissolves the tension.

## Open Questions

- Exact title (working title: "The Wrong Question")
- Whether the stronger claim holds: that under ergodicity economics the individual/collective tension fully dissolves (needs exploratory simulation to verify)
- How much historical narrative to include for measles/smallpox (deep research will inform this)
- Whether the framework comparison in section 9 works better as a table, heatmap, or narrative
