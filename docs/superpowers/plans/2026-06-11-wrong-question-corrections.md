# "The Wrong Question" Corrections Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the confirmed simulation bugs and factual errors in `posts/2026-03-28-the-wrong-question/index.qmd`, and reframe the Free-Rider section so the figure and prose match the corrected model.

**Architecture:** Single Quarto post with embedded Python (`jupyter: python3`, `cache: true`). Each "test" is a render + a standalone recomputation of the key figure value, asserting it matches the prose. We fix the math first (it changes the narrative), then the prose, then the standalone factual one-liners.

**Tech Stack:** Quarto, Python (numpy, scipy, matplotlib) via project `.venv`. Render with `QUARTO_PROFILE=drafts QUARTO_PYTHON=.venv/bin/python quarto render <file>`.

---

## Why the reframe (read before starting)

Three independent reviews (local execution, Codex xhigh, Gemini 3.1 Pro) plus a Codex-verified stress test (verdict: SOUND-WITH-CAVEATS) established:

1. The original `find_nash_equilibrium` used **synchronous best-response updates that oscillate 0%↔100%** and never converge; the reported value was a parity artifact. The rendered `fig-free-rider` showed Nash coverage of **0%** for Measles/Smallpox/Gray Threat (gaps of 96/88/100 pp) — contradicting the prose, which says smallpox "Nash and social optimum nearly converge."
2. `perceived_benefit` used **population burden** `(1-1/Re)*(1-v*eff)*cfr`, double-counting the susceptible-fraction term. Personal risk for an unvaccinated person is `(1-1/Re)*cfr`.
3. Corrected (true fixed point + personal risk + efficacy factor), the **bare-rational free-rider gap is ≈0** at the essay's parameters, because adverse-event risk is ~2000× smaller than disease risk. A real, disease-dependent gap re-emerges only as **private/perceived vaccine cost** rises above the objective serious-adverse-event rate (multiplier `m`). This wedge includes inconvenience, needle aversion, mild side effects, ambiguity/trust — **not only "misperception."** Do not call it "misperception" in the prose; call it private/perceived cost.

Corrected reference numbers (π = 1−1/Re, benefit = eff·cfr·π, Nash = fixed point of the decreasing best-response map, social planner uses true risk):

| Disease | Threshold | Social opt | Nash m=1 | Nash m=20 | Nash m=100 |
|---|---|---|---|---|---|
| Measles | 96.2% | 96.2% | 96.2% | 95.9% | 94.6% |
| Smallpox | 87.7% | 87.7% | 87.7% | 87.7% | 87.5% |
| Gray Threat | 100% | 100% | 98.6% | 85.2% | 46.2% |
| Black Swan | 125%* | 100% | 100% | 99.9% | 89.7% |

*Black Swan threshold exceeds 100% (unreachable with imperfect vaccine). Key qualitative facts: bare gap ≈0; Measles gap small in pp but **sub-threshold for any m>1** (→ endemic); Smallpox needs no constraint (self-interest dominates at any m); Gray Threat gap grows fast with private cost.

---

## File Structure

- **Modify:** `posts/2026-03-28-the-wrong-question/index.qmd` — the only file changed. All code blocks, prose, and margin notes live here.
- **Scratch (not committed):** `/tmp/verify_*.py` — standalone recomputations used to verify each figure before committing.

Render/verify command used throughout (run from repo root):
```bash
QUARTO_PROFILE=drafts QUARTO_PYTHON=.venv/bin/python quarto render posts/2026-03-28-the-wrong-question/index.qmd 2>&1 | tail -5
```

Commit discipline: one commit per task, message describing the *why*.

---

## Task 1: Fix the free-rider model (personal risk + true Nash fixed point)

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd` — `fig-free-rider` code block (currently lines ~232–287: `compute_disease_burden`, `find_nash_equilibrium`, `find_social_optimum`).

- [ ] **Step 1: Write a standalone verification that the corrected model converges and reproduces the reference table**

Create `/tmp/verify_freerider.py`:
```python
import numpy as np
from scipy.stats import lognorm

def pi_unvax(v, R0, eff):
    """Personal lifetime infection risk for an unvaccinated person (endemic SIR)."""
    Re = R0 * (1 - v * eff)
    return max(0.0, 1 - 1 / Re) if Re > 1 else 0.0

