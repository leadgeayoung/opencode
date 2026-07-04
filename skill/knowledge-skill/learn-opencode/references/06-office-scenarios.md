# Office Scenarios

---

## C1 — File Organization

**Three-step method**: Analyze Status → Define Rules → Batch Execute

### Key Tools & Limits

| Tool | Purpose | Limits |
|------|---------|--------|
| `list` | Directory tree | `path`(absolute), `ignore`(globs), max 100 files |
| `glob` | Find files by pattern | `pattern`+`path`, max 100 sorted by mtime |
| `grep` | Search contents (regex) | `pattern`+`include`, max 100 sorted by mtime |
| `bash` | Execute commands | `workdir`, timeout default 2min, output max 30000 chars |

### Built-in `list` Ignore List

`node_modules/`, `__pycache__/`, `.git/`, `dist/`, `build/`, `target/`, `vendor/`, `bin/`, `obj/`, `.idea/`, `.vscode/`, `.zig-cache/`, `zig-out`, `.coverage`, `coverage/`, `tmp/`, `temp/`, `.cache/`, `cache/`, `logs/`, `.venv/`, `venv/`, `env/`

### TUI Commands

- `!ls -la` — prefix `!` to run shell command
- `@file` — injects file content into context
- `opencode /path` — launch directly in a directory

### Ignore Rules

`glob`/`grep`/`list` use ripgrep internally → respect `.gitignore`. Create `.ignore` to explicitly include:
```
!node_modules/
!dist/
```

### Batch Rename Workflow

1. AI analyzes directory
2. AI shows rename plan (old→new) for confirmation
3. Execute after user confirms

### Safety: Permission Config

```jsonc
{ "permission": { "edit": "ask" } }
```

`permission` supports `allow`/`ask`/`deny`. `edit` covers write/modify/patch.

### Common Organization Needs

- Batch rename (photos by date)
- Categorize archive (sort by type)
- Content search (find keywords)
- Dedupe cleanup (dry-run first)

### Analysis Methods

1. **`list`**: `List files and subdirectories...tell me: subdirectories, file type distribution, naming patterns`
2. **`glob`**: `Find all image files (**/*.jpg)...list by mtime newest to oldest`
3. **Plan mode**: comprehensive analysis with suggested plan

### Categorize Prompt

```
Categorize files into subdirectories by type:
- Images (jpg, png, gif) → Images/
- Documents (pdf, doc, docx, txt) → Documents/
- Videos (mp4, mov, avi) → Videos/
- Others → Others/
Requirements: 1) Show results for confirmation first 2) Then execute
```

### Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Files deleted/modified | No list/confirmation first | Output "operation list" first |
| Rename rules wrong | Lack executable details | Fill in format/source/sequence/override |
| Partial results | Tool limit (100) | Narrow scope with specific path/pattern |
| Files not found | ripgrep follows `.gitignore` | Use `.ignore` to re-include |
| `list` misses dirs | Built-in ignore list | Use `glob`/`grep` directly |

---

## C2 — Data Processing

**Workflow**: Understand Structure → Define Goals → Execute Analysis → Output Results

### Key Tools

| Tool | Purpose | Limits |
|------|---------|--------|
| `read` | Read file (pagination) | `offset`(0-based), `limit`(default 2000 lines) |
| `webfetch` | Fetch webpage | `http/https` only, timeout default 30s(max 120s), 5MB limit. Format: text/markdown/html |
| `bash` | Run scripts | `timeout`(ms, default 2min), `workdir`, output 30000 chars |

### Data Tasks

- **Analysis**: sums, averages, trends
- **Filtering**: records matching conditions
- **Conversion**: CSV↔JSON, merge, Excel import
- **Report generation**: Markdown tables/charts

### Step-by-step

