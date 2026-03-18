---
name: airesearchorchestrator:research-intent-clarification
description: Clarify research intent through iterative first-principles questioning before starting any research phase. Use when initializing a new project, when the research idea is vague, or before running Survey phase.
user-invocable: false
argument-hint: [research-topic-or-idea]
allowed-tools: Read, Write, Edit, Grep, Glob, Skill, AskUserQuestion
---
# Research Intent Clarification

## Purpose

Ensure the researcher's intent is fully understood before starting any research phase. This skill uses first-principles questioning to uncover hidden assumptions, clarify goals, and align expectations between the researcher and the orchestrator.

## When to Use

- **Initializing a new project** - Before creating project structure
- **Research idea is vague** - "I want to do NLP research" without specifics
- **Before Survey phase** - Ensure literature review targets the right questions
- **After brainstorming** - Confirm the selected idea is what the researcher wants

## Flow

```
Research Idea Input
        │
        ▼
┌─────────────────────┐
│ 1. Assess Clarity   │  Score: 0.0-1.0
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
 < 0.4        ≥ 0.4
    │           │
    ▼           │
┌─────────────┐ │
│ Brainstorm  │ │  Call research-ideation
└─────┬───────┘ │
      │         │
      └────┬────┘
           │
           ▼
┌─────────────────────┐
│ 2. Clarification    │  Max 5 rounds
│    Loop             │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 3. Generate         │
│    Confirmation Doc │
└─────────┬───────────┘
          │
          ▼
    Ready for Init
```

## Step 1: Assess Intent Clarity

### Clarity Score Algorithm

Evaluate the research idea across five dimensions:

| Dimension | Weight | Evaluation Criteria |
|-----------|--------|---------------------|
| **Problem Definition** | 25% | Is the specific problem clearly stated? |
| **Solution Direction** | 25% | Is there a sense of what approach might work? |
| **Contribution Type** | 20% | Is the expected contribution type clear? |
| **Constraints** | 15% | Are timeline, resources, and venue understood? |
| **Novelty Claim** | 15% | Is there a hypothesis about what's new? |

### Scoring Guide

```python
def assess_clarity(idea: str, context: dict) -> float:
    """
    Returns a clarity score from 0.0 to 1.0.

    Score interpretation:
    - 0.0-0.3: Very vague, needs brainstorming
    - 0.3-0.4: Unclear, recommend brainstorming
    - 0.4-0.6: Partially clear, needs clarification
    - 0.6-0.8: Mostly clear, minor clarifications
    - 0.8-1.0: Clear, ready to proceed
    """
    scores = {}

    # Problem Definition
    scores["problem"] = evaluate_problem_definition(idea)
    # Check for: specific problem statement, importance, impact

    # Solution Direction
    scores["solution"] = evaluate_solution_direction(idea, context)
    # Check for: prior attempts, intuition, constraints

    # Contribution Type
    scores["contribution"] = evaluate_contribution_type(idea, context)
    # Check for: method/theory/application/benchmark

    # Constraints
    scores["constraints"] = evaluate_constraints(context)
    # Check for: timeline, venue, resources

    # Novelty Claim
    scores["novelty"] = evaluate_novelty_claim(idea)
    # Check for: key insight, challenged assumptions

    return weighted_average(scores)
```

### Suggested Actions by Score

| Score Range | Action | Rationale |
|-------------|--------|-----------|
| 0.0-0.3 | **MUST brainstorm** | Too vague to guide research |
| 0.3-0.4 | **Recommend brainstorming** | Significant gaps in understanding |
| 0.4-0.6 | Clarification loop | Enough to start, needs refinement |
| 0.6-0.8 | Minor clarification | Quick check before proceeding |
| 0.8-1.0 | Proceed directly | Clear enough to start research |

## Step 2: First-Principles Question Bank

### Problem Dimension

```markdown
1. 你试图解决的具体问题是什么？
   - What specific problem are you trying to solve?

2. 这个问题为什么重要？有什么影响？
   - Why is this problem important? What's the impact?

3. 如果不解决这个问题会怎样？
   - What happens if this problem isn't solved?

4. 谁会从解决方案中受益？
   - Who would benefit from a solution?

5. 这个问题已经存在多久了？
   - How long has this problem existed?
```

### Solution Dimension

```markdown
1. 之前有哪些尝试？为什么不够好？
   - What attempts have been made? Why aren't they good enough?

2. 你的直觉是什么方法可能有效？
   - What's your intuition about what might work?

3. 有什么约束限制可能的解决方案？
   - What constraints limit possible solutions?

4. 有哪些技术路线你认为不太可能成功？
   - Which technical routes do you think won't work?

5. 你有没有部分有效的初步想法？
   - Do you have preliminary ideas that partially work?
```

### Contribution Dimension

```markdown
1. 你希望做出什么类型的贡献？
   - What type of contribution do you want to make?

   Types:
   - [ ] Novel Method (新方法)
   - [ ] Theoretical Analysis (理论分析)
   - [ ] Application Study (应用研究)
   - [ ] Benchmark/Evaluation (基准评估)
   - [ ] Survey/Review (综述)

2. 什么样的成果算成功？
   - What would constitute a successful outcome?

3. 最小可行贡献是什么？
   - What's the minimum viable contribution?

4. 你希望达到什么水平的验证？
   - What level of validation do you want?
```

### Context Dimension

```markdown
1. 目标期刊/会议是什么？
   - What's the target venue?

2. 时间线是怎样的？
   - What's the timeline?

3. 有什么计算资源和数据可用？
   - What compute resources and data are available?

4. 有没有合作者或导师的约束？
   - Any collaborator or advisor constraints?

5. 有没有必须引用的论文或方法？
   - Any papers or methods you must cite?
```

### Novelty Dimension

```markdown
1. 你的关键洞察或想法是什么？
   - What's your key insight or idea?

2. 现有工作的哪些假设可以被挑战？
   - Which assumptions in existing work can be challenged?

3. 你认为最大的创新点是什么？
   - What do you think is your biggest innovation?

4. 有没有类似的工作？如果有，你的不同之处？
   - Is there similar work? If so, how is yours different?
```

## Step 3: Clarification Loop

### Loop Control

```python
MAX_ROUNDS = 5
MIN_CONFIRMATION_SCORE = 0.7

def run_clarification_loop(idea: str, context: dict) -> ClarificationResult:
    """
    Execute clarification loop until confirmed or max rounds reached.
    """
    rounds = []
    current_idea = idea
    clarity_score = assess_clarity(current_idea, context)

    while len(rounds) < MAX_ROUNDS and clarity_score < MIN_CONFIRMATION_SCORE:
        # Generate targeted questions based on gaps
        gaps = identify_clarity_gaps(current_idea, context, clarity_score)
        questions = generate_questions_for_gaps(gaps)

        # Ask questions (via AskUserQuestion tool)
        responses = ask_questions(questions)

        # Update idea based on responses
        current_idea = synthesize_idea(current_idea, responses)

        # Record round
        rounds.append({
            "round": len(rounds) + 1,
            "questions": questions,
            "responses": responses,
            "clarity_before": clarity_score,
            "clarity_after": assess_clarity(current_idea, context),
        })

        clarity_score = rounds[-1]["clarity_after"]

    return ClarificationResult(
        original_idea=idea,
        clarified_idea=current_idea,
        clarity_score=clarity_score,
        rounds=rounds,
        confirmed=clarity_score >= MIN_CONFIRMATION_SCORE,
    )
```

### Question Selection Strategy

Select questions based on the lowest-scoring dimensions:

```python
def select_questions(clarity_scores: dict) -> list[str]:
    """
    Select 2-3 questions targeting the weakest dimensions.
    """
    # Sort dimensions by score (ascending)
    sorted_dims = sorted(clarity_scores.items(), key=lambda x: x[1])

    # Select questions from lowest-scoring dimensions
    questions = []
    for dim, score in sorted_dims[:2]:  # Top 2 weakest
        questions.extend(get_dimension_questions(dim, count=2))

    return questions[:5]  # Max 5 questions per round
```

## Step 4: Generate Confirmation Document

After the clarification loop (or if initial clarity was high), generate:

**File:** `.autoresearch/research-intent-confirmation.md`

```markdown
# Research Intent Confirmation

## Clarified Research Idea

[Final mutually agreed understanding]

## Key Parameters

- **Problem:** [Specific problem statement]
- **Approach:** [Proposed direction]
- **Contribution:** [Expected contribution type]
- **Venue:** [Target venue]
- **Timeline:** [Key dates]

## Clarification History

### Round 1
**Questions:**
1. [Question]
**Responses:**
1. [Response]

## Confirmation

- **Clarity Score:** [0.0-1.0]
- **Rounds:** [Number]
- **Status:** [Confirmed / Needs Further Discussion]
```

## Integration with research-ideation

### Trigger Conditions

Call `research-ideation` skill when:
- Clarity score < 0.4
- User explicitly requests help
- Idea is abstract without specific direction
- Reference papers provided but no clear angle

### Integration Code

```python
def should_trigger_brainstorming(assessment: ClarityAssessment, context: dict) -> bool:
    """Determine if brainstorming skill should be invoked."""
    if assessment.score < 0.4:
        return True
    if context.get("explicit_help_request"):
        return True
    if assessment.is_abstract and not assessment.has_direction:
        return True
    if context.get("reference_papers") and not assessment.has_angle:
        return True
    return False

def trigger_brainstorming(idea: str, context: dict) -> None:
    """Invoke research-ideation skill."""
    invoke_skill("research-ideation", idea, {
        "domain": context.get("domain"),
        "reference_papers": context.get("reference_papers", []),
        "constraints": context.get("constraints", {}),
    })
```

## Hard Rules

1. **Never skip for low clarity** - If score < 0.4, MUST brainstorm
2. **Max 5 rounds** - Don't endless loop; escalate if unclear
3. **Document everything** - All Q&A must be recorded
4. **Confirm before proceeding** - Get explicit confirmation
5. **Use first-principles** - Start from fundamentals, not assumptions

## Output

After completion:
1. Generate `research-intent-confirmation.md`
2. Update project state with clarity score
3. Proceed to project initialization or Survey phase

## Related Skills

- [research-ideation](../research-ideation/SKILL.md) - For brainstorming research ideas
- [orchestrator](../orchestrator/SKILL.md) - Main orchestration skill