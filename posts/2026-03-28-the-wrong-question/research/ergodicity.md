# Ergodicity Economics

This note separates three things:

- what Peters and related authors explicitly argue
- what critics explicitly object to
- what I think follows for vaccination policy by inference

That distinction matters because direct public-health applications of ergodicity economics appear to be sparse.

## Core framework

### Ensemble averages versus time averages

Ole Peters' central claim is simple:

- An **ensemble average** asks what happens across many parallel copies of a system at one time.
- A **time average** asks what happens to one system as it evolves through time.

If those coincide, the process is ergodic for the observable you care about. If they do not, replacing time with probability can give systematically misleading advice.

Peters' complaint about standard economic reasoning is that many risk problems are treated as if expected value or expected utility were automatically the right object, even when the underlying process is one of compounding growth and repeated multiplicative shocks.

### What the 2019 Nature Physics paper argues

In "The ergodicity problem in economics," Peters argues that:

- ergodicity is a restrictive property, not a default assumption
- many economic processes are growth processes far from equilibrium
- in such settings, time-average growth can be the right criterion rather than an expectation over hypothetical parallel worlds
- this reframes puzzles about leverage, risk, inequality, and bankruptcy

The paper's core move is not "probability is wrong." It is:

> Do not replace a dynamic problem with a probabilistic one unless the replacement is justified by the process.

### Simplest coin-flip / repeated gamble illustration

Use a gamble with two outcomes each round:

- heads: wealth multiplies by `1.5`
- tails: wealth multiplies by `0.6`
- each with probability `0.5`

Then:

- ensemble-average multiplier per round:
  - `(1.5 + 0.6) / 2 = 1.05`
- time-average multiplier per round:
  - `(1.5 * 0.6)^(1/2) = sqrt(0.9) approx 0.9499`

So the same gamble looks:

- profitable in expectation across parallel universes
- wealth-destroying over time for a repeated player

In log terms:

- expected log growth = `0.5 * ln(1.5) + 0.5 * ln(0.6) = 0.5 * ln(0.9) < 0`

That is the cleanest intuition pump for the essay. The issue is not "bad luck." The issue is that multiplicative downside is not repaired by arithmetic averaging.

### Growth-rate optimal strategy

Under ergodicity-style reasoning, the relevant objective in repeated multiplicative settings is often:

- maximize expected log growth

That differs from expected-value maximization because expected value tolerates arbitrarily large downside if the average payoff is positive, while log-growth optimization punishes ruin and excessive leverage much more strongly.

## Kelly criterion connection

### Why Kelly is the closest mathematical cousin

The Kelly criterion chooses the fraction of wealth to stake so as to maximize long-run expected log growth.

That is why it is the natural bridge between classic gambling theory and ergodicity economics:

- both treat wealth as a dynamic process
- both focus on compounding
- both treat ruin or overbetting as central pathologies

### Intuition for the essay

Kelly-style reasoning says:

- even a positive-expected-value bet should not be taken at full size if it creates too much multiplicative downside
- overbetting reduces long-run growth and can create near-certain ruin

The vaccination analogue is not "betting" in the literal sense. It is:

- repeated annual or seasonal exposure to infection risk
- occasional large health shocks
- a smaller, more predictable intervention cost

That structure is exactly where time-average reasoning becomes interesting.

## Application to health and policy

### Direct applications in the literature

I did **not** find a well-established published literature applying ergodicity economics directly to vaccination policy or routine public-health mandates.

The closest bodies of work are:

- insurance and self-insurance decisions
- leverage and repeated risk-taking
- portfolio choice under multiplicative uncertainty
- disaster-risk management where avoiding ruin dominates maximizing average payoff

So the vaccination application is mostly an extension of the framework, not a summary of a mature subfield.

### How to frame a vaccination decision in ergodicity terms

A useful stylized model is:

- vaccinating imposes a small predictable cost `c`
- not vaccinating preserves that cost in most years
- but sometimes imposes a large multiplicative health loss `L`
- infection probability `p` depends on herd immunity and behavior

