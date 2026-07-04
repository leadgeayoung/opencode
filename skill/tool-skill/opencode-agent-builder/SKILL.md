---
name: opencode-agent-builder
description: |
  Design and build AI agents within the opencode ecosystem. Covers primary/subagent/all-mode agents, permission systems, workflow patterns, and skill-based knowledge injection.
  Provides: opencode agent configuration templates (JSON + Markdown), subagent type patterns, 5 workflow design patterns (Prompt Chaining, Routing, Parallelization, Orchestrator-Worker, Evaluator-Optimizer), ACI design principles, permission granularity guides.
  Suitable for: creating custom agents with specific tool permissions, designing multi-agent orchestration, building domain-specialized subagents (code review, research, docs), injecting expertise via skills, configuring primary agent behavior.
  Not suitable for: MCP server configuration, writing AGENTS.md project rules, general coding tasks without agent creation, modifying opencode built-in agent internals.
compatibility: opencode
user-invocable: true
---

# opencode Agent Builder

Build AI agents within the opencode ecosystem. When a user asks to "create an agent", "build an assistant", or "design an AI system", follow this workflow.

## 1. Architecture Overview

| Concept | Description |
|---------|-------------|
| **Primary** | Tab-cycled agents with full conversation history. Default: Build (full tools), Plan (restricted) |
| **Subagent** | `@name`-invoked experts. Session Isolation — no access to parent's history. Auto-selected by Task tool based on `description` |
| **All** | Dual identity: Tab=Primary (has history), `@`=Subagent (no history) |
| **Session Isolation** | Subagents run in independent child sessions with zero memory of parent context |
| **Task tool** | Primary's mechanism to spawn subagents. Description field drives automatic selection |

### Built-in Agents (reference)

| Agent | Mode | Role |
|-------|------|------|
| Build | Primary (default) | Full tool access, standard development |
| Plan | Primary | edit+bash = ask, analysis/planning only |
| General | Subagent | Multi-step tasks, full tools except todowrite |
| Explore | Subagent | Read-only codebase exploration |
| Scout | Subagent | External docs + dependency research (read-only) |

## 2. Five Design Patterns

Match the user's task to the appropriate pattern:

### Pattern 1: Prompt Chaining

**When**: Fixed sequential steps, each output feeds the next.

Example: Translate → Polish → Format

Implementation: Define steps in agent prompt, or chain subagents sequentially.

### Pattern 2: Routing

**When**: Classify input then dispatch to specialized processing.

Example:
- `bug` → `@bug-fixer`
- `performance` → `@optimizer`
- `security` → `@auditor`

Implementation: Primary agent classifies and delegates via Task tool to appropriate subagent.

### Pattern 3: Parallelization

**When**: Multiple independent tasks execute simultaneously.

Example: Lint + security scan + style check running in parallel.

Implementation: Primary spawns multiple subagents concurrently via Task tool, aggregates results.

### Pattern 4: Orchestrator-Worker

**When**: Complex task decomposable into subtasks with a central coordinator.

Example: PR review — orchestrator delegates to `@code-reviewer` + `@test-writer`, synthesizes final review.

Implementation: Orchestrator primary agent with `task` permission controlling which subagents are visible.

### Pattern 5: Evaluator-Optimizer

**When**: Output quality requires iterative refinement.

Example: Draft → Evaluate → Fix → Re-validate.

Implementation: Generation loop with quality gates. Use `steps` field to limit iterations.

## 3. Configuration Decision Tree

```
User needs → Which configuration method?

Just project-level rules?
  └── AGENTS.md

Single specialized tool?
  └── Subagent: .opencode/agent/<name>.md

Replace default Build/Plan behavior?
  └── Custom Primary: opencode.jsonc agent field

Multi-agent collaboration?
  └── Orchestrator + Workers: JSON + Markdown hybrid

Domain expertise needed?
  └── Skill injection: skill/<name>/SKILL.md

Not sure where to start?
  └── opencode agent create (interactive CLI)
```

### CLI Quick Start

```bash
opencode agent create
# 1. Choose location: global (~/.config/opencode/agent/) or project (.opencode/agent/)
# 2. Enter description
# 3. AI generates system prompt + identifier
# 4. Select allowed permissions
# 5. Markdown file created
```

### Configuration Methods Detail

**Markdown config** (`.opencode/agent/<name>.md` or `~/.config/opencode/agent/<name>.md`):

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

**JSON config** (`opencode.jsonc`):

```jsonc
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for quality issues",
      "mode": "subagent",
      "temperature": 0.2,
      "steps": 30,
      "color": "#4CAF50",
      "prompt": "You are a code reviewer...",
      "permission": { "edit": "deny" }
    }
  }
}
```

**Hybrid**: Use Markdown for prompt body, JSON for parameters. JSON overrides same-named fields in `.md`.

## 4. Design Patterns in Detail

### 4a. Custom Subagent

