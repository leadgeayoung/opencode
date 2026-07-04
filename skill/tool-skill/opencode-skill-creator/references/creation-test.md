# Creation Process & Testing

## 5-Step Creation Process

### Step 1: Clarify Requirements

| Question | Purpose |
|----------|---------|
| What specific problem does this solve? | Clarify value |
| When should it be triggered? | Design description |
| What does successful output look like? | Acceptance criteria |
| What are the edge cases? | Avoid omissions |

Good candidates: Reusable knowledge, multi-person processes, stable patterns.
Not suitable: One-time tasks, frequently changing content, project-specific conventions (use AGENTS.md).

### Step 2: Write name

Short, clear, lowercase, hyphen-separated. Reflect core functionality.

### Step 3: Write description (Most Critical)

Must include: specific capability, trigger scenarios, target use case, boundary limits.

Template:
```yaml
description: |
  [One sentence: core capability]
  Provides: [resources the skill contains]
  Suitable for: [trigger scenario 1], [trigger scenario 2]
  Not suitable for: [boundary scenario 1], [boundary scenario 2]
```

### Step 4: Write main instructions

Structure with Markdown — headers, lists, tables. Be actionable. Provide concrete examples. Reference detailed docs (`references/`).

### Step 5: Test and Validate

## Test Matrix

| Test Type | Content | Expected | Priority |
|-----------|---------|----------|----------|
| Trigger Test | "Help me query last quarter's revenue" | Skill activates | P0 |
| Boundary Test | "Query revenue" (no time range) | Asks then executes | P1 |
| Negative Test | "Help me write an email" | Doesn't activate | P0 |
| Output Test | Verify output format | Format correct | P1 |
| Error Test | Wrong input parameters | Graceful error | P2 |

## Trigger Test Cases

```
# Should activate
"Use [skill-name] skill"              → Explicit request
"Help me [core capability]"           → Semantic match
"[domain keyword]"                    → Keyword match

# Should NOT activate
"[unrelated task]"                    → Out of scope
"[edge case not in boundary list]"    → Boundary respected
```

## Manual Test Checklist

- [ ] Trigger test: all 3+ positive cases activate
- [ ] Negative test: all 3+ boundary cases don't activate
- [ ] Output test: format matches expectations
- [ ] Novice test: non-experts can successfully use
- [ ] Reference test: all `references/` files exist
- [ ] Error test: clear messages on wrong input

## Collaborative Creation

```
User: Help me create a data warehouse skill. I'll describe our tables and business logic.
Agent: Sure, tell me:
  1. What are your main data tables?
  2. What business terms need definition?
  3. What rules must be followed when querying?
```

## Learning from Failures

When a skill-produced output is wrong, reflect the fix back into the skill:
- Was the instruction not clear enough?
- Was an edge case not covered?
- Was a constraint not emphasized?
