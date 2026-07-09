# Choices (Branching / Trade-offs / Consequences)

## What problem this solves

Player decisions don't matter. Every path converges to the same outcome, making choices feel cosmetic.

## Core concepts

- **Branch**: A point where the player's decision affects subsequent content
- **Cost**: What the player gives up (consume an item, lose access to a path, forfeit an ending)
- **Irreversibility**: A choice that permanently closes other options
- **Consequence**: How the game world changes in response to a choice

## Design strategies

### Strategy A: Resource trade-off

The player must spend a limited resource to gain something, knowing they cannot use it elsewhere.

**When to use**: Games with limited inventory, currency systems, consumable items.

**Design tips**:
- The resource must be genuinely limited — if the player can grind for more, the trade-off is meaningless
- Signal scarcity before the choice point

**Trade-off**: Small design effort, big player impact. Works in any genre.

### Strategy B: Route branch

The player chooses between mutually exclusive paths, each with unique content.

**When to use**: Games with multiple endings, faction systems, alignment systems.

**Design tips**:
- Each branch should have unique content worth replaying for
- The branch point should be clearly signposted
- Late-game branches feel more impactful than early ones (the player has invested more)

**Trade-off**: Content doubles with every branch — expensive to produce.

### Strategy C: Moral/ambiguous choice

No obviously "right" answer. Each option has both positive and negative consequences.

**When to use**: Narrative-heavy games, games aiming for emotional impact, mature themes.

**Design tips**:
- Both options should be defensible (the player should hesitate)
- Deliver consequences later, not immediately — delayed feedback is more powerful
- Avoid obvious good/evil labeling. Let the player justify their own choice

**Trade-off**: Hardest to design well. If the consequences feel arbitrary, the player resents the game.

## Verification

- [ ] Each branch leads to observably different outcomes
- [ ] Consumed resources are actually consumed (not duplicated)
- [ ] Irreversible choices are properly locked after the decision
- [ ] All branches are playable (no broken content on any path)
- [ ] Edge case: player saves before a choice, reloads, picks differently (works correctly)
- [ ] Edge case: player tries to use a consumed item after it's gone (graceful handling)
