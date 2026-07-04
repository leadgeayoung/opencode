# 11 — Permissions System

## 1. Overview

The `permission` config controls which actions require approval. Each rule resolves to one of three actions.

Since v1.1.1, the legacy `tools` boolean config is deprecated and merged into `permission`. The old `tools` config is still supported for backward compatibility.

## 2. Permission Actions

| Action | Behavior |
|--------|----------|
| `"allow"` | Run without approval |
| `"ask"` | Prompt for approval each time |
| `"deny"` | Block the action (tool not available) |

## 3. Configuration

### 3.1 Simple Global Set

```jsonc
{
  "permission": "allow"        // everything allowed
}
```

```jsonc
{
  "permission": {
    "*": "ask",                // all tools prompt
    "bash": "allow",           // except bash
    "edit": "deny"             // and edit is blocked
  }
}
```

### 3.2 Granular Rules (Object Syntax)

Use object with wildcard patterns for fine-grained control. Rules evaluated by pattern match; **last matching rule wins**.

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

**Common pattern**: Put catch-all `"*"` first, then specific rules. Last match wins.

### 3.3 Auto Mode

```bash
opencode --auto                            # auto-approve all non-denied
opencode run --auto "Refactor this module" # same for run command
```

- Only changes `ask` → auto-approve
- Explicit `deny` is still enforced
- Toggle in TUI: Command Palette → **Enable auto-approve permissions**
- When active, a muted `auto` indicator shows next to agent name

### 3.4 Environment Variable Override

```bash
export OPENCODE_PERMISSION='{"bash": "deny", "edit": "ask"}'
```

Inline JSON permissions override config file.

## 4. Wildcard Pattern Matching

| Pattern | Matches |
|---------|---------|
| `*` | Zero or more of any character |
| `?` | Exactly one character |
| `git *` | `git status`, `git commit -m "x"` (parsed command name + args) |
| `rm *` | `rm -rf /tmp` but NOT `echo rm` |
| `*.env` | `.env`, `.prod.env` |

### 4.1 Bash Command Parsing

Uses **tree-sitter** to parse bash commands. Matching operates on the parsed command name and arguments, not the raw string. This means:

- `"rm *"` matches `rm -rf /tmp` (command name is `rm`) but not `echo rm` (command name is `echo`)
- `"git *"` matches `git status` and `git commit -m "msg"` (command name is `git`)
- `"grep *"` matches `grep pattern file.txt` but not bare `grep` without arguments
- `"*"` matches every command

### 4.2 Home Directory Expansion

Patterns starting with `~` or `$HOME` are expanded:

- `~/projects/*` → `/Users/username/projects/*`
- `$HOME/projects/*` → `/Users/username/projects/*`
- `~` → `/Users/username`

## 5. Available Permissions (Complete)

| Key | Gated Tools | Granular? | Default |
|-----|-------------|-----------|---------|
| `read` | `read` | Yes (path patterns) | `allow` (but `.env` files denied) |
| `edit` | `write`, `edit`, `apply_patch` | Yes (path patterns) | `allow` |
| `glob` | `glob` | Yes (pattern patterns) | `allow` |
| `grep` | `grep` | Yes (pattern patterns) | `allow` |
| `list` | `list` (directory listing) | Yes (path patterns) | `allow` |
| `bash` | `bash` | Yes (parsed command patterns) | `allow` |
| `task` | `task` (subagent spawning) | Yes (subagent name patterns) | `allow` |
| `external_directory` | Any tool touching paths outside worktree | Yes (path patterns) | `ask` |
| `todowrite` | `todowrite`, `todoread` | No (shorthand only) | `allow` |
| `webfetch` | `webfetch` | Yes (URL patterns) | `allow` |
| `websearch` | `websearch` | Yes (query patterns) | `allow` |
| `lsp` | `lsp` (code intelligence queries) | Non-granular | `allow` |
| `skill` | `skill` (loading SKILL.md) | Yes (skill name patterns) | `allow` |
| `question` | `question` (AI asks user) | No (shorthand only) | `allow` |
| `doom_loop` | Recovery prompts when same tool called 3× with identical input | No (shorthand only) | `ask` |

**Granular permissions** accept either `"allow" | "ask" | "deny"` or an object `{ pattern: action, ... }`. **Non-granular** accept only the shorthand string.

### 5.1 Custom Tool & MCP Matching

Permission keys match wildcard patterns against the **tool name**, so the same mechanism covers built-ins, custom tools, and MCP tools:

```jsonc
{
  "permission": {
    "mymcp_*": "deny",         // deny every tool from "mymcp" MCP server
    "mymcp_search": "ask"      // except this one (last match wins)
  }
}
```

## 6. Default Permissions (When Unconfigured)

### 6.1 Global Defaults

```jsonc
{
  // Implicit defaults (unchanged):
  "permission": {
    "read":              "allow",
    "edit":              "allow",
    "glob":              "allow",
    "grep":              "allow",
    "list":              "allow",
    "bash":              "allow",
    "task":              "allow",
    "todowrite":         "allow",
    "webfetch":          "allow",
    "websearch":         "allow",
    "lsp":               "allow",
    "skill":             "allow",
    "question":          "allow",
    "external_directory": "ask",
    "doom_loop":         "ask"
  }
}
```

