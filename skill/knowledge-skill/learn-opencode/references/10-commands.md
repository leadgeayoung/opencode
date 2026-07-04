# 10 — Custom Commands

## 1. Overview

Custom commands let you define reusable prompts that run when typed in the TUI as `/command-name`. They complement built-in commands (`/init`, `/undo`, `/redo`, `/share`, `/help`).

## 2. Command File Locations

| Location | Scope | Priority |
|----------|-------|----------|
| `.opencode/commands/*.md` | Project | High |
| `~/.config/opencode/commands/*.md` | Global | Medium |
| `command` field in `opencode.json` | Depends | Merged (JSON > MD) |

**Resolution order**: Project-level commands override global commands of the same name. JSON config `command` field takes highest priority when there's a name collision with a `.md` file.

**Filename = command name**: `organize-invoices.md` → `/organize-invoices`

## 3. Configuration Formats

### 3.1 Markdown (File-based)

File: `.opencode/commands/test.md` or `~/.config/opencode/commands/test.md`

```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-sonnet-4-20250514
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

**Frontmatter fields**:

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Shown in TUI autocomplete |
| `agent` | No | Agent to execute (default: current agent). If a subagent, triggers subagent invocation unless `subtask: false` |
| `model` | No | Override model for this command |
| `subtask` | No | `true` forces subagent mode; `false` suppresses it |

**Body = template**: The Markdown body (after frontmatter) becomes the prompt sent to the AI.

### 3.2 JSON (Config-based)

In `opencode.json` or `.opencode/opencode.json`:

```jsonc
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-sonnet-4-20250514",
      "subtask": true
    }
  }
}
```

**JSON fields**:

| Field | Required | Description |
|-------|----------|-------------|
| `template` | **Yes** | The prompt body (string, supports placeholders) |
| `description` | No | Shown in TUI when typing `/` |
| `agent` | No | Override agent. If refers to a subagent, triggers subagent call unless `subtask: false` |
| `model` | No | Override model ID (`provider/model-id`) |
| `subtask` | No | `true` → force subagent mode regardless of agent config; `false` → suppress subagent even if agent is a subagent |

### 3.3 Override Rules

- **Same name as built-in** → overrides built-in command (e.g., custom `/undo` replaces the built-in)
- **MD file conflicts with JSON** → JSON takes priority
- **Same name in project vs global** → project wins

## 4. Placeholders & Template Syntax

### 4.1 Argument Placeholders

| Token | Replaced with |
|-------|---------------|
| `$ARGUMENTS` | All arguments passed to the command |
| `$1`, `$2`, `$3`, ... | Positional arguments (1-indexed) |
| `$*` | All arguments (passthrough) |
| `$@` | All arguments individually quoted (passthrough) |

Example (`component.md`):

```markdown
---
description: Create a new React component
---
Create a new React component named $1 with TypeScript support.
Include proper typing and a Storybook story.
```

Usage: `/component Button` → replaces `$1` with `Button`.

Multiple arguments:

```markdown
---
description: Create a file with content
---
Create a file named $1 in directory $2 with content: $3
```

Usage: `/create-file config.json src "{ \"key\": \"value\" }"`

### 4.2 Shell Output Embedding

Syntax: `` !`command` `` — executes the shell command at **call time** (not file creation time) and injects its output into the prompt.

```markdown
---
description: Analyze test coverage
---
Here are the current test results:

!`npm test`

Based on these results, suggest improvements to increase coverage.
```

```markdown
---
description: Review recent changes
---
Recent git commits:

!`git log --oneline -10`

Review these changes and suggest any improvements.
```

```markdown
---
description: Organize invoices
---
Please organize invoice PDFs from the $1 directory into $2:

1. First output "list of operations to be performed", don't execute directly
2. Execute after I confirm

Hint: Today is !`date +%Y-%m-%d`
```

Commands run in the project root directory. Output becomes part of the prompt.

### 4.3 File References in Templates

Syntax: `@path/to/file` — injects file content into the prompt.

```markdown
---
description: Review component
---
Review the component in @src/components/Button.tsx.
Check for performance issues and suggest improvements.
```

- Paths are relative to project root
- Supports `@` in both Markdown and JSON `template` strings
- Content is embedded at call time, not definition time

## 5. Full Command Options Reference

### 5.1 template

The prompt sent to the LLM. Required in JSON config; in Markdown, the body text IS the template.

Supports `$ARGUMENTS`, `$1`-`$N`, `$*`, `$@`, `` !`cmd` ``, and `@file` syntax.

### 5.2 description

Displayed in the TUI autocomplete when user types `/`. Helps users discover and understand commands.

### 5.3 agent

Specifies which agent executes the command.

- If **omitted**: uses the current active agent
- If set to a **subagent**: triggers a subagent invocation (the subagent handles the task in a child session, not polluting the main context)
- If `subtask: false` is set alongside an agent: prevents subagent invocation even if the agent is a subagent

### 5.4 subtask

Boolean. Forces or suppresses subagent invocation:

- `true` → always run as subagent (child session), regardless of agent config
- `false` → never run as subagent, even if target agent has `mode: subagent`
- Omitted → follows the agent's mode setting

### 5.5 model

Overrides the model for this specific command:

```jsonc
{
  "command": {
    "deep-analyze": {
      "template": "Deeply analyze $1",
      "model": "anthropic/claude-opus-4-5-thinking"
    }
  }
}
```

Format: `"providerId/modelId"`

## 6. Built-in Commands (Non-custom)

| Command | Aliases | Purpose | Keybind |
|---------|---------|---------|---------|
| `/new` | `/clear` | Create new session | `Ctrl+X N` |
| `/sessions` | `/resume`, `/continue` | List/switch sessions | `Ctrl+X L` |
| `/undo` | — | Undo last message + file changes (needs Git) | `Ctrl+X U` |
| `/redo` | — | Redo previously undone message | `Ctrl+X R` |
| `/compact` | `/summarize` | Compress context to save tokens | `Ctrl+X C` |
| `/export` | — | Export conversation as Markdown | `Ctrl+X X` |
| `/share` | — | Create public share link | — |
| `/unshare` | — | Remove public share link | — |
| `/details` | — | Toggle tool execution details | — |
| `/editor` | — | Open external editor for composing | `Ctrl+X E` |
| `/thinking` | — | Toggle display of reasoning blocks | — |
| `/init` | — | Create/update AGENTS.md | — |
| `/connect` | — | Add a provider (interactive) | — |
| `/models` | — | List available models | `Ctrl+X M` |
| `/agents` | — | List agents | `Ctrl+X A` |
| `/copy` | — | Copy entire conversation to clipboard | — |
| `/exit` | `/quit`, `/q` | Exit OpenCode | `Ctrl+X Q` |
| `/help` | — | Show help | — |
| `/stats` | — | Token usage, cost, session count | — |
| `/version` | — | Show version | — |

Custom commands can **override** any built-in by using the same name.

## 7. Best Practices

- **Use descriptive filenames**: `analyze-coverage.md` not `cov.md`
- **Set agent for specialized work**: Point analysis commands to `plan` agent (read-only)
- **Use subtask for expensive ops**: Keeps main context clean
- **Shell embedding for dynamic context**: `` !`git log` `` or `` !`npm test` `` makes commands reactive to current state
- **Combine $ARGUMENTS with !`cmd`**: `Analyze the output of !\`$1\`` for dynamic shell commands
- **Keep templates focused**: One command = one task
- **Check for shell injection**: User-provided `$ARGUMENTS` in shell commands needs caution
