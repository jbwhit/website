# Epidemiological Data

This note is optimized for essay use rather than for a formal systematic review. Where the literature gives clean numbers, I give them. Where the literature is context-sensitive or the public-health sources do not publish a single canonical number, I say so explicitly.

## Measles

### Basic reproduction number (R0)

- The standard public-health working range is about `12-18`.
- A systematic review of published estimates found a much wider range because methods and settings differed substantially; the median estimate reported in that review was about `15.3`.
- For modeling in the essay, `R0 = 15` is a defensible central estimate.

### Case fatality rate (overall and by age)

- In high-income settings, the cleanest CDC-style summary is not a single age-stratified CFR table but a complication profile:
  - pneumonia in about `1-6%` of cases
  - encephalitis in about `1 per 1,000-2,000` cases
  - death risk highest in infants, children age `<=5`, and adults age `>=20`
- Historically in the United States, a common rule-of-thumb is about `1-3 deaths per 1,000 reported cases` in severe outbreaks, though modern supportive care and case ascertainment make direct comparisons messy.
- Global mortality remains much higher where nutrition, health-system capacity, and baseline immunity are worse. WHO/CDC estimated about `800,062` measles deaths in 2000 and about `107,482` in 2023 worldwide.

### Vaccine efficacy

- `1 dose`: about `93%` effective against measles.
- `2 doses`: about `97%` effective against measles.

### Adverse events

#### Serious adverse events

- CDC's public safety page does **not** give one single aggregate "serious adverse event rate per million doses" for MMR.
- The cleanest quantified serious event on the CDC page is febrile seizure: about `1 in 3,000-4,000` children, or roughly `250-333 per million` doses, typically `6-14` days after vaccination.
- CDC's Pink Book says evidence supports causal links for anaphylaxis, febrile seizures, thrombocytopenic purpura, transient arthralgia, and measles inclusion body encephalitis in persons with severe immunodeficiency, but does not collapse them into one published total rate.
- For the essay, the safest wording is: **serious vaccine-caused events are orders of magnitude rarer than serious measles outcomes; the best cleanly sourced quantified serious event from CDC material is febrile seizure at roughly a few hundred per million doses.**

#### Mild adverse events

- CDC lists pain at the injection site, fever, mild rash, and cheek/neck gland swelling as the most common adverse events.
- A recent FDA label trial for `M-M-R II` given with `VARIVAX` found:
  - measles-like rash in about `2.7-2.9%`
  - fever `>=38.0 C` in about `66.5-66.8%`
- I would treat the fever figure as an upper-bound solicited trial number rather than as the best population-level "routine MMR" estimate. The rash figure is more portable.

### Herd immunity threshold

- In the simple homogeneous-mixing formula without vaccine failure, the threshold is:
  - `1 - 1/R0`
- For measles with `R0 = 12-18`, that yields about `91.7-94.4%`.
- Adjusting for two-dose MMR efficacy (`e = 0.97`), required coverage is:
  - `v* = (1 - 1/R0) / e`
  - which gives about `94.5-97.3%`
- This is why public-health practice often treats `95%` two-dose coverage as the practical minimum target.
- Observed reality is harsher than the simple formula because clustering matters: a population can average `95%` and still sustain outbreaks if low-coverage pockets are geographically or socially concentrated.

### Historical vaccination coverage and outbreaks

- Before vaccine licensure, the United States had roughly `3-4 million` measles infections per year; nearly all children were infected by age 15.
- `1963`: first measles vaccine licensed in the United States.
- `1968`: improved attenuated vaccine replaced earlier versions.
- `1989`: outbreaks among vaccinated school-aged children drove the shift to a routine second dose of MMR.
- `2000`: measles declared eliminated from the United States, meaning no continuous endemic spread for `>12 months`.
- Worldwide:
  - MCV1 coverage rose from about `72%` in 2000 to `83%` in 2023, and MCV2 from about `18%` to `74%` over the same span.
  - WHO's more recent immunization fact sheet reports global first-dose measles coverage at `84%` in 2024, still below the `86%` seen in 2019.
- When coverage slips, measles is usually the first major disease to reappear because of its extreme transmissibility. The large U.S. outbreak in 2019 and post-pandemic resurgences in multiple countries fit that pattern.

## Smallpox

### Basic reproduction number (R0)

- Modern re-analysis of historical outbreaks suggests `R0` was usually about `3.5-6`.
- Older biodefense models sometimes assumed much higher values, but the tighter `3.5-6` range is the more defensible baseline.

### Case fatality rate

- Variola major: roughly `30%` case fatality.
- Variola minor: usually `<1%`.
- CDC's smallpox review summarizes overall historical mortality as about `30%`.

### Vaccine efficacy

- CDC states that vaccinia vaccine efficacy was **never measured precisely in controlled trials**.
- Epidemiologic studies nevertheless showed:
  - strong protection for `<5 years` after primary vaccination
  - substantial but waning protection for `>10 years`
- Post-exposure vaccination within the first few days after exposure could prevent disease or attenuate severity.

### Adverse event rates

- Serious complications are much more common in primary vaccinees than in revaccinees.
- CDC's 2001 vaccinia review reports:
  - death about `1 per million` primary vaccinations
  - death about `0.25 per million` revaccinations
