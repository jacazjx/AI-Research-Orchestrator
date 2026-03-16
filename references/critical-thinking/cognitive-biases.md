# Cognitive Biases in Research

A comprehensive catalog of cognitive biases relevant to AI/ML research, with identification strategies, mitigation techniques, and practical examples.

## Overview

Cognitive biases systematically distort research judgment, leading to flawed conclusions and wasted resources. Understanding these biases is essential for conducting rigorous AI/ML research.

```
┌─────────────────────────────────────────────────────────────────┐
│              COGNITIVE BIAS IMPACT ON RESEARCH                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  RESEARCH PHASE          SUSCEPTIBLE BIAS                       │
│  ─────────────           ─────────────────                      │
│  Question Formulation   → Confirmation Bias, Availability      │
│  Literature Review      → Confirmation Bias, Selection Bias    │
│  Experimental Design    → Bias Blind Spot, Optimism Bias       │
│  Data Collection         → Sampling Bias, Observer Bias         │
│  Analysis               → P-hacking, HARKing, Publication Bias  │
│  Interpretation         → Confirmation Bias, Sunk Cost Fallacy │
│  Publication            → Publication Bias, Outcome Reporting  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Confirmation Bias

### Definition

The tendency to search for, interpret, favor, and recall information in a way that confirms or supports one's prior beliefs or values.

### Manifestation in AI/ML Research

| Stage | Manifestation | Example |
|-------|---------------|---------|
| Hypothesis Formation | Focusing only on supportive evidence | Only reading papers that support your approach |
| Data Selection | Choosing data that confirms hypotheses | Selecting "clean" examples for demos |
| Metric Selection | Choosing metrics that favor your method | Switching metrics until your method wins |
| Interpretation | Interpreting ambiguous results favorably | Attributing failures to implementation bugs |
| Literature Review | Ignoring contradictory evidence | Not citing papers that challenge assumptions |

### Identification Checklist

```markdown
## Confirmation Bias Self-Assessment

### In Research Design
- [ ] Have I considered alternative hypotheses equally?
- [ ] Am I testing my method against the strongest baselines?
- [ ] Would I accept negative results as meaningful?
- [ ] Have I sought out contradictory evidence?
- [ ] Am I designing fair comparisons?

### In Analysis
- [ ] Did I pre-specify all analyses?
- [ ] Am I including all experimental conditions?
- [ ] Have I avoided post-hoc rationalization?
- [ ] Am I reporting failed approaches?
- [ ] Would my conclusions hold with different metrics?

### In Reporting
- [ ] Am I presenting balanced findings?
- [ ] Am I citing contradictory work?
- [ ] Am I acknowledging limitations?
- [ ] Am I being transparent about negative results?
```

### Mitigation Strategies

```python
# confirmation_bias_mitigation.py

class ConfirmationBiasMitigation:
    """
    Strategies to mitigate confirmation bias in research
    """

    @staticmethod
    def adversarial_testing(results, hypothesis):
        """
        Actively try to disprove your hypothesis

        Instead of: "How can I show my method works?"
        Ask: "What would prove my method doesn't work?"
        """
        adversarial_tests = {
            'stress_tests': 'Test on worst-case scenarios',
            'ablation_studies': 'Remove components to see if they matter',
            'negative_examples': 'Find cases where method fails',
            'alternative_metrics': 'Use metrics that might not favor you',
            'strong_baselines': 'Compare to competitive alternatives'
        }
        return adversarial_tests

    @staticmethod
    def devil_advocate_analysis():
        """
        Assign a team member to argue against your conclusions
        """
        questions = [
            "What's the strongest argument against your hypothesis?",
            "What evidence would convince you that you're wrong?",
            "What would a skeptic say about your methodology?",
            "Are there alternative explanations for your results?",
            "What assumptions are you making that could be wrong?"
        ]
        return questions

    @staticmethod
    def blind_analysis():
        """
        Conduct analysis without knowing which condition is which
        """
        protocol = {
            'data_blinding': 'Rename conditions (A, B, C) before analysis',
            'metric_blinding': 'Have someone else compute metrics',
            'interpretation_blinding': 'Analyze results blind to hypothesis'
        }
        return protocol
