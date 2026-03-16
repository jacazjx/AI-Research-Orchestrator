# Reporting Standards Reference

This document provides summaries of key reporting standards for scientific research. Use these standards when auditing research outputs for completeness and transparency.

## Clinical Trials

### CONSORT (CONsolidated Standards of Reporting Trials)

**Purpose:** Improve reporting of randomized controlled trials (RCTs)

**Key Requirements:**
- 25-item checklist for reporting RCTs
- Flow diagram showing participant progression through trial phases
- Clear description of randomization, blinding, and sample size calculation

**Essential Elements:**
1. **Title:** Identify as randomized trial
2. **Abstract:** Structured summary with trial design, methods, results, conclusions
3. **Introduction:** Scientific background and trial objectives
4. **Methods:**
   - Trial design (parallel, factorial, cluster)
   - Eligibility criteria for participants
   - Interventions for each group with sufficient detail for replication
   - Outcomes (primary and secondary)
   - Sample size calculation
   - Randomization procedure
   - Blinding mechanism
   - Statistical methods
5. **Results:**
   - Participant flow (CONSORT flow diagram)
   - Dates of recruitment and follow-up
   - Baseline data for each group
   - Numbers analyzed (intention-to-treat)
   - Outcomes and effect sizes with confidence intervals
   - Harms and adverse events
6. **Discussion:** Limitations, generalizability, interpretation
7. **Registration:** Trial registration number and name of registry
8. **Funding:** Source of funding

**Checklist Category Summary:**
- Title and Abstract (2 items)
- Introduction (2 items)
- Methods (11 items)
- Results (7 items)
- Discussion (3 items)
- Other (2 items)

### SPIRIT (Standard Protocol Items: Recommendations for Interventional Trials)

**Purpose:** Guidance for clinical trial protocols

**Key Elements:** Scientific rationale, objectives, design, methodology, statistical considerations, organization.

---

## Systematic Reviews and Meta-Analyses

### PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)

**Purpose:** Transparent reporting of systematic reviews and meta-analyses

**Key Requirements:**
- 27-item checklist
- PRISMA flow diagram showing study selection process

**Essential Elements:**
1. **Title:** Identify as systematic review, meta-analysis, or both
2. **Abstract:** Structured summary with objectives, data sources, eligibility criteria, participants, interventions, study appraisal and synthesis methods, results, limitations, conclusions
3. **Introduction:** Rationale and objectives with PICO framework
4. **Methods:**
   - Protocol and registration information
   - Eligibility criteria using PICO (Population, Intervention, Comparison, Outcomes)
   - Information sources (databases searched, dates)
   - Search strategy
   - Study selection process
   - Data collection process
   - Data items (variables and definitions)
   - Risk of bias assessment
   - Summary measures
   - Synthesis methods
   - Additional analyses (sensitivity, subgroup)
5. **Results:**
   - Study selection (PRISMA flow diagram)
   - Study characteristics
   - Risk of bias within studies
   - Results of individual studies
   - Synthesis of results
   - Risk of bias across studies
   - Additional analyses
6. **Discussion:** Summary of evidence, limitations, conclusions
7. **Funding:** Funding sources and role in review

**PRISMA Flow Diagram Stages:**
- Identification: Records identified from databases
- Screening: Records screened, records excluded
- Eligibility: Full-text assessed, full-text excluded with reasons
- Included: Studies included in synthesis

### PRISMA-P (PRISMA for Protocols)

**Purpose:** Reporting systematic review protocols

**Key Elements:** 17-item checklist for protocol registration and planning.

---

## Observational Studies

### STROBE (STrengthening the Reporting of OBservational studies in Epidemiology)

**Purpose:** Strengthen reporting of observational studies

**Study Types:** Cohort, case-control, cross-sectional

**Essential Elements (22-item checklist):**
1. **Title and Abstract:** Indicate study design in title
2. **Introduction:** Background/rationale, objectives
3. **Methods:**
   - Study design with key dates
   - Setting, participants, eligibility criteria
   - Variables (outcomes, exposures, predictors, confounders)
   - Data sources and measurement methods
   - Bias mitigation strategies
   - Study size and power calculation
   - Quantitative variables handling
   - Statistical methods (including missing data, subgroup analyses)
4. **Results:**
   - Participant flow (numbers at each stage)
   - Descriptive data (baseline characteristics)
   - Outcome data (numbers for each exposure category)
   - Main results (effect estimates, confidence intervals)
   - Other analyses (sensitivity, subgroup)
5. **Discussion:** Key results, limitations, generalizability, interpretation
6. **Other:** Funding sources

**Cohort-Specific Items:**
- Describe matching criteria for exposed/unexposed
- Describe follow-up methods

**Case-Control-Specific Items:**
- Describe selection of cases and controls
- Describe matching criteria

**Cross-Specific Items:**
- Describe sampling method
- Describe rationale for sample size

---

## Animal Research

### ARRIVE (Animal Research: Reporting of In Vivo Experiments)

**Purpose:** Improve reporting of animal experiments for reproducibility and ethical standards

**Current Version:** ARRIVE 2.0 (2020)

