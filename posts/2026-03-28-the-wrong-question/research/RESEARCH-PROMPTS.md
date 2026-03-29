# Research Prompts for "The Wrong Question" Essay

Submit these to Gemini Deep Research or Codex. Each prompt specifies where to save output.

---

## Prompt 1: Epidemiological Data

**Save output to:** `posts/2026-03-28-the-wrong-question/research/epidemiology.md`

**Prompt:**

I'm writing an essay about vaccination policy that uses real epidemiological data to ground its argument. I need sourced, quantitative data on the following. Please provide specific numbers with citations (journal papers, WHO/CDC data, or textbook references).

**Measles:**
- Basic reproduction number (R0) — point estimate and range from literature
- Case fatality rate (overall and by age group in developed countries)
- Vaccine efficacy (1-dose and 2-dose MMR)
- Serious adverse event rate for MMR vaccine (per million doses)
- Mild adverse event rate (fever, rash, etc.)
- Herd immunity threshold (theoretical from R0 and observed)
- Historical vaccination coverage data (US/global) — key milestones and outbreaks when coverage dropped

**Smallpox:**
- Basic reproduction number (R0)
- Case fatality rate (variola major vs. variola minor)
- Vaccine efficacy (vaccinia-based vaccine)
- Adverse event rates (serious: encephalitis, progressive vaccinia, etc.)
- Herd immunity threshold
- Timeline of WHO eradication campaign — key dates, strategies, final cases
- What made eradication possible (no animal reservoir, visible symptoms, ring vaccination)

**General herd immunity dynamics:**
- The relationship between R0, vaccine efficacy (e), and herd immunity threshold: threshold = (1 - 1/R0) / e
- How does the "benefit curve" (disease burden as a function of coverage) actually behave? Is it truly S-shaped? What does the SIR model predict?
- What does "effective reproduction number" (Re) look like as a function of vaccination coverage?
- Any empirical data on non-linear dynamics of disease transmission as vaccination rates change

**For my hypothetical archetypes, I need plausible parameter ranges:**
- A "Gray Threat" disease: moderate R0 (3-5), moderate case fatality (1-3%), vaccine efficacy ~70-80%, adverse event rate ~1 in 10,000 serious — are these internally consistent?
- A "Black Swan Pandemic" disease: novel pathogen, what ranges of R0 and CFR have been observed in historical pandemics? What does high parameter uncertainty look like in practice?

Format the output as markdown with clear sections and a references list at the end.

---

## Prompt 2: Philosophy and Political Theory

**Save output to:** `posts/2026-03-28-the-wrong-question/research/philosophy.md`

**Prompt:**

I'm writing an essay that examines vaccination policy through multiple philosophical frameworks. I need a research summary of the following, with key quotes and citations where possible.

**Rawls and the Veil of Ignorance applied to public health:**
- Has Rawls himself written about public health obligations? If not, what have Rawlsian scholars argued about vaccination?
- How does the "maximin" principle (maximize the minimum outcome) apply to vaccination policy? What policy would a Rawlsian choose behind the veil?
- The veil hides multiple distinct unknowns: immune status, contact network, family circumstances, population coverage level. Has anyone analyzed how different uncertainty sets lead to different policy conclusions?
- Key papers or books on Rawlsian approaches to public health

**Mill's Harm Principle:**
- How does Mill's harm principle ("your liberty ends where harm to others begins") apply to infectious disease?
- Where is the line between self-regarding and other-regarding actions for vaccination? Is choosing not to vaccinate a self-regarding act (my body) or other-regarding (I can infect you)?
- Has this been debated in the philosophical literature? Key positions?

**Communitarian vs. Libertarian arguments:**
- The libertarian case against vaccine mandates — strongest versions (not straw men)
- The communitarian case for collective health obligations — key thinkers
- Where does the mainstream philosophical consensus land, if there is one?

**Legal/historical precedent:**
- Jacobson v. Massachusetts (1905) — what was the argument, what did the court decide, and how has it been interpreted since?
- How do other liberal democracies handle the legal/philosophical basis for mandates?

Format as markdown with sections, key quotes, and a references list.

---

## Prompt 3: Ergodicity Economics

**Save output to:** `posts/2026-03-28-the-wrong-question/research/ergodicity.md`

**Prompt:**

I'm writing an essay that uses ergodicity economics (Ole Peters' framework) to reframe the individual-vs-collective debate in vaccination policy. I need a thorough research summary.

**Core framework:**
- Ole Peters' central argument: what is the difference between ensemble averages and time averages? What does it mean for a system to be non-ergodic?
- The key paper: "The ergodicity problem in economics" (Nature Physics, 2019) — summarize the main argument and examples
- The simplest illustration: the coin-flip gamble where the ensemble average is positive but the time average leads to ruin. Walk through the math.
- What is the growth-rate optimal strategy and how does it differ from expected-value maximization?

**Kelly criterion connection:**
- How does the Kelly criterion relate to ergodicity economics?
- What does "growth-rate optimal" betting mean, and how is it analogous to repeated health decisions?

