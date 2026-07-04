# OpenCode Configuration — Complete Reference

Config files use JSON or JSONC (JSON with Comments). Schema: `https://opencode.ai/config.json`. TUI settings use `tui.json` (schema: `https://opencode.ai/tui.json`).

---

## Configuration File Locations (8-level priority, low→high)

Configs **merge**, not replace. Later sources override earlier ones on conflicting keys; non-conflicting keys from all sources are preserved.

| # | Source | Path / Mechanism | Scope |
|---|---|---|---|
| 1 | **Remote** | `/.well-known/opencode` (fetched on auth) | Organizational defaults |
| 2 | **Global** | `~/.config/opencode/opencode.json` | User preferences |
| 3 | **Custom path** | `$OPENCODE_CONFIG` env var | Custom override |
| 4 | **Project root** | `./opencode.json` (or traversing up to nearest Git dir) | Project-specific |
| 5 | **`.opencode/` dir** | `./.opencode/opencode.json` + subdirs | Project plugins/agents/skills |
| 6 | **Custom dir** | `$OPENCODE_CONFIG_DIR` env var (same subdir structure as `.opencode/`) | Custom directory override |
| 7 | **Inline** | `$OPENCODE_CONFIG_CONTENT` env var (raw JSON string) | Runtime override |
| 8 | **Managed** (admin) | macOS: `/Library/Application Support/opencode/` — Linux: `/etc/opencode/` — Windows: `%ProgramData%\opencode` | Enforced, not user-overridable |
| — | **macOS MDM** | `.mobileconfig` via `ai.opencode.managed` preference domain | Highest priority, cannot be overridden |

### Managed macOS `.mobileconfig` Example

```xml
<dict>
  <key>PayloadType</key>
  <string>ai.opencode.managed</string>
  <key>share</key>
  <string>disabled</string>
  <key>permission</key>
  <dict>
    <key>*</key>
    <string>ask</string>
  </dict>
</dict>
```

### Directory Structure (`~/.config/opencode/`)

```
~/.config/opencode/
├── opencode.json / opencode.jsonc   # Main config
├── tui.json / tui.jsonc             # TUI-specific config
├── AGENTS.md                        # Global rules/instructions
├── agent/                           # Agent definitions (Markdown)
├── agents/                          # Plural also supported
├── command/                         # Command definitions (Markdown)
├── commands/                        # Plural also supported
├── plugin/                          # Local plugin files
├── plugins/                         # Plural also supported
├── skill/                           # Skills
├── skills/                          # Plural also supported
├── tool/                            # Custom tools
├── tools/                           # Plural also supported
├── theme/                           # Custom themes
└── themes/                          # Plural also supported
```

---

## Common Mistakes: Correct vs Wrong Key Names

| Correct | Wrong (will be ignored) |
|---------|------------------------|
| `provider` | `providers` |
| `permission` | `permissions` |
| `agent` | `agents` |
| `command` | `commands` |
| `formatter` | `formatters` |
| `keybinds` | `keybind` |
| `small_model` | `smallmodel`, `small-model` |
| `default_agent` | `defaultAgent` |
| `disabled_providers` | `disabledProviders` |
| `enabled_providers` | `enabledProviders` |
| `autoupdate` | `autoUpdate`, `auto_update` |

---

## Complete Config Key Reference