**Essential 10 Items (Must Report):**
1. **Study design:** Experimental groups, timeline
2. **Sample size:** How sample size was determined
3. **Inclusion/exclusion criteria:** Animals included/excluded from analysis
4. **Randomization:** How animals were allocated to groups
5. **Blinding:** Blinding during experiments and outcome assessment
6. **Outcome measures:** Primary and secondary outcomes defined
7. **Statistical methods:** Methods used for analysis
8. **Experimental animals:** Species, strain, sex, age, weight
9. **Housing and husbandry:** Housing conditions, husbandry
10. **Ethical statement:** Ethical approvals obtained

**Recommended Set (Additional Items):**
- Abstract (structured)
- Background
- Objectives
- Ethical statement (details)
- Housing and husbandry (details)
- Animal handling
- Experimental procedures
- Results (baseline data, numbers analyzed, adverse events)
- Interpretation
- Generalizability
- Protocol registration
- Data access
- Conflicts of interest
- Funding

---

## Genomics and Microarray Data

### MIAME (Minimum Information About a Microarray Experiment)

**Purpose:** Ensure microarray data is fully documented for interpretation and replication

**Six Critical Elements:**
1. **Experimental Design:**
   - Type of experiment (normal vs. diseased, time course, dose response, etc.)
   - Experimental factors and their values
   - Experimental variables (growth conditions, treatment protocols)
   - Replicate information (technical and biological replicates)
   - Quality control measures

2. **Array Design:**
   - Platform type
   - Probe sequences
   - Array annotation
   - Spot annotation

3. **Samples:**
   - Source of samples
   - Extraction methods
   - Sample preparation protocols
   - Labeling protocols
   - Hybridization procedures

4. **Hybridizations:**
   - Hybridization date
   - Hybridization protocol
   - Hybridization conditions
   - Scanner used

5. **Measurements:**
   - Raw data files
   - Normalized data
   - Data processing methods
   - Quality assessment metrics

6. **Normalization Controls:**
   - Normalization method
   - Control spots
   - Control samples

**Data Submission Repositories:**
- GEO (Gene Expression Omnibus)
- ArrayExpress
- SRA (Sequence Read Archive)

---

## Machine Learning and AI Research

### CLAIM (Checklist for Artificial Intelligence in Medical Imaging)

**Purpose:** Reporting standards for AI/ML in medical imaging

**Key Elements:**
1. **Study Design:** Prospective/retrospective, multi-center vs. single-center
2. **Data Sources:** Description of datasets, acquisition protocols
3. **Data Partitioning:** Training, validation, test set splits
4. **Model Architecture:** Description of model, hyperparameters
5. **Implementation Details:** Software frameworks, hardware, training time
6. **Evaluation Metrics:** Primary and secondary metrics with justification
7. **Statistical Analysis:** Confidence intervals, statistical tests
8. **Comparison Methods:** Baseline methods compared

### TRIPOD (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis)

**Purpose:** Prediction model development and validation

**Key Elements:**
- Source of data
- Participants (eligibility, outcome definition)
- Sample size justification
- Handling of missing data
- Model development (predictors, modeling method)
- Model performance (discrimination, calibration)
- Model validation (internal, external)

---

## General Statistical Reporting Standards

### SAMPL (Statistical Analyses and Methods in the Published Literature)

**Purpose:** Guidelines for statistical reporting

**Key Principles:**
1. **Describe the statistical methods with enough detail to enable replication**
2. **Report effect sizes with confidence intervals**
3. **Report exact p-values, not just significance thresholds**
4. **Report multiple comparison corrections when applicable**
5. **Report assumptions and verify them**
6. **Report handling of missing data**
7. **Report sample size calculations**

---

## How to Use These Standards in Audits

When auditing research outputs, map the relevant standards:

| Research Type | Primary Standard | Secondary Standards |
|---------------|------------------|---------------------|
| RCT (clinical trial) | CONSORT | SPIRIT (for protocols) |
| Systematic review | PRISMA | PRISMA-P (for protocols) |
| Cohort study | STROBE | - |
| Case-control study | STROBE | - |
| Cross-sectional study | STROBE | - |
| Animal experiment | ARRIVE | - |
| Microarray/genomics | MIAME | - |
| AI/ML medical imaging | CLAIM | TRIPOD |
| Prediction model | TRIPOD | - |

### Audit Checklist Application

For each audit, include a section referencing the applicable standard:

```markdown
## Reporting Standards Compliance

| Standard | Applicable | Compliance | Gaps |
|----------|------------|------------|------|
| CONSORT | Yes/No | X% | [List gaps] |
| PRISMA | Yes/No | X% | [List gaps] |
| STROBE | Yes/No | X% | [List gaps] |
| ARRIVE | Yes/No | X% | [List gaps] |
| MIAME | Yes/No | X% | [List gaps] |

**Critical Gaps:**
- [Gap 1]
- [Gap 2]

**Recommendations:**
- [Recommendation to address gaps]
```

---

## References

- CONSORT 2010 Statement: www.consort-statement.org
- PRISMA 2020 Statement: www.prisma-statement.org
- STROBE Statement: www.strobe-statement.org
- ARRIVE Guidelines 2.0: arriveguidelines.org
- MIAME Guidelines: www.fged.org/projects/miame/
- CLAIM Checklist: www CLAIM-checklist.org
- TRIPOD Statement: www.tripod-statement.org