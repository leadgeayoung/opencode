# 02 — Daily Usage

## 1. TUI Interface

Four areas:

| Area | Description |
|------|-------------|
| **Status Bar / Header** | Version, active mode (Plan/Build), token count, model name |
| **Sidebar** | Session list; auto-shows on terminals >120 columns wide (v1.1.57+) |
| **Chat Area** | Message history with tool results, diffs, agent responses |
| **Input Area** | Multi-line prompt; smart prompts vary by mode (v1.1.58+) |

**Core operations trio**:

| Symbol | Purpose | Example |
|--------|---------|---------|
| `@` | Reference file, agent, or configured reference | `@src/main.ts`, `@explore`, `@docs/README.md` |
| `!` | Execute shell command | `!ls -la`, `!git status` |
| `/` | Slash command | `/help`, `/new`, `/models` |

**Common TUI shortcuts**:

| Shortcut | Action |
|----------|--------|
| Tab | Toggle Plan ↔ Build mode |
| Ctrl+C | Interrupt response / clear input / exit |
| Ctrl+L | Clear screen |
| Ctrl+X | Leader key (prefix — release, then next key) |
| Ctrl+X N | New session |
| Esc | Cancel / back |

**Version history**:
- v1.1.57: Sidebar auto-show/hide
- v1.1.58: Input smart prompts per mode
- v1.1.60: Hide header option via command palette (Ctrl+P)
- Hide username: `Ctrl+P` → search "username"

**TUI config** (`tui.json` / `tui.jsonc`):

```jsonc
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "opencode",
  "leader_timeout": 2000,
  "keybinds": { "leader": "ctrl+x", "command_list": "ctrl+p" },
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
  }
}
```

| Option | Default | Notes |
|--------|---------|-------|
| `theme` | `"opencode"` | See [themes](/docs/themes) |
| `leader_timeout` | `2000` | ms to wait after leader key |
| `scroll_speed` | `3` | Min `0.001`; ignored if `scroll_acceleration.enabled=true` |
| `scroll_acceleration.enabled` | `false` | macOS-style; overrides `scroll_speed` |
| `diff_style` | `"auto"` | `"auto"` adapts to width, `"stacked"` always single-column |
| `mouse` | `true` | `false` preserves native terminal selection/scrolling |
| `attention.enabled` | `false` | Desktop notifications + sounds for questions/perms/errors/done |
| `attention.notifications` | `true` | Terminal-mediated desktop notifications (when blurred) |
| `attention.sound` | `true` | Sound effects |
| `attention.volume` | `0.4` | 0–1 |
| `attention.sound_pack` | `"opencode.default"` | Override individual sounds: `default`, `question`, `permission`, `error`, `done`, `subagent_done` |

Set `OPENCODE_TUI_CONFIG` for custom TUI config path.

---

## 2. Copy/Paste

| Method | How-to |
|--------|--------|
| **Mouse drag** | Drag-select text → auto-copies on release (no Ctrl+C needed) |
| **Keyboard (Leader+Y)** | `Ctrl+X` then `Y` — copies last assistant response |
| **Command** | `/copy` — copies entire conversation to clipboard |
| **System copy** | Mac: hold `Option` then drag; Windows: hold `Shift` then drag |
| **Windows manual** | v1.1.64+: direct drag-select works; `Ctrl+C` also works for manual copy |

**Critical**: `Ctrl+C` in terminal = interrupt/clear, NOT copy. Use drag-select or `Ctrl+X Y` instead.

**Garbled text fix**: Use `Ctrl+D` to gracefully exit (not `Ctrl+C`).

**Experimental**: `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT=true` disables auto-copy-on-select.

---

## 3. 10 Core Tools (6 file ops + 4 special)

### File operation tools

| Tool | Purpose | Key params | Permission key |
|------|---------|------------|----------------|
| **read** | Read files/directories | `filePath`(absolute), `offset`(1-based line), `limit`(default 2000) | `read` |
| **write** | Create/overwrite files | Must `read` first; auto LSP check after | `edit` |
| **edit** | Exact string replacement | 9-layer smart matching; `replaceAll` | `edit` |
| **bash** | Execute shell commands | `timeout`(default 2min), `workdir` | `bash` |
| **grep** | Search file contents | Regex supported; max 100 results sorted by mtime; `include` filter | `grep` |
| **glob** | Find files by pattern | Glob patterns; max 100 results sorted by mtime | `glob` |