**Application to health/policy:**
- Has anyone applied ergodicity economics to public health decisions specifically? If so, what did they find?
- If not, what's the closest application? (Insurance, financial decisions under repeated risk, etc.)
- How would you frame a vaccination decision in ergodicity terms? Is repeated annual health affected by vaccination a non-ergodic process? Why or why not?
- Key question: if you model an individual's health trajectory over a lifetime of annual disease exposure, does the time-average optimal vaccination decision differ from the ensemble-average optimal decision? Under what conditions?

**Criticisms and limitations:**
- What are the main criticisms of ergodicity economics? (Overreach, mischaracterization of expected utility theory, etc.)
- Where does the framework clearly apply vs. where is it a stretch?
- Doctor and Peters' response to critics

Format as markdown with sections, mathematical notation where helpful, and a references list.

---

## Prompt 4: Taleb, Fat Tails, and the Precautionary Principle

**Save output to:** `posts/2026-03-28-the-wrong-question/research/fat-tails.md`

**Prompt:**

I'm writing an essay about vaccination policy that uses Nassim Taleb's ideas about fat tails and the precautionary principle. I need a research summary.

**Fat tails and risk domains:**
- How does Taleb distinguish between thin-tailed (Mediocristan) and fat-tailed (Extremistan) risk domains?
- Where do pandemics sit? Is pandemic severity fat-tailed? What about pandemic frequency?
- What does it mean operationally that a risk is fat-tailed? Why does standard cost-benefit analysis (expected value) fail for fat-tailed risks?
- The concept of "ruin" — absorbing barriers and why avoiding ruin dominates optimization

**The Precautionary Principle:**
- Taleb's formal version of the precautionary principle (with Yaneer Bar-Yam, Rupert Read, et al.) — what does the paper argue?
- When does the precautionary principle apply? (Systemic, multiplicative, spreading risks with undefined upper bounds)
- When does it NOT apply? (Local, additive, bounded risks)
- How does this map to pandemic risk vs. seasonal flu risk?

**Correlated tail risk:**
- Why does correlated risk change the individual-vs-collective calculation?
- If everyone's worst-case scenario happens together (pandemic), individual risk assessment is meaningless — explain this argument
- "Skin in the game" as applied to collective health decisions — what does Taleb argue?

**Policy implications:**
- Under fat-tailed pandemic risk, what does Taleb's framework suggest about vaccination infrastructure as a policy (not just individual decisions)?
- How does the precautionary principle interact with vaccine adverse events (which are thin-tailed)?
- The asymmetry: disease risk is potentially fat-tailed, vaccine risk is thin-tailed — what does this imply?

**Key sources:**
- "The Precautionary Principle" paper (with methodology for distinguishing PP-applicable risks)
- Relevant sections of Antifragile, Skin in the Game, The Black Swan
- Statistical Consequences of Fat Tails (technical)

Format as markdown with sections and a references list.

---

## Prompt 5: Institutional Design and Mandate Mechanisms

**Save output to:** `posts/2026-03-28-the-wrong-question/research/institutional-design.md`

**Prompt:**

I'm writing an essay about vaccination policy that proposes a "policy ladder" (recommend → subsidize → school-entry requirement → outbreak-triggered mandate → universal mandate). I need research on how these mechanisms actually work in practice.

**The policy ladder in practice:**
- For each level, give real-world examples of countries/jurisdictions that operate at that level for various vaccines:
  1. Recommend (public information campaigns only)
  2. Subsidize (free vaccines, remove cost barriers)
  3. School/workplace entry requirements
  4. Outbreak-triggered mandates (temporary, activated by conditions)
  5. Universal mandates
- Which vaccines tend to sit at which levels? (e.g., flu = recommend/subsidize, measles = school-entry in most US states)

**Vaccine injury compensation:**
- US Vaccine Injury Compensation Program (VICP) — how does it work, what does it cover, how is it funded?
- UK Vaccine Damage Payment Scheme
- Why do these programs exist? What problem do they solve in the mandate framework?
- How do compensation programs affect public willingness to accept mandates?

**Exemption frameworks:**
- Medical exemptions: universally accepted, how are they granted?
- Religious exemptions: which jurisdictions allow them, controversies
- Philosophical/personal belief exemptions: which jurisdictions, impact on coverage rates
- Evidence on how exemption availability affects vaccination rates

**Legitimacy and trust:**
- What makes a vaccination mandate politically legitimate in a liberal democracy?
- The role of transparency, compensation, and exemptions in maintaining legitimacy
- Historical examples where mandates backfired (generated resistance) vs. succeeded
- The smallpox eradication campaign as a case study in mandate design

**Key insight I'm looking for:** The essay argues that the individual-vs-collective framing is a false dichotomy. From an institutional design perspective, how do well-designed mandate systems address individual concerns (compensation, exemptions, transparency) while achieving collective goals? Is this a practical example of the dichotomy dissolving?

Format as markdown with sections and a references list.
