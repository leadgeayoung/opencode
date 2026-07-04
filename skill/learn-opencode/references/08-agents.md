# 08 — Agents

## 1. Architecture & Types

### Agent Types

| Type | Invoke | Description |
|------|--------|-------------|
| **Primary** | Tab (cycle) | Direct conversation; handles Build/Plan modes |
| **Subagent** | `@name` | Expert invoked by Primary or manually via `@` |
| **All** | Tab + `@` | Can be both primary and subagent |

### Built-in Agents

| Agent | Mode | Role |
|-------|------|------|
| **Build** | Primary (default) | Full tool access; standard development |
| **Plan** | Primary | Restricted (edit+bash = `ask`); analysis/planning only |
| **General** | Subagent | Multi-step tasks, full tools except todowrite |
| **Explore** | Subagent | Read-only codebase exploration |
| **Scout** | Subagent | External docs + dependency research (read-only); clones repos to managed cache |
| **Compaction** | Primary (hidden) | Auto-compacts long context |
| **Title** | Primary (hidden) | Auto-generates session titles |
| **Summary** | Primary (hidden) | Auto-creates session summaries |

### Subagent Execution Mechanism (CRITICAL)

1. **Session Isolation** — runs in a NEW independent Session (child session)
2. **No historical memory** — cannot see the Primary's conversation history
3. **Context = only Prompt** — the AI's world is only the task description passed to it
4. **All mode dual identity** — Tab=Primary (has history), @=Subagent (no history)
5. **Child session navigation**: `<Leader>+Down` enters first child; `Right`/`Left` cycles children; `Up` returns to parent

### How Subagents Are Invoked

- **Automatically** — Primary agent's Task tool spawns subagents based on their descriptions
- **Manually** — `@agent-name` in user message
- **Users can always `@` any subagent**, even if task permissions deny it

---

## 2. Configuration

### Location & Priority

| Location | Scope | Priority |
|----------|-------|----------|
| `.opencode/agent/*.md` | Project | High |
| `~/.config/opencode/agent/*.md` | Global | Medium |
| `agent` field in `opencode.json` | Depends | Merged (JSON overrides same-named fields in .md) |

**Naming rule**: filename = agent name. `docs-writer.md` → `@docs-writer`

### JSON Configuration (`opencode.json`)

```jsonc
{
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "{file:./prompts/build.txt}",
      "permission": { "edit": "allow", "bash": "allow" }
    },
    "plan": {
      "mode": "primary",
      "model": "anthropic/claude-haiku-4-20250514",
      "permission": { "edit": "deny", "bash": "deny" }
    },
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0.2,
      "steps": 30,
      "color": "#4CAF50",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "permission": { "edit": "deny" }
    }
  }
}
```

### Markdown Configuration (`agents/<name>.md`)

**File location**: `.opencode/agent/` (project) or `~/.config/opencode/agent/` (global)

```yaml
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash: deny
---

You are in code review mode. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations
```

### Frontmatter Fields (Markdown) / JSON Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `description` | string | — | Summary for auto-selection; **required** |
| `mode` | enum | `all` | `subagent` / `primary` / `all` |
| `model` | string | Inherits | `provider/model`. Empty = Primary's model (subagent) or global model (primary) |
| `prompt` | string | Built-in | System prompt (body text in Markdown; `{file:./path.txt}` in JSON) |
| `temperature` | number | Model default (0 for most, 0.55 for Qwen) | 0.0–1.0 |
| `top_p` | number | — | 0.0–1.0; alternative to temperature |
| `steps` | number | Unlimited | Max iterations (replaces deprecated `maxSteps`) |
| `hidden` | boolean | `false` | Hide from `@` menu (subagent only) |
| `color` | string | — | Hex `#RRGGBB` or theme color (`primary`, `secondary`, `accent`, `success`, `warning`, `error`, `info`) |
| `permission` | object | — | Permission rules |
| `disable` | boolean | `false` | Disable the agent |
| `options` | object | — | Pass-through parameters to Provider |

### Merge Rules

