# 0→1 New Game Creation

Use when the user wants to create a brand new game from nothing.

## The 5-Step Pipeline

Each step produces a concrete artifact. You drive the process; sub-agents do the work.

### Step 1: Concept Lock

**Your role**: If the user says "随便" or "你决定", choose a type and theme yourself. Do not proceed without clarity.

Artifact: a one-liner: "A [genre] game about [theme] with [unique twist]".

**Prompt template** (to yourself — no sub-agent needed):

> User wants: [what they said]
> Locked concept: A [genre] game about [theme]

### Step 2: Design Document

**Delegate to**: `designer` sub-agent (read-only)

Prompt structure:

```
Task(designer): "Design a [genre] game about [theme]. Include:

1. Story & premise (~2 paragraphs)
2. Scene list (name + description for each)
3. Item list (name + purpose)
4. NPC list (name + role + dialogue)
5. Ending conditions
6. Player commands that should work

Output: structured design document in markdown."
```

Acceptance: the document has clear scenes, items, NPCs, and endings — enough for a builder to implement without asking follow-ups.

QA: read the document back. If anything is ambiguous, ask designer to clarify.

### Step 3: Build

**Delegate to**: `builder` sub-agent (r/w/bash)

Prompt structure:

```
Task(builder): "Implement the following game design document as a playable game:

[design document from Step 2]

Requirements:
- Use the target framework/engine available in the project
- All scenes, items, NPCs, and endings from the design doc must be present
- The game must be runnable (python/ruby/etc with a single command)
- Follow existing code conventions in the project
- File: [path/to/game_file]

When done, verify the game starts without errors."
```

Acceptance: game file exists, imports clean, launches without crash.

QA: run the launcher command. Confirm zero startup errors.

### Step 4: Test

**Delegate to**: `reviewer` sub-agent (read/bash)

Prompt structure:

```
Task(reviewer): "Test the game at [path/to/game_file].

Do:
1. Start a new game
2. Walk through every scene
3. Try every command mentioned in the design
4. Pick up and use every item
5. Trigger every ending
6. Try edge cases: look at nothing, use in wrong scene, go to invalid direction

Report bugs with: scene name, command used, what happened vs what should happen."
```

Acceptance: a test report listing all tested paths and their results.

QA: if bugs exist, return to Step 3 for fixes. Loop until reviewer reports all paths pass.

### Step 5: Deliver

**Your role**: Present the result to the user.

Template:

```
游戏做好了！

  文件： [path]
  类型： [genre]
  故事： [one-sentence premise]
  场景数： [N]
  结局数： [N]
  操作： [most common commands]
```

## State Machine

```
[Concept Lock] → [Design Doc] → [Build] → [Test]
                                        ↓
                                   bugs? → [Fix] → [Test]
                                        ↓
                                   clean → [Deliver]
```