**Best for**: Single-domain experts (code review, security audit, docs, research).

Key design decisions:
- `description` drives Task tool auto-selection — be specific, not generic
- `mode: subagent` — invoked via `@name` or Task tool
- Permission: start strict, relax as needed
- `temperature`: 0.0–0.2 for deterministic tasks, 0.3–0.5 for balanced, 0.6–1.0 for creative

Complete examples:

```yaml
# Security Auditor
---
description: Performs security audits and identifies vulnerabilities
mode: subagent
permission:
  edit: deny
---
You are a security expert. Focus on:
- Input validation vulnerabilities
- Authentication and authorization flaws
- Data exposure risks
- Dependency vulnerabilities
```

```yaml
# Documentation Writer
---
description: Writes and maintains project documentation
mode: subagent
permission:
  bash: deny
---
You are a technical writer. Create clear, comprehensive documentation.
Focus on: clear explanations, proper structure, code examples.
```

```yaml
# Quick Thinker (limited iterations)
---
description: Fast reasoning with minimal steps
mode: subagent
steps: 5
temperature: 0.1
---
You are a quick thinker. Solve problems with minimal steps.
```

### 4b. Custom Primary Agent

**Best for**: Replacing default Build/Plan with customized behavior.

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
    }
  }
}
```

Multiple primary agents are cycled via Tab / Shift+Tab.

### 4c. Orchestrator + Workers

**Best for**: Complex multi-step workflows.

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

Key: `task` permission controls which subagents are visible to the orchestrator. `"deny"` removes them from Task tool description entirely.

### 4d. Knowledge Injection via Skills

**Best for**: Domain expertise that's reusable across projects.

See the full opencode skill system reference: `references/opencode-agent-guide.md`

## 5. Permission System Design

### Three Actions

| Action | Effect |
|--------|--------|
| `"allow"` | Run without approval |
| `"ask"` | Prompt for approval |
| `"deny"` | Block completely |

### Permission Scopes

| Scope | Gates | Granular? |
|-------|-------|-----------|
| `read` | `read` tool | Path patterns |
| `edit` | `write`, `edit`, `apply_patch` | Path patterns |
| `bash` | `bash` tool | Command patterns |
| `task` | Subagent invocation via Task tool | Agent name patterns |
| `skill` | Loading SKILL.md | Skill name patterns |
| `external_directory` | Paths outside project worktree | Path patterns |
| `glob`, `grep`, `webfetch`, `websearch`, `todowrite`, `lsp`, `question`, `doom_loop` | Respective tools | Various |

### Granular Rules Design

Derive permissions from "what can this agent do?":

```
Read-only agent       → edit: deny, bash: deny
Code reviewer         → edit: deny, bash: "git diff" + "git log*" + "grep *" allow
Full development      → default allow, "rm *": deny, "sudo *": deny
Documentation writer  → bash: deny, edit: allow (restrict to docs/ path)
```

Granular syntax (last matching rule wins):

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

### Wildcard Reference

| Pattern | Matches |
|---------|---------|
| `*` | Everything |
| `git *` | All git commands |
| `git status *` | Git status with args |
| `mymcp_*` | All tools from mymcp server |
| `orchestrator-*` | All agents with prefix |
| `*.env` | All .env files |

## 6. ACI Design (Agent-Computer Interface)

Tool descriptions are the agent's window into capabilities. Design them well:

- Write like excellent docstrings for a junior developer
- Include usage examples and edge cases
- Avoid formats requiring precise counting or complex escaping
- Use clear parameter names with types and defaults
- Test descriptions by asking: "would the model know when to use this?"

## Design Principles

1. **Keep it simple** — avoid unnecessary complexity
2. **Transparency first** — make agent decision paths visible
3. **ACI carefully** — tool descriptions determine success
4. **Start strict, relax** — easier to open permissions than close them
5. **Let the model reason** — don't hardcode workflows

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Permission too loose | Risk of destructive actions | Start strict, relax based on real needs |
| Permission too tight | Agent can't complete tasks | Analyze failure and add necessary permissions |
| Vague description | Subagent never auto-selected | Be specific about scenarios and capabilities |
| No step limit | Agent loops indefinitely | Set `steps` based on task complexity |
| Over-engineering | Complexity before need | Start with `opencode agent create`, iterate |

## Reference Reading

Loaded on demand when needed:

**opencode-specific reference**:
- `references/opencode-agent-guide.md` — Agent type quick reference, all config fields, 5 design patterns, permission scopes, config paths

**General agent design philosophy** (background context):
- `references/agent-philosophy.md` — Deep dive: the model IS the agent, code is the harness

**General agent implementation patterns** (conceptual reference):
- `references/minimal-agent.py` — Minimal working agent (~80 lines, Python/Anthropic SDK)
- `references/tool-templates.py` — Tool definition and implementation templates
- `references/subagent-pattern.py` — Context isolation via subagent pattern
