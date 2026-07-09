# 1→N Game Enhancement

Use when a game already exists and the user wants to add features, expand content, or deepen mechanics.

## Phase Decomposition

Divide the enhancement into phases ordered by dependency. Each phase contains one or more tasks.

### Standard Phase Order

| Phase | What goes here | Depends on |
|-------|---------------|------------|
| P0: Foundation | Engine tweaks, data structure changes, new hooks | — |
| P1: World | New scenes, new paths, map expansion | P0 |
| P2: Mechanics | Puzzles, time systems, trade-offs, new verbs | P1 |
| P3: Characters | New NPCs, dynamic dialogue, relationship systems | P2 |
| P4: Content | Endings, collectibles, hidden content | P3 |
| P5: Polish | Easter eggs, description variants, regression sweep | P4 |

If a phase has no work, skip it. If the enhancement is small, fold multiple phases into one.

### Task Structure

Each task within a phase follows this template:

```markdown
## Task N: [short name]

### Expectation
- [ ] Acceptance item 1
- [ ] Acceptance item 2

### Implementation notes
[precise instructions for the sub-agent]

### QA
[how to verify this task independently]
```

## Per-Task Execution Loop

For every task:

```
1. READ current game file(s)  →  understand latest state
2. WRITE task prompt          →  include Acceptance + Must Do + Must Not Do
3. DELEGATE to sub-agent      →  let them implement
4. REVIEW output              →  read the diff, verify logic
5. RUN game                   →  confirm no crash
6. MARK done                  →  update plan, record learnings
7. REPEAT for next task
```

## Same-File Constraint

When all changes land in the same file, tasks within a phase MUST execute serially. Parallel work is only possible when changes affect separate files.

## Verification Wave

After ALL phases are complete, run a full regression:

```
=== VERIFICATION WAVE ===

F1: Game starts without error
F2: All original scenes still accessible
F3: All original commands still work
F4: All original endings still reachable
F5: All new scenes accessible (including edge-case paths)
F6: All new mechanics work (puzzles, trades, time systems)
F7: All new NPCs appear and respond correctly
F8: All new endings reachable
F9: No dead-end paths where player is stuck
F10: Edge-case commands don't crash (invalid input, wrong scene, etc)

Result: ___ / 10 gates passed
```

## Learning Record

After each task, append a one-liner to a notepad or log:

```
[task N] what worked / what didn't / surprising finding
```

This accumulates into a project memory that speeds up later tasks.
