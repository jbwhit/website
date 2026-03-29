# Ergodicity Economics

This note synthesizes the core concepts of ergodicity economics, its relationship to the Kelly criterion, and its specific (often inferential) applications to public health and vaccination policy. It distinguishes between the explicit claims made by the framework's founders, the applications developed by adjacent thinkers, and the criticisms from mainstream economics.

## Core framework

### Ensemble Averages versus Time Averages

Ole Peters' central argument in ergodicity economics challenges a foundational assumption in standard economic reasoning: the use of expected value (or expected utility) to evaluate risky decisions.

- An **ensemble average** calculates the expected outcome across many parallel copies of a system at a single point in time (e.g., the average outcome if a million people take a gamble once).
- A **time average** calculates the compounded outcome for a *single* system (or person) as it evolves through time (e.g., the outcome if one person takes the gamble a million times sequentially).

A process is **ergodic** if the ensemble average equals the time average. However, Peters argues that most real-world economic and health processes are **non-ergodic**. For non-ergodic processes—particularly those involving multiplicative compounding or irreversible "ruin"—using the ensemble average (probability) to guide an individual's time-series decision can lead to catastrophic advice.

### "The ergodicity problem in economics" (2019)

In his 2019 *Nature Physics* paper, Peters argues that mainstream economics historically tried to fix a math problem (non-ergodicity) by inventing a psychological concept (risk aversion via Expected Utility Theory). 

The core argument is:
- Ergodicity is a highly restrictive property, not a safe default assumption.
- Wealth and health are often dynamic, multiplicative growth processes far from equilibrium.
- In these settings, individuals naturally and rationally optimize their **time-average growth rate** rather than an expectation over hypothetical parallel worlds.
- What behavioral economists call "irrational risk aversion" is often simply a rational individual refusing to play a non-ergodic game where the time-average is negative, even if the ensemble-average is positive.

### The Simplest Coin-Flip Gamble

The classic intuition pump used by Peters is a repeated multiplicative coin-flip game.

Imagine a gamble where your total wealth is multiplied based on a coin flip:
- Heads (50%): Wealth multiplies by 1.5 (+50%)
- Tails (50%): Wealth multiplies by 0.6 (-40%)

**Ensemble Average (Parallel Universes):**
- The expected multiplier per round is `(1.5 * 0.5) + (0.6 * 0.5) = 1.05`.
- In expectation across many people, wealth grows by 5% per round. It looks like a great bet.

**Time Average (One Person Over Time):**
- If you play repeatedly, the time-average multiplier per round converges to the geometric mean: `(1.5 * 0.6)^(1/2) = (0.9)^(1/2) ≈ 0.948`.
- For an individual playing sequentially, wealth shrinks by about 5.2% per round. Over time, the probability of approaching ruin (wealth going to zero) approaches 100%.

The expected log growth is negative: `0.5 * ln(1.5) + 0.5 * ln(0.6) = 0.5 * ln(0.9) ≈ -0.052`. 

### Growth-Rate Optimal Strategy

Under ergodicity economics, rather than maximizing expected value (which tolerates huge downside risks if the upside is astronomically high), rational actors in multiplicative environments maximize **expected log growth**. This approach severely punishes the risk of ruin, because a single zero multiplier sets the entire compounding time-series to zero permanently.

## Kelly Criterion Connection

### Relationship to Ergodicity Economics

The Kelly criterion (developed by J.L. Kelly Jr. in 1956) is the mathematical predecessor and closest cousin to ergodicity economics. While Kelly designed a formula for optimal bet sizing to maximize the long-term compounding growth rate of wealth, Peters generalized this concept into a broader critique of economic theory. 

Both frameworks share identical fundamental math:
- They treat wealth (or health) as a dynamic, compounding process.
- They aim to maximize the geometric growth rate (logarithmic utility).
- They recognize that "overbetting" even a positive-expected-value proposition will reduce long-term growth and guarantee eventual ruin.

### "Growth-Rate Optimal" Betting and Health Decisions

In a public health context, a "growth-rate optimal" strategy means allocating resources or making individual choices that maximize the long-term survival and flourishing (growth rate) of an individual's health time-series. Just as the Kelly criterion demands fractional betting to ensure one never goes bankrupt, applying it to health means avoiding irreversible "ruin" (death, permanent disability) at almost all costs.

Repeated exposure to pathogens is analogous to placing repeated bets. A disease might have a low probability of death per infection, but over a lifetime of seasonal exposures, the risk of "ruin" compounds.

## Application to Health and Policy

### Direct Applications in the Literature

Direct application of ergodicity economics in formal public health literature is relatively sparse, but the concepts are heavily championed by adjacent thinkers:
- **Nassim Taleb:** Uses ergodicity and the Precautionary Principle to argue against taking systemic tail risks (like novel pandemics). He emphasizes that avoiding ruin is the only rational strategy in non-ergodic domains.
- **Luca Dellanna:** Applies ergodicity to behavioral health and management, arguing that people who seem "paranoid" about small risks (or small side effects) are rationally protecting their non-repeating time-series from irreversible ruin.

