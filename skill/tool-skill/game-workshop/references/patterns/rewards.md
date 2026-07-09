# Reward Systems (Collectibles / Endings / Secrets)

## What problem this solves

Once the player finishes the main path, there's no reason to explore further. The world feels shallow.

## Core concepts

- **Collectible**: An item or flag the player accumulates over time, with no immediate effect
- **Counter**: The threshold that determines when enough has been gathered
- **Unlock**: The reward that appears when the counter is met
- **Secret**: Content gated behind non-obvious player actions

## Design strategies

### Strategy A: Quantity gate

Collect N of something to unlock a reward.

**When to use**: Games with exploration, games that benefit from replayability, any genre where players explore.

**Design tips**:
- Make the count visible to the player (so they know they're making progress)
- Allow collecting more than needed (don't hard-lock if the player misses one)
- The best rewards change how the ending feels, not just a score screen

**Trade-off**: Works universally but can feel like busywork if the collectibles aren't meaningfully placed.

### Strategy B: Combination gate

A specific combination of items or flags triggers a hidden outcome.

**When to use**: Puzzle-heavy games, games with alchemy/crafting, secret endings.

**Design tips**:
- Give subtle hints, not explicit instructions
- The combination should be discoverable through gameplay, not guesswork
- A failed combination should give a hint, not just silence

**Trade-off**: High satisfaction when discovered, but risks being too obscure.

### Strategy C: Exploration reward

Non-obvious player actions (looking at an object twice, using an item on itself, entering a command at a specific scene) produce unexpected outcomes.

**When to use**: Games with a strong sense of place, games with a dedicated audience.

**Design tips**:
- Easter eggs should never be required for completion
- The payoff should be proportional to the obscurity (good reward for obscure action)
- Consider a "hint NPC" or "hint item" for ambitious secrets

**Trade-off**: Minimal effort, high delight — but invisible to most players.

## Verification

- [ ] All collectibles can be acquired through normal gameplay
- [ ] Counter-based unlocks trigger at the correct threshold
- [ ] Combination unlocks only trigger with the exact combination
- [ ] Secrets are optional (game is completable without them)
- [ ] Edge case: player has 0 collectibles (should not crash or show garbage)
- [ ] Edge case: player has more than the required N collectibles (should still work)
- [ ] Edge case: player tries secret actions before the prerequisite (no crash, appropriate response)
