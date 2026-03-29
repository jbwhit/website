# Epidemiological Data

This note provides sourced, quantitative epidemiological data optimized for an essay on vaccination policy. It synthesizes point estimates, ranges, and consensus figures from public health authorities and the peer-reviewed literature.

## Measles

### Basic reproduction number (R0)
- The standard public-health working range is about **12–18**.
- A systematic review of published estimates (Guerra et al., 2017) found a much wider range due to differing methods and settings, with a reported median estimate of **15.3**.
- For modeling purposes, **R0 = 15** serves as a defensible, highly transmissible central estimate.

### Case fatality rate (overall and by age)
In high-income settings, the CDC frames the burden of measles primarily as a complication profile rather than a single age-stratified CFR:
- **Pneumonia:** Occurs in about **1 to 6%** (or 1 in 20) of cases.
- **Encephalitis:** Occurs in about **1 per 1,000** cases.
- **Death:** Historically in the United States, mortality was about **1 to 3 deaths per 1,000 reported cases** (0.1–0.3%). The risk of death is highest in infants, children under 5, and adults over 20.
- Globally, mortality remains much higher in areas with lower nutrition and health-system capacity. The WHO and CDC estimated about **107,482 measles deaths worldwide in 2023**, a significant decrease from approximately 800,000 in 2000.

### Vaccine efficacy (MMR)
- **1 dose:** Approximately **93%** effective against measles.
- **2 doses:** Approximately **97%** effective against measles.

### Adverse events
#### Serious adverse events (per million doses)
The CDC and WHO report that the MMR vaccine is exceptionally safe. Serious adverse events are rare and can be quantified as follows:
- **Severe Allergic Reaction (Anaphylaxis):** Extremely rare, estimated at **1 to 10 cases per million doses** (Vaccine Safety Datalink studies often cite around 5.1 per million).
- **Postvaccinial Encephalitis:** Extremely rare, estimated at approximately **1 case per million doses**.
- **Thrombocytopenic Purpura (ITP):** A temporary low platelet count occurring in about **25 to 40 cases per million doses** (roughly 1 in 40,000). For context, natural rubella infection causes ITP at a much higher rate (roughly 1 in 3,000 cases).
- **Febrile Seizures:** Triggered by a rapid rise in fever, occurring in approximately **250 to 333 cases per million doses** (1 in 3,000 to 4,000 children). They are generally not associated with long-term health problems.
- *Takeaway for the essay:* Serious vaccine-caused events are measurable but orders of magnitude rarer than serious outcomes from natural measles infection. 

#### Mild adverse events
- **Fever:** Approximately **5% to 15%** of vaccine recipients develop a fever (103°F or higher), usually lasting 1–2 days.
- **Mild Rash:** About **2% to 5%** of recipients develop a mild, non-contagious, measles-like rash.
- **Joint Pain/Stiffness:** Occurs in up to **25%** of females past puberty who were not previously immune to rubella.

### Herd immunity threshold
- Using the simple homogeneous-mixing formula without vaccine failure, the theoretical threshold is `1 - 1/R0`. For measles (R0 = 12–18), that yields about **91.7–94.4%**.
- Adjusting for two-dose MMR efficacy (`e = 0.97`), the required coverage is `v* = (1 - 1/R0) / e`, yielding **94.5–97.3%**.
- Public-health practice treats **95% two-dose coverage** as the practical minimum target. However, because of clustering, a population can average 95% overall and still sustain outbreaks if low-coverage pockets are geographically or socially concentrated.

### Historical vaccination coverage and outbreaks
- **Pre-1963:** The United States had roughly 3–4 million measles infections per year; nearly all children were infected by age 15.
- **1963:** First measles vaccine licensed in the U.S.
- **1968:** Improved attenuated vaccine replaced earlier versions.
- **1989:** Outbreaks among vaccinated school-aged children drove the shift to a routine second dose of MMR.
- **2000:** Measles declared eliminated from the United States (no continuous endemic spread for >12 months).
- **Global:** First-dose coverage rose from about 72% in 2000 to 86% in 2019, dropping slightly to **84% in 2024**. When coverage slips, measles is usually the first major disease to reappear due to its extreme transmissibility (e.g., the large U.S. outbreak in 2019).

---

## Smallpox

### Basic reproduction number (R0)
- Modern re-analysis of historical outbreaks (e.g., Gani & Leach, 2001) suggests an R0 of about **3.5–6**.

### Case fatality rate
- **Variola major:** Roughly **30%** case fatality.
- **Variola minor:** Usually **<1%**.

### Vaccine efficacy
- The CDC notes that vaccinia vaccine efficacy was **never measured precisely in controlled trials**.
- Epidemiologic observation showed strong protection for **<5 years** after primary vaccination, with substantial but waning protection for **>10 years**. Post-exposure vaccination within a few days of exposure could prevent or attenuate the disease.