```

---

## 2. Publication Bias

### Definition

The tendency for journals, reviewers, and researchers to preferentially publish positive or novel results, leading to a distorted literature.

### Forms in AI/ML Research

```
┌─────────────────────────────────────────────────────────────────┐
│              PUBLICATION BIAS VARIANTS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FILE DRAWER PROBLEM                                            │
│  ├── Null/negative results unpublished                          │
│  ├── Literature becomes biased toward positive findings         │
│  └── Others waste time on approaches known to fail              │
│                                                                 │
│  OUTCOME REPORTING BIAS                                         │
│  ├── Selective reporting of successful outcomes                 │
│  ├── Hiding failed experiments                                  │
│  └── Cherry-picking favorable metrics                           │
│                                                                 │
│  TIME-LAG BIAS                                                  │
│  ├── Positive results published faster                          │
│  ├── Negative results delayed or never published                │
│  └── Literature temporarily skewed                              │
│                                                                 │
│  CITATION BIAS                                                  │
│  ├── Positive results cited more                                │
│  ├── Negative results ignored                                   │
│  └── Apparent consensus may be illusory                          │
│                                                                 │
│  NOVELTY BIAS                                                   │
│  ├── Incremental improvements harder to publish                │
│  ├── Negative results of novel methods unpublished              │
│  └── Replication studies undervalued                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Impact on AI/ML Literature

```markdown
## Publication Bias Effects in AI/ML

### Overstated Performance
- Reported benchmark performance often doesn't replicate
- "Winning" methods may be overfitting to benchmarks
- Selection bias in which runs are reported

### Wasted Research Effort
- Multiple groups attempt same failed approaches
- Negative results not shared
- Redundant failures across the field

### Distorted Progress Perception
- Apparent progress may be illusory
- "State-of-the-art" claims may not hold
- Community follows unpromising directions

### Examples in AI/ML

1. **Benchmark Overfitting**
   - Methods optimized for specific test sets
   - Performance doesn't transfer to real applications
   - Literature shows continuous improvement, reality may not

2. **Hyperparameter Selection**
   - Best hyperparameters selected based on test performance
   - Implicit overfitting to benchmarks
   - True generalization unclear

3. **Architecture Search**
   - Neural architecture search papers report best found
   - Many architectures tried but not reported
   - True cost of search underestimated
```

### Mitigation Strategies

```markdown
## Combating Publication Bias

### For Individual Researchers
- [ ] Preregister studies and commit to reporting all results
- [ ] Publish null/negative results (workshops, arXiv)
- [ ] Report all experimental conditions
- [ ] Include failed approaches in papers
- [ ] Cite negative result papers

### For Research Groups
- [ ] Create internal repository of failed experiments
- [ ] Share negative results at conferences
- [ ] Reward transparent reporting
- [ ] Conduct replications
- [ ] Publish replication studies

### For Venues
- [ ] Accept registered reports
- [ ] Create tracks for negative results
- [ ] Value replications
- [ ] Require full experimental disclosure
- [ ] Incentivize transparent reporting

### For the Field
- [ ] Support journals for negative results
- [ ] Develop norms for reporting failures
- [ ] Create shared databases of failed approaches
- [ ] Include negative results in meta-analyses
```

---

## 3. HARKing (Hypothesizing After Results Known)

### Definition

Presenting a post-hoc hypothesis as if it were a priori—claiming to have predicted a finding that was actually discovered after the data were analyzed.

### HARKing in AI/ML Research

```
┌─────────────────────────────────────────────────────────────────┐
│                    HARKING PATTERNS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  THE RETROACTIVE HYPOTHESIS                                     │
│  ├── Try multiple approaches                                    │
│  ├── Report only the successful one                            │
│  └── Write hypothesis as if it were planned                     │
│                                                                 │
│  THE TUNED THEORY                                               │
│  ├── Tune hyperparameters extensively                           │
│  ├── Observe what works                                         │
│  └── Develop theory to explain after the fact                   │
│                                                                 │
│  THE SELECTIVE BASELINE                                         │
│  ├── Compare against many baselines                             │
│  ├── Report only favorable comparisons                          │
│  └── Justify baseline selection post-hoc                        │
│                                                                 │
│  THE EVOLVING CLAIM                                             │
│  ├── Start with one research question                           │
│  ├── Find unexpected results                                    │
│  └── Shift narrative to match findings                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### HARKing Detection

```markdown
## Is This HARKing?