### Top-Level Keys

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `$schema` | string | — | JSON schema URL for validation |
| `model` | string | — | Default model: `provider/model` (e.g. `anthropic/claude-sonnet-4-5`) |
| `small_model` | string | falls back to `model` | Cheap model for lightweight tasks (title gen, etc.) |
| `default_agent` | string | `"build"` | Default primary agent. Must be a primary agent; falls back to `"build"` if invalid. |
| `shell` | string | auto-detected | Default shell (`pwsh`, `cmd.exe`, `/bin/zsh`, `/bin/bash`, or absolute path) |
| `logLevel` | string | `"INFO"` | One of: `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `username` | string | system username | Custom display name in conversations |
| `share` | string | `"manual"` | `"manual"` \| `"auto"` \| `"disabled"` |
| `autoupdate` | bool / string | `true` | `true` \| `false` \| `"notify"` |
| `snapshot` | bool | `true` | Enable file-change snapshots for undo/redo |
| `mode` | object | — | **Deprecated.** Use `agent` instead. |
| `autoshare` | bool | — | **Deprecated.** Use `share` instead. |

---

### `provider` — Provider Configuration

| Sub-key | Type | Description |
|---------|------|-------------|
| `{providerId}.options.apiKey` | string | API key, supports `{env:VAR}` / `{file:path}` |
| `{providerId}.options.baseURL` | string | Custom API base URL |
| `{providerId}.options.timeout` | int \| false | Request timeout in ms (default: `300000`). `false` to disable. |
| `{providerId}.options.headerTimeout` | int \| false | Header response timeout in ms. `false` to disable. |
| `{providerId}.options.chunkTimeout` | int | Timeout between streamed SSE chunks |
| `{providerId}.options.setCacheKey` | bool | Enable prompt cache key (default: `false`) |
| `{providerId}.options.enterpriseUrl` | string | GitHub Enterprise URL (for Copilot auth) |
| `{providerId}.options.headers` | object | Custom HTTP headers (`{ "Header-Name": "value" }`) |
| `{providerId}.whitelist` | string[] | Only these model IDs appear in picker |
| `{providerId}.blacklist` | string[] | Hide these model IDs from picker |
| `{providerId}.npm` | string | AI SDK package (e.g. `@ai-sdk/openai-compatible`) |
| `{providerId}.name` | string | Display name in UI |
| `{providerId}.models` | object | Model-specific overrides (see below) |

#### Provider-Specific: Amazon Bedrock Options

| Option | Type | Description |
|--------|------|-------------|
| `region` | string | AWS region (e.g. `us-east-1`) |
| `profile` | string | AWS named profile from `~/.aws/credentials` |
| `endpoint` | string | VPC endpoint URL (alias for `baseURL`; takes precedence) |

#### `provider.{id}.models.{modelId}` — Model-Level Config

| Sub-key | Type | Description |
|---------|------|-------------|
| `id` | string | Override model ID (e.g. custom ARN for Bedrock) |
| `name` | string | Display name |
| `options` | object | Model-specific options (passed to provider) |
| `variants` | object | Custom variant definitions |
| `variants.{name}.disabled` | bool | Disable this variant |
| `provider.api` | string | Per-model custom API URL (v1.1.60+) |
| `provider.npm` | string | Per-model custom SDK package |
| `limit.context` | int | Max context tokens |
| `limit.input` | int | Max input tokens |
| `limit.output` | int | Max output tokens |
| `cost.input` | number | Per-token input cost |
| `cost.output` | number | Per-token output cost |
| `cost.cache_read` | number | Cache read cost |
| `cost.cache_write` | number | Cache write cost |
| `modalities.input` | string[] | e.g. `["text", "image"]` |
| `modalities.output` | string[] | e.g. `["text"]` |
| `status` | string | `"alpha"` \| `"beta"` \| `"deprecated"` \| `"active"` |
| `headers` | object | Custom headers for this model |

#### Variants

| Model | Built-in Variants |
|-------|-------------------|
| Anthropic | `high` (default, high thinking budget), `max` (maximum thinking budget) |
| OpenAI | `none`, `minimal`, `low`, `medium`, `high`, `xhigh` |
| Google | `low`, `high` |

Custom variants in config:
```jsonc
{ "provider": { "openai": { "models": { "gpt-5": { "variants": {
  "thinking": { "reasoningEffort": "high", "textVerbosity": "low" },
  "fast": { "disabled": true }
}}}}}}
```

---

### `disabled_providers` / `enabled_providers`

| Key | Type | Description |
|-----|------|-------------|
| `disabled_providers` | string[] | Providers to never load (higher priority than `enabled_providers`) |
| `enabled_providers` | string[] | Only these providers are loaded; all others ignored |

Example:
```json
{ "disabled_providers": ["openai", "gemini"], "enabled_providers": ["anthropic"] }
```

---

### `server` — Server Config

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `port` | int | `4096` | Listen port |
| `hostname` | string | `"0.0.0.0"` | Listen hostname |
| `mdns` | bool | `true` | Enable mDNS service discovery |
| `mdnsDomain` | string | `"opencode.local"` | Custom mDNS domain |
| `cors` | string[] | — | Additional CORS origins (full origins: `"https://app.example.com"`) |

---

### `tui` (in `tui.json`) — TUI Config

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `theme` | string | `"opencode"` | UI theme name |
| `leader_timeout` | int | `2000` | ms to wait after leader key |
| `scroll_speed` | float | `3` | Scroll speed (min `0.001`). Ignored if `scroll_acceleration.enabled` is `true`. |
| `scroll_acceleration.enabled` | bool | `false` | macOS-style smooth scrolling |
| `diff_style` | string | `"auto"` | `"auto"` (adapts to width) \| `"stacked"` (single column) |
| `mouse` | bool | `true` | Enable/disable mouse capture |
| `keybinds` | object | — | Keyboard shortcut overrides (merged with defaults) |
| `attention` | object | disabled | Desktop notifications and sounds |

#### `attention` Object

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `enabled` | bool | `false` | Enable notifications and sounds |
| `notifications` | bool | `true` | Desktop notifications (when terminal blurred) |
| `sound` | bool | `true` | Play sounds |
| `volume` | float | `0.4` | Volume `0`–`1` |
| `sound_pack` | string | `"opencode.default"` | Sound pack ID |
| `sounds.default` | string | — | Custom sound file path |
| `sounds.question` | string | — | Question sound |
| `sounds.permission` | string | — | Permission prompt sound |
| `sounds.error` | string | — | Error sound |
| `sounds.done` | string | — | Task complete sound |
| `sounds.subagent_done` | string | — | Subagent complete sound |

---

### `permission` — Permission System

Each key resolves to `"allow"` | `"ask"` | `"deny"`.

```json
{ "permission": "allow" }
{ "permission": { "*": "ask", "bash": "allow", "edit": "deny" } }
```

**Granular (object syntax)** for `read`, `edit`, `glob`, `grep`, `bash`, `task`, `skill`, `lsp`, `external_directory`:

```json
{ "permission": { "bash": { "*": "ask", "git *": "allow", "rm *": "deny" } } }
```

#### All Permission Keys

| Key | Gates | Granular? | Default |
|-----|-------|-----------|---------|
| `read` | `read` tool (file path) | Yes | `"allow"` (but `*.env`, `*.env.*` → `"deny"`; `*.env.example` → `"allow"`) |
| `edit` | `edit`, `write`, `apply_patch` (file path) | Yes | `"allow"` |
| `glob` | `glob` tool (pattern) | Yes | `"allow"` |
| `grep` | `grep` tool (regex) | Yes | `"allow"` |
| `list` | directory listing | Yes | `"allow"` |
| `bash` | `bash` tool (command) | Yes | `"allow"` |
| `task` | subagent invocation (agent name) | Yes | `"allow"` |
| `skill` | skill loading (skill name) | Yes | `"allow"` |
| `lsp` | LSP queries | Yes | `"allow"` |
| `external_directory` | paths outside project worktree | Yes | `"ask"` |
| `doom_loop` | same tool call repeated 3× | No | `"ask"` |
| `question` | ask user during execution | No | `"allow"` |
| `webfetch` | URL fetching | No | `"allow"` |
| `websearch` | web search | No | `"allow"` |
| `todowrite` | todo list management | No | `"allow"` |

Wildcard matching: `*` = any chars, `?` = one char. Home expansion: `~/path` and `$HOME/path` supported.

---

### `agent` — Agent Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `{name}.description` | string | — | **Required.** When to use this agent |
| `{name}.mode` | string | `"all"` | `"primary"` \| `"subagent"` \| `"all"` |
| `{name}.model` | string | main model | Per-agent model override (`provider/model`) |
| `{name}.variant` | string | — | Default model variant |
| `{name}.prompt` | string | — | System prompt (supports `{file:path}`) |
| `{name}.temperature` | float | model default | `0.0`–`1.0` |
| `{name}.top_p` | float | — | `0.0`–`1.0` |
| `{name}.steps` | int | unlimited | Max agentic iterations before text-only |
| `{name}.maxSteps` | int | — | **Deprecated.** Use `steps`. |
| `{name}.disable` | bool | `false` | Disable this agent |
| `{name}.hidden` | bool | `false` | Hide from `@` autocomplete (subagent only) |
| `{name}.color` | string | — | Hex color (`#FF5733`) or theme token (`primary`, `accent`, `warning`, etc.) |
| `{name}.permission` | object | — | Per-agent permission overrides |
| `{name}.tools` | object | — | **Deprecated.** Use `permission`. |
| `{name}.options` | object | — | Additional options passed to provider |