### 9-layer edit matching strategies

1. **Exact match** — byte-for-byte
2. **Ignore leading/trailing whitespace** — trim both sides
3. **First/last line anchors** — match ends of string
4. **Normalize whitespace** — collapse internal whitespace
5. **Indentation tolerance** — fuzzy tab/space differences
6. **Escape character handling** — unicode/escape equivalence
7. **Boundary trimming** — trim surrounding context
8. **Context-aware** — use surrounding lines for disambiguation
9. **Multiple matches** — `replaceAll` flag replaces every occurrence

### Special tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **Task** | Subagent spawning | AI delegates work to subagents |
| **WebFetch** | Fetch web content | `webfetch` permission |
| **TodoWrite** | Manage todo lists | Disabled for subagents by default |
| **Skill** | Load SKILL.md | `skill` permission |

### Additional tools

| Tool | Purpose | Gate |
|------|---------|------|
| **websearch** | Web search via Exa AI | `OPENCODE_ENABLE_EXA=true` or OpenCode provider |
| **lsp** (experimental) | Code intelligence (defs, refs, hover) | `OPENCODE_EXPERIMENTAL_LSP_TOOL=true` |
| **apply_patch** | Apply patches/diffs | `edit` permission |
| **question** | Ask user questions during execution | `question` permission |

### Rules

- **Dedicated tools > bash** for file operations (read, edit, write, grep, glob)
- **bash output** truncated at 2000 lines / 50 KB
- **bash safety**: tree-sitter parse + permission confirmation
- **grep/glob** use ripgrep internally; respect `.gitignore`
- Create `.ignore` to override — e.g., `!node_modules/` to allow searching node_modules

### Tool collaboration examples

- **Renaming function**: `grep` for old name → `edit` each file → `bash` to verify
- **Adding feature**: `read` existing patterns → `write` new file → `bash` to run tests
- **Debugging**: `bash` to reproduce → `grep` for related code → `read` the file → `edit` fix

---

## 4. Sessions

### Storage

```
~/.local/share/opencode/storage/session/<project-id>/<session-id>.json
```

### Slash commands

| Command | Aliases | Purpose | Keybind |
|---------|---------|---------|---------|
| `/new` | `/clear` | Create new session | `Ctrl+X N` |
| `/sessions` | `/resume`, `/continue` | List and switch sessions | `Ctrl+X L` |
| `/undo` | — | Undo last message + file changes (needs Git) | `Ctrl+X U` |
| `/redo` | — | Redo previously undone message (needs Git) | `Ctrl+X R` |
| `/compact` | `/summarize` | Compress context to save tokens | `Ctrl+X C` |
| `/export` | — | Export conversation as Markdown, open in `$EDITOR` | `Ctrl+X X` |
| `/share` | — | Create public share link | — |
| `/unshare` | — | Remove public share link | — |
| `/details` | — | Toggle tool execution details | — |
| `/editor` | — | Open external editor for composing | `Ctrl+X E` |
| `/thinking` | — | Toggle display of reasoning blocks | — |
| `/init` | — | Create/update AGENTS.md | — |
| `/connect` | — | Add a provider | — |
| `/exit` | `/quit`, `/q` | Exit OpenCode | `Ctrl+X Q` |

### CLI session commands

```bash
# List sessions
opencode session list
opencode session list -n 10 --format json

# Delete a session
opencode session delete <sessionID>

# Export session as JSON
opencode export [sessionID]

# Import session
opencode import <file|url>
opencode import session.json
opencode import https://opncd.ai/s/abc123
```

### Session flags (TUI launch)

```bash
opencode                    # Start TUI in current dir
opencode /path/to/project   # Start TUI in specific dir
opencode -c                 # Continue last session
opencode -s <sessionID>     # Continue specific session
opencode --fork             # Fork when continuing (copies history)
```

### Fork

- Copies history into a new session with `(fork #N)` suffix
- Configure keybind: `"keybinds": { "session_fork": "<leader>f" }`