The closest mainstream applications involve insurance decisions, disaster-risk management, and portfolio choice under multiplicative uncertainty.

### Framing Vaccination Decisions in Ergodicity Terms

Health over a lifetime is fundamentally a non-ergodic process. You cannot die in 10% of parallel universes and average it out; death is an absorbing state that ends the time-series.

A stylized ergodicity model of vaccination:
- **Vaccination:** Imposes a known, highly predictable, and generally additive small cost $c$ (sore arm, small risk of severe reaction). It protects against severe disease.
- **Disease Exposure:** Involves a probability $p$ of a massive, multiplicative loss $L$ (death, long COVID) that permanently impairs the body's future "growth" capacity.

**Does time-average optimal behavior differ from ensemble-average optimal behavior?**
Yes. An expected-value public health official looks at the ensemble: "If 1 million people get sick, only 10,000 die, and 990,000 acquire natural immunity. The average population outcome is acceptable." 

An individual looking at their time-average recognizes that natural infection introduces a distinct risk of an absorbing state (ruin). If the vaccine's risk of ruin is orders of magnitude lower than the disease's risk of ruin, the time-average optimal decision strongly favors vaccination, even if the vaccine has high additive costs (like feeling sick for a day).

### Explaining Vaccine Hesitancy

Conversely, ergodicity economics elegantly explains rational vaccine hesitancy. If an individual *perceives* the vaccine itself as carrying a risk of ruin (e.g., a rare fatal blood clot), they are faced with two competing tail risks. If they believe their probability of encountering the disease is low (perhaps due to others vaccinating), but the vaccine intervention is a guaranteed exposure to a non-zero risk of ruin, a time-average optimizer will reject the vaccine. Public health messaging fails when it quotes ensemble averages ("safe for 99.999% of people") to an individual trying to solve for $P=1$ survival of their own time-series.

## Criticisms and Limitations

### The Mainstream Economics Critique

Mainstream economists (such as Jason Doctor, Peter Wakker, Alexis Akira Toda, and others) have fiercely criticized ergodicity economics:

1. **Redundancy (Isomorphism):** Critics argue that maximizing the time-average growth rate is mathematically identical to Expected Utility Theory (EUT) using a logarithmic utility function ($U(w) = \ln(w)$). Therefore, EE is just EUT rebranded, not a new paradigm.
2. **Mischaracterization of EUT:** Critics argue Peters attacks a straw man. EUT does not assume "parallel universes" or ergodicity. It is a static theory of preferences at a moment in time, and economists already have advanced dynamic models (like Life-Cycle Consumption) for time-series optimization.
3. **One-Size-Fits-All Risk Aversion:** EE implies everyone *should* maximize log-growth. Economists argue this dictatorially imposes a specific level of risk aversion on everyone, ignoring individual subjective preferences (e.g., a retiree and a teenager should have different risk tolerances).
4. **"Pseudoscience" Claims:** Some critics (e.g., Toda) have called EE pseudoscience because it oversells its novelty, is practically unfalsifiable regarding human preferences, and dismisses decades of established economic literature.

### Peters and Co-Authors' Response

Peters and his defenders argue:
- **Dynamics First:** Even if the math maps to logarithmic utility, the *reasoning* matters. Utility should not be smuggled in as a subjective psychological quirk ("risk aversion") if the physical dynamics of the system already dictate that a linear expectation leads to physical ruin.
- **Objective vs. Subjective:** They argue it is scientifically superior to derive risk behavior from the objective properties of the environment (the compounding nature of the gamble) rather than arbitrarily tweaking subjective utility functions to fit observed behavior.

### Conclusion for the Essay

For the purposes of vaccination policy, ergodicity economics provides a powerful clarifying lens. It demonstrates that individuals naturally and rationally evaluate health interventions based on the avoidance of irreversible ruin to their personal time-series, rather than maximizing the ensemble averages preferred by public health cost-benefit analyses. A successful mandate or policy must address individual ruin explicitly, rather than dismissing it as a statistical rounding error.

## References

- Peters, Ole. "The ergodicity problem in economics." *Nature Physics* 15 (2019): 1216-1221.
- Peters, Ole, and Murray Gell-Mann. "Evaluating gambles using dynamics." *Chaos* 26 (2016).
- Kelly, J. L. Jr. "A New Interpretation of Information Rate." *Bell System Technical Journal* 35 (1956): 917-926.
- Taleb, Nassim Nicholas. *Skin in the Game* and *The Black Swan*. (Applications of non-ergodicity and absorbing barriers to risk).
- Dellanna, Luca. *Ergodicity*. (Application of EE to individual behaviors and health).
- Toda, Alexis Akira. "Ergodicity Economics is Pseudoscience." (Critical review representing the mainstream economics backlash).
- Ford, Nick, and John Kay. "Critique of ergodicity economics," and reply / rejoinder discussion in *Econ Journal Watch* 21, no. 1 (2024).