### Red Flags in Papers
□ Hypothesis perfectly matches results
□ No mention of alternative approaches tried
□ No negative or null results reported
□ Theory introduced only after results
□ No preregistration for confirmatory study
□ Hyperparameters seem "magically" optimal
□ Baselines seem carefully selected

### Self-Assessment Questions
- Did I know this result before running the experiment?
- Would I have made this prediction a priori?
- Have I tried other approaches that failed?
- Am I adjusting my theory to fit my results?
- If the result was different, would I still have a theory?
```

### HARKing vs. Legitimate Exploration

```
┌─────────────────────────────────────────────────────────────────┐
│          HARKING vs. EXPLORATION vs. CONFIRMATION               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EXPLORATORY ANALYSIS (Legitimate)                              │
│  ├── Explicitly labeled as exploratory                          │
│  ├── Used to generate hypotheses                                │
│  ├── Findings treated as preliminary                            │
│  ├── Requires confirmatory follow-up                            │
│  └── Multiple comparisons corrected                             │
│                                                                 │
│  CONFIRMATORY ANALYSIS (Legitimate)                             │
│  ├── Hypothesis stated before data collection/analysis         │
│  ├── Analysis plan prespecified                                 │
│  ├── Results interpreted relative to hypothesis                 │
│  ├── No selective reporting                                    │
│  └── Preregistered                                              │
│                                                                 │
│  HARKING (Problematic)                                         │
│  ├── Post-hoc hypothesis presented as a priori                 │
│  ├── Exploratory findings presented as confirmatory             │
│  ├── No distinction between generation and testing              │
│  ├── Selective reporting of successful predictions              │
│  └── Inflated type I error rate                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Mitigation Strategies

```python
# harking_mitigation.py

class HARKingPrevention:
    """
    Framework to prevent HARKing in research
    """

    def __init__(self):
        self.prior_hypotheses = []
        self.exploratory_findings = []
        self.confirmatory_results = []

    def register_hypothesis(self, hypothesis, rationale, predictions):
        """
        Register hypothesis BEFORE data collection/analysis
        """
        entry = {
            'id': len(self.prior_hypotheses),
            'hypothesis': hypothesis,
            'rationale': rationale,
            'predictions': predictions,
            'timestamp': datetime.now().isoformat(),
            'type': 'preregistered'
        }
        self.prior_hypotheses.append(entry)
        return entry['id']

    def log_exploratory(self, finding, context):
        """
        Log exploratory findings with clear labeling
        """
        entry = {
            'finding': finding,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'type': 'exploratory'
        }
        self.exploratory_findings.append(entry)

    def create_analysis_plan(self):
        """
        Create a prespecified analysis plan
        """
        plan = {
            'primary_hypotheses': self.prior_hypotheses,
            'statistical_tests': [],
            'success_criteria': [],
            'secondary_analyses': [],
            'exploratory_analyses': []
        }
        return plan

    def generate_report(self):
        """
        Generate transparent report
        """
        report = """
# Research Transparency Report

## Preregistered Hypotheses
{hypotheses}

## Confirmatory Results
{confirmatory}

## Exploratory Findings
Note: These findings are exploratory and require confirmatory studies.
{exploratory}

## Deviations from Preregistration
{deviations}
"""
        return report
```

---

## 4. P-hacking and Multiple Comparisons

### Definition

The practice of analyzing data in multiple ways to find statistically significant results, often by selectively reporting outcomes, adjusting analyses, or running multiple comparisons without correction.

### P-hacking Techniques in AI/ML

```markdown
## Common P-hacking Practices in AI/ML

### Multiple Metric Hacking
- Try many metrics, report only significant ones
- Switch between accuracy, F1, AUC, etc.
- Create custom metrics that favor your method

### Selective Reporting
- Run many experiments, report only successes
- Try many hyperparameter combinations
- Select favorable random seeds

### Subgroup Analysis
- Find subgroups where method works well
- Report subgroup results without correction
- Define subgroups post-hoc

### Data Analysis Flexibility
- Try different preprocessing options
- Experiment with data splits
- Exclude "outliers" selectively

### Baseline Manipulation
- Compare to weak baselines
- Use non-optimal hyperparameters for baselines
- Report selected baseline comparisons
```

### Multiple Comparisons Problem