- **JSON overrides** same-named fields in `.md` (best practice: use `.md` for prompt body, `opencode.json` for parameters)
- **External prompt file**: `"prompt": "{file:./prompts/code-reviewer.txt}"` (relative to config file)
- Agent permissions merge with global config; agent rules take precedence

### CLI Agent Creation

```bash
opencode agent create
```

Interactive steps:
1. Choose location: global or project-specific
2. Enter description
3. AI generates system prompt + identifier
4. Select allowed permissions (everything else denied)
5. Markdown file created

---

## 3. Permissions System

### Actions

| Action | Effect |
|--------|--------|
| `"allow"` | Run without approval |
| `"ask"` | Prompt for approval |
| `"deny"` | Block the action |

### Permission Scopes

| Key | Gates | Granular? |
|-----|-------|-----------|
| `read` | `read` | Yes (path patterns) |
| `edit` | `write`, `edit`, `apply_patch` | Yes (path patterns) |
| `glob` | `glob` | Yes (pattern patterns) |
| `grep` | `grep` | Yes (regex patterns) |
| `bash` | `bash` | Yes (command patterns) |
| `task` | `task` (subagent invocation) | Yes (agent name patterns) |
| `skill` | `skill` (loading SKILL.md) | Yes (skill name patterns) |
| `lsp` | `lsp` (experimental) | Non-granular |
| `question` | `question` | Non-granular |
| `webfetch` | `webfetch` | Non-granular |
| `websearch` | `websearch` | Non-granular |
| `todowrite` | `todowrite`, `todoread` | Non-granular |
| `external_directory` | Paths outside project worktree | Yes (path patterns) |
| `doom_loop` | Same tool call repeated 3× | Non-granular |

### Default Permissions

- Most tools: `"allow"`
- `doom_loop`: `"ask"`
- `external_directory`: `"ask"`
- `read`: `"allow"` but `.env` files denied:

```jsonc
{
  "permission": {
    "read": {
      "*": "allow",
      "*.env": "deny",
      "*.env.*": "deny",
      "*.env.example": "allow"
    }
  }
}
```

### Granular Rule Syntax (Object Form)

For `read`, `edit`, `glob`, `grep`, `bash`, `task`, `skill`, `external_directory`:

```jsonc
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny",
      "grep *": "allow"
    },
    "edit": {
      "*": "deny",
      "packages/web/src/content/docs/*.mdx": "allow"
    }
  }
}
```

**Wildcards**: `*` = zero or more chars, `?` = exactly one char

**Evaluation**: last matching rule wins. Put `"*"` first, specifics after.

### Pattern Matching for Bash Commands

- Uses tree-sitter for parsing (command name + arguments)
- `"grep"` matches bare `grep`; `"grep *"` matches `grep pattern file.txt`
- `"git status"` works for default; `"git status *"` needed with arguments

### External Directory Permissions

Allow tool calls touching paths outside the project working directory:

```jsonc
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    }
  }
}
```

Home directory expansion: `~` or `$HOME` supported. Inherits workspace defaults; layer extra rules to restrict:

```jsonc
{
  "permission": {
    "external_directory": { "~/projects/personal/**": "allow" },
    "edit": { "~/projects/personal/**": "deny" }
  }
}
```

### Auto Mode

```bash
opencode --auto
opencode run --auto "Refactor this module"
```

- Auto-approves requests that would normally `ask`
- Explicit `"deny"` rules still enforced
- Toggle in TUI: command palette → Enable/Disable auto-approve permissions
- When active, prompt shows muted `auto` indicator

### "Ask" UI Outcomes

| Choice | Effect |
|--------|--------|
| `once` | Approve just this request |
| `always` | Approve matching requests for rest of session |
| `reject` | Deny the request |

### Permission in Agent Config (JSON)

```jsonc
{
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git *": "allow",
          "git commit *": "ask",
          "git push *": "deny",
          "grep *": "allow"
        }
      }
    }
  }
}
```

### Permission in Agent Config (Markdown)

```yaml
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
    "grep *": allow
```

### Task Permissions (Subagent Access Control)

Control which subagents an agent can invoke via Task tool:

```jsonc
{
  "agent": {
    "orchestrator": {
      "mode": "primary",
      "permission": {
        "task": {
          "*": "deny",
          "orchestrator-*": "allow",
          "code-reviewer": "ask"
        }
      }
    }
  }
}
```

- `"deny"` removes subagent from Task tool description (model won't attempt)
- Last matching rule wins
- Users can always `@` any subagent directly despite task permissions

### Wildcard Permission Matching for Tools

Permission keys match tool names via wildcards — works for built-ins, custom tools, and MCP:

```jsonc
{
  "permission": {
    "mymcp_*": "deny",
    "mymcp_search": "ask"
  }
}
```

### Legacy `tools` Config (Deprecated)

```jsonc
{
  "tools": { "write": true, "bash": true },
  "agent": {
    "plan": {
      "tools": { "write": false, "bash": false }
    }
  }
}
```

`true` = `{"*": "allow"}`, `false` = `{"*": "deny"}`. Use `permission` instead.

---

## 4. Temperature Guide

| Range | Use Case |
|-------|----------|
| 0.0–0.2 | Code analysis, planning, deterministic tasks |
| 0.3–0.5 | General development, balanced |
| 0.6–1.0 | Brainstorming, creative, exploration |

Model defaults: 0 for most models, 0.55 for Qwen models.

---

## 5. Five Workflow Design Patterns

### Pattern 1: Prompt Chaining

Sequential steps where each output feeds the next. Good for tasks decomposable into fixed subtrades. Trade latency for accuracy.

Example: Translate → Polish → Format

```text
Step 1: Translate source to target language
Step 2: Polish the translation for native fluency
Step 3: Format according to style guide
```

### Pattern 2: Routing

Classify input, then route to specialized processing.

Example: Code issue classifier:
- `bug` → `@bug-fixer`
- `performance` → `@optimizer`
- `security` → `@auditor`

### Pattern 3: Parallelization

Execute multiple independent tasks simultaneously, aggregate results.

- **Sectioning**: independent subtasks (e.g., lint + security + style simultaneously)
- **Voting**: same task from multiple perspectives (e.g., multiple code quality checks)

### Pattern 4: Orchestrator-Worker

Orchestrator delegates subtasks to workers, synthesizes results.

Example: PR Review
1. Analyze changes
2. `@code-reviewer` for code quality
3. `@test-writer` for test coverage
4. Synthesize final review

### Pattern 5: Evaluator-Optimizer

Generate → Evaluate → Iterate.

Example: Report generation with quality loop
1. Draft report
2. Validate against criteria
3. Fix issues
4. Re-validate

### Core Design Principles

1. **Keep it simple** — avoid unnecessary complexity
2. **Transparency first** — make agent decision paths visible
3. **Carefully design ACI** — Agent-Computer Interface (tool descriptions)

---

## 6. Tool Interface Design (ACI)

- Tool descriptions should be like excellent docstrings for junior developers
- Include usage examples and edge cases
- Avoid formats requiring precise counting or complex escaping
- Use clear parameter names with types and defaults

---

## 7. Passthrough Parameters

Unknown fields in Agent config are passed through directly to the Provider:

```jsonc
{
  "agent": {
    "deep-thinker": {
      "description": "Agent that uses high reasoning effort",
      "model": "openai/gpt-5",
      "reasoningEffort": "high",
      "textVerbosity": "low"
    }
  }
}
```

Examples: `reasoningEffort`, `textVerbosity`, `reasoningSummary` — model/provider-specific.

---

## 8. Agent Skills

### Location Discovery

| Path | Scope |
|------|-------|
| `.opencode/skills/<name>/SKILL.md` | Project |
| `~/.config/opencode/skills/<name>/SKILL.md` | Global |
| `.claude/skills/<name>/SKILL.md` | Project (Claude compat) |
| `~/.claude/skills/<name>/SKILL.md` | Global (Claude compat) |

### SKILL.md Frontmatter

```yaml
---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---
```

- `name` (required): 1–64 chars, lowercase alphanumeric + hyphens, regex `^[a-z0-9]+(-[a-z0-9]+)*$`
- `description` (required): 1–1024 chars
- Loaded on-demand via `skill({ name: "..." })` tool

### Skill Permissions

```jsonc
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

Per-agent override in frontmatter:

```yaml
permission:
  skill:
    "documents-*": "allow"
```

---

## 9. Debugging Agents

- **Test with specific inputs** — narrow, focused test cases
- **Check token usage** — `/stats`, `opencode stats`
- **Review tool call sequences** — `/details` toggles execution details
- **Configuration diagnostics** — `opencode debug`

### Useful Commands

```bash
opencode agent create          # Interactive agent creation
opencode debug                 # Config diagnostics
opencode models                # List available models
opencode models --refresh      # Refresh model cache
opencode stats --days 30       # Usage statistics
opencode export [sessionID]    # Export session as JSON
opencode session list          # List all sessions
```

### Environment Variables

| Variable | Effect |
|----------|--------|
| `OPENCODE_EXPERIMENTAL=true` | Master experimental switch |
| `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true` | Background subagent tasks |
| `OPENCODE_DISABLE_CLAUDE_CODE=1` | Disable Claude compat |
| `OPENCODE_DISABLE_AUTOCOMPACT=true` | Disable auto-compaction |

---

## 10. Complete Working Examples

### Code Reviewer Agent (Markdown)

`~/.config/opencode/agents/code-reviewer.md`:

```yaml
---
description: Reviews code for best practices and potential issues
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
    "grep *": allow
  webfetch: deny
---

You are a code reviewer. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations

Provide constructive feedback without making direct changes.
```

### Security Auditor Agent (Markdown)

```yaml
---
description: Performs security audits and identifies vulnerabilities
mode: subagent
permission:
  edit: deny
---

You are a security expert. Focus on identifying potential security issues.
Look for:
- Input validation vulnerabilities
- Authentication and authorization flaws
- Data exposure risks
- Dependency vulnerabilities
- Configuration security issues
```

### Documentation Writer Agent (Markdown)

```yaml
---
description: Writes and maintains project documentation
mode: subagent
permission:
  bash: deny
---

You are a technical writer. Create clear, comprehensive documentation.
Focus on:
- Clear explanations
- Proper structure
- Code examples
- User-friendly language
```

### Quick Thinker with Step Limit (JSON)

```jsonc
{
  "agent": {
    "quick-thinker": {
      "description": "Fast reasoning with limited iterations",
      "mode": "subagent",
      "steps": 5,
      "temperature": 0.1,
      "prompt": "You are a quick thinker. Solve problems with minimal steps."
    }
  }
}
```

### Orchestrator with Task Permissions (JSON)

```jsonc
{
  "agent": {
    "orchestrator": {
      "mode": "primary",
      "permission": {
        "task": {
          "*": "deny",
          "orchestrator-*": "allow",
          "code-reviewer": "ask",
          "test-writer": "allow"
        }
      },
      "prompt": "You are a project orchestrator. Decompose work into subagent tasks."
    }
  }
}
```

---

## 11. Quick Reference

### Permission Pattern Wildcards

| Pattern | Matches |
|---------|---------|
| `*` | Everything |
| `git *` | All git commands |
| `git status *` | Git status with args |
| `mymcp_*` | All tools from mymcp server |
| `orchestrator-*` | All agents with prefix |
| `*.env` | All .env files |
| `~/projects/**` | Home-expanded path |

### Keybindings for Agent Navigation

| Binding | Action |
|---------|--------|
| Tab | Cycle primary agents |
| `Shift+Tab` | Reverse cycle |
| `Ctrl+X A` | Agent list |
| `<Leader>+Down` | Enter first child session |
| `Right` | Next child session |
| `Left` | Previous child session |
| `Up` | Return to parent session |

### Config File Paths Quick Reference

| Purpose | Path |
|---------|------|
| Project agents | `.opencode/agent/*.md` |
| Global agents | `~/.config/opencode/agent/*.md` |
| Project config | `./opencode.json` |
| Global config | `~/.config/opencode/opencode.json` |
| Project skills | `.opencode/skills/*/SKILL.md` |
| Global skills | `~/.config/opencode/skills/*/SKILL.md` |
| Project rules | `./AGENTS.md` |
| Global rules | `~/.config/opencode/AGENTS.md` |
