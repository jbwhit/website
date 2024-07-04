# Difference-in-Differences (DiD) Checklist

**Purpose:** To systematically guide researchers through the process of conducting a Difference-in-Differences analysis, ensuring key steps and considerations are addressed.

**Background:** This checklist is inspired by a [tweet from @pedrohcgs](https://x.com/pedrohcgs/status/1798384924409360506), which outlined essential steps in DiD analysis. It has been expanded to create a more comprehensive, actionable checklist for researchers and analysts.

## Checklist

1. **Prepare Data and Visualize Treatment**
   - [ ] Plot treatment rollout (use panelView R package)
   - [ ] Record number of units treated per cohort
   - [ ] Plot average outcomes over time by cohort

2. **Select Comparison Groups**
   - [ ] Assess Parallel Trends assumption
   - [ ] Consider who decides treatment and what they know
   - [ ] Determine allowable types of selection

3. **Conduct Initial Analysis**
   - [ ] Perform event study (no covariates) to assess Parallel Trends

4. **Refine Analysis with Covariates**
   - [ ] If needed, add covariates affecting untreated outcome growth
   - [ ] Check for overlap in covariates
   - [ ] Use regression adjustment DiD if extrapolating
   - [ ] Rerun event study with covariates to reassess Parallel Trends

5. **Sensitivity Analysis**
   - [ ] Perform sensitivity analysis for Parallel Trends violations
   - [ ] Consider using honestDiD R package

6. **Alternative Methods**
   - [ ] Explore other methods if Parallel Trends remains implausible

**Action:** Use this checklist to ensure a thorough and methodologically sound Difference-in-Differences analysis. Document your decisions and findings at each step to support your research conclusions.