def herd_threshold(R0, eff):
    return (1 / eff) * (1 - 1 / R0)

def nash_coverage(R0, eff, cfr, adv, m=1.0, sigma=0.8):
    """True Nash = fixed point of the decreasing best-response map (bisection).
    Agent vaccinates iff cost_sensitivity * m * adv < eff * cfr * pi_unvax(v)."""
    dist = lognorm(s=sigma, scale=1.0)
    def best_response(v):
        benefit = eff * cfr * pi_unvax(v, R0, eff)
        return dist.cdf(benefit / (m * adv))
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if best_response(mid) - mid > 0 else (lo, mid)
    return (lo + hi) / 2

def social_optimum(R0, eff, cfr, adv, sigma=0.8, n=3000):
    dist = lognorm(s=sigma, scale=1.0)
    best = (0.0, np.inf)
    for v in np.linspace(0, 1, n):
        disease = pi_unvax(v, R0, eff) * (1 - v * eff) * cfr
        vax = v * (dist.expect(lambda x: x, lb=0, ub=dist.ppf(v)) / v) * adv if v > 0 else 0.0
        if disease + vax < best[1]:
            best = (v, disease + vax)
    return best[0]

arch = [("Measles", 15, .97, .002, 1e-6), ("Smallpox", 6, .95, .30, 15e-6),
        ("Gray", 4, .75, .02, 1e-4), ("BlackSwan", 4, .60, .05, 5e-5)]
for name, R0, eff, cfr, adv in arch:
    print(f"{name:10s} thr={herd_threshold(R0,eff)*100:5.1f} opt={social_optimum(R0,eff,cfr,adv)*100:5.1f} "
          f"nash(m=1)={nash_coverage(R0,eff,cfr,adv,1)*100:5.1f} nash(m=20)={nash_coverage(R0,eff,cfr,adv,20)*100:5.1f}")
```

- [ ] **Step 2: Run it and confirm it matches the reference table**

Run: `cd /tmp && uv run --with numpy --with scipy python verify_freerider.py`
Expected (±0.2pp): `Measles thr=96.2 opt=96.2 nash(m=1)=96.2 nash(m=20)=95.9`; `Smallpox thr=87.7 opt=87.7 nash(m=1)=87.7 nash(m=20)=87.7`; `Gray thr=100.0 opt=100.0 nash(m=1)=98.6 nash(m=20)=85.2`; `BlackSwan opt=100.0 nash(m=1)=100.0 nash(m=20)=99.9`.

- [ ] **Step 3: Replace the model functions in the qmd**

In `fig-free-rider`, replace `compute_disease_burden`, `find_nash_equilibrium`, and `find_social_optimum` with these (note the new `m` private-cost multiplier, default 1.0, and the efficacy factor in the benefit):
```python
def personal_risk(coverage, R0, efficacy):
    """Lifetime infection probability for an *unvaccinated* individual (endemic SIR).
    Note: this is the individual's own risk, NOT population burden — it is not
    scaled by the susceptible fraction."""
    Re = R0 * (1 - coverage * efficacy)
    return max(0.0, 1 - 1 / Re) if Re > 1 else 0.0

def population_burden(coverage, R0, efficacy, cfr):
    """Fraction of the whole population suffering serious harm (used for the
    social optimum, where the susceptible-fraction scaling *is* correct)."""
    Re = R0 * (1 - coverage * efficacy)
    if Re <= 1:
        return 0.0
    return (1 - 1 / Re) * (1 - coverage * efficacy) * cfr

