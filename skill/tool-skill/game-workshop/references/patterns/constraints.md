# Constraints (Lock / Key / Gate)

## What problem this solves

The player can reach the ending immediately. There's no sense of progression — nothing stands between them and the conclusion.

## Core concepts

- **Gate**: Something that blocks progress (locked door, blocked path, missing knowledge)
- **Key**: Something that opens the gate (physical item, password, skill, completed prerequisite)
- **Condition**: The rule connecting gate and key ("unlock only if player has X and Y")

## Design strategies

### Strategy A: Physical key

The player must find a specific item and use it at the gate.

**When to use**: Adventure games, exploration-heavy games, inventory-based puzzles.

**Design tips**:
- Place the key before the gate (the player should see the gate first, then find the key, then return)
- The key should feel useful, not like a fetch quest

**Trade-off**: Simplest to implement, but can feel mechanical.

### Strategy B: Knowledge/information key

The player must learn something (password, sequence, pattern) to pass the gate.

**When to use**: Mystery games, detective games, games with lore-driven puzzles.

**Design tips**:
- The information should be discoverable through gameplay, not guesswork
- Consider multiple sources for the same information so one missed clue doesn't soft-lock the player

**Trade-off**: Richer than physical keys, but risks player frustration if the clue is too obscure.

### Strategy C: State gate

A gate that opens automatically when the world reaches a certain condition.

**When to use**: Story-driven games, games with relationship systems, metroidvania-style progression.

**Design tips**:
- The condition should be observable (the player can see why the gate opened)
- Combine with NPC dialogue to hint at what conditions need to be met

**Trade-off**: Least explicit — the player may not understand why the gate opened or what they did.

## Verification

- [ ] Gate is locked when approached without the key
- [ ] Gate unlocks when the key is obtained and properly used
- [ ] Gate stays unlocked once opened (no re-locking unless intentional)
- [ ] Key cannot be used on unrelated gates
- [ ] Edge case: player acquires key before reaching the gate (should still work)
- [ ] Edge case: player loses/drops the key (should re-lock or maintain state appropriately)