### Share

| Mode | Config | Behavior |
|------|--------|----------|
| Manual (default) | `"share": "manual"` | Use `/share` to share; link copied to clipboard |
| Auto-share | `"share": "auto"` | Every new conversation auto-shared |
| Disabled | `"share": "disabled"` | Sharing completely disabled |

Share URL format: `https://opncd.ai/s/<share-id>`

### Session lifecycle

`Create (opencode / /new)` → `Active (prompting)` → `Compact (/compact)` → `Archive` / `Delete`

Auto-compact disabled: `OPENCODE_DISABLE_AUTOCOMPACT=true`

### Stats

```bash
opencode stats --days 30 --tools 10 --models 5 --project
```

In TUI: `/version` shows version, `/stats` shows token usage, `/models` lists available models.

---

## 5. 15 Essential Shortcuts

### Leader key mechanism

Prefix: `Ctrl+X` (default leader key). Press, **release**, then press the action key.

`leader_timeout` (default 2000ms) controls how long to wait for the next key after leader.

### Master table

| Shortcut | Action | Config key |
|----------|--------|------------|
| `Enter` | Send / submit message | `input_submit` |
| `Shift+Enter` | New line (insert) | `input_newline` |
| `Ctrl+C` | Clear input / interrupt / exit | `input_clear` / `app_exit` |
| `Ctrl+D` | Graceful exit | `app_exit` |
| `Tab` | Toggle agent (Plan↔Build) | `agent_cycle` |
| `Shift+Tab` | Reverse agent cycle | `agent_cycle_reverse` |
| `Ctrl+L` | Clear screen | — |
| `Ctrl+P` | Command palette | `command_list` |
| `Ctrl+X N` | New session | `session_new` |
| `Ctrl+X L` | Session list | `session_list` |
| `Ctrl+X U` | Undo | `messages_undo` |
| `Ctrl+X R` | Redo | `messages_redo` |
| `Ctrl+X M` | Model list | `model_list` |
| `Ctrl+X A` | Agent list | `agent_list` |
| `Ctrl+X C` | Compact session | `session_compact` |
| `Ctrl+X Y` | Copy last response | `messages_copy` |
| `Ctrl+X F` | Fork session | `session_fork` (default `none`) |
| `Ctrl+T` | Cycle model variants (thinking depth) | `variant_cycle` |
| `Ctrl+X E` | Open editor | `editor_open` |
| `Ctrl+X X` | Export session | `session_export` |
| `Ctrl+X Q` | Exit | `app_exit` |
| `Ctrl+X T` | Theme list | `theme_list` |
| `Ctrl+X G` | Session timeline | `session_timeline` |
| `Ctrl+X H` | Toggle tips | `tips_toggle` |
| `Ctrl+X S` | Status view | `status_view` |
| `Ctrl+X B` | Sidebar toggle | `sidebar_toggle` |
| `F2` | Cycle recent models | `model_cycle_recent` |
| `Shift+F2` | Reverse cycle recent models | `model_cycle_recent_reverse` |

### Message scrolling

| Shortcut | Action |
|----------|--------|
| `PageUp` / `Ctrl+Alt+B` | Scroll up one page |
| `PageDown` / `Ctrl+Alt+F` | Scroll down one page |
| `Ctrl+Alt+U` | Half page up |
| `Ctrl+Alt+D` | Half page down |
| `Ctrl+G` / `Home` | Jump to top |
| `Ctrl+Alt+G` / `End` | Jump to bottom |

### Readline input shortcuts (desktop app)

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Move to line start |
| `Ctrl+E` | Move to line end |
| `Ctrl+B` | Back one character |
| `Ctrl+F` | Forward one character |
| `Alt+B` | Back one word |
| `Alt+F` | Forward one word |
| `Ctrl+U` | Delete to line start |
| `Ctrl+K` | Delete to line end |
| `Ctrl+W` | Delete previous word |
| `Alt+D` | Delete next word |
| `Ctrl+D` | Delete character under cursor |
| `Ctrl+T` | Transpose characters |
| `Ctrl+G` | Cancel popup / abort response |
| `↑` / `↓` | Browse input history |

### Permission dialog shortcuts

