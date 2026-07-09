# Delegation — Agent Selection & Prompt Engineering

## Agent Selection Matrix

| Task type | Recommended agent | Tools | When to use |
|-----------|-----------------|-------|-------------|
| **Multi-step feature implementation** | `builder` | r/w/bash | Adding scenes, mechanics, NPCs, endings — any task that creates or modifies files |
| **Design** | `designer` | read-only | Creating structured design docs from vague concepts |
| **Testing/Review** | `reviewer` | read/bash | Walking through a game end-to-end, reporting bugs |
| **Codebase exploration** | `explore` | read-only | Understanding existing code structure before planning |
| **Quick single edit** | (direct tool use) | — | One-line fix, simple rename, obvious bug fix — no agent needed |

## Prompt Structure

Every delegation prompt should follow this template:

```
### 1. TASK
One sentence describing what to do.

### 2. EXPECTED OUTCOME
- [ ] Acceptance gate 1
- [ ] Acceptance gate 2
- [ ] Acceptance gate 3

### 3. MUST DO
- Step-by-step implementation guidance
- Specific files to read first
- Specific files to modify
- Verification steps

### 4. MUST NOT DO
- Boundaries and constraints
- What to preserve (don't break X)
- Style rules to follow

### 5. CONTEXT
Current state of the relevant files or systems.
Key variables, flags, or data structures involved.
Recent changes that affect this task.
```

## Quality Gates per Agent Type

| Agent | Before marking done |
|-------|-------------------|
| `builder` | File exists, imports clean, launches without error |
| `designer` | Document covers scenes, items, NPCs, endings — no ambiguity |
| `reviewer` | Report lists all scenes visited, all commands tried, all outcomes recorded |
| `explore` | Returns file paths + key code sections relevant to the query |

## Error Recovery

| Situation | Response |
|-----------|----------|
| Agent produces wrong output | Read the output, identify the gap, write a more specific prompt |
| Agent produces incomplete output | Add missing acceptance gates, re-delegate |
| Agent breaks existing functionality | Revert the file, add "MUST NOT change X" to prompt, re-delegate |
| Agent times out | Split the task into smaller sub-tasks |