#### Built-in Agents

| Agent | Mode | Role |
|-------|------|------|
| `build` | primary | Default; all tools enabled |
| `plan` | primary | Read-only; `edit: ask`, `bash: ask` by default |
| `general` | subagent | Multi-step tasks; full tool access |
| `explore` | subagent | Read-only code exploration |
| `scout` | subagent | External docs / dependency research, read-only |
| `compaction` | primary (hidden) | Automatic context compaction |
| `title` | primary (hidden) | Automatic session title generation |
| `summary` | primary (hidden) | Automatic session summary |

---

### `command` — Custom Commands

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `{name}.template` | string | **Yes** | Prompt sent to LLM. Supports `$ARGUMENTS`, `$1`,`$2`,..., `!`cmd``, `@file` |
| `{name}.description` | string | No | TUI display description |
| `{name}.agent` | string | No | Agent to execute (default: current agent) |
| `{name}.model` | string | No | Model override |
| `{name}.subtask` | bool | No | Force subagent invocation |

Commands also defined as Markdown files in `~/.config/opencode/commands/` or `.opencode/commands/`.

---

### `formatter` — Code Formatters

| Value | Meaning |
|-------|---------|
| Omitted / `false` | Formatters disabled |
| `true` | Enable all built-in formatters |
| `{...}` | Enable built-ins with overrides + custom |