def find_nash_equilibrium(R0, efficacy, cfr, adverse_rate, m=1.0,
                          sigma=0.8, n_iter=80):
    """Voluntary-vaccination Nash equilibrium = the fixed point of the
    (decreasing) best-response map, found by bisection so it cannot oscillate.
    An agent vaccinates iff its private/perceived vaccine cost is below the
    expected benefit: cost_sensitivity * m * adverse_rate < efficacy * cfr * risk.
    m >= 1 scales the *private/perceived* vaccine cost above the objective
    serious-adverse-event rate (inconvenience, mild side effects, distrust, fear)."""
    from scipy.stats import lognorm
    dist = lognorm(s=sigma, scale=1.0)

    def best_response(coverage):
        benefit = efficacy * cfr * personal_risk(coverage, R0, efficacy)
        return dist.cdf(benefit / (m * adverse_rate))

    lo, hi = 0.0, 1.0
    for _ in range(n_iter):
        mid = (lo + hi) / 2
        if best_response(mid) - mid > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def find_social_optimum(R0, efficacy, cfr, adverse_rate, n_points=2000, sigma=0.8):
    """Coverage minimizing total social cost. The planner uses the *true*
    adverse-event rate (no private-cost inflation)."""
    from scipy.stats import lognorm
    dist = lognorm(s=sigma, scale=1.0)
    coverages = np.linspace(0, 1, n_points)
    total = []
    for c in coverages:
        disease_cost = population_burden(c, R0, efficacy, cfr)
        if c > 0:
            avg_sens = dist.expect(lambda x: x, lb=0, ub=dist.ppf(c)) / c
            vaccine_cost = c * avg_sens * adverse_rate
        else:
            vaccine_cost = 0.0
        total.append(disease_cost + vaccine_cost)
    return coverages[np.argmin(np.array(total))]
```

- [ ] **Step 4: Update the archetype loop and Black Swan handling**

The archetype loop already calls `find_nash_equilibrium(R0, eff, cfr, adv)` and `find_social_optimum(...)`. Leave the `m=1.0` default here (this figure shows the *bare-rational* baseline). Keep the existing Black Swan hatching. No tuple changes needed.

- [ ] **Step 5: Render and verify the figure now matches reality**

Run: `QUARTO_PROFILE=drafts QUARTO_PYTHON=.venv/bin/python quarto render posts/2026-03-28-the-wrong-question/index.qmd 2>&1 | tail -3`
Expected: `Output created: ...`. Then visually open `_site/posts/2026-03-28-the-wrong-question/index_files/figure-html/fig-free-rider-output-1.png` and confirm the Nash (orange) and Social-optimum (teal) bars are now **nearly equal** for all archetypes (gaps ≤ ~1.5 pp), i.e. the old "0% Nash / 96pp gap" artifact is gone.

- [ ] **Step 6: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "fix: correct free-rider model — personal risk + true Nash fixed point

The agent loop used synchronous best-response updates that oscillate 0<->100%
and never converge; reported value was a parity artifact (Nash=0% for measles/
smallpox/gray). It also used population burden as personal risk, double-counting
the susceptible fraction. Replace with a bisection fixed point of the decreasing
best-response map, personal risk = 1-1/Re, benefit = eff*cfr*risk, and a private-
cost multiplier m (default 1). Bare-rational gap is now ~0, matching theory.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 2: Add the private-cost panel that shows where the gap actually comes from

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd` — add a second figure after `fig-free-rider` (a new `{python}` block, label `fig-private-cost`).

This replaces the deleted "enormous free-rider tax" story with the real one: the gap is ≈0 under objective costs and grows disease-dependently as private/perceived cost rises.

- [ ] **Step 1: Add the figure block**

Insert immediately after the `fig-free-rider` block:
````markdown
```{python}
#| label: fig-private-cost
#| fig-cap: "Where the free-rider gap actually comes from. Under objective vaccine costs (left edge, m=1) voluntary coverage essentially reaches the social optimum for every disease. A gap opens only as the *private/perceived* cost of vaccination rises above the objective serious-adverse-event rate (m). For measles the coverage gap stays small in percentage points — but any m>1 puts coverage below the herd threshold, so the consequence (endemic vs. eliminated) is binary. For the moderate-contagion Gray Threat the gap grows steeply. For high-severity smallpox, self-interest alone holds coverage near the optimum regardless of m."

ms = np.linspace(1, 100, 40)
fig, ax = plt.subplots(figsize=(9, 5))
colors = {"Measles-like": "#c9613a", "Smallpox-like": "#458588",
          "Gray Threat": "#b16286", "Black Swan": "#7c6f64"}
for name, R0, eff, cfr, adv in [("Measles-like", 15.0, 0.97, 0.002, 1e-6),
                                ("Smallpox-like", 6.0, 0.95, 0.30, 15e-6),
                                ("Gray Threat", 4.0, 0.75, 0.02, 1e-4),
                                ("Black Swan", 4.0, 0.60, 0.05, 5e-5)]:
    opt = find_social_optimum(R0, eff, cfr, adv) * 100
    gaps = [opt - find_nash_equilibrium(R0, eff, cfr, adv, m=m) * 100 for m in ms]
    ax.plot(ms, gaps, linewidth=2.2, label=name, color=colors[name])

ax.set_xlabel("Private / perceived vaccine cost, relative to objective risk (m)", fontsize=12)
ax.set_ylabel("Free-rider gap (social optimum − Nash, pp)", fontsize=12)
ax.set_title("The Free-Rider Gap Is Driven by Perceived Cost, Not Bare Self-Interest", fontsize=13)
ax.legend(fontsize=10, loc="upper left")
ax.set_xlim(1, 100)
ax.set_ylim(0, None)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()
```
````