1. **Understand structure**: `@sales.csv Analyze this CSV: rows, columns, data types, null/abnormal values`
2. **Basic stats**: `@sales.csv Total sales, average order, top 5 products, monthly trend`
3. **Filter**: `@sales.csv Orders over 1000 yuan, January orders, Beijing customers. Save as filtered_sales.csv`
4. **Generate report**: `@sales.csv Generate monthly report with sales overview, product analysis, regional analysis. Save as monthly-report.md`
5. **Format conversion**: `@sales.csv Convert to JSON, extract customers as CSV, generate Excel format`

### Advanced: Online Data

`webfetch` fetches webpages for analysis. Ask AI to explain format (text/markdown/html) and conversion plan.

### Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Inaccurate analysis | File too large | AI summarizes structure+sampling first, then full analysis |
| Wrong calculations | Misunderstood columns/units | AI restates column meanings first |
| `webfetch` error | URL not http/https | Confirm protocol |
| Content too large | Exceeds 5MB | Use smaller page or segment |

---

## C3 — Learning Programming with AI

**Method**: Concept → Practice → Problem-solving → Project

### Key Tools/Commands

| Tool | Purpose | Details |
|------|---------|---------|
| `@explore` subagent | Codebase exploration | Invoke via `@`. Levels: quick/medium/very thorough |
| `skill` tool | Load reusable SKILL.md templates | Paths: `.opencode/skill/*/SKILL.md`, `.claude/skills/*/SKILL.md` |
| `/editor` | External editor | Uses `EDITOR` env var |
| `/details` | Toggle tool execution details | Built-in TUI command |
| `codesearch` | Search API/library usage | Configurable tokens (1000-2000+, default 2000+) |
| `lsp` (experimental) | LSP operations | Needs `OPENCODE_EXPERIMENTAL_LSP_TOOL=true`. 9 ops: goToDefinition, findReferences, hover, documentSymbol, workspaceSymbol, goToImplementation, prepareCallHierarchy, incomingCalls, outgoingCalls |

### codesearch Activation

Available when: providerID is `opencode`, or `OPENCODE_ENABLE_EXA=true`/`1`. Boolean env vars recognize `true`/`1` as truthy.

### Learning Flow

1. **Choose language**: `@explore` to assess project, or ask AI for recommendations
2. **Learn concept**: `Teach me what a variable is...give example...let me do exercise`
3. **Write code**: `/editor` for long code; switch to Build mode for practice files
4. **Solve problems**: Paste error → AI explains + fixes
5. **Project**: `Give me a suitable practice project...guide me step by step`

### Effective Questions

- Bad: `Why doesn't this code work`
- Good: `This code gives IndexError, I expected...here's the code: print(my_list[1])`

### Skill File Example

```markdown
---
name: python-basics
description: Python basics teaching
---
Explain Python basic concepts, provide exercises, help debug common errors.
```

Skill discoverable paths: `.opencode/skill/<name>/SKILL.md`, `~/.config/opencode/skill/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md`, `~/.claude/skills/<name>/SKILL.md`

### Config Variable Substitution

`{env:VAR}` and `{file:path}` in config. Note: `apiKey` goes in `provider.<id>.options.apiKey`, NOT `provider.<id>.apiKey`:
```jsonc
{ "provider": { "openai": { "options": { "apiKey": "{env:OPENAI_API_KEY}" } } } }
```

---

## C4 — Automation Scripts

**Identifying opportunities**: repeated execution, clear rules, time-consuming, error-prone

**Automation layers**: Manual → One-click Command → Scripted → External Scheduling

### Key Features

| Feature | Purpose | Details |
|---------|---------|---------|
| Custom Commands | Fixed `/command-name` from templates | Markdown body = template |
| Command Arguments | `$ARGUMENTS`, `$1`, `$2`... | Positional |
| Shell Embedding | `` !`command` `` | Injects command output into prompt |
| File Reference | `@path/to/file` | Injects file content |
| `opencode run` | Non-interactive scripting | `opencode run [message..]` |
| MCP Servers | External tools | Tools auto-available, consume context |
| `/compact` | Compress session | Alias `/summarize`, shortcut `ctrl+x c` |

### Custom Command File Locations

- Project: `.opencode/command/`
- Global: `~/.config/opencode/command/`

### Method 1: Markdown Command File