Per-formatter object:

| Key | Type | Description |
|-----|------|-------------|
| `disabled` | bool | Disable this formatter |
| `command` | string[] | Command + args (`["npx", "prettier", "--write", "$FILE"]`) |
| `environment` | object | Env vars (`{ "NODE_ENV": "development" }`) |
| `extensions` | string[] | File extensions (`[".js", ".ts"]`) |

Built-in formatters: `air`, `biome`, `cargofmt`, `clang-format`, `cljfmt`, `dart`, `dfmt`, `gleam`, `gofmt`, `htmlbeautifier`, `ktlint`, `mix`, `nixfmt`, `ocamlformat`, `ormolu`, `oxfmt`, `pint`, `prettier`, `rubocop`, `ruff`, `rustfmt`, `shfmt`, `standardrb`, `terraform`, `uv`, `zig`.

---

### `lsp` — LSP Servers

| Value | Meaning |
|-------|---------|
| Omitted / `false` | LSP disabled |
| `true` | Enable all built-in LSP servers |
| `{...}` | Enable built-ins with overrides + custom |

Per-LSP object:

| Key | Type | Description |
|-----|------|-------------|
| `disabled` | bool | Disable this LSP server |
| `command` | string[] | Command + args (`["rust-analyzer"]`) |
| `extensions` | string[] | File extensions (`[".rs"]`) |
| `env` | object | Environment variables |
| `initialization` | object | LSP `initialize` params |

Built-in LSP servers: `astro`, `bash`, `clangd`, `csharp`, `clojure-lsp`, `dart`, `deno`, `elixir-ls`, `eslint`, `fsharp`, `gleam`, `gopls`, `hls`, `jdtls`, `julials`, `kotlin-ls`, `lua-ls`, `nixd`, `ocaml-lsp`, `oxlint`, `php intelephense`, `prisma`, `pyright`, `razor`, `ruby-lsp`, `rust`, `sourcekit-lsp`, `svelte`, `terraform`, `tinymist`, `typescript`, `vue`, `yaml-ls`, `zls`.