| Key | Action |
|-----|--------|
| `y` | Allow |
| `n` | Deny |
| `a` | Always allow (this session) |
| `Ctrl+F` | Toggle fullscreen permission prompt |

### Disable a keybind

```jsonc
{ "keybinds": { "session_compact": "none" } }
```

### Multiple bindings

```jsonc
{ "keybinds": { "app_exit": "ctrl+c,ctrl+d,<leader>q" } }
```

### Advanced binding (object form)

```jsonc
{
  "keybinds": {
    "messages_copy": ["<leader>y", "ctrl+shift+c"],
    "input_paste": { "key": "ctrl+v", "preventDefault": false }
  }
}
```

### Windows notes

- `input_undo` defaults to `ctrl+z,ctrl+-,super+z` (Ctrl+Z added because Windows lacks POSIX suspend)
- `terminal_suspend` forced to `none`
- `Shift+Enter` may need terminal config — see `%LOCALAPPDATA%\Packages\...\settings.json`

---

## 6. Global Rules (AGENTS.md)

### File locations (load order)

| Priority | File | Scope |
|----------|------|-------|
| 1 | `./AGENTS.md` or `./CLAUDE.md` (walk up from cwd) | Project-specific |
| 2 | `~/.config/opencode/AGENTS.md` | Global (personal) |
| 3 | `~/.claude/CLAUDE.md` | Claude Code fallback (if no global AGENTS.md) |

**Merge, not override**: All found rules are combined into context.

**Claude Code compatibility** (disabled via `OPENCODE_DISABLE_CLAUDE_CODE=1`):
- `CLAUDE.md` in project root (fallback if no `AGENTS.md`)
- `~/.claude/CLAUDE.md` (fallback if no `~/.config/opencode/AGENTS.md`)
- `~/.claude/skills/` (see [Agent Skills](/docs/skills))

### /init command

- Scans repo, creates/updates `AGENTS.md`
- Captures: build/lint/test commands, architecture, conventions, setup quirks
- Improves in-place if `AGENTS.md` already exists