- [ ] **Step 2: Render and verify the four curves behave per the reference table**

Run the render command. Then confirm in the PNG: at m=1 all gaps ≈0; Gray Threat rises steeply (≈15pp by m=20, where Nash=85.2 vs opt=100); Smallpox stays flat near 0; Measles rises only gently (≈0.3pp at m=20). Cross-check one value:
Run: `cd /tmp && uv run --with numpy --with scipy python -c "import verify_freerider as v; print('Gray gap m=20:', round(v.social_optimum(4,.75,.02,1e-4)*100 - v.nash_coverage(4,.75,.02,1e-4,20)*100,1))"`
Expected: `Gray gap m=20: 14.8` (±0.5).

- [ ] **Step 3: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "feat: add private-cost panel showing the real source of the free-rider gap

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 3: Rewrite the Free-Rider prose to match the corrected figures

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd` — the prose of "The Free-Rider Trap" section (currently lines ~208–365), especially the paragraphs after `fig-free-rider` (lines ~351–361) and the setup at lines ~224–226.

- [ ] **Step 1: Fix the model-description paragraph (was lines ~224–226)**

Replace the sentence describing the model (the one beginning "Each agent compares the perceived cost of vaccination...") so it states: agents compare their **private/perceived** vaccine cost against the personal benefit (efficacy × disease risk for an unvaccinated person), and the equilibrium is the fixed point where no agent wants to switch. Remove any claim that the model "iterates until it reaches a Nash equilibrium" via repeated coverage updates — it is solved as a fixed point. Add one sentence: "Crucially, the relevant cost is not the objective rate of serious vaccine harm but the cost each person *perceives* — which folds in inconvenience, mild side effects, distrust, and fear alongside genuine risk."

- [ ] **Step 2: Replace the three results paragraphs (was lines ~351–361)**

Replace the "The pattern is striking... free-rider tax is enormous" / smallpox / Gray Threat / Black Swan paragraphs with prose consistent with the corrected figures. Required claims (write in the essay's voice, ~4 short paragraphs):
  - **Baseline (objective cost):** when the only vaccine cost is the objective rate of serious harm, self-interest essentially reaches the social optimum for every archetype — the bare-rational free-rider gap is close to zero. The dramatic "everyone defects" story is an artifact of treating vaccination as more costly than it objectively is.
  - **Measles:** the gap in *coverage* stays small even as perceived cost climbs — measles is so contagious that an unvaccinated person's risk stays high until coverage is almost exactly at threshold. But "almost at threshold" is precisely the cliff from the nonlinearity section: any wedge of perceived cost pushes voluntary coverage *below* the threshold, flipping the disease from eliminated to endemic. Small gap, decisive consequence.
  - **Smallpox:** with a 30% fatality rate, the personal benefit swamps any plausible perceived cost, so voluntary coverage tracks the optimum regardless. You don't need to invoke collective duty when survival instinct does the work. (This claim is unchanged from the original and is correct.)
  - **Gray Threat / Black Swan:** moderate contagion plus a higher perceived cost opens a genuinely large gap, and the herd threshold is unreachable anyway — so the policy target itself is murky. This is where disagreement is real.
  - End with the bridge sentence already in the essay (game theory reveals the trap but not how to escape it).

- [ ] **Step 3: Update the threshold margin note (was lines ~216–217 and ~220–221)**

Keep the Bauch & Earn (2004) and Geoffard & Philipson (1997) citations — they are correct and now *more* apt. Adjust the public-goods margin note so it no longer implies a huge standing gap; the divergence is sharpest near the threshold and grows with perceived cost.

- [ ] **Step 4: Render and read the section end-to-end for figure/prose consistency**

Run the render command. Open the rendered HTML section and confirm: no remaining sentence claims a large measles/smallpox free-rider gap; the prose matches both figures.

- [ ] **Step 5: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "fix: rewrite free-rider prose to match corrected model

Reframe around private/perceived vaccine cost (not 'misperception'): bare-rational
gap ~0, gap grows disease-dependently with perceived cost, measles' small coverage
gap is decisive via the threshold nonlinearity. Smallpox claim unchanged.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 4: Fix the ergodicity prose/figure contradiction

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd` — prose after `fig-ergodicity` (currently lines ~531–543).