Then:

- vaccinator growth factor per period: `1 - c`
- non-vaccinator ensemble factor: `1 - pL`
- non-vaccinator time-average factor: `(1 - L)^p`

The two criteria can diverge because:

- arithmetic averaging discounts rare large losses
- geometric growth treats those losses as permanently compounding damage

### Does time-average optimal behavior differ from ensemble-average optimal behavior?

Yes, under plausible conditions.

The divergence is most likely when:

- exposure repeats over time
- losses are multiplicative rather than purely additive
- downside is severe
- vaccine cost is small
- risk is not perfectly insured or pooled away

That means the best essay claim is **not** "ergodicity always flips the policy recommendation." The better and more defensible claim is:

- time-average reasoning systematically strengthens the case for self-protection against rare severe losses
- therefore it shrinks the apparent rational case for free-riding

That matches the direction of your local simulation results in `ergodicity-findings.md`.

### When the framework is strongest and weakest

Strongest:

- repeated exposures
- multiplicative or compounding life effects
- downside that permanently impairs future capacity
- situations where large losses are not fully socialized

Weakest:

- one-shot decisions
- additive harms with easy recovery
- settings where pooled insurance genuinely neutralizes individual downside
- cases where health states do not compound in any useful sense

So "annual exposure over a lifetime" is a stronger ergodicity case than "single isolated vaccination choice."

## Criticisms and limitations

### Main criticisms

The main critiques are:

- ergodicity economics overstates the novelty of its results
- many of its prescriptions resemble expected utility with log utility or related dynamic utility forms
- some examples rely on special wealth dynamics or effectively infinite-horizon repetition
- not every policy problem is a multiplicative growth problem

Critics in the recent debate with Peters argue that expected utility theory and ergodicity economics diverge for identifiable reasons, but that the gap is narrower than Peters sometimes suggests.

### Fair criticism for your essay

The most serious caution is:

- vaccination decisions are partly biological and institutional, not just stochastic wealth processes
- health is not literally a scalar portfolio that compounds in one clean way
- many of the benefits of vaccination are external and collective, not just private time-average gains

That means ergodicity economics should be used as a clarifying lens, not as a total theory of public health.

### Peters and co-authors' reply

Peters' reply is essentially:

- the dynamic process comes first
- utility should not be smuggled in as arbitrary psychology if the process itself already identifies the relevant growth criterion
- once you model repeated multiplicative dynamics properly, "risk preference" questions often become dynamic optimization questions

Even if one does not accept the full critique of expected utility, that is still a useful methodological warning for the essay.

## Best essay-safe synthesis

The strongest version of the ergodicity argument for vaccination is:

1. Repeated infectious exposure is a dynamic process, not just a one-shot lottery.
2. Severe infections impose losses that are at least partly multiplicative over a life course.
3. Arithmetic averages therefore understate the lived cost of free-riding.
4. Time-average reasoning moves the individually rational choice closer to the collectively optimal one.

I would **not** claim that ergodicity alone dissolves every liberty-versus-collective tension. I would claim that it changes the baseline math in a way that makes free-riding look much less rational than naive expected-value reasoning suggests.

## References

- Peters, Ole. "The ergodicity problem in economics." *Nature Physics* 15 (2019): 1216-1221. https://www.nature.com/articles/s41567-019-0732-0
- Peters, Ole, and Murray Gell-Mann. "Evaluating gambles using dynamics." *Chaos* 26 (2016).
- Peters, Ole, and Alexander Adamou. "The time interpretation of expected utility theory."
- Kelly, J. L. Jr. "A New Interpretation of Information Rate." *Bell System Technical Journal* 35 (1956): 917-926.
- Ford, Nick, and John Kay. "Critique of ergodicity economics," and reply / rejoinder discussion in *Econ Journal Watch* 21, no. 1 (2024). PDF: https://econjwatch.org/File+download/1309/EJWCompleteIssueMar2024.pdf
- Thorp, Edward O. and later Kelly-criterion literature on long-run log-growth optimization.
