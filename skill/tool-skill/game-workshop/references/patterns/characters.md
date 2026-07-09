# Character Systems (NPCs / Relationships / Dialogue)

## What problem this solves

NPCs are static information kiosks. They say the same thing every time, regardless of what the player has done.

## Core concepts

- **State**: The NPC's current relationship level or attitude toward the player
- **Conditional dialogue**: Different responses based on state, player inventory, world phase, or past actions
- **Presence**: Where and when the NPC appears, which may change based on game state
- **Reaction**: How the NPC responds to player actions (giving items, using items on them, reaching milestones)

## Design strategies

### Strategy A: Linear relationship

The NPC progresses through fixed stages as the player completes tasks.

**When to use**: Quest-driven games, story-adventure games, RPGs with quest chains.

**Design tips**:
- Each stage should have unique dialogue and potentially unique behavior
- Stages should be one-way (you don't regress unless intentional)

**Trade-off**: Simple but predictable — the player knows exactly what to do to progress the relationship.

### Strategy B: Conditional presence

NPCs appear in different places at different times or under different conditions.

**When to use**: Games with time systems, open-world games, immersive simulations.

**Design tips**:
- Give NPCs a schedule the player can learn and exploit
- Missing an NPC should feel like a consequence, not a bug

**Trade-off**: Adds depth but creates testing complexity — every NPC × every location × every phase must be verified.

### Strategy C: Reactive dialogue

NPC dialogue changes based on what the player has done, said, or acquired — even outside the NPC's quest chain.

**When to use**: Games aiming for deep immersion, games with interconnected systems.

**Design tips**:
- Use a simple flag system to track player actions across the game
- NPCs commenting on unrelated accomplishments makes the world feel alive
- Don't overdo it — one or two reactive lines per NPC is enough

**Trade-off**: Scalability problem — dialogue trees explode with N flags.

## Verification

- [ ] Each NPC appears at their expected location(s) and time(s)
- [ ] Dialogue changes appropriately as the game progresses
- [ ] Missing an NPC appearance doesn't break the game
- [ ] Edge case: talking to an NPC before and after a major event yields different dialogue
- [ ] Edge case: talking to an NPC repeatedly in the same state doesn't crash or produce gibberish
- [ ] All NPC interactions are optional (player can still finish the game without talking to anyone, unless designed otherwise)