---

### `mcp` — MCP Server Configuration

Keyed by server name. Each value is either:

**Local server:**
```json
{ "type": "local", "command": ["node", "server.js"], "cwd": ".", "environment": {}, "enabled": true, "timeout": 5000 }
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `type` | `"local"` | **Yes** | Local subprocess |
| `command` | string[] | **Yes** | Command + args |
| `cwd` | string | No | Working directory (relative to workspace) |
| `environment` | object | No | Env vars |
| `enabled` | bool | No | Start on boot |
| `timeout` | int | No | Request timeout in ms (default: `5000`) |

**Remote server:**
```json
{ "type": "remote", "url": "https://mcp.example.com/sse", "headers": {}, "enabled": true, "timeout": 5000 }
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `type` | `"remote"` | **Yes** | Remote SSE endpoint |
| `url` | string | **Yes** | Server URL |
| `headers` | object | No | Custom HTTP headers |
| `enabled` | bool | No | Start on boot |
| `oauth` | object \| `false` | No | OAuth config or `false` to disable auto-detection |
| `timeout` | int | No | Request timeout in ms (default: `5000`) |

**Disable-only:**
```json
{ "enabled": false }
```

#### OAuth Config (for remote MCP)

| Key | Type | Description |
|-----|------|-------------|
| `clientId` | string | OAuth client ID (or try dynamic client reg) |
| `clientSecret` | string | OAuth client secret |
| `scope` | string | OAuth scopes |
| `callbackPort` | int | Callback port (default: `19876`) |
| `redirectUri` | string | Full redirect URI (default: `http://127.0.0.1:19876/mcp/oauth/callback`) |

---

### `plugin` — Plugins

```json
{ "plugin": ["opencode-helicone-session", "@my-org/custom-plugin"] }
```

| Format | Description |
|--------|-------------|
| `"npm-package-name"` | npm package |
| `["npm-package-name", { ...options }]` | npm package with options |
| `"./path/to/plugin.ts"` | Local TypeScript file |
| `"./path/to/plugin.js"` | Local JavaScript file |

---

### `references` — External References

Keyed by alias name.

**Local directory:**
```json
{ "references": { "docs": { "path": "../docs", "description": "...", "hidden": false } } }
```

**Git repository:**
```json
{ "references": { "sdk": { "repository": "owner/repo", "branch": "main", "description": "...", "hidden": false } } }
```

**String shorthand:**
```json
{ "references": { "docs": "../docs", "effect": "Effect-TS/effect" } }
```

| Field | Local | Git | Description |
|-------|-------|-----|-------------|
| `path` | Yes | No | Relative/absolute/`~/` path |
| `repository` | No | Yes | Git URL, host/path, or `owner/repo` |
| `branch` | No | Yes | Branch or ref (default: repo default) |
| `description` | Yes | Yes | Agent guidance (included in context) |
| `hidden` | Yes | Yes | Hide from `@` autocomplete |

Alias restrictions: no `/`, whitespace, backticks, or commas.

---

### `compaction` — Context Compaction

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `auto` | bool | `true` | Auto-compact when context full |
| `prune` | bool | `false` | Remove old tool outputs |
| `tail_turns` | int | `2` | Recent user turns to keep verbatim |
| `preserve_recent_tokens` | int | — | Max tokens to preserve from recent turns |
| `reserved` | int | `10000` | Token buffer to avoid overflow during compaction |

---

### `tool_output` — Output Truncation

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `max_lines` | int | `2000` | Lines before truncation |
| `max_bytes` | int | `51200` | Bytes before truncation |

---

### `attachment.image` — Image Handling

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `auto_resize` | bool | `true` | Resize oversized images (vs reject) |
| `max_width` | int | `2000` | Max width in pixels |
| `max_height` | int | `2000` | Max height in pixels |
| `max_base64_bytes` | int | `5242880` | Max base64 payload size |

---

### `watcher` — File Watcher

| Key | Type | Description |
|-----|------|-------------|
| `ignore` | string[] | Glob patterns to ignore (e.g. `["node_modules/**", "dist/**", ".git/**"]`) |

