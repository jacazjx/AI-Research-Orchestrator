# Validity Types in Research

A comprehensive guide to understanding and applying validity concepts in AI/ML research. Validity determines whether your research actually measures what you intend to measure and whether findings can be trusted.

## Overview

Validity is the cornerstone of credible research. In AI/ML research, validity concerns are particularly complex due to the nature of algorithmic systems, data dependencies, and the gap between benchmark performance and real-world application.

```
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDITY ECOSYSTEM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌───────────────┐     ┌───────────────┐                    │
│    │   INTERNAL    │     │   EXTERNAL    │                    │
│    │   VALIDITY    │────▶│   VALIDITY    │                    │
│    └───────┬───────┘     └───────┬───────┘                    │
│            │                     │                             │
│            ▼                     ▼                             │
│    ┌───────────────┐     ┌───────────────┐                    │
│    │  CONSTRUCT    │     │  ECOLOGICAL   │                    │
│    │   VALIDITY    │     │   VALIDITY    │                    │
│    └───────────────┘     └───────────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Internal Validity

### Definition

Internal validity refers to the degree to which a study establishes a trustworthy cause-and-effect relationship between the treatment (independent variable) and the outcome (dependent variable), free from confounding factors.

### Threats to Internal Validity

| Threat Category | Description | AI/ML Example |
|-----------------|-------------|---------------|
| Selection Bias | Non-random assignment creates pre-existing differences | Training on non-representative data splits |
| History Effects | External events during study affect outcomes | Dataset drift during long training runs |
| Maturation | Natural changes in subjects over time | Model behavior changes with data accumulation |
| Instrumentation | Changes in measurement tools or procedures | Different evaluation metrics across runs |
| Testing Effects | Pre-testing influences post-test results | Overfitting to validation set |
| Regression to Mean | Extreme scores tend toward average | Performance on outliers regresses |
| Attrition | Dropout creates non-random samples | Selective removal of hard examples |
| Confounding Variables | Third variables explain the relationship | Data preprocessing differences |

### Internal Validity in AI/ML Research

#### Experimental Control Checklist

```markdown
## Internal Validity Checklist for AI/ML Experiments

### Data Controls
- [ ] Random seeds documented and fixed for reproducibility
- [ ] Data splits stratified and documented
- [ ] Training/validation/test sets properly isolated
- [ ] No data leakage between splits
- [ ] Class distributions balanced or documented

### Training Controls
- [ ] Hyperparameters fixed or systematically varied
- [ ] Training duration consistent across conditions
- [ ] Hardware differences controlled or documented
- [ ] Software versions recorded
- [ ] Batch ordering randomized

### Evaluation Controls
- [ ] Same evaluation metrics used across conditions
- [ ] Statistical significance tests applied
- [ ] Multiple runs conducted (n >= 3)
- [ ] Confidence intervals reported
- [ ] Bonferroni correction for multiple comparisons
```

### Example: Controlling for Confounds in Neural Architecture Studies

```
Problem: Comparing two neural architectures for image classification

CONFOUNDED DESIGN:
- Architecture A: Trained for 100 epochs with learning rate 0.001
- Architecture B: Trained for 50 epochs with learning rate 0.01

INTERNAL VALIDITY ISSUES:
- Different training durations (confound)
- Different learning rates (confound)
- Cannot attribute performance differences to architecture

VALID DESIGN:
- Architecture A: Trained for 100 epochs with LR 0.001, seed=42
- Architecture B: Trained for 100 epochs with LR 0.001, seed=42
- Repeated with seeds: 42, 123, 456, 789, 1001
- Additional ablation: Learning rate sensitivity analysis

