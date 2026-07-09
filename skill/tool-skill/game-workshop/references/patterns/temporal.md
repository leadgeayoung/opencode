# Temporal Systems

## What problem this solves

The game world feels static. Nothing changes as time passes or as the story progresses. The player has no sense of rhythm or urgency.

## Core concepts

- **Phase**: A discrete world state (dawn, day, dusk, night; early/late game; act 1/2/3)
- **Trigger**: What causes a phase transition (enter a scene, use an item, complete a task, pure time)
- **Variant**: Content that changes per phase (scene descriptions, NPC positions, available items, dialogue)

## Design strategies

### Strategy A: Linear progression

Phases advance in a fixed sequence triggered by player actions.

**When to use**: Story-driven games, narrative adventures, games with clear acts/chapters.

**Design tips**:
- Each phase gate should feel earned, not arbitrary
- Phase transitions are good moments to deliver story beats

**Trade-off**: Predictable — the player knows exactly how to advance time.

### Strategy B: Conditional states

World state changes based on what the player has done, not just where they go.

**When to use**: Open-ended games, sandbox games, immersive sims.

**Design tips**:
- A single trigger can affect multiple systems simultaneously
- Combine with character relationships for richer reactivity

**Trade-off**: Harder to test — state explosion as conditions multiply.

## Verification

- [ ] Each phase has distinct, observable content
- [ ] Phase transitions happen when expected (and only then)
- [ ] Content from earlier phases is still accessible or appropriately replaced
- [ ] Edge case: rapidly cycling phases doesn't break anything
- [ ] All scenes have appropriate content for all phases