### Instructions in opencode.json

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/guidelines.md",
    ".cursor/rules/*.md",
    "https://raw.githubusercontent.com/my-org/shared-rules/main/style.md"
  ]
}
```

| Feature | Detail |
|---------|--------|
| Glob patterns | `packages/*/AGENTS.md`, `.cursor/rules/*.md` |
| URLs | Remote files, 5s fetch timeout |
| `~/` expansion | Home directory paths |
| Relative paths | Relative to the config file |
| Absolute paths | `/home/user/rules.md` |
| Combine | Merged with AGENTS.md — not overridden |

### Team & monorepo

```jsonc
// Monorepo: one AGENTS.md per package
{ "instructions": ["packages/*/AGENTS.md"] }
```

Commit `AGENTS.md` to Git so the whole team benefits.

### External refs in AGENTS.md

Use `@docs/xxx.md` syntax. AI loads references **lazily** (on demand), not preemptively.

```markdown
# TypeScript Project Rules
For TypeScript code style: @docs/typescript-guidelines.md
For React patterns: @docs/react-patterns.md
For API standards: @docs/api-standards.md
For testing guidelines: @test/testing-guidelines.md
CRITICAL: Load on need-to-know basis. Treat as mandatory.
```

### References system

Configure via `opencode.json`:

```jsonc
{
  "references": {
    "docs": { "path": "../product-docs", "description": "Product behavior docs" },
    "sdk": { "repository": "anomalyco/opencode-sdk-js", "branch": "main" },
    "internal": { "path": "../internal", "hidden": true }
  }
}
```

| Field | Description |
|-------|-------------|
| `path` | Local directory (relative, absolute, `~/`) |
| `repository` | Git URL, host/path, or `owner/repo` |
| `branch` | Optional branch/ref |
| `description` | Guidance for when to use; references with descriptions are auto-advertised to agents |
| `hidden` | Omit from `@` autocomplete (but still available if described) |

Usage: `@docs`, `@docs/subdir/file.md`, `@sdk/src/client.ts`

---

## 7. Environment Management

### Auth commands

```bash
opencode auth login          # Interactive login (opens provider prompt)
opencode auth login -p anthropic -m api-key   # Non-interactive
opencode auth list           # List auth'd providers (alias: ls)
opencode auth logout         # Clear provider credentials
```

### Auth storage

```
~/.local/share/opencode/auth.json
```

### Auth priority (high → low)

1. **Environment variables** (e.g., `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`)
2. **auth.json** (`~/.local/share/opencode/auth.json`)
3. **Config file** (`opencode.json`)
4. **`.env` file** in project root (loaded on startup)

### Model management

| Action | Method |
|--------|--------|
| List models in TUI | `/models` or `Ctrl+X M` |
| List models in CLI | `opencode models [provider]` |
| Refresh model cache | `opencode models --refresh` |
| Cycle recent models | `F2` (forward), `Shift+F2` (reverse) |
| Cycle model variants | `Ctrl+T` (reasoning effort) |

### Version & stats

| Command | What it shows |
|---------|---------------|
| `/version` | OpenCode version |
| `/stats` | Token usage, cost, session count |
| `opencode stats --days 30 --tools 10` | Detailed stats for last 30 days |
| `opencode --version` | Version from CLI |

### Key environment variables

| Variable | Purpose |
|----------|---------|
| `OPENCODE_CONFIG` | Custom config file path |
| `OPENCODE_TUI_CONFIG` | Custom TUI config path |
| `OPENCODE_CONFIG_DIR` | Config directory |
| `OPENCODE_CONFIG_CONTENT` | Inline JSON config |
| `OPENCODE_PERMISSION` | Inline JSON permissions |
| `OPENCODE_SERVER_PASSWORD` | Basic auth password for serve/web |
| `OPENCODE_SERVER_USERNAME` | Basic auth username (default `opencode`) |
| `OPENCODE_DISABLE_AUTOUPDATE` | Disable auto-update checks |
| `OPENCODE_DISABLE_AUTOCOMPACT` | Disable auto-compaction |
| `OPENCODE_DISABLE_CLAUDE_CODE` | Disable all `.claude/` support |
| `OPENCODE_ENABLE_EXA` | Enable websearch tool |
| `OPENCODE_MODELS_URL` | Custom models endpoint |
| `OPENCODE_DISABLE_MODELS_FETCH` | Disable remote model list fetch |
| `OPENCODE_GIT_BASH_PATH` | Path to Git Bash on Windows |
| `OPENCODE_CLIENT` | Client identifier (default `cli`) |

### Experimental env vars

| Variable | Effect |
|----------|--------|
| `OPENCODE_EXPERIMENTAL=true` | Master switch for experimental |
| `OPENCODE_EXPERIMENTAL_LSP_TOOL=true` | Enable LSP code intelligence tool |
| `OPENCODE_EXPERIMENTAL_BASH_DEFAULT_TIMEOUT_MS` | Override bash default timeout |
| `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX` | Max LLM output tokens |
| `OPENCODE_EXPERIMENTAL_PLAN_MODE` | Enable plan mode |
| `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS` | Background subagent tasks |
| `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` | Disable auto-copy on select |

---

## 8. Git Basics

### undo / redo and Git

| Feature | Git repo required? | Effect without Git |
|---------|-------------------|-------------------|
| `/undo` | **Yes** for file revert | Only undo conversation (no file restore) |
| `/redo` | **Yes** for file restore | Only redo conversation |

Internally, OpenCode uses Git snapshots to track file state per message. Each message captures the diff.

```bash
/undo   # Ctrl+X U — removes last user msg + response + reverts file changes
/redo   # Ctrl+X R — restores the undone changes
```

`/undo` can be run multiple times to step back through history.

### Git operations via `!`

```bash
!git status
!git diff
!git log --oneline -10
!git add -A && git commit -m "feat: add auth middleware"
```

AI can **generate commit messages** based on changes made.

### Non-Git projects

- Only conversation undo/redo works
- File changes cannot be reverted automatically
- Use `!git init` to start tracking if desired

### GitHub agent

```bash
opencode github install    # Install GitHub Actions workflow
opencode github run        # Run in CI (or locally with --event)
```

### PR command

```bash
opencode pr <number>       # Fetch + checkout PR branch, then run OpenCode
```