---

### `instructions` — Additional Rules

```json
{ "instructions": ["CONTRIBUTING.md", "docs/guidelines.md", ".cursor/rules/*.md"] }
```

Array of paths, URLs, or glob patterns to additional instruction files. Supports `@` prefix for file references.

---

### `experimental` — Experimental Features

| Key | Type | Description |
|-----|------|-------------|
| `batch_tool` | bool | Enable batch tool |
| `openTelemetry` | bool | AI SDK telemetry spans |
| `disable_paste_summary` | bool | Disable paste summary |
| `primary_tools` | string[] | Tools restricted to primary agents only |
| `continue_loop_on_deny` | bool | Continue agent loop on denied tool call |
| `mcp_timeout` | int | MCP request timeout in ms |
| `policies` | array | Policy statements (see below) |

#### `experimental.policies[]`

| Key | Type | Description |
|-----|------|-------------|
| `effect` | `"allow"` \| `"deny"` | Policy effect |
| `action` | `"provider.use"` | Action to control |
| `resource` | string | Resource ID / wildcard (e.g. `"openai"`, `"company-*"`) |

Global policy takes priority over project policy for same resource.

---

### `reference` (deprecated) / `skills` / `enterprise`

| Key | Type | Description |
|-----|------|-------------|
| `reference` | object | **Deprecated.** Use `references`. |
| `skills.paths` | string[] | Additional skill folder paths |
| `skills.urls` | string[] | URLs to fetch skills from (e.g. `https://example.com/.well-known/skills/`) |
| `enterprise.url` | string | Enterprise URL |

---

### `tools` (deprecated)

Legacy boolean tool control — auto-migrates to `permission`:

| `tools` value | Equivalent `permission` |
|---------------|------------------------|
| `"write": false` → | `"edit": "deny"` |
| `"bash": false` → | `"bash": "deny"` |
| `"write": true` → | `"edit": "allow"` |

---

## Variable Substitution

| Syntax | Resolution | Example |
|--------|-----------|---------|
| `{env:VAR_NAME}` | Environment variable | `{env:ANTHROPIC_API_KEY}` |
| `{file:path}` | File contents | `{file:~/.secrets/openai-key}` |

File paths: relative to config file, absolute (`/path`), or home-relative (`~/path`).

---

## Enterprise / Air-Gapped Env Vars

| Variable | Effect |
|----------|--------|
| `OPENCODE_DISABLE_MODELS_FETCH=true` | Skip remote model list fetch |
| `OPENCODE_MODELS_PATH=path` | Local models.json path |
| `OPENCODE_MODELS_URL=url` | Internal models.dev mirror |
| `OPENCODE_DISABLE_DEFAULT_PLUGINS=true` | Skip bundled plugin install |
| `OPENCODE_DISABLE_AUTOUPDATE=true` | Disable auto-updates |
| `OPENCODE_DISABLE_LSP_DOWNLOAD=true` | Disable LSP auto-download |
| `OPENCODE_DISABLE_PROJECT_CONFIG=true` | Ignore project-level configs |
| `OPENCODE_ENABLE_EXA=true` | Enable websearch tool |
| `OPENCODE_EXPERIMENTAL_LSP_TOOL=true` | Enable experimental LSP tool |

---

## Model Loading Priority

1. `--model` / `-m` CLI flag (`provider/model`)
2. `model` key in config
3. Last used model (persisted)
4. First model by internal priority

---

## Complete Example: `opencode.jsonc`

