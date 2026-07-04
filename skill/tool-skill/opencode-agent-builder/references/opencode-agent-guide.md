# opencode Agent Quick Reference

## Agent Types

| Type | Invoke | Behavior |
|------|--------|----------|
| **Primary** | Tab (cycle) | Full conversation history, direct user interaction |
| **Subagent** | `@name` | Session Isolation — no parent history, spawned via Task tool or manually |
| **All** | Tab + `@` | Tab=Primary (has history), `@`=Subagent (no history) |

## Config Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `description` | string | — | Summary for auto-selection; required |
| `mode` | enum | `all` | `subagent` / `primary` / `all` |
| `model` | string | Inherits | `provider/model`. Empty = inherit |
| `prompt` | string | Built-in | System prompt (body in Markdown; `{file:./path.txt}` in JSON) |
| `temperature` | number | Model default | 0.0–1.0 |
| `top_p` | number | — | Alternative to temperature |
| `steps` | number | Unlimited | Max iterations |
| `hidden` | boolean | `false` | Hide from `@` menu (subagent only) |
| `color` | string | — | Hex `#RRGGBB` or theme color |
| `permission` | object | — | Tool permission rules |
| `disable` | boolean | `false` | Disable the agent |
| `options` | object | — | Pass-through to Provider |

## Config File Paths

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

## 5 Design Patterns

| Pattern | When | How |
|---------|------|-----|
| Prompt Chaining | Fixed sequential steps | Chain subagents or define steps in prompt |
| Routing | Classify → dispatch | Primary classifies, delegates via Task tool |
| Parallelization | Independent subtasks | Spawn multiple subagents concurrently |
| Orchestrator-Worker | Complex → decompose | Orchestrator primary + worker subagents |
| Evaluator-Optimizer | Iterative refinement | Generate → evaluate → fix loop |

## Permission Scopes

| Scope | Gates | Granularity |
|-------|-------|-------------|
| `read` | `read` tool | Path patterns |
| `edit` | `write`, `edit`, `apply_patch` | Path patterns |
| `glob` | `glob` tool | Pattern patterns |
| `grep` | `grep` tool | Regex patterns |
| `bash` | `bash` tool | Command patterns |
| `task` | Subagent invocation | Agent name patterns |
| `skill` | Skill loading | Skill name patterns |
| `external_directory` | Outside project | Path patterns |

## Temperature Guide

| Range | Use Case |
|-------|----------|
| 0.0–0.2 | Code analysis, planning, deterministic tasks |
| 0.3–0.5 | General development, balanced |
| 0.6–1.0 | Brainstorming, creative, exploration |

## Debug Commands

```bash
opencode agent create     # Interactive agent creation
opencode debug            # Config diagnostics
opencode models           # List available models
opencode stats --days 30  # Usage statistics
opencode session list     # List all sessions
```

## Subagent Auto-Selection

1. Primary agent's Task tool lists available subagents based on `task` permission
2. Model evaluates task semantics against each subagent's `description`
3. On match, spawns subagent in isolated child session
4. Subagent completes work, returns summary to primary
5. Primary continues with result in context