```
┌─────────────────────────────────────────────────────────────────┐
│               MULTIPLE COMPARISONS PROBLEM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WITH 1 COMPARISON:                                            │
│  Probability of false positive (α = 0.05) = 5%                  │
│                                                                 │
│  WITH 10 COMPARISONS:                                          │
│  Probability of at least one false positive = 40%               │
│  Calculation: 1 - (0.95)^10 = 0.401                            │
│                                                                 │
│  WITH 20 COMPARISONS:                                          │
│  Probability of at least one false positive = 64%               │
│  Calculation: 1 - (0.95)^20 = 0.642                            │
│                                                                 │
│  IN AI/ML CONTEXT:                                             │
│  - Multiple architectures tested                                │
│  - Multiple hyperparameter settings                             │
│  - Multiple datasets                                            │
│  - Multiple metrics                                             │
│  → Inflated false positive rate                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Correction Methods

```python
# multiple_comparisons.py

import numpy as np
from scipy import stats

class MultipleComparisonsCorrection:
    """
    Methods for correcting multiple comparisons
    """

    @staticmethod
    def bonferroni(p_values, alpha=0.05):
        """
        Bonferroni correction - conservative
        Adjusts alpha by dividing by number of tests
        """
        n = len(p_values)
        adjusted_alpha = alpha / n
        significant = [p < adjusted_alpha for p in p_values]
        return significant, adjusted_alpha

    @staticmethod
    def holm_bonferroni(p_values, alpha=0.05):
        """
        Holm-Bonferroni - less conservative
        Sequential rejection procedure
        """
        n = len(p_values)
        sorted_indices = np.argsort(p_values)
        sorted_p = np.array(p_values)[sorted_indices]

        significant = np.zeros(n, dtype=bool)
        for i, p in enumerate(sorted_p):
            if p < alpha / (n - i):
                significant[sorted_indices[i]] = True
            else:
                break

        return significant

    @staticmethod
    def benjamini_hochberg(p_values, alpha=0.05):
        """
        Benjamini-Hochberg - FDR control
        Controls false discovery rate, not family-wise error
        """
        n = len(p_values)
        sorted_indices = np.argsort(p_values)
        sorted_p = np.array(p_values)[sorted_indices]

        # Find largest k such that p(k) <= k * alpha / n
        significant = np.zeros(n, dtype=bool)
        for i in range(n-1, -1, -1):
            if sorted_p[i] <= (i + 1) * alpha / n:
                significant[sorted_indices[:i+1]] = True
                break

        return significant

    @staticmethod
    def report_multiple_comparisons(tests_performed, correction_method='bonferroni'):
        """
        Generate report for multiple comparisons
        """
        report = f"""
## Multiple Comparisons Report

### Tests Performed
- Number of tests: {len(tests_performed)}
- Correction method: {correction_method}

### Original vs. Corrected Significance
| Test | Original p | Corrected p | Significant |
|------|-----------|-------------|-------------|
"""
        # Generate report entries
        return report


# Example usage
def example_multiple_comparisons():
    """
    Example: Comparing multiple models on multiple datasets
    """
    # Simulated p-values from 5 models on 4 datasets = 20 comparisons
    np.random.seed(42)
    p_values = np.random.uniform(0, 0.1, 20)  # Simulated p-values

    correction = MultipleComparisonsCorrection()

    print("Bonferroni correction:")
    sig_bonf, adj_alpha = correction.bonferroni(p_values)
    print(f"  Adjusted alpha: {adj_alpha:.4f}")
    print(f"  Significant: {sum(sig_bonf)}/{len(p_values)}")

    print("\nBenjamini-Hochberg correction:")
    sig_bh = correction.benjamini_hochberg(p_values)
    print(f"  Significant: {sum(sig_bh)}/{len(p_values)}")
```

### P-hacking Prevention Checklist

```markdown
## P-hacking Prevention Checklist

### Before Analysis
- [ ] Preregister primary hypotheses
- [ ] Preregister primary analysis plan
- [ ] Specify primary outcome metric
- [ ] Determine sample size/runs in advance
- [ ] Define inclusion/exclusion criteria

### During Analysis
- [ ] Stick to preregistered analysis
- [ ] Document all analyses performed
- [ ] Apply multiple comparison correction
- [ ] Report all tests conducted
- [ ] Distinguish exploratory from confirmatory