The sim at `coverage_gt = 0.70` gives `p_inf ≈ 0.47`, so the free-rider *mean* health collapses — which contradicts "Free-riders' mean health holds up... free-riding pays." The outright disagreement zone is razor-thin (`p_inf ≈ 2.4%`, requiring coverage ≈ 99%), which the essay already admits at lines ~539–541. Fix the setup prose to match; do not change the simulation coverage (keeping 0.70 keeps the trajectory plot legible).

- [ ] **Step 1: Verify the actual simulation outcome to quote correct numbers**

Create `/tmp/verify_ergodicity.py`:
```python
import numpy as np
rng = np.random.default_rng(42)
R0, eff, cov, sev, vax_cost, N, T = 4.0, 0.75, 0.70, 0.20, 0.005, 1000, 40
Re = R0 * (1 - cov * eff)
p_inf = 1 - 1 / Re if Re > 1 else 0.0
vax = np.ones((N, T + 1)); free = np.ones((N, T + 1))
for t in range(T):
    vax[:, t + 1] = vax[:, t] * (1 - vax_cost)
    hit = rng.random(N) < p_inf
    free[:, t + 1] = free[:, t] * np.where(hit, 1 - sev, 1.0)
print(f"p_inf={p_inf:.3f}  free mean(final)={free[:,-1].mean():.3f}  "
      f"free median(final)={np.median(free[:,-1]):.3f}  vax mean(final)={vax[:,-1].mean():.3f}")
```
Run: `cd /tmp && uv run --with numpy python verify_ergodicity.py`
Expected: `p_inf=0.474 free mean(final)≈0.20 free median(final)≈0.09 vax mean(final)≈0.82` (free-rider mean clearly *declines*, median worse).

- [ ] **Step 2: Rewrite the two paragraphs after the figure (was lines ~531–533)**

Replace the "Free-riders' mean health holds up... Expected-value reasoning says 'free-riding pays'" framing. New claims, consistent with the numbers above:
  - At this coverage the free-rider *mean* health already declines (to ~0.20 over 40 years) — even ensemble/expected-value reasoning favors vaccinating here. The point is not that the mean "looks fine."
  - The signature of non-ergodicity is the **gap between mean and median** (~0.20 vs ~0.09) and the spread of individual trajectories: the mean is propped up by a lucky minority who dodged every hit, while the typical lived trajectory is far worse.
  - Keep the existing honest admission (lines ~539–541) that the outright *direction*-disagreement zone is razor-thin (~0.25 pp) and the real finding is **magnitude** — ensemble reasoning systematically understates the cost of free-riding. This now reads consistently with the setup instead of contradicting it.

- [ ] **Step 3: Render and verify**

Run the render command. Confirm the paragraphs above `fig-ergodicity`'s discussion no longer say the mean "holds up" or that "free-riding pays," and that the mean/median numbers cited match the figure.

- [ ] **Step 4: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "fix: align ergodicity prose with what the simulation shows

At coverage 0.70 the free-rider mean declines too; the real signal is the
mean-median gap and trajectory spread, not 'free-riding pays.' Matches the
essay's own later admission that the direction-disagreement zone is razor-thin.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 5: Fix the standalone factual errors

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd` — independent one-line prose/margin edits. Each is exact-string replacement.

- [ ] **Step 1: Jensen domain (was line ~536)**

Find: `Jensen's inequality guarantees $\ln(1-c)/\ln(1-L) < c/L$ for all $L > 0$`
Replace `for all $L > 0$` with `for all $0 < c < L$` (verified: 700/2500 grid violations when `c ≥ L`; holds in the sensible regime where the vaccine costs less than the disease).

