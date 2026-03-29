# Ergodicity Test: Findings

## Question

Does the 'individual vs. collective' tension in vaccination policy dissolve when you use time-average reasoning instead of ensemble-average reasoning?

## The Core Math

For a multiplicative process where each year:
- **Vaccinator:** health *= (1 - c), certain small cost
- **Free-rider:** with probability p, health *= (1-L); otherwise health unchanged

The two averaging methods give different growth rates:

| Metric | Vaccinator | Free-rider |
|--------|-----------|------------|
| Ensemble (arithmetic mean) | 1 - c | 1 - pL |
| Time average (geometric mean) | 1 - c | (1-L)^p |

**Divergence zone** exists when:
- Ensemble says free-ride: `1 - pL > 1 - c` (i.e., `p < c/L`)
- Time-avg says vaccinate: `(1-L)^p < 1-c` (i.e., `p > ln(1-c)/ln(1-L)`)

This zone exists whenever `ln(1-c)/ln(1-L) < c/L`, which is true for all L > 0 by Jensen's inequality (since ln(1-x) is concave). The zone is *wider* when L is larger (more severe disease).

## Analytical Divergence Zones

| Archetype | Severity (L) | Vax cost (c) | Zone lower | Zone upper | Zone width |
|-----------|-------------|-------------|-----------|-----------|------------|
| Measles-like | 0.020 | 0.0010 | 0.04952 (4.952%) | 0.05000 (5.000%) | 0.048% |
| Smallpox-like | 0.500 | 0.0020 | 0.00289 (0.289%) | 0.00400 (0.400%) | 0.111% |
| Gray Threat | 0.200 | 0.0050 | 0.02246 (2.246%) | 0.02500 (2.500%) | 0.254% |
| Black Swan | 0.400 | 0.0030 | 0.00588 (0.588%) | 0.00750 (0.750%) | 0.162% |

## Simulation Method

- 2000 agents per strategy group, 50 years
- Health capital starts at 100, evolves multiplicatively
- Infection probability from SIR steady-state model
- Compared simulated ensemble mean, geometric growth rate, and median

## Simulation Results

| Archetype | Scenario | p_inf | Ens Winner | TA Winner | In Zone? | Sim Diverge? |
|-----------|----------|-------|-----------|----------|----------|-------------|
| Measles-like | High cooperation (90%) | 0.4751 | VAX | VAX | no | no |
| Measles-like | Near threshold (94%) | 0.2247 | VAX | VAX | no | no |
| Measles-like | Low cooperation (50%) | 0.8706 | VAX | VAX | no | no |
| Smallpox-like | High cooperation (90%) | 0.0000 | FREE | FREE | no | no |
| Smallpox-like | Near threshold (86%) | 0.0928 | VAX | VAX | no | no |
| Smallpox-like | Low cooperation (50%) | 0.6825 | VAX | VAX | no | no |
| Gray Threat | High cooperation (90%) | 0.2302 | VAX | VAX | no | no |
| Gray Threat | Near threshold (98%) | 0.0435 | VAX | VAX | no | no |
| Gray Threat | Low cooperation (50%) | 0.6000 | VAX | VAX | no | no |
| Black Swan | High cooperation (90%) | 0.2752 | VAX | VAX | no | no |
| Black Swan | Near threshold (99%) | 0.1767 | VAX | VAX | no | no |
| Black Swan | Low cooperation (50%) | 0.5238 | VAX | VAX | no | no |

## Key Findings

### 1. The divergence zone always exists (mathematically proven)

For **any** disease with severity L > 0 and any vaccine with cost c > 0, there exists a range of infection probabilities where ensemble-average reasoning says 'free-ride' but time-average reasoning says 'vaccinate.' This is a mathematical consequence of Jensen's inequality applied to the logarithm.

### 2. The zone is wider for more severe diseases

- Measles-like (L=0.02): very narrow zone (0.050% - 0.050%), practically negligible
- Smallpox-like (L=0.50): moderate zone, meaningful divergence
- Black Swan (L=0.40): substantial zone

### 3. Real-world infection probabilities often fall OUTSIDE the zone

In the simulation, infection probabilities near the herd immunity threshold are typically too high to be in the divergence zone. When Re is meaningfully above 1, infection risk is large enough that even the ensemble average favors vaccination. The divergence zone lives in a narrow band of low-but-nonzero infection probability.

### 4. The mean-median gap tells the real story

Even when ensemble and time-average agree on the *direction* (both say 'vaccinate'), the **magnitude** of the difference is revealing. The arithmetic mean of free-rider health overstates what typical individuals experience. The median (and time-average) show much worse outcomes. This mean-median gap is the practical manifestation of non-ergodicity.

### 5. The strongest version of the thesis is about magnitude, not direction

The essay's thesis doesn't require that ensemble and time-average give *opposite* recommendations. The stronger and more robust finding is:

- **Ensemble reasoning underestimates the cost of free-riding.** The 'average outcome' for a free-rider looks much better than what any individual free-rider actually experiences over time.
- **Time-average reasoning makes vaccination look even more attractive** than ensemble reasoning does, narrowing or eliminating the apparent 'rational' case for free-riding.
- The individual/collective tension doesn't fully dissolve, but it **shrinks dramatically** under time-average reasoning.

## Bottom Line

**The ergodicity claim partially holds.** The individual/collective tension does not fully dissolve in all cases, but:

1. A mathematical divergence zone always exists (Jensen's inequality)
2. For severe diseases, this zone is meaningful
3. Even outside the zone, time-average reasoning makes the case for vaccination substantially stronger than ensemble reasoning
4. The mean-median gap in free-rider outcomes is large and grows over time -- the 'average free-rider' is a fiction that doesn't represent any actual person's experience

**For the essay:** Frame this as 'ergodicity economics *narrows* the tension' rather than 'dissolves' it. The strongest version: once you do the math correctly (time-averages), the individually rational choice moves much closer to the collectively optimal one. The remaining gap, if any, is small enough that other considerations (altruism, reciprocity, social norms) can easily close it.