`.opencode/command/organize-invoices.md`:
```markdown
---
description: Organize invoices (archive + rename)
agent: build
model: anthropic/claude-opus-4-5-thinking
---
Organize invoice PDFs from $1 directory into $2:
Requirements:
1. Output operation list first, don't execute directly
2. Execute after I confirm
Today: !`date +%Y-%m-%d`
```

Run: `/organize-invoices ~/Downloads ~/Documents/Finance/Invoices`

### Method 2: JSONC Config

```jsonc
{
  "command": {
    "organize-invoices": {
      "template": "Organize invoice PDFs from $1 into $2...",
      "description": "Organize invoices",
      "agent": "build",
      "model": "anthropic/claude-opus-4-5-thinking",
      "subtask": true
    }
  }
}
```

`template` required; `description`/`agent`/`model`/`subtask` optional. `subtask: true` forces subagent usage.

### Script Generation Best Practice

Always request: **preview mode (dry-run)** + **execute mode** + detailed logs. Biggest fear: "write once and run directly."

```
Help me create a script scripts/organize_invoices.py:
- Scan source directory for PDFs
- Parse date/amount
- Generate target directory structure
- Output detailed logs
Requirements: preview mode + execute mode, minimal runnable command
```

### MCP Config Example

```jsonc
{
  "mcp": {
    "mcp_everything": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-everything"]
    }
  }
}
```

MCP tools auto-available but consume context. Use `enabled: false` to disable.

### Common Pitfalls

| Symptom | Cause | Solution |
|---------|-------|----------|
| Command "not working" | Template in frontmatter, not body | Body content is the template |
| Name conflict | Same as built-in command | Avoid `/init`, `/share`, etc. |
| `` !`cmd` `` wrong output | Executes in project root | Write relative paths |
| `apiKey` doesn't work | Written at `provider.<id>.apiKey` | Must be `provider.<id>.options.apiKey` |

---

## MCP Web Image Generation

**Core flow**: Open page → Enter prompt → Wait → Download

### Jimeng (https://jimeng.jianying.com)

- AI opens page via MCP (`chrome-devtools_new_page`)
- Takes snapshot, finds "Image Generation" button, clicks
- `fill` tool enters prompt into input box
- Clicks generate button
- `wait_for` waits for "Download" (下载) text to appear
- Clicks download → saved to browser default download dir

**Sensitive word alternatives**:
- "Ultraman" (奥特曼) → "Cosmic hero" / "Giant of Light"
- "Sun Wukong" (孙悟空) → "Eastern myth monkey king" / "Monkey King"

**Generation time**: 30-60 seconds. Generates 4 images. Need to handle watermark settings popup.

### Gemini (https://gemini.google.com/app)

- AI opens page, enters prompt in chat input
- Gemini auto-recognizes as image generation request
- `wait_for` waits for "Download full-size image" button
- Clicks download → saved to default download dir

**Generation time**: 15-30 seconds. Usually generates 1 image. Content moderation relatively lenient. **Needs VPN**.

### Comparison

| Aspect | Gemini | Jimeng |
|--------|--------|--------|
| Access | Needs VPN | Direct (domestic) |
| Speed | 15-30s | 30-60s |
| Moderation | Lenient | Strict |
| Images | Usually 1 | Usually 4 |

### Batch Generation

```
Generate these 5 images, download to images folder:
1. Cyberpunk street
2. Ink wash landscape
...
```
AI processes sequentially: open → prompt → wait → download → next.

### Auto-rename

```
Rename downloaded file to cyberpunk-street.png
```
```bash
mv ~/Downloads/jimeng-xxx.png ~/Desktop/images/cyberpunk-street.png
```

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Page won't open | Network issue | Gemini needs VPN; check Jimeng login |
| Prompt blocked | Content moderation | Use alternative descriptions |
| Can't find download dir | System language | `~/Downloads/` (en) vs `~/下载/` (zh) |
| MCP connection failed | Chrome remote debugging not enabled | Check `chrome://inspect/#remote-debugging` |
