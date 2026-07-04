# Context Compaction, Thinking Depth, Debugging, Web Search & CLI Automation

## Context Compaction (20-compaction.md)

### Overview
Context compaction reduces token usage when the conversation approaches the model's context window limit. It is critical for maintaining long, productive sessions without hitting context ceilings.

### Trigger Mechanisms

| Trigger | How |
|---|---|
| **Automatic** | Fires when context nears the model's token limit (configurable threshold) |
| **Manual** | `/compact` or `/summarize` commands |
| **Keyboard Shortcut** | `ctrl+x c` (Windows/Linux) or `cmd+x c` (macOS) |

### Configuration

```json
{
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 10000
  }
}
```

| Key | Type | Default | Description |
|---|---|---|---|
| `auto` | boolean | `true` | Enable automatic compaction when context is near the limit |
| `prune` | boolean | `true` | Remove old tool outputs (file reads, search results, etc.) to save tokens |
| `reserved` | number | `10000` | Token buffer to reserve — compaction fires when remaining space drops below this |

### How Compaction Works (Internal Architecture)

1. **Detection**: The context manager monitors token usage after each turn
2. **Summary Agent**: When triggered (auto or manual), a dedicated **summary agent** generates a condensed summary of the conversation so far
3. **Compaction Agent**: A separate **compaction agent** handles the actual compression:
   - Removes pruned tool outputs (if `prune: true`)
   - Replaces older conversation turns with the generated summary
   - Preserves the most recent N turns for continuity
   - Maintains all file contents, session state, and task context
4. **Recovery**: The summary is injected at the top of the context after compaction, so the model retains awareness of what happened earlier

### Best Practices
- Run `/compact` manually before switching tasks in a long session
- Keep `prune: true` for most use cases (dramatic token savings)
- Increase `reserved` for complex tasks that need more buffer
- If compaction happens too frequently, consider a larger context model variant
- After compaction, the model may lose fine-grained details — use `/details` to bring back specifics

---

## Thinking Depth (21-thinking-depth.md)

### Overview
Thinking depth controls how much reasoning the model performs before responding. Deeper thinking improves quality for complex tasks but uses more tokens and latency.

### Model Variants

Configure thinking budgets via model `variants` in `opencode.json`:

```json
{
  "variants": {
    "fast": { "model": "gpt-4o-mini", "thinking": 0 },
    "balanced": { "model": "gpt-4o", "thinking": 4096 },
    "deep": { "model": "gpt-4o", "thinking": 16384 }
  }
}
```

| Variant | Thinking Budget | Use Case |
|---|---|---|
| `fast` | 0 (no thinking) | Quick lookups, simple edits, yes/no questions |
| `balanced` | 4096 | Default — general development tasks |
| `deep` | 16384 | Complex reasoning, architecture design, debugging tricky bugs |

### Switching Depth

- **`Ctrl+T`** — Cycle through depth levels interactively
- **`/model <variant>`** — Switch to a specific variant by name
- The current thinking depth is displayed in the TUI status bar

### How It Works
- Thinking budget is passed to models that support extended thinking (Claude, etc.)
- For models without native thinking, OpenCode simulates chain-of-thought internally
- Higher budgets produce more thorough reasoning but consume more tokens and time
- The budget is a _maximum_, not a fixed amount — the model uses what it needs

### When to Use Each Depth

| Task | Recommended Depth |
|---|---|
| "What does this function do?" | Fast / Balanced |
| "Fix this typo" | Fast |
| "Debug this race condition" | Deep |
| "Design the architecture for 20 microservices" | Deep |
| "Refactor this module" | Balanced |
| "Explain this concept" | Balanced |
| "Write unit tests" | Balanced / Deep |
| "Read this file" | Fast |

---

## Debugging & Diagnostics (22-debugging.md)

### Commands

| Command | Description |
|---|---|
| `opencode debug config` | View the effective configuration (all sources merged, including plugins) |
| `opencode debug config --json` | Same as above but raw JSON output |
| `opencode debug` | General diagnostic information |
| `opencode debug [subcommand]` | Various diagnostic subcommands |

### Configuration Debugging
- Shows resolved config from all layers: defaults → `opencode.json` → plugin injection → environment variables → CLI flags
- Plugin-injected settings are clearly marked
- `--json` flag is useful for piping to tools like `jq`

### Log Levels

| Level | Usage |
|---|---|
| `ERROR` | Only errors (production use) |
| `WARN` | Warnings and errors |
| `INFO` | Normal operational info (default) |
| `DEBUG` | Detailed diagnostic information |
| `TRACE` | Extremely verbose, includes raw API payloads |

Set via:
- CLI: `--log-level DEBUG`
- Config: `"logLevel": "debug"`
- Environment: `LOG_LEVEL=debug`

### Environment Variables for Debugging

| Variable | Effect |
|---|---|
| `OPENCODE_LOG_LEVEL` | Override log level |
| `OPENCODE_DEBUG` | Enable debug mode |
| `OPENCODE_TRACE` | Enable trace mode (very verbose) |
| `OPENCODE_DEV` | Development mode with extra diagnostics |

### Troubleshooting Common Issues

| Symptom | Check |
|---|---|
| Model not responding | API key validity, rate limits, network connectivity |
| Config not taking effect | Run `opencode debug config` to see resolved values |
| Plugin not loading | Check plugin path, format, and syntax |
| Compaction issues | Check `reserved` value, try manual `/compact` |
| Slow responses | Check model provider, thinking budget, network |
| GitHub integration failing | Check workflow logs in Actions, verify secrets |
| Share link not working | Check `enterprise.url` config, network access |

---

## Web Search (23-web-search.md)

### Two Tools

| Tool | Function | Trigger |
|---|---|---|
| `websearch` | Search the web (results from search engine) | Automatic (AI decides) or explicit |
| `webfetch` | Fetch and read a specific URL | Automatic (AI decides) or explicit |

### `webfetch` Configuration

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | required | HTTP or HTTPS URL only |
| `format` | enum | `"markdown"` | `"text"`, `"markdown"`, or `"html"` |
| `timeout` | number | `30` | Timeout in seconds (max: 120) |

- Response limit: **5MB** maximum
- HTML content is automatically converted to Markdown for readability
- HTTP URLs are auto-upgraded to HTTPS
- Useful for: reading documentation, blog posts, API specs, news articles

### `websearch` Activation

| Activation Method | Description |
|---|---|
| **OpenCode Zen hosted models** | Web search enabled by default when using Zen's free models |
| **`OPENCODE_ENABLE_EXA=true`** | Enable Exa-powered web search for custom provider setups |

- Without either, web search tools are available but may return limited or no results
- The AI **automatically decides** when to search — you don't need to request it explicitly
- Context from search results is incorporated into the model's responses

### Use Cases
- **Latest information**: Get current docs, API changes, release notes
- **Documentation**: Fetch library/framework docs that aren't in the training cut-off
- **Research**: Gather information from multiple sources
- **Troubleshooting**: Search error messages and solutions
- **Code examples**: Find real-world usage patterns

### Best Practices
- The AI is good at deciding when to search — let it handle proactively
- For specific URLs, mention the URL in your prompt (AI will use `webfetch`)
- Be specific about what you're looking for to get better search results
- Use markdown format for most readable results

---

## CLI Automation (24-cli-automation.md)

### `opencode run` — Non-Interactive Mode

```bash
opencode run [message..]
```

Run OpenCode in non-interactive (headless) mode. The model processes the prompt and exits.

### Options

| Flag | Description |
|---|---|
| `-m, --model <model>` | Specify which model/variant to use |
| `--print-logs` | Print execution logs to stdout |
| `--log-level <level>` | Set log level (TRACE, DEBUG, INFO, WARN, ERROR) |
| `--timeout <seconds>` | Maximum execution time before abort |
| `--no-progress` | Suppress progress indicators |
| `--output <format>` | Output format (text, json) |

### Examples

```bash
# Basic run
opencode run "review the changes in src/"

# Specify model
opencode run -m claude-sonnet-4 "design a database schema for a blog"

# With logging
opencode run --print-logs --log-level DEBUG "debug why tests fail"

# Pipe input
cat error.log | opencode run "fix all errors in this log"

# Capture output
result=$(opencode run "what is the current git branch?")
```

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success — task completed |
| `1` | General error |
| `2` | Invalid arguments |
| `130` | Interrupted (Ctrl+C) |
| `137` | Killed (OOM, timeout) |

### CI/CD Integration

**GitHub Actions:**
```yaml
- name: Automated Code Review
  run: opencode run "review the PR diff" --print-logs
  env:
    PROVIDER_API_KEY: ${{ secrets.PROVIDER_API_KEY }}
```

**GitLab CI:**
```yaml
opencode-review:
  image: opencode/opencode:latest
  script:
    - opencode run "review this merge request" --print-logs
```

**Script Integration:**
```bash
#!/bin/bash
# Automate code fixes with OpenCode
for file in $(git diff --name-only); do
  opencode run "fix any bugs in $file" --print-logs
done
```

### Best Practices
- Always use `--print-logs` in CI for audit trail
- Set `--timeout` to prevent runaway executions in pipelines
- Use `--output json` for programmatic consumption of results
- Pin OpenCode version in CI configs for reproducibility
- Store API keys in CI/CD secrets, never in code
- For batch operations, loop over `opencode run` calls rather than crafting mega-prompts
- Exit codes are suitable for `if` conditionals in shell scripts
