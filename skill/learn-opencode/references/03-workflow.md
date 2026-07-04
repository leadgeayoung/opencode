# Workflow

---

## 1. Plan vs Build

### Two Primary Agents

| Agent | Type | Permissions |
|-------|------|-------------|
| **Build** | Primary | All tools, read-write |
| **Plan** | Primary | Read-only, edit deny (only `.opencode/plans/*.md` allow) |

**Switch between them**: Press the **Tab** key.

### Plan Agent Permission Config

```typescript
{
  edit: { "*": "deny", ".opencode/plans/*.md": "allow", ... },
  bash: "allow"
}
```

### When to Use Each

| Agent | Use For |
|-------|---------|
| **Plan** | Analyze code, planning, code review, learn codebase |
| **Build** | Write features, fix bugs, refactor, create files |

### Default Configuration

```jsonc
{
  "agent": {
    "build": {
      "mode": "primary",
      "temperature": 0.3,
      "permission": {
        "edit": "allow",
        "bash": "allow"
      }
    },
    "plan": {
      "mode": "primary",
      "temperature": 0.1,
      "permission": {
        "edit": { "*": "deny", ".opencode/plans/*.md": "allow" },
        "bash": "allow"
      }
    }
  }
}
```

### Temperature Details

| Agent | Temperature | Behavior |
|-------|-------------|----------|
| Plan | 0.1 | Low — deterministic, focused analysis |
| Build | 0.3 | Medium — balanced creativity and precision |

### Max Steps

- `maxSteps` — **deprecated**
- Use `steps` instead to limit agent iterations.

### plan_enter / plan_exit (Experimental)

**Requirements:**
- `OPENCODE_EXPERIMENTAL=true` or `OPENCODE_EXPERIMENTAL_PLAN_MODE=true` environment variable
- Requires CLI client (not Web/IDE)

**Flow:**
1. Build Agent calls `plan_enter` → switches to Plan mode
2. Plan Agent calls `plan_exit` → returns to Build mode

### Plan File Storage

| Scenario | Path |
|----------|------|
| Git project | `.opencode/plans/<timestamp>-<slug>.md` |
| No VCS | `~/.local/share/opencode/plans/<timestamp>-<slug>.md` |

### TODO Tracking

- Tell the AI: *"track progress with TODO"* for complex multi-step tasks.
- AI uses internal **todoread** / **todowrite** tools to maintain a structured task checklist.

---

## 2. Agents System

### Two Agent Types

| Type | Invoke | Description |
|------|--------|-------------|
| **Primary** | Tab switch | Direct conversation (build, plan) |
| **Subagent** | `@name` | Expert invoked by Primary (explore, general) |

### Built-in Agents

| Agent | Type | Specializes | Permissions |
|-------|------|-------------|-------------|
| `build` | primary | Full-stack development | All tools |
| `plan` | primary | Analysis / planning | edit deny (plans allow) |
| `explore` | subagent | Quick code search | `grep` / `glob` / `list` / `bash` / `read` / `webfetch` / `websearch` / `codesearch` |
| `general` | subagent | Complex research | `todoread`/`todowrite`: deny |

### Explore Subagent Depth Levels

| Level | Description |
|-------|-------------|
| quick | Basic, fast scan |
| medium | Balanced depth |
| very thorough | Comprehensive analysis |

### Hidden Agents

- `title` — auto-run
- `summary` — auto-run
- `compaction` — auto-run

### Subagent Execution Mechanism

- Runs in a **new independent Session**
- Cannot see the Primary agent's conversation history
- Must provide **complete context in the prompt** (no back-references)

### Auto-Invocation

- Primary Agent **auto-selects** the best subagent based on the agent's `description` field.

### Session Navigation

| Key | Action |
|-----|--------|
| `<leader>→` | Next session |
| `<leader>←` | Previous session |
| `<leader>↑` | Parent session |

### Agent List

- `<leader>a` — opens the agent list/selector

---

## 3. Project Initialization (`/init`)

### Command

- `/init` — generates `AGENTS.md` in the project root.
- Advanced: `/init Pay special attention to X` — passes custom parameters to the init process.

### What init Scans

- Project files and directory structure
- Build commands, test commands, lint commands
- Code style conventions
- Naming conventions

### Integrations

| Source | Path(s) |
|--------|---------|
| Cursor rules | `.cursor/rules/`, `.cursorrules` |
| Copilot rules | `.github/copilot-instructions.md` |

- **Improves** existing `AGENTS.md` rather than overwriting it.

### Rules File Lookup Order

| Priority | Location |
|----------|----------|
| 1 | Project root: `AGENTS.md` or `CLAUDE.md` |
| 2 | Global: `~/.config/opencode/AGENTS.md` |
| 3 | `~/.claude/CLAUDE.md` |
| 4 | `$OPENCODE_CONFIG_DIR/AGENTS.md` |
| 5 | `instructions` array in `opencode.json` |

### instructions Config

- Supports **glob patterns**
- Supports **URLs** (5-second timeout)
- Supports `~/` expansion
- Supports **absolute and relative paths**

### Merge Behavior

- **All** found rules files are **merged** — not overridden. Content from multiple sources is combined.