```jsonc
{
  "$schema": "https://opencode.ai/config.json",

  // --- Model ---
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
  "default_agent": "build",

  // --- Shell ---
  "shell": "pwsh",

  // --- Logging ---
  "logLevel": "INFO",

  // --- Server ---
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": true,
    "mdnsDomain": "opencode.local",
    "cors": ["http://localhost:5173"]
  },

  // --- Provider ---
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}",
        "baseURL": "https://api.anthropic.com",
        "timeout": 600000,
        "setCacheKey": true
      }
    },
    "openai": {
      "options": {
        "apiKey": "{env:OPENAI_API_KEY}"
      },
      "models": {
        "gpt-5": {
          "options": { "reasoningEffort": "high" },
          "variants": {
            "fast": { "reasoningEffort": "low" },
            "deep": { "reasoningEffort": "high" }
          }
        }
      }
    },
    "amazon-bedrock": {
      "options": {
        "region": "us-east-1",
        "profile": "my-profile"
      }
    }
  },

  // --- Provider allow/block ---
  "disabled_providers": [],
  "enabled_providers": ["anthropic", "openai"],

  // --- Permissions ---
  "permission": {
    "*": "allow",
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny"
    },
    "edit": "allow",
    "doom_loop": "ask",
    "external_directory": "ask"
  },

  // --- Agents ---
  "agent": {
    "plan": {
      "mode": "primary",
      "model": "anthropic/claude-haiku-4-5",
      "temperature": 0.1,
      "permission": {
        "edit": "deny",
        "bash": "deny"
      }
    },
    "code-reviewer": {
      "description": "Reviews code for quality and security",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-5",
      "color": "#ff6b6b",
      "prompt": "You are a senior code reviewer. Focus on security, performance, and maintainability.",
      "permission": {
        "edit": "deny",
        "bash": "ask"
      }
    }
  },

  // --- Commands ---
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show failures.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-haiku-4-5"
    },
    "component": {
      "template": "Create a React component named $ARGUMENTS with TypeScript.",
      "description": "Create new component"
    }
  },

  // --- Formatters ---
  "formatter": true,

  // --- LSP ---
  "lsp": {
    "typescript": { "disabled": false },
    "rust": { "command": ["rust-analyzer"] }
  },

  // --- MCP ---
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "."],
      "enabled": true
    },
    "company-api": {
      "type": "remote",
      "url": "https://mcp.company.com/sse",
      "enabled": false
    }
  },

  // --- Plugins ---
  "plugin": ["opencode-helicone-session"],

  // --- References ---
  "references": {
    "docs": { "path": "../docs", "description": "Product documentation" },
    "sdk": { "repository": "anomalyco/opencode-sdk-js", "branch": "main" }
  },

  // --- Compaction ---
  "compaction": {
    "auto": true,
    "prune": false,
    "tail_turns": 2,
    "reserved": 10000
  },

  // --- Watcher ---
  "watcher": {
    "ignore": ["node_modules/**", "dist/**", ".git/**"]
  },

  // --- Tool Output ---
  "tool_output": {
    "max_lines": 2000,
    "max_bytes": 51200
  },

  // --- Attachments ---
  "attachment": {
    "image": {
      "auto_resize": true,
      "max_width": 2000,
      "max_height": 2000,
      "max_base64_bytes": 5242880
    }
  },

  // --- Behavior ---
  "share": "manual",
  "autoupdate": true,
  "snapshot": true,
  "username": "dev-user",

  // --- Instructions ---
  "instructions": ["AGENTS.md", "CONTRIBUTING.md"],

  // --- Experimental ---
  "experimental": {
    "batch_tool": true,
    "openTelemetry": false,
    "disable_paste_summary": false,
    "primary_tools": ["bash", "edit"],
    "continue_loop_on_deny": false,
    "mcp_timeout": 300000,
    "policies": [
      { "effect": "deny", "action": "provider.use", "resource": "openai" }
    ]
  }
}
```

## Complete Example: `tui.jsonc`

```jsonc
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight",
  "leader_timeout": 2000,
  "scroll_speed": 3,
  "scroll_acceleration": { "enabled": false },
  "diff_style": "auto",
  "mouse": true,
  "attention": {
    "enabled": false,
    "notifications": true,
    "sound": true,
    "volume": 0.4,
    "sound_pack": "opencode.default"
  },
  "keybinds": {
    "leader": "ctrl+x",
    "command_list": "ctrl+p",
    "session_new": "<leader>n",
    "model_list": "<leader>m",
    "agent_list": "<leader>a",
    "agent_cycle": "tab",
    "agent_cycle_reverse": "shift+tab"
  }
}
```