### During Reporting
- [ ] Report all experimental conditions
- [ ] Report all metrics computed
- [ ] Explain multiple comparison corrections
- [ ] Report effect sizes, not just p-values
- [ ] Be transparent about exploratory analyses

### Self-Assessment Questions
- Did I decide on my analysis before looking at results?
- Would I still report this if the result was different?
- Have I corrected for multiple comparisons?
- Am I being transparent about all tests conducted?
```

---

## 5. Sunk Cost Fallacy

### Definition

The tendency to continue an endeavor once an investment in money, effort, or time has been made, even when the endeavor is unlikely to succeed.

### Manifestation in AI/ML Research

```
┌─────────────────────────────────────────────────────────────────┐
│                 SUNK COST IN AI RESEARCH                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROJECT CONTINUATION                                           │
│  ├── "We've already spent months on this approach"             │
│  ├── "The compute costs are already paid"                       │
│  └── "We need results to justify the investment"               │
│                                                                 │
│  MODEL DEVELOPMENT                                              │
│  ├── Over-optimizing a fundamentally flawed architecture        │
│  ├── Adding complexity to rescue a poor approach               │
│  └── Refusing to abandon a non-performing model                 │
│                                                                 │
│  INFRASTRUCTURE                                                 │
│  ├── Continuing with inadequate tools because of training      │
│  ├── Maintaining legacy systems beyond usefulness               │
│  └── Over-customizing instead of adopting better alternatives   │
│                                                                 │
│  RESEARCH DIRECTION                                             │
│  ├── Pursuing unproductive lines of inquiry                     │
│  ├── Ignoring evidence of failure                               │
│  └── Framing failures as "almost successes"                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Sunk Cost Decision Framework

```python
# sunk_cost_assessment.py

class SunkCostAssessment:
    """
    Framework for assessing whether to continue or abandon
    """

    def __init__(self, project_name):
        self.project_name = project_name
        self.assessment = {}

    def evaluate(self):
        """
        Conduct sunk cost evaluation
        """
        questions = {
            'independent_value': """
If you were starting today with no prior investment, would you
choose this project? (Yes/No)
            """,
            'evidence_trend': """
Has recent evidence made the project more or less promising?
(More promising / Less promising / Same)
            """,
            'alternatives': """
Are there clearly better alternatives that would deliver similar
value faster? (Yes/No)
            """,
            'completion_viability': """
Is the remaining work likely to produce valuable results?
(Very likely / Somewhat likely / Unlikely)
            """,
            'opportunity_cost': """
What could be achieved with resources currently devoted to this project?
            """,
            'emotional_attachment': """
Is emotional attachment to the project affecting judgment?
(Yes/No/Unsure)
            """
        }

        for key, question in questions.items():
            self.assessment[key] = input(question).strip()

        return self.make_recommendation()

    def make_recommendation(self):
        """
        Generate recommendation based on assessment
        """
        stop_indicators = [
            self.assessment.get('independent_value') == 'No',
            self.assessment.get('evidence_trend') == 'Less promising',
            self.assessment.get('alternatives') == 'Yes',
            self.assessment.get('completion_viability') == 'Unlikely'
        ]

        if sum(stop_indicators) >= 3:
            return "RECOMMENDATION: Consider terminating or pivoting project"
        elif sum(stop_indicators) >= 2:
            return "RECOMMENDATION: Re-evaluate project direction and scope"
        else:
            return "RECOMMENDATION: Project appears viable, continue monitoring"

    def generate_report(self):
        """
        Generate sunk cost assessment report
        """
        report = f"""
# Sunk Cost Assessment: {self.project_name}

## Assessment Results
{json.dumps(self.assessment, indent=2)}

## Key Questions for Decision Making

1. **The Fresh Start Test**: If starting today, would you choose this?
   → {self.assessment.get('independent_value', 'Not assessed')}

2. **The Opportunity Cost**: What else could be done with these resources?
   → {self.assessment.get('opportunity_cost', 'Not assessed')}

3. **The Evidence Test**: Is the trend in evidence positive?
   → {self.assessment.get('evidence_trend', 'Not assessed')}

4. **The Objectivity Test**: Are emotions affecting judgment?
   → {self.assessment.get('emotional_attachment', 'Not assessed')}

## Sunk Costs (Ignore These)
- Time already invested
- Compute already used
- Code already written
- Papers already published

## Forward-Looking Costs (Consider These)
- Time remaining to completion
- Compute remaining needed
- Alternative uses of resources
- Value of expected outcomes
"""
        return report
```