- That same review notes that severe complications such as progressive vaccinia and postvaccinial encephalitis were reported at `0 per 10,000` in one 1991-1996 adult primary-vaccinee series, but historical rates were higher in broader populations, especially infants and people with skin disease or immune compromise.
- The essay-safe takeaway is: **smallpox vaccine risk was real and non-trivial by modern standards, but still much smaller than untreated smallpox risk.**

### Herd immunity threshold

- With `R0 = 3.5-6`, the theoretical threshold is about `71-83%`.
- If one assumes vaccine efficacy near `95%`, required coverage is roughly `75-87%`.

### WHO eradication campaign timeline and why it worked

- `1959`: WHO adopted an eradication resolution, but progress was uneven.
- `1967`: intensified global eradication program began.
- `1975`: last naturally occurring case of variola major.
- `1977`: last naturally occurring case of smallpox overall, in Somalia.
- `1980`: WHO certified global eradication.

Key reasons eradication was possible:

- no animal reservoir
- no chronic asymptomatic carriage
- highly visible clinical presentation
- transmission mostly after symptoms appeared
- an effective vaccine
- surveillance-containment / ring vaccination was operationally feasible

## General herd immunity dynamics

### Core formula

- In the simplest leaky-vaccine model:
  - `Re(v) = R0 * (1 - e * v)`
  - herd threshold `v* = (1 - 1/R0) / e`
- This is the right first-pass formula for the essay.

### What does the benefit curve look like?

- In a simple SIR model, disease burden as a function of coverage is **non-linear** and drops sharply near the point where `Re` crosses `1`.
- I would not describe it as a perfect logistic "S-curve" unless you are speaking loosely.
- A better phrasing is:
  - **above the epidemic threshold, burden declines gradually**
  - **near `Re = 1`, burden falls steeply**
  - **below `Re = 1`, sustained transmission collapses**
- Mathematically, the final epidemic size in the homogeneous SIR model is determined implicitly by:
  - `z = 1 - exp(-Re * z)`
- That produces the sharp threshold behavior your local `explore_herd_immunity.py` script is already visualizing.

### Effective reproduction number as a function of coverage

- In the simplest model, `Re(v)` is linear in coverage.
- Disease burden is not linear in coverage because epidemic size depends non-linearly on whether `Re` is above or below `1`.
- This is the clean mathematical reason the social return to vaccination accelerates near the threshold.

### Empirical non-linearity

- Measles is the best empirical example because small coverage losses can produce very large outbreak differences once local immunity gaps open.
- The key empirical lesson is not merely "coverage matters"; it is that **coverage heterogeneity** matters. National averages can look acceptable while local clusters remain explosively vulnerable.

## Plausible parameter ranges for the essay's archetypes

### "Gray Threat"

Proposed parameters:

- `R0 = 3-5`
- `CFR = 1-3%`
- vaccine efficacy `70-80%`
- serious vaccine adverse event rate `~1 in 10,000`

These are internally consistent.

- The implied herd threshold is about `57-83%` depending on the exact `R0` and efficacy.
- This would describe a disease that is substantially more dangerous than seasonal flu, materially transmissible, but still far from measles.
- A vaccine with `70-80%` efficacy and a serious adverse event rate of `1 in 10,000` would be reactogenic by modern routine-vaccine standards but still quite plausible in an emergency or novel-platform context.

### "Black Swan Pandemic"

The right historical lesson is not one magic point estimate but a wide prior.

- Historical pandemic `R0` values have ranged from roughly `1-2` for some influenza waves to `>6` for highly transmissible SARS-CoV-2 variants.
- Historical fatality measures have ranged from well below `1%` for mild pandemics to around `10%` for SARS and roughly `34%` for MERS, though those latter examples were not global pandemics.
- Early uncertainty is often the real policy problem:
  - under-ascertainment of cases
  - changing denominator for fatality estimates
  - uncertain dispersion / superspreading
  - uncertain immune escape
  - uncertain age gradient

For the essay, the cleanest "black swan" move is to model **parameter uncertainty itself** rather than pretending the planner knows the true `R0` or fatality rate early.

## References

- CDC. "Measles Vaccination." https://www.cdc.gov/measles/vaccines/index.html
- CDC. "MMR Vaccine Safety." https://www.cdc.gov/vaccine-safety/vaccines/mmr.html
- CDC. "Measles (Rubeola)." Yellow Book. https://www.cdc.gov/yellow-book/hcp/travel-associated-infections-diseases/measles-rubeola.html
- CDC. "History of Measles." https://www.cdc.gov/measles/about/history.html
- CDC. "Progress Toward Measles Elimination - Worldwide, 2000-2023." MMWR. https://www.cdc.gov/mmwr/volumes/73/wr/mm7345a4.htm
- FDA. "Package Insert - Measles, Mumps, and Rubella Virus Vaccine Live." https://www.fda.gov/media/75191/download
- Guerra FM, et al. "The basic reproduction number (R0) of measles: a systematic review." Lancet Infectious Diseases / related literature on measles transmission estimates.
- Hethcote HW. "The Mathematics of Infectious Diseases." SIAM Review 42, no. 4 (2000).
- World Health Organization. "Immunization coverage." https://www.who.int/news-room/fact-sheets/detail/immunization-coverage
- Gani R, Leach S. "Transmission potential of smallpox in contemporary populations." Nature 414 (2001). https://pubmed.ncbi.nlm.nih.gov/11742399/
- CDC. "Vaccinia (Smallpox) Vaccine: Recommendations of the Advisory Committee on Immunization Practices (ACIP), 2001." https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5010a1.htm