### Adverse event rates
Serious complications were much more common in primary vaccinees than in revaccinees. Based on historical data (e.g., 1968 surveys):
- **Death:** Overall, about **1 per million** primary vaccinations and **0.25 per million** revaccinations.
- **Progressive Vaccinia (Vaccinia Necrosum):** A life-threatening complication occurring at **1 to 1.5 cases per million** vaccinations. Fatality was 15–33% with treatment.
- **Postvaccinial Encephalitis:** Incidence varied by vaccine strain. The U.S. NYCBH strain had an incidence of approximately **2.9 per million**. Other strains used globally had much higher rates (up to 44.9 per million). The case fatality rate was 10–25%.
- *Takeaway for the essay:* Smallpox vaccine risk was real and non-trivial by modern standards, but the extreme danger of untreated smallpox made the risk calculation overwhelmingly favor vaccination.

### Herd immunity threshold
- With R0 = 3.5–6, the theoretical threshold is **71–83%**.
- Assuming vaccine efficacy near 95%, the required coverage is roughly **75–87%**.

### WHO eradication campaign
- **1959:** WHO adopted an eradication resolution (progress was uneven).
- **1967:** Intensified global eradication program began.
- **1975:** Last naturally occurring case of variola major (Bangladesh).
- **1977:** Last naturally occurring case of smallpox overall (Somalia).
- **1980:** WHO certified global eradication.
- **Why it worked:** No animal reservoir, no chronic asymptomatic carriage, highly visible clinical presentation, transmission occurred mostly after symptoms appeared, an effective vaccine, and the operational feasibility of surveillance-containment ("ring vaccination").

---

## General Herd Immunity Dynamics

### Core formula
- In the simplest leaky-vaccine model, the effective reproduction number is `Re(v) = R0 * (1 - e * v)`.
- The herd immunity threshold (HIT) is `v* = (1 - 1/R0) / e`.

### The benefit curve and disease burden
- **Is it truly S-shaped?** In a standard SIR model, the cumulative number of infections (total disease burden) over time follows an **S-shaped (sigmoidal) curve**.
- When mapping **vaccination coverage against disease burden** (the "benefit curve"), the relationship is profoundly non-linear.
  - Initial increases in coverage offer direct protection with linear, additive benefits.
  - As coverage approaches the herd immunity threshold, the marginal benefit increases sharply due to the compounding effect of indirect protection ("bending the curve").
  - Once coverage crosses the threshold ($R_e < 1$), the risk of sustained transmission collapses precipitously, and disease burden plateaus.

### Effective reproduction number as a function of coverage
- In the simplest mathematical model, $R_e(v)$ decreases **linearly** as vaccination coverage $v$ increases.
- However, the final epidemic size (the actual societal burden) is a **highly non-linear** function of $R_e$. A small change in $R_e$ near 1.0 translates to massive differences in total outbreak size.

### Empirical non-linearity
- The best empirical demonstration of this non-linearity is **coverage heterogeneity**. If a national population averages 95% coverage, but immunity is clustered such that certain local networks have 70% coverage, those pockets will behave as if the national threshold was never met, sustaining explosive outbreaks.

---

## Plausible Parameter Ranges for Essay Archetypes

### 1. The "Gray Threat" Disease
A hypothetical moderate, persistent threat.
- **R0:** 3–5
- **CFR:** 1–3%
- **Vaccine Efficacy:** 70–80%
- **Serious Adverse Event Rate:** ~1 in 10,000 (100 per million)
- **Consistency Check:** These parameters are internally consistent. The implied herd threshold is 57–83% (depending on specific R0 and efficacy). A vaccine with these parameters would be considered quite reactogenic by modern routine standards but entirely plausible for a novel platform deployed against a disease much more dangerous than seasonal flu.

### 2. The "Black Swan Pandemic"
A novel pathogen with high parameter uncertainty.
- **Historical Ranges:** R0 values have ranged from ~1.5 (some influenza strains) to >6 (highly transmissible SARS-CoV-2 variants or smallpox). Case fatality rates have ranged from <0.1% to ~10% (SARS-CoV-1) and ~34% (MERS).
- **The Core Issue:** In a true Black Swan scenario, the initial policy problem is **parameter uncertainty**. Planners do not know the true R0, CFR, dispersion factor, or immune escape capability early on. A model of a Black Swan should emphasize the failure of expected-value optimization under fat-tailed uncertainty rather than anchoring on a single plausible point estimate.

---

## References

- **CDC.** "Measles Vaccination." [cdc.gov/measles](https://www.cdc.gov/measles/vaccines/index.html)
- **CDC.** "MMR Vaccine Safety." [cdc.gov/vaccine-safety](https://www.cdc.gov/vaccine-safety/vaccines/mmr.html)
- **CDC.** "Progress Toward Measles Elimination - Worldwide, 2000-2023." *MMWR*.
- **Gani R, Leach S. (2001).** "Transmission potential of smallpox in contemporary populations." *Nature*, 414: 748-751.
- **Guerra FM, et al. (2017).** "The basic reproduction number (R0) of measles: a systematic review." *Lancet Infectious Diseases*, 17(12): e420-e428.
- **Hethcote HW. (2000).** "The Mathematics of Infectious Diseases." *SIAM Review*, 42(4).
- **World Health Organization.** "Immunization coverage." Fact sheets.
- **CDC.** "Vaccinia (Smallpox) Vaccine: Recommendations of the Advisory Committee on Immunization Practices (ACIP), 2001." *MMWR*, 50(RR-10).