---

## 6. Anchoring Bias

### Definition

The tendency to rely too heavily on the first piece of information offered (the "anchor") when making decisions.

### Impact on AI/ML Research

```markdown
## Anchoring in AI Research Contexts

### Budget and Resource Allocation
- Initial budget proposal anchors final allocation
- First cost estimate anchors expectations
- Prior year's spending anchors current budget

### Model Selection
- First model tried anchors subsequent choices
- Initial performance numbers anchor expectations
- Baseline selection anchored by common practice

### Evaluation Standards
- First metric tried anchors metric selection
- Benchmark scores anchor improvement expectations
- State-of-the-art numbers anchor progress perception

### Negotiation and Collaboration
- Initial position in discussions anchors outcomes
- First proposal anchors compromise range
- Prior agreements anchor future terms
```

### Mitigation Strategies

```markdown
## Anchoring Bias Mitigation

### Recognition Strategies
- [ ] Identify potential anchors in decisions
- [ ] Question whether anchor is relevant
- [ ] Consider multiple starting points
- [ ] Seek diverse perspectives

### Counter-Strategies
- [ ] Deliberately generate alternatives before evaluating
- [ ] Use multiple reference points
- [ ] Establish criteria before seeing options
- [ ] Reset analysis by changing context

### Practical Techniques
1. **Pre-commitment**: Decide on criteria before seeing options
2. **Multiple Anchors**: Generate several options before choosing
3. **Devil's Advocate**: Argue against the anchor
4. **Fresh Eyes**: Have unbiased person review
5. **Explicit Reset**: Start analysis from scratch periodically
```

---

## 7. Availability Bias

### Definition

The tendency to overestimate the importance of information that is available, recent, or memorable.

### Manifestation in AI/ML Research

```
┌─────────────────────────────────────────────────────────────────┐
│                 AVAILABILITY BIAS IN AI RESEARCH                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  RECENT PAPERS                                                  │
│  ├── Over-weighting recent conference papers                    │
│  ├── Ignoring older but relevant work                           │
│  └── "Hot topics" receiving disproportionate attention          │
│                                                                 │
│  MEMORABLE RESULTS                                              │
│  ├── Sensational findings remembered more                       │
│  ├── Large effect sizes over-represented                        │
│  └── Failures and null results under-weighted                   │
│                                                                 │
│  ACCESSIBLE DATA                                                │
│  ├── Convenient datasets overused                               │
│  ├── Harder-to-obtain data ignored                              │
│  └── Benchmark-centric research                                 │
│                                                                 │
│  VISIBLE SUCCESS                                                │
│  ├── Successful projects more visible                           │
│  ├── Published results over-represented                         │
│  └── Survivor bias in visible examples                          │
│                                                                 │
│  PERSONAL EXPERIENCE                                            │
│  ├── Own successful approaches overweighted                      │
│  ├── Techniques from past projects over-applied                 │
│  └── Familiar methods preferred                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Mitigation Framework

```python
# availability_bias_mitigation.py

class AvailabilityBiasMitigation:
    """
    Strategies to counteract availability bias in research
    """

    @staticmethod
    def systematic_literature_review(question, databases, date_range):
        """
        Conduct systematic review to counter recency bias
        """
        protocol = {
            'search_strategy': {
                'databases': databases,
                'date_range': date_range,
                'search_terms': [],
                'inclusion_criteria': [],
                'exclusion_criteria': []
            },
            'bias_countering': {
                'include_older_work': 'Must include papers from before recent trend',
                'include_null_results': 'Search for null findings and failures',
                'include_other_venues': 'Look beyond top conferences',
                'cross_disciplinary': 'Search related fields'
            }
        }
        return protocol

    @staticmethod
    def balanced_evaluation_checklist():
        """
        Checklist to ensure balanced consideration
        """
        checklist = {
            'perspectives': [
                'Have I considered approaches I am unfamiliar with?',
                'Have I considered older work (5+ years)?',
                'Have I considered work from other venues?',
                'Have I considered null/negative results?',
                'Have I considered approaches that failed?'
            ],
            'data': [
                'Have I considered datasets beyond the popular ones?',
                'Have I considered real-world vs benchmark performance?',
                'Have I considered edge cases and failures?',
                'Have I considered different domains?'
            ],
            'methods': [
                'Have I considered simple baselines?',
                'Have I considered older techniques?',
                'Have I considered approaches outside my expertise?',
                'Have I considered hybrid approaches?'
            ]
        }
        return checklist

    @staticmethod
    def generate_alternatives_exercise(current_approach):
        """
        Generate diverse alternatives to counter availability bias
        """
        prompts = [
            f"What if {current_approach} doesn't work? What else could work?",
            "What would someone from a different field try?",
            "What approach was popular 10 years ago? Would it work now?",
            "What's the simplest thing that could work?",
            "What would a skeptic of this approach suggest?",
            "What approaches have been tried and abandoned? Why?"
        ]
        return prompts