### 6.2 Read Default (with .env protection)

```jsonc
{
  "read": {
    "*": "allow",
    "*.env": "deny",
    "*.env.*": "deny",
    "*.env.example": "allow"
  }
}
```

`.env` files are denied by default. `.env.example` is explicitly allowed.

### 6.3 Plan Agent Default Permissions (from source)

The built-in **Plan** agent uses these defaults:

```jsonc
{
  "question": "allow",
  "edit": {
    "*": "deny",
    ".opencode/plans/*.md": "allow"
    // plus data dir: <opencode-data>/plans/*.md
  },
  "external_directory": {
    // <opencode-data>/plans/* is allowed
  }
}
```

Plan agent: read-only by default except plan files.

## 7. What "Ask" Does in the UI

When a permission prompts, the UI offers three outcomes:

| Choice | Effect |
|--------|--------|
| `once` | Approve this single request |
| `always` | Approve matching pattern for rest of session |
| `reject` | Deny the request |

The `always` patterns are suggested by the tool (e.g., bash approval may whitelist `git status*`).

### 7.1 Permission Dialog Shortcuts

| Key | Action |
|-----|--------|
| `y` | Allow (once) |
| `n` | Deny |
| `a` | Always allow (this session) |
| `Ctrl+F` | Toggle fullscreen permission prompt |

## 8. Per-Agent Permissions

Agent permissions **override** global permissions. Agent rules take precedence.

### 8.1 JSON Config

```jsonc
{
  "permission": {
    "bash": { "*": "ask", "git *": "allow", "git commit *": "deny", "git push *": "deny" }
  },
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
    },
    "plan": {
      "permission": {
        "edit": "deny"
      }
    }
  }
}
```

### 8.2 Markdown Agent Permissions

File: `~/.config/opencode/agents/review.md`

```markdown
---
description: Code review without edits
mode: subagent
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
    "grep *": allow
  webfetch: deny
---
Only analyze code and suggest changes.
```

### 8.3 Task Permissions (Subagent Control)

Control which subagents an agent can invoke via the Task tool:

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

- `deny` removes the subagent from the Task tool description entirely (model won't attempt it)
- `allow` permits invocation without prompting
- `ask` prompts before spawning the subagent
- Users can ALWAYS invoke any subagent manually via `@mention` regardless of task permissions

## 9. Legacy `tools` Config (Deprecated)

Auto-converts to permissions. Supported for backward compatibility.

```jsonc
{
  "tools": {
    "write": false,       // → edit: deny
    "bash": false,        // → bash: deny
    "webfetch": true,     // → webfetch: allow
    "read": true
  }
}
```

| tools value | Equivalent permission |
|-------------|----------------------|
| `true` | `{ "*": "allow" }` |
| `false` | `{ "*": "deny" }` |

Agent-level `tools` overrides global `tools`. Wildcards work too:

```jsonc
{
  "agent": {
    "readonly": {
      "tools": {
        "mymcp_*": false,     // deny all mymcp tools
        "write": false,
        "edit": false
      }
    }
  }
}
```

## 10. External Directory Permissions

Controls access to paths **outside** the project working directory. Affects any tool taking a path input: `read`, `edit`, `glob`, `grep`, `bash` commands touching external paths.

```jsonc
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow",
      "/shared/data": "allow"
    }
  }
}
```

- Home expansion (`~`) works for pattern writing but does NOT make the path part of the workspace
- Allowed directories inherit the same defaults as the workspace
- Add tool-specific restrictions on top:

```jsonc
{
  "permission": {
    "external_directory": { "~/projects/personal/**": "allow" },
    "edit": { "~/projects/personal/**": "deny" }    // read-only external
  }
}
```

Default: `"ask"` (prompts when tools touch paths outside worktree).

## 11. Permissions Cheatsheet

| Goal | Config |
|------|--------|
| Approve nothing | `"permission": "deny"` |
| Approve everything | `"permission": "allow"` |
| Block all edits | `{ "edit": "deny" }` |
| Block all bash | `{ "bash": "deny" }` |
| Block dangerous commands | `{ "bash": { "*": "allow", "rm *": "deny" } }` |
| Only allow git | `{ "bash": { "*": "deny", "git *": "allow" } }` |
| Allow git, block push | `{ "bash": { "*": "ask", "git *": "allow", "git push *": "deny" } }` |
| Read-only agent | `{ "edit": "deny", "bash": "deny" }` |
| Only allow plan edits | `{ "edit": { "*": "deny", ".opencode/plans/*.md": "allow" } }` |
| Allow external dirs | `{ "external_directory": { "/path": "allow" } }` |
| Limit subagents | `{ "task": { "*": "deny", "explore": "allow" } }` |
| MCP tool control | `{ "mymcp_*": "deny" }` |
| Disable doom_loop | `{ "doom_loop": "allow" }` |