- [ ] **Step 2: VICP excise tax (was line ~720)**

Find: `The US Vaccine Injury Compensation Program ($0.75 excise tax per dose)`
Replace `per dose` with `per disease prevented per dose — $2.25 for a three-disease vaccine like MMR`. (HRSA: $0.75 per taxable disease.)

- [ ] **Step 3: Vavřička miscitation (was line ~638)**

Find the policy-ladder level-5 example: `France's 11-vaccine mandate, upheld in *Vavřička v. Czech Republic*, 2021`
Replace with: `France's 11-vaccine childhood mandate; the comparable Czech regime was upheld in *Vavřička v. Czech Republic*, 2021`. (The ECHR case concerned the Czech mandate, not France's.)

- [ ] **Step 4: Fire-death risk comparison (was line ~185)**

Find: `The Gray Threat's hypothetical rate (1 in 10,000) is closer to the lifetime risk of dying in a fire.`
Replace `the lifetime risk of dying in a fire` with `the lifetime risk of dying from accidental electrocution or exposure to excessive heat`. (US lifetime fire-death risk is ~1 in 1,300 — an order of magnitude off; pick an event that is genuinely ~1 in 10,000.)

- [ ] **Step 5: "Most contagious" overclaim (was line ~42)**

Find: `measles — the most contagious common infectious disease we know`
Replace `the most contagious` with `one of the most contagious`. (Matches CDC phrasing; avoids an unsourced superlative.)

- [ ] **Step 6: 96% vs threshold rounding (was lines ~118 and ~214)**

Line ~118: Find `By 96% coverage, infections drop to near zero` → replace `By 96%` with `By about 97%` (the threshold is 96.2%, so 96% is still marginally below it).
Line ~214: Find `Going from 96% to 95% coverage doesn't reduce herd protection by 1%. It can destroy it entirely.` → replace with `Crossing from just above the threshold to just below it doesn't reduce herd protection by a little. It can destroy it entirely.`

- [ ] **Step 7: Measles complication rates (was line ~178)**

Find: `with serious complications (encephalitis, pneumonia) affecting another 1-3 per 1,000`
Replace with: `with pneumonia in up to 1 in 20 children, encephalitis in roughly 1 in 1,000, and death in 1-3 per 1,000 in developed countries`. (Separates endpoints per CDC; the original folded pneumonia in at far too low a rate.) Then adjust the following sentence's "Total serious-harm probability from infection: about 3 per 1,000" to "Mortality and encephalitis alone run about 3-4 per 1,000, with milder serious complications considerably more common" so the downstream 3,000:1 ratio still parses (the order-of-magnitude conclusion is unchanged).

- [ ] **Step 8: Cirillo–Taleb hedge (was line ~412)**

Find: `found a tail exponent $\alpha < 1$ — meaning infinite mean and variance`
Replace with: `fit a tail exponent $\alpha < 1$ under their dual-distribution model — implying, within that model, an infinite theoretical mean and variance (a conclusion later authors have contested)`. (The infinite-mean claim is model-dependent and disputed.)

- [ ] **Step 9: Measles annual-case figure (was line ~121)**

Find: `Today, with coverage in the low 90s, annual cases number in the hundreds`
Replace with a dated, range-based statement: `From 2020-2024, US coverage in the low 90s held annual cases to the dozens-to-low-hundreds; a 2025-2026 resurgence pushed that into the thousands as coverage slipped`. (Codex via web search reports >2,000 US cases in 2025 and 2026 — verify against the current CDC measles-cases page before committing; if you cannot confirm, use "From 2020-2024... dozens to low hundreds" and drop the resurgence clause rather than assert an unverified number.)

- [ ] **Step 10: Render and verify all edits land cleanly**

Run the render command. Expected: `Output created: ...` with no errors. Grep the source to confirm no stale strings remain:
Run: `grep -n "per dose\|most contagious common\|for all \$L > 0\|number in the hundreds\|dying in a fire" posts/2026-03-28-the-wrong-question/index.qmd`
Expected: no matches (all replaced).

- [ ] **Step 11: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "fix: factual corrections from review (VICP, Vavricka, risk comparisons, rates)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 6: Update synthesis section + final full render

**Files:**
- Modify: `posts/2026-03-28-the-wrong-question/index.qmd` — "The Right Question" synthesis (currently lines ~621–735), specifically the Game Theory row of the framework heatmap and its column commentary, which assumed a large free-rider gap.

- [ ] **Step 1: Reconcile the framework heatmap commentary**

The heatmap `levels` matrix (lines ~661–667) is explicitly the author's qualitative judgment — it does not need to be recomputed. But the surrounding prose (lines ~711–717, the "Read the columns" paragraphs) describes the Game Theory framework as showing an "enormous" free-rider gap for measles. Edit those sentences so Game Theory's contribution is stated as: voluntary coverage falls *just* short of the threshold under any positive perceived cost, and that small shortfall is decisive because of the nonlinearity — not a large standing gap. Keep the Measles/Smallpox "frameworks mostly agree" conclusion (still true) and the Gray Threat "frameworks scatter" conclusion (still true).

- [ ] **Step 2: Check the "3,000 to 1" and "30 to 1" EV ratios still hold after Task 5 Step 7**

Re-read the EV section (lines ~178–192) after the complication-rate edit. The benefit-to-cost ratio claims (3,000:1 for measles, 30:1 for Gray Threat) must still parse. If the revised serious-harm number changed the stated arithmetic, adjust the ratio sentences so the numbers are internally consistent (the order-of-magnitude conclusion is unchanged; only ensure the quoted multiplication still works).

- [ ] **Step 3: Full site render with the drafts profile**

Run: `QUARTO_PROFILE=drafts QUARTO_PYTHON=.venv/bin/python quarto render posts/2026-03-28-the-wrong-question/index.qmd 2>&1 | tail -5`
Expected: `Output created: ...`, no Python errors.

- [ ] **Step 4: Read the full rendered post once, start to finish**

Open `_site/posts/2026-03-28-the-wrong-question/index.html`. Confirm: every figure matches its caption and the surrounding prose; no internal contradictions remain; all five corrected/added figures render.

- [ ] **Step 5: Commit**

```bash
git add posts/2026-03-28-the-wrong-question/index.qmd
git commit -m "fix: reconcile synthesis commentary with corrected free-rider result

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 7: Final review gate (do NOT publish yet)

- [ ] **Step 1: Run a Codex xhigh review of the final diff**

Per the project's Review & Approval Protocol, get a final verdict before considering publication:
```bash
git diff cf3d6c7..HEAD -- posts/2026-03-28-the-wrong-question/index.qmd > /tmp/wq-final.diff
codex exec --sandbox read-only -c model_reasoning_effort="xhigh" -c tools.web_search=true \
  "Review this diff to a vaccination-policy essay for any remaining factual errors, figure/prose contradictions, or modeling mistakes. The free-rider model was rebuilt around a true Nash fixed point and a private-cost multiplier; verify the prose now matches the figures. Diff:\n$(cat /tmp/wq-final.diff)" \
  < /dev/null > /tmp/codex-wq-final.txt 2>&1
```
Read the final answer (after the last `codex` marker). Triage findings; apply fixes; re-review until clean.

- [ ] **Step 2: Leave `draft: true` in place**

Do not remove `draft: true`. Publishing is a separate, explicit decision for Jonathan after this review gate passes. Report the final verdict and stop.

---

## Self-Review (completed)

- **Spec coverage:** (A) bugs → Tasks 1, 4; (B) reframe → Tasks 2, 3, 6; (C) factual fixes → Task 5; modeling refinements (π=1−1/Re, eff factor) → Task 1. Synthesis consistency → Task 6. Review gate → Task 7. All covered.
- **Placeholder scan:** Task 5 Step 9 (measles case count) intentionally contains a verify-or-fallback instruction rather than a hard number, because the figure is time-sensitive and must be checked against the live CDC page at execution time — this is a deliberate guard, not a placeholder.
- **Consistency:** Function names align across tasks (`personal_risk`, `population_burden`, `find_nash_equilibrium(…, m=…)`, `find_social_optimum`). The `m` multiplier defaults to 1.0 in `fig-free-rider` (Task 1) and is swept in `fig-private-cost` (Task 2). Reference numbers in the header table match the verification scripts in Tasks 1–2.