```

---

## 8. Selection Bias and Sampling Bias

### Definition

Selection bias occurs when the sample used in a study is not representative of the population intended to be analyzed. Sampling bias is a specific type where the sampling method favors certain outcomes.

### Types in AI/ML Research

```markdown
## Selection Bias Types in AI/ML

### Data Selection Bias
- Non-representative training data
- Convenient sample selection
- Censored data (survivor bias)
- Selection based on outcomes

### Model Selection Bias
- Selecting models based on validation performance
- Hyperparameter tuning on test data (implicit)
- Selecting favorable random seeds
- Reporting best of multiple runs without disclosure

### Publication Selection Bias
- Selecting successful experiments for publication
- Cherry-picking favorable datasets
- Selecting metrics that favor proposed method
- Selecting favorable baselines

### User Selection Bias
- Selection bias in user studies
- Self-selection in surveys
- Attrition bias in longitudinal studies
- Convenience sampling of participants
```

### Detection and Mitigation

```python
# selection_bias_assessment.py

import numpy as np
from scipy import stats

class SelectionBiasAssessment:
    """
    Tools for detecting and assessing selection bias
    """

    @staticmethod
    def compare_distributions(sample, reference, feature_names=None):
        """
        Compare sample distribution to reference population
        """
        results = {}
        n_features = sample.shape[1] if len(sample.shape) > 1 else 1

        for i in range(n_features):
            if feature_names:
                name = feature_names[i]
            else:
                name = f'feature_{i}'

            # Statistical tests
            ks_stat, ks_p = stats.ks_2samp(sample[:, i], reference[:, i])

            results[name] = {
                'ks_statistic': ks_stat,
                'ks_p_value': ks_p,
                'sample_mean': np.mean(sample[:, i]),
                'reference_mean': np.mean(reference[:, i]),
                'sample_std': np.std(sample[:, i]),
                'reference_std': np.std(reference[:, i]),
                'bias_detected': ks_p < 0.05
            }

        return results

    @staticmethod
    def detect_reported_result_bias(reported_results, all_results):
        """
        Detect if reported results are cherry-picked
        """
        if len(all_results) <= 1:
            return "Insufficient data for comparison"

        reported_mean = np.mean(reported_results)
        all_mean = np.mean(all_results)
        all_std = np.std(all_results)

        z_score = (reported_mean - all_mean) / all_std if all_std > 0 else 0

        return {
            'reported_mean': reported_mean,
            'all_runs_mean': all_mean,
            'z_score': z_score,
            'potential_bias': z_score > 1.5,
            'interpretation': 'Reported results significantly above average' if z_score > 1.5 else 'No strong evidence of cherry-picking'
        }

    @staticmethod
    def model_selection_bias_check(validation_scores, test_scores, n_runs):
        """
        Check for model selection bias (selecting based on validation)
        """
        # If validation scores are consistently higher than test scores
        # after selection, there may be selection bias

        correlation = np.corrcoef(validation_scores, test_scores)[0, 1]

        return {
            'validation_test_correlation': correlation,
            'selection_bias_risk': 'High' if correlation < 0.5 else ('Medium' if correlation < 0.7 else 'Low'),
            'recommendation': 'Use held-out test set for final evaluation' if correlation < 0.7 else 'Validation-test alignment looks reasonable'
        }
```

---

## 9. Optimism Bias

### Definition

The tendency to overestimate the probability of positive events and underestimate the probability of negative events.

### Manifestation in AI/ML Projects

```
┌─────────────────────────────────────────────────────────────────┐
│                 OPTIMISM BIAS IN AI PROJECTS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROJECT PLANNING                                               │
│  ├── Underestimating time to completion                         │
│  ├── Underestimating resource requirements                      │
│  ├── Overestimating success probability                         │
│  └── Underestimating technical challenges                        │
│                                                                 │
│  PERFORMANCE ESTIMATION                                         │
│  ├── Overestimating model performance                           │
│  ├── Underestimating edge cases                                 │
│  ├── Overestimating generalization                              │
│  └── Underestimating failure modes                              │
│                                                                 │
│  RISK ASSESSMENT                                                │
│  ├── Underestimating deployment risks                           │
│  ├── Underestimating ethical concerns                           │
│  ├── Overestimating user acceptance                             │
│  └── Underestimating maintenance burden                          │
│                                                                 │
│  COMPETITIVE POSITION                                           │
│  ├── Overestimating novelty                                     │
│  ├── Underestimating competitors                                │
│  ├── Overestimating barriers to entry                           │
│  └── Underestimating complexity of deployment                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Calibration Framework

```markdown
## Optimism Calibration Framework

### Pre-Mortem Analysis
Before starting a project, imagine it has failed. Generate reasons:

1. **Technical Failures**
   - What technical challenges could derail us?
   - What assumptions might be wrong?
   - What could go wrong with the approach?

2. **Resource Failures**
   - What could cause us to run out of time?
   - What could cause us to run out of compute?
   - What could cause us to run out of people?

3. **External Failures**
   - What could competitors do?
   - What external events could affect us?
   - What could users reject?

### Reference Class Forecasting
Instead of estimating from inside view, use outside view:

1. Identify similar past projects
2. Gather statistics on those projects
3. Use those statistics to predict current project

### Planning Fallacy Correction
Multiply time estimates by:
- 2x for familiar tasks
- 3x for moderately novel tasks
- 4x for highly novel tasks
```

---

## 10. Bias Blind Spot

### Definition

The tendency to see oneself as less susceptible to biases than others, leading to failure to correct for one's own biases.

### Self-Assessment

```markdown
## Bias Blind Spot Self-Assessment

### Questions to Ask Yourself

1. Do I believe I am less biased than my colleagues?
2. Do I think my research approach is more objective?
3. Do I believe my conclusions are more data-driven?
4. Do I think I avoid the pitfalls I see in others?

### If You Answered "Yes"

You may be experiencing bias blind spot. Everyone is susceptible to bias.

### Countermeasures

- [ ] Assume you are biased (you probably are)
- [ ] Seek external review
- [ ] Use structured decision processes
- [ ] Get feedback from critics
- [ ] Apply bias checklists to yourself, not just others
- [ ] Consider: "What would convince me I'm wrong?"
```

---

## Summary: Bias Quick Reference

| Bias | Definition | Key Manifestation | Primary Mitigation |
|------|------------|-------------------|-------------------|
| Confirmation | Seeking confirming evidence | Only seeing supportive results | Adversarial testing, devil's advocate |
| Publication | Preferring positive results | Literature bias | Publish null results |
| HARKing | Retroactive hypotheses | Presenting exploration as confirmation | Preregistration |
| P-hacking | Multiple comparisons | Selective significance | Correction, preregistration |
| Sunk Cost | Irrecoverable investment bias | Continuing failed projects | Fresh start test |
| Anchoring | Over-relying on first info | Budget, metric anchoring | Multiple starting points |
| Availability | Over-weighting available info | Recency bias | Systematic review |
| Selection | Non-representative samples | Cherry-picking results | Representative sampling |
| Optimism | Overestimating success | Underestimating risk | Pre-mortem, reference class |
| Bias Blind Spot | Seeing self as less biased | Ignoring own biases | Assume you are biased |

---

## References

1. Kahneman, D. (2011). *Thinking, Fast and Slow*.
2. Nuzzo, R. (2015). How scientists fool themselves. *Nature*.
3. Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLOS Medicine*.
4. Gelman, A., & Loken, E. (2014). The statistical crisis in science. *American Scientist*.
5. Nosek, B. A., et al. (2015). Promoting an open research culture. *Science*.