STATISTICAL ANALYSIS:
- Paired t-test across seeds
- Effect size (Cohen's d) reported
- 95% confidence intervals
```

### Decision Tree: Assessing Internal Validity

```
START: Evaluating Internal Validity
│
├── Is there a clear independent variable?
│   ├── NO → Invalid: Cannot establish causal relationship
│   └── YES → Continue
│
├── Is there random assignment or randomization?
│   ├── NO → Document potential selection bias
│   └── YES → Continue
│
├── Are confounding variables controlled?
│   ├── NO → Invalid: Rival explanations possible
│   └── YES → Continue
│
├── Are measurement instruments consistent?
│   ├── NO → Invalid: Instrumentation threat
│   └── YES → Continue
│
├── Are appropriate statistical tests used?
│   ├── NO → Weak: Results may be spurious
│   └── YES → HIGH INTERNAL VALIDITY
```

---

## 2. External Validity

### Definition

External validity refers to the extent to which research findings can be generalized to other populations, settings, times, and measures beyond the specific study conditions.

### Types of Generalization

```
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL VALIDITY DIMENSIONS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  POPULATION VALIDITY                                            │
│  ├── Sample → Target Population                                 │
│  ├── Demographics representativeness                            │
│  └── Cultural and geographic factors                            │
│                                                                 │
│  ECOLOGICAL VALIDITY                                            │
│  ├── Lab conditions → Real-world conditions                     │
│  ├── Environment representativeness                             │
│  └── Task authenticity                                          │
│                                                                 │
│  TEMPORAL VALIDITY                                              │
│  ├── Current findings → Future applicability                    │
│  ├── Historical period effects                                  │
│  └── Technological obsolescence                                 │
│                                                                 │
│  CONTEXTUAL VALIDITY                                            │
│  ├── Research setting → Application settings                    │
│  ├── Domain transferability                                     │
│  └── Cross-domain applicability                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Threats to External Validity in AI/ML

| Threat | Description | Mitigation Strategy |
|--------|-------------|---------------------|
| Benchmark Overfitting | Models optimized for specific benchmarks fail in practice | Multiple diverse benchmarks |
| Distribution Shift | Real-world data differs from training distribution | Domain adaptation, robustness testing |
| Selection Bias in Datasets | Common datasets don't represent target population | Dataset analysis, bias documentation |
| Simplified Task Assumptions | Research tasks oversimplify real-world complexity | Realistic task design |
| Hardware Dependencies | Results depend on specific hardware configurations | Hardware-agnostic metrics |
| Software Stack Dependencies | Framework-specific optimizations may not transfer | Cross-framework validation |

### Example: External Validity in Computer Vision Research

```python
# Example: Assessing External Validity of Image Classification Model

class ExternalValidityAssessment:
    """
    Framework for evaluating external validity of CV models
    """

    def assess_population_validity(self, model, test_sets):
        """
        Evaluate generalization across different populations
        """
        results = {}

        # Standard benchmark (ImageNet validation)
        results['imagenet'] = model.evaluate(test_sets['imagenet'])

        # Demographic subsets (if available)
        results['age_groups'] = {
            group: model.evaluate(data)
            for group, data in test_sets['demographics'].items()
        }

        # Geographic regions
        results['geographic'] = {
            region: model.evaluate(data)
            for region, data in test_sets['geographic'].items()
        }

        # Fairness metrics
        results['fairness_gap'] = self.compute_performance_gap(results)

        return results

    def assess_ecological_validity(self, model, deployment_scenarios):
        """
        Evaluate real-world performance
        """
        results = {}

        # Lab conditions (clean, controlled data)
        results['controlled'] = model.evaluate(deployment_scenarios['clean'])

        # Real-world conditions
        results['real_world'] = {
            'noisy': model.evaluate(deployment_scenarios['noisy']),
            'adversarial': model.evaluate(deployment_scenarios['adversarial']),
            'compressed': model.evaluate(deployment_scenarios['compressed']),
            'partial_occlusion': model.evaluate(deployment_scenarios['occluded'])
        }

        # Performance degradation analysis
        results['robustness_score'] = self.compute_robustness(results)

        return results
```

### External Validity Checklist for AI Research Papers

```markdown
## External Validity Assessment

### Population Generalization
- [ ] Dataset demographics documented
- [ ] Known biases in training data acknowledged
- [ ] Performance across subgroups analyzed
- [ ] Fairness metrics reported
- [ ] Limitations of training population discussed

### Task Generalization
- [ ] Multiple benchmarks used for evaluation
- [ ] Out-of-distribution testing conducted
- [ ] Real-world deployment scenarios considered
- [ ] Task complexity levels evaluated
- [ ] Failure modes documented

### Setting Generalization
- [ ] Hardware requirements specified
- [ ] Computational cost reported
- [ ] Framework dependencies noted
- [ ] Reproducibility instructions provided
- [ ] Cross-platform testing (if applicable)

### Temporal Considerations
- [ ] Dataset recency discussed
- [ ] Potential for concept drift acknowledged
- [ ] Long-term performance monitoring suggested
- [ ] Update/retraining requirements addressed
```

---

## 3. Construct Validity

### Definition

Construct validity refers to the degree to which a test or measure accurately assesses the theoretical construct or trait it was designed to measure. It answers: "Are we measuring what we think we're measuring?"

### Components of Construct Validity

```
┌─────────────────────────────────────────────────────────────────┐
│                  CONSTRUCT VALIDITY COMPONENTS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CONVERGENT VALIDITY                                            │
│  │                                                              │
│  ├── Measures that should be related ARE related              │
│  ├── Example: Accuracy and F1 should correlate for balanced   │
│  │   classification                                            │
│  └── Established through multi-trait correlations              │
│                                                                 │
│  DISCRIMINANT VALIDITY                                          │
│  │                                                              │
│  ├── Measures that should NOT be related are NOT related      │
│  ├── Example: Model size and fairness should be independent   │
│  └── Established through divergent correlations                │
│                                                                 │
│  NOMOLOGICAL VALIDITY                                           │
│  │                                                              │
│  ├── Construct fits within theoretical network                 │
│  ├── Relationships match theoretical predictions               │
│  └── Consistent with existing theory                            │
│                                                                 │
│  CONTENT VALIDITY                                                │
│  │                                                              │
│  ├── Measure covers all aspects of the construct               │
│  ├── Comprehensive coverage of the domain                      │
│  └── Expert judgment of adequacy                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Construct Validity in AI/ML: Key Constructs

| Construct | Common Operationalizations | Validity Concerns |
|-----------|---------------------------|-------------------|
| Intelligence | Benchmark performance | Narrow task definition |
| Fairness | Demographic parity, equal opportunity | Single metric insufficient |
| Robustness | Adversarial accuracy, distribution shift | May not capture real-world failures |
| Efficiency | FLOPs, inference time, memory | Tradeoffs not captured |
| Interpretability | Feature importance, attention weights | Proxy may not match human understanding |

### Example: Construct Validity of "Model Fairness"

```markdown
## Construct Validity Analysis: Model Fairness

### Theoretical Construct
"Fairness" in ML models refers to the absence of discrimination against
individuals based on protected attributes (race, gender, age, etc.)

### Operationalization Problem
Fairness is a complex, multi-dimensional construct, yet researchers often
use single metrics as proxies.

### Validity Assessment

CONVERGENT VALIDITY CHECK:
- Do different fairness metrics correlate?
  - Demographic Parity ↔ Equalized Odds: WEAK correlation
  - Equal Opportunity ↔ Predictive Parity: CONTEXT-DEPENDENT
  - Result: Single metrics DO NOT capture the full construct

DISCRIMINANT VALIDITY CHECK:
- Is fairness independent from accuracy?
  - Fairness-Accuracy Tradeoff: Often NEGATIVELY correlated
  - Result: These are distinct constructs (good)

CONTENT VALIDITY CHECK:
- Does one metric capture all fairness concerns?
  - Demographic Parity: Misses calibration issues
  - Equalized Odds: Misses intersectional concerns
  - Individual Fairness: Not captured by group metrics
  - Result: Multiple metrics REQUIRED

CONSTRUCT VALIDITY THREATS:
1. Construct Underrepresentation: Single metrics miss aspects
2. Construct-Irrelevant Variance: Metrics influenced by data distribution
3. Mono-operation Bias: Single operationalization

RECOMMENDATION:
Use multiple fairness metrics with clear justification for each choice.
Document which aspects of fairness are captured and which are missed.
```

### Construct Validity Checklist

```markdown
## Construct Validity Assessment

### Definition Phase
- [ ] Construct clearly defined theoretically
- [ ] Construct distinguished from related constructs
- [ ] Boundaries of construct specified
- [ ] Expert consensus on construct meaning

### Operationalization Phase
- [ ] Multiple operationalizations considered
- [ ] Operationalization justified theoretically
- [ ] Measurement procedure documented
- [ ] Alternative measures acknowledged

### Validation Phase
- [ ] Convergent validity tested
- [ ] Discriminant validity tested
- [ ] Known-groups validation (if applicable)
- [ ] Criterion validation against established measures

### AI/ML Specific Considerations
- [ ] Proxy measures identified as proxies
- [ ] Limitations of operationalization discussed
- [ ] Construct breadth vs. depth tradeoff addressed
- [ ] Domain-specific validity concerns noted
```

---

## 4. Ecological Validity

### Definition

Ecological validity refers to the extent to which research findings can be generalized to real-world settings. It specifically addresses whether the conditions of the study reflect the conditions of the natural environment where the phenomenon occurs.

### Laboratory vs. Real-World Conditions

```
┌─────────────────────────────────────────────────────────────────┐
│           ECOLOGICAL VALIDITY CONTINUUM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CONTROLLED LAB          SIMULATED           REAL-WORLD         │
│  CONDITIONS               CONDITIONS         DEPLOYMENT          │
│                                                                 │
│  ◄─────────────────────────────────────────────────────────►    │
│  High Internal          Medium             High External        │
│  Validity               Both               Validity             │
│                         Medium                                  │
│                                                                 │
│  AI/ML Examples:                                                │
│  • Clean benchmark       • Data              • Production       │
│    datasets                augmentation        environment       │
│  • Standardized          • Domain            • Edge cases       │
│    splits                  adaptation          & failures       │
│  • Fixed hyperparams     • Adversarial       • User behavior    │
│                           testing              variability      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ecological Validity Threats in AI/ML Research

| Threat | Lab Condition | Real-World Reality | Impact |
|--------|---------------|-------------------|--------|
| Clean Data | Preprocessed, labeled data | Noisy, incomplete data | Performance degradation |
| Stationary Distribution | Fixed test set | Distribution shift | Model drift |
| Single Task | Task-specific training | Multi-task demands | Capability gaps |
| Fixed Inputs | Standard formats | Variable inputs | System failures |
| Perfect Availability | Always running | Resource constraints | Degraded performance |
| Ethical Abstraction | Simulated scenarios | Real human impact | Harm potential |
| Static Models | No updates | Continuous updates | Maintenance burden |

### Example: Ecological Validity in Recommender Systems Research

```python
class EcologicalValidityFramework:
    """
    Framework for assessing ecological validity in recommender systems
    """

    def compare_lab_real_world(self, model, lab_data, real_world_data):
        """
        Compare performance in controlled vs. real conditions
        """

        # LAB CONDITIONS (Typical research setup)
        lab_results = {
            'data': 'Static movie ratings dataset',
            'evaluation': 'Hold-out split, offline metrics',
            'metrics': {
                'RMSE': model.evaluate(lab_data, metric='rmse'),
                'Precision@K': model.evaluate(lab_data, metric='precision'),
                'NDCG': model.evaluate(lab_data, metric='ndcg')
            },
            'assumptions': [
                'Users have stable preferences',
                'All items always available',
                'No position bias in display',
                'Rating reflects true preference'
            ]
        }

        # REAL-WORLD CONDITIONS (Deployment reality)
        real_world_results = {
            'data': 'Production log data',
            'evaluation': 'Online A/B test, user behavior',
            'metrics': {
                'CTR': model.online_evaluate('click_through_rate'),
                'Conversion': model.online_evaluate('conversion'),
                'Session_Duration': model.online_evaluate('session_duration'),
                'User_Retention': model.online_evaluate('retention')
            },
            'unmeasured_factors': [
                'Cold-start users/items',
                'Item catalog changes',
                'Seasonal/temporal effects',
                'Competing recommendations',
                'User interface effects',
                'Privacy constraints'
            ]
        }

        # ECOLOGICAL VALIDITY ASSESSMENT
        validity_assessment = {
            'metric_correlation': self.correlate(lab_results, real_world_results),
            'performance_gap': self.compute_gap(lab_results, real_world_results),
            'unmeasured_threats': self.identify_threats(real_world_results),
            'recommendations': self.generate_recommendations()
        }

        return validity_assessment
```

### Ecological Validity Decision Framework

```
START: Assessing Ecological Validity of AI Research
│
├── Does the task reflect real-world complexity?
│   ├── NO → LOW ecological validity
│   │        → Document simplifications
│   │        → Recommend real-world validation
│   └── YES → Continue
│
├── Does the data reflect real-world distribution?
│   ├── NO → MEDIUM ecological validity
│   │        → Acknowledge distribution differences
│   │        → Test on real-world data
│   └── YES → Continue
│
├── Does the evaluation reflect real-world success?
│   ├── NO → MEDIUM ecological validity
│   │        → Add real-world metrics
│   │        → Consider online evaluation
│   └── YES → Continue
│
├── Are failure modes realistic?
│   ├── NO → LOW ecological validity
│   │        → Analyze real failure cases
│   │        → Test edge cases
│   └── YES → HIGH ecological validity
```

### Ecological Validity Checklist

```markdown
## Ecological Validity Assessment Checklist

### Task Authenticity
- [ ] Task reflects real-world application
- [ ] Complexity matches deployment scenario
- [ ] Success criteria aligned with user needs
- [ ] Edge cases considered
- [ ] Multi-task scenarios tested (if applicable)

### Data Authenticity
- [ ] Data source documented
- [ ] Preprocessing steps justified
- [ ] Known distribution differences acknowledged
- [ ] Real-world data testing conducted
- [ ] Privacy/ethical constraints noted

### Evaluation Authenticity
- [ ] Metrics reflect real-world success
- [ ] Offline-online gap analyzed
- [ ] Human evaluation included (if applicable)
- [ ] Long-term effects considered
- [ ] Failure impact assessed

### Deployment Considerations
- [ ] Computational constraints addressed
- [ ] Latency requirements considered
- [ ] Maintenance requirements discussed
- [ ] Update/monitoring strategies outlined
- [ ] Ethical implications of deployment noted
```

---

## 5. Validity Trade-offs and Integration

### The Validity Tension

Researchers often face trade-offs between different types of validity. Understanding these tensions is crucial for research design.

```
┌─────────────────────────────────────────────────────────────────┐
│                   VALIDITY TRADE-OFFS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INTERNAL VALIDITY ◄───────────────────► EXTERNAL VALIDITY     │
│  (Control)                              (Generalization)        │
│                                                                 │
│  • Tight control limits generalization                          │
│  • High ecological validity may introduce confounds             │
│  • Balance through multi-phase research                          │
│                                                                 │
│  CONSTRUCT VALIDITY ◄──────────────────► PRACTICAL UTILITY     │
│  (Theoretical accuracy)                 (Applicability)         │
│                                                                 │
│  • Perfect constructs may be impractical                        │
│  • Practical measures may lack validity                         │
│  • Multiple operationalizations help                             │
│                                                                 │
│  STATISTICAL CONCLUSION ◄──────────────► PRACTICAL SIGNIFICANCE │
│  (P-values)                              (Effect sizes)         │
│                                                                 │
│  • Statistical significance ≠ practical importance             │
│  • Large samples can detect tiny effects                        │
│  • Report both significance and effect size                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Integrated Validity Assessment Framework

```markdown
## Comprehensive Validity Assessment

### Phase 1: Research Design
1. Define primary construct(s) of interest
2. Identify validity types most relevant to research question
3. Anticipate validity threats
4. Design multi-method approach if possible

### Phase 2: Implementation
1. Document all operationalizations
2. Implement controls for internal validity
3. Plan for external validity assessment
4. Create validity audit trail

### Phase 3: Analysis
1. Assess each validity type systematically
2. Document validity limitations
3. Conduct sensitivity analyses
4. Triangulate findings across methods

### Phase 4: Reporting
1. Report validity assessment transparently
2. Acknowledge limitations explicitly
3. Provide recommendations for improvement
4. Enable replication and extension
```

### Validity Assessment Template

```markdown
## Validity Assessment Report

### Research Question
[State the primary research question]

### Construct Definition
[Define the key constructs under study]

### Internal Validity Assessment
- Controls implemented: [List]
- Remaining threats: [List]
- Mitigation strategies: [List]
- Confidence level: [High/Medium/Low]

### External Validity Assessment
- Population generalizability: [Assessment]
- Setting generalizability: [Assessment]
- Temporal considerations: [Assessment]
- Limitations: [List]

### Construct Validity Assessment
- Operationalization justification: [Explanation]
- Convergent validity evidence: [Evidence]
- Discriminant validity evidence: [Evidence]
- Alternative operationalizations: [List]

### Ecological Validity Assessment
- Task authenticity: [Assessment]
- Data authenticity: [Assessment]
- Evaluation authenticity: [Assessment]
- Gap analysis: [Analysis]

### Overall Validity Conclusion
[Summarize validity profile and limitations]
```

---

## 6. Validity in Specific AI/ML Research Contexts

### Benchmark Studies

```markdown
## Validity Considerations for Benchmark Studies

### Internal Validity
- Document all hyperparameters and seeds
- Report confidence intervals across multiple runs
- Control for computational resources
- Use consistent preprocessing

### External Validity
- Test on multiple benchmarks
- Include out-of-distribution datasets
- Report performance variance across domains
- Acknowledge benchmark-specific optimizations

### Construct Validity
- Clarify what benchmark measures
- Discuss benchmark limitations
- Avoid conflating benchmark performance with general capability
- Consider multiple benchmarks for complex constructs

### Ecological Validity
- Benchmark vs. deployment gap
- Real-world task correspondence
- Data distribution alignment
- Failure mode relevance
```

### Algorithm Comparison Studies

```markdown
## Validity Considerations for Algorithm Comparisons

### Internal Validity
- Statistical significance testing (paired tests)
- Multiple comparison corrections
- Consistent evaluation protocol
- Control for implementation differences

### External Validity
- Cross-dataset validation
- Domain transfer analysis
- Hyperparameter sensitivity
- Generalization bounds

### Construct Validity
- What does "better" mean?
- Multiple performance dimensions
- Trade-off analysis (accuracy vs. speed)
- Fair comparison of capabilities

### Ecological Validity
- Implementation complexity
- Computational requirements
- Practical deployment considerations
- Maintenance burden
```

### Applied AI Research

```markdown
## Validity Considerations for Applied AI Research

### Internal Validity
- Clear intervention definition
- Controlled deployment conditions
- Confounding variable identification
- A/B testing where possible

### External Validity
- User population representativeness
- Context transferability
- Scalability considerations
- Cultural/regional factors

### Construct Validity
- User-centered outcome measures
- Stakeholder construct alignment
- Qualitative validity triangulation
- Expert validation

### Ecological Validity
- Real deployment conditions
- User behavior authenticity
- System integration complexity
- Longitudinal effects
```

---

## Summary: Quick Reference

### Validity Types at a Glance

| Type | Core Question | Key Threats | AI/ML Priority |
|------|---------------|-------------|----------------|
| Internal | Is the causal relationship valid? | Confounds, bias, selection | High - controlled experiments |
| External | Can findings be generalized? | Distribution shift, domain gap | High - real-world applicability |
| Construct | Are we measuring the right thing? | Proxy inadequacy, narrow metrics | Critical - AI constructs are complex |
| Ecological | Do findings apply in real settings? | Simplified tasks, clean data | High - deployment gap |

### Validity Assessment Quick Checklist

```markdown
## Minimum Validity Standards for AI Research

□ Define constructs clearly
□ Document operationalizations
□ Control for major confounds
□ Report statistical significance AND effect sizes
□ Test on multiple datasets/domains
□ Acknowledge validity limitations
□ Discuss generalizability constraints
□ Address real-world applicability
```

---

## References and Further Reading

1. Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002). *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*.

2. Cronbach, L. J., & Meehl, P. E. (1955). Construct validity in psychological tests. *Psychological Bulletin*.

3. Firestone, C. (2020). Performance vs. competence in human–computer comparisons. *Cognition*.

4. Raji, I. D., et al. (2020). Closing the AI accountability gap: Defining an end-to-end framework for internal algorithmic auditing. *FAccT*.

5. Koch, G., et al. (2023). Benchmarking as a scientific methodology. *Nature Methods*.