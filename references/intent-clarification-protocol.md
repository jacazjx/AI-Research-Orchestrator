# Intent Clarification Protocol

## Purpose

This document defines the protocol for clarifying research intent before starting any research phase. It ensures mutual understanding between the researcher and the orchestrator.

---

## Overview

The intent clarification process serves as a "Gate 0" before the formal research workflow begins. It prevents:

- Misaligned research direction
- Wasted effort on unclear objectives
- Scope creep during later phases
- Frustration from unmet expectations

---

## Process Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    INTENT CLARIFICATION                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Assess Clarity                                       │
│                                                              │
│ Input: Research idea, context                               │
│ Output: ClarityAssessment (score, gaps, suggestion)         │
│                                                              │
│ Dimensions:                                                  │
│   - Problem Definition (25%)                                │
│   - Solution Direction (25%)                                │
│   - Contribution Type (20%)                                 │
│   - Constraints (15%)                                       │
│   - Novelty Claim (15%)                                     │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
     Score < 0.4                       Score ≥ 0.4
              │                               │
              ▼                               ▼
┌─────────────────────┐          ┌─────────────────────────────┐
│ Step 1a: Brainstorm │          │ Step 2: Clarification Loop  │
│                     │          │                              │
│ Trigger:            │          │ Max rounds: 5               │
│ research-ideation   │          │ Target score: 0.7+          │
│ skill               │          │                              │
└─────────────────────┘          │ Each round:                 │
              │                   │   1. Generate questions     │
              │                   │   2. Get responses          │
              │                   │   3. Synthesize             │
              │                   │   4. Re-assess              │
              │                   └─────────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Generate Confirmation Document                       │
│                                                              │
│ Output: .autoresearch/research-intent-confirmation.md        │
│                                                              │
│ Contains:                                                    │
│   - Clarified research idea                                  │
│   - Key parameters (venue, timeline, resources)             │
│   - Success criteria                                         │
│   - Clarification history                                    │
│   - Confirmation status                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Project Initialization                               │
│                                                              │
│ Generate:                                                    │
│   - CLAUDE.md or AGENTS.md (based on platform)              │
│   - Project structure                                        │
│   - State file                                               │
│                                                              │
│ Then: Proceed to Survey phase                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Evaluation Criteria

### Dimension 1: Problem Definition (25%)

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | No clear problem stated; very vague ("I want to do ML research") |
| 0.3-0.5 | Problem mentioned but not specific ("Improve NLP models") |
| 0.5-0.7 | Problem defined with some specificity ("Improve NER for medical texts") |
| 0.7-0.9 | Clear problem with context and importance ("NER for medical texts lacks domain adaptation; this affects clinical NLP pipelines") |
| 0.9-1.0 | Fully specified problem with stakeholders, impact, and urgency |

### Dimension 2: Solution Direction (25%)

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | No idea how to approach |
| 0.3-0.5 | Vague direction ("Use transformers") |
| 0.5-0.7 | Specific approach mentioned ("Fine-tune BioBERT with domain adaptation") |
| 0.7-0.9 | Approach with justification and alternatives considered |
| 0.9-1.0 | Detailed methodology with expected challenges |

### Dimension 3: Contribution Type (20%)

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | No idea what type of contribution |
| 0.3-0.5 | General sense ("Make something better") |
| 0.5-0.7 | Type identified but vague ("Novel method") |
| 0.7-0.9 | Clear contribution type with scope ("New domain adaptation method for NER") |
| 0.9-1.0 | Specific contribution claim with validation criteria |

### Dimension 4: Constraints (15%)

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | No constraints mentioned |
| 0.3-0.5 | Some constraints ("Need to finish by summer") |
| 0.5-0.7 | Key constraints stated ("EMNLP deadline, 2 GPUs available") |
| 0.7-0.9 | Comprehensive constraints with priorities |
| 0.9-1.0 | All constraints documented with contingency plans |

### Dimension 5: Novelty Claim (15%)

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | No novelty discussion |
| 0.3-0.5 | Claims novelty without justification ("This is new") |
| 0.5-0.7 | Identifies gap ("Current methods don't handle X well") |
| 0.7-0.9 | Clear novelty claim with differentiation ("Unlike Y, we do Z") |
| 0.9-1.0 | Strong novelty claim with preliminary evidence |

---

## Question Bank

### Problem Questions

1. **What specific problem are you trying to solve?**
   - Follow-up: Can you be more specific about the problem scope?
   - Follow-up: Who would benefit most from solving this?

2. **Why is this problem important? What's the impact?**
   - Follow-up: Are there concrete metrics for measuring impact?
   - Follow-up: Has this problem gotten worse recently?

3. **What happens if this problem isn't solved?**
   - Follow-up: Is there a deadline or critical timeline?
   - Follow-up: Are there workarounds people currently use?

### Solution Questions

1. **What attempts have been made? Why aren't they good enough?**
   - Follow-up: What specifically was lacking in prior approaches?
   - Follow-up: Are there partial solutions we could build on?

2. **What's your intuition about what might work?**
   - Follow-up: What evidence supports this intuition?
   - Follow-up: Have you tested any parts of this intuition?

3. **What constraints limit possible solutions?**
   - Follow-up: Are these constraints hard or soft?
   - Follow-up: Could any constraints be relaxed?

### Contribution Questions

1. **What type of contribution do you want to make?**
   - Options: Novel Method, Theoretical Analysis, Application Study, Benchmark, Survey

2. **What would constitute a successful outcome?**
   - Follow-up: Can you define specific success metrics?
   - Follow-up: What's the minimum acceptable outcome?

3. **What's the minimum viable contribution?**
   - Follow-up: What's the absolute minimum that would be valuable?
   - Follow-up: What would an incremental improvement look like?

### Constraint Questions

1. **What's the target venue?**
   - Follow-up: Is there a specific deadline?
   - Follow-up: Are there formatting or length requirements?

2. **What's the timeline?**
   - Follow-up: Are there hard deadlines or milestones?
   - Follow-up: What's your availability for this project?

3. **What compute resources and data are available?**
   - Follow-up: Are there any budget constraints?
   - Follow-up: Do you have access to necessary datasets?

### Novelty Questions

1. **What's your key insight or idea?**
   - Follow-up: What makes this insight unique?
   - Follow-up: Where did this insight come from?

2. **Which assumptions in existing work can be challenged?**
   - Follow-up: What happens if those assumptions don't hold?
   - Follow-up: Why haven't others challenged these assumptions?

3. **Is there similar work? If so, how is yours different?**
   - Follow-up: Can you articulate the key differentiator?
   - Follow-up: What would a reviewer say is novel about your approach?

---

## Integration with research-ideation

### Trigger Conditions

Invoke `research-ideation` skill when:

1. **Clarity score < 0.4** - Idea too vague to guide research
2. **User explicitly requests help** - "I need help developing my idea"
3. **Abstract idea without direction** - "I want to do NLP research"
4. **Reference papers provided without angle** - Papers present but no clear hypothesis

### Handoff Protocol

When triggering brainstorming:

```python
invoke_skill("research-ideation", {
    "initial_idea": idea,
    "domain": context.get("domain"),
    "reference_papers": context.get("reference_papers", []),
    "constraints": {
        "venue": context.get("venue"),
        "timeline": context.get("timeline"),
        "resources": context.get("resources"),
    },
})
```

### Return from Brainstorming

The `research-ideation` skill returns:
- Ranked list of 3-5 concrete ideas
- Each with: hypothesis, approach, novelty, feasibility, validation path

After brainstorming:
1. Present ideas to researcher
2. Let them select or refine
3. Re-assess clarity of selected idea
4. Continue with clarification loop if needed

---

## Confirmation Document Format

### Required Fields

```markdown
# Research Intent Confirmation

## Clarified Research Idea

[Final mutually agreed understanding - 2-3 sentences]

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Problem | [Specific problem] |
| Approach | [Proposed direction] |
| Contribution | [Type and scope] |
| Venue | [Target venue] |
| Timeline | [Key dates] |
| Resources | [Available resources] |

## Success Criteria

### Minimum Success
- [Criterion 1]
- [Criterion 2]

### Target Success
- [Criterion 1]
- [Criterion 2]

## Clarification History

### Round 1 (YYYY-MM-DD HH:MM)
**Questions:**
1. [Question]
**Responses:**
1. [Response]
**Clarity:** 0.45 → 0.62

### Round 2 (YYYY-MM-DD HH:MM)
...

## Confirmation

- **Final Clarity Score:** 0.78
- **Rounds:** 3
- **Status:** Confirmed
- **Confirmed At:** YYYY-MM-DD HH:MM
```

---

## Platform Detection

The system automatically detects the platform and generates appropriate instruction files:

| Platform | Detection Method | Instruction File |
|----------|------------------|------------------|
| Claude Code | `CLAUDE.md` exists or environment | `CLAUDE.md` |
| Codex/OpenAI | MCP config or explicit flag | `AGENTS.md` |
| Unknown | Default to Claude Code | `CLAUDE.md` |

### Detection Logic

```python
def detect_platform(project_root: Path) -> str:
    """Detect the current platform."""
    # Check for existing instruction files
    if (project_root / "CLAUDE.md").exists():
        return "claude"
    if (project_root / "AGENTS.md").exists():
        return "codex"

    # Check environment
    if os.environ.get("CLAUDE_CODE"):
        return "claude"
    if os.environ.get("OPENAI_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY"):
        return "codex"

    # Default
    return "claude"
```

---

## Error Handling

### Unclear After Max Rounds

If clarity score remains below threshold after 5 rounds:

1. **Document the situation** - Record all Q&A history
2. **Escalate to researcher** - "I'm having trouble understanding your research direction"
3. **Offer options:**
   - Schedule a call for synchronous discussion
   - Try brainstorming skill for structured ideation
   - Start with exploratory Survey phase

### Conflicting Information

If responses contradict each other:

1. **Highlight the conflict** - "You mentioned X earlier, but now Y"
2. **Ask for clarification** - "Which is your priority?"
3. **Document the resolution** - Note which was correct

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-17 | Initial protocol definition |

---

## References

- [research-intent-clarification SKILL.md](../skills/research-intent-clarification/SKILL.md)
- [intent_clarification.py](../scripts/intent_clarification.py)
- [orchestrator SKILL.md](../skills/orchestrator/SKILL.md)