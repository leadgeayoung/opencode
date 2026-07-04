# Appendix: Complete Reference

## CLI Reference (cli.md)

### Top-Level Commands

| Command | Description |
|---|---|
| `opencode` | Start the terminal UI (TUI) session |
| `opencode run [message..]` | Non-interactive execution mode |
| `opencode serve` | Start OpenCode in server mode (HTTP API) |
| `opencode web` | Start the web interface (browser-based UI) |
| `opencode auth login` | Authenticate with OpenCode Zen or a provider |
| `opencode auth list` | List authenticated accounts |
| `opencode export` | Export the current session to a JSON file |
| `opencode import <url\|file>` | Import a session from a URL or JSON file |
| `opencode github install` | Install the OpenCode GitHub App |
| `opencode upgrade` | Upgrade OpenCode to the latest version |
| `opencode uninstall` | Remove OpenCode from the system |
| `opencode debug` | Run diagnostic checks |
| `opencode debug config` | View effective configuration |
| `opencode debug config --json` | View config as JSON |

### Common Global Flags

| Flag | Description |
|---|---|
| `-y, --yes` | Skip confirmation prompts |
| `--log-level <level>` | Set log level (TRACE, DEBUG, INFO, WARN, ERROR) |
| `--no-color` | Disable colored output |
| `--config <path>` | Specify config file path |
| `--help` | Show help |
| `--version` | Show version |

### `opencode run` Flags

| Flag | Description |
|---|---|
| `-m, --model <model>` | Model/variant to use |
| `--print-logs` | Print execution logs |
| `--timeout <seconds>` | Execution timeout |
| `--no-progress` | Suppress progress indicators |
| `--output <format>` | Output format (text, json) |
| `--log-level <level>` | Log level override |

### `opencode serve` Flags

| Flag | Description |
|---|---|
| `--port <port>` | Server port (default: 8080) |
| `--host <host>` | Bind address (default: localhost) |
| `--max-sessions <n>` | Max concurrent sessions |

---

## Built-in Commands (commands.md)

### Session Management

| Command | Description |
|---|---|
| `/new` | Start a fresh session (clears current context) |
| `/sessions` | List all saved/resumed sessions |
| `/export` | Export current session to JSON file |
| `/import` | Import a session from file or URL |
| `/share` | Create a public share link for the session |

### Undo/Redo

| Command | Description |
|---|---|
| `/undo` | Undo the last action/turn |
| `/redo` | Redo a previously undone action |

### Context Management

| Command | Description |
|---|---|
| `/compact` | Manually trigger context compaction |
| `/summarize` | Generate a summary of the session so far |
| `/details` | Expand a compacted section back to full detail |
| `/copy` | Copy the last response to clipboard |
| `/editor` | Open the system editor for multi-line input |

### Model & Provider

| Command | Description |
|---|---|
| `/models` | List all available models |
| `/model <name>` | Switch to a different model/variant |

### UI & Display

| Command | Description |
|---|---|
| `/theme <name>` | Switch to a specific theme |
| `/themes` | List all available themes |
| `/version` | Show OpenCode version info |
| `/stats` | Show session statistics (tokens used, turns, etc.) |
| `/init` | Show the welcome/introduction screen |

### Help & Exit

| Command | Description |
|---|---|
| `/help` | Show help information |
| `/exit` | Exit the session |

---

## Config Reference (config-ref.md)

### Top-Level Config Keys (opencode.json)

| Key | Type | Description |
|---|---|---|
| `provider` | string | AI provider (e.g., `"openai"`, `"anthropic"`) |
| `model` | string | Default model ID |
| `variants` | object | Named model variants with different thinking budgets |
| `systemPrompt` | string | Custom system prompt |
| `compaction` | object | Context compaction settings (`auto`, `prune`, `reserved`) |
| `share` | string | Share behavior: `"manual"`, `"auto"`, `"disabled"` |
| `themes` | object | Theme configuration |
| `keybindings` | object | Custom keybindings |
| `logLevel` | string | Default log level |
| `plugins` | object | Plugin configuration |
| `agents` | object | Custom agent definitions |
| `enterprise` | object | Enterprise settings (`url`, custom branding) |
| `experimental` | object | Feature flags for experimental capabilities |

### Provider Config

| Key | Type | Description |
|---|---|---|
| `apiKey` | string | API key (alternative to env var) |
| `baseUrl` | string | Custom API endpoint |
| `model` | string | Model to use with this provider |
| `maxTokens` | number | Max output tokens |
| `temperature` | number | Sampling temperature |
| `thinking` | number | Thinking budget (for supported models) |

### Plugin Config

| Key | Type | Description |
|---|---|---|
| `path` | string | Path to plugin file or directory |
| `enabled` | boolean | Whether the plugin is active |
| `config` | object | Plugin-specific configuration |

---

## Ecosystem (ecosystem.md)

### Official Integrations

| Integration | Type | Description |
|---|---|---|
| **GitHub App** | Platform | Issue/PR comments, Actions workflows |
| **GitLab CI/CD** | Platform | Runner-based automation, Duo chat |
| **OpenCode Zen** | Service | Hosted service with free models |

### Editor Integrations

| Editor | Integration Method |
|---|---|
| VS Code | OpenCode extension (command palette, shortcuts) |
| JetBrains | OpenCode plugin (IntelliJ, PyCharm, WebStorm, etc.) |
| Neovim | opencode.nvim plugin |
| Emacs | opencode.el package |
| Terminal | Native TUI (built-in, no plugin needed) |

### Companion Tools

| Tool | Description |
|---|---|
| **opencode-action** | GitHub Action for CI/CD pipelines |
| **opencode-gitlab** | GitLab CI/CD templates |
| **opencode-sdk** | SDK for building custom plugins and integrations |
| **opencode-api** | REST API for programmatic access |

### Community Ecosystem

- **Plugins**: Custom plugins for linting, testing, deployment, etc.
- **Agents**: Pre-built agents for specialized tasks
- **Themes**: Community-contributed color themes
- **Prompts**: Shared prompt templates and patterns
- **Workflows**: Reusable automation workflows

---

## Experimental Features (experimental-features.md)

### Feature Flags

Experimental features must be explicitly enabled via config:

```json
{
  "experimental": {
    "batch_tool": false,
    "openTelemetry": false,
    "agent_networks": false,
    "multi_modal": false,
    "streaming_ui": false
  }
}
```

| Feature | Flag | Description |
|---|---|---|
| **Batch Tool** | `batch_tool` | Execute multiple tool calls in parallel batches |
| **OpenTelemetry** | `openTelemetry` | Export traces to OpenTelemetry collector |
| **Agent Networks** | `agent_networks` | Allow agents to spawn sub-agents and form networks |
| **Multi-modal** | `multi_modal` | Enable image/audio input support |
| **Streaming UI** | `streaming_ui` | Real-time streaming of model output in TUI |

### Warnings
- Experimental features may change or be removed without major version bump
- Performance impact is not guaranteed
- Some features require specific model/provider support
- Report bugs on GitHub Issues

---

## FAQ (faq.md)

### General

**Q: What is OpenCode?**
A: An AI-powered coding assistant that operates in your terminal. It understands your codebase, can edit files, run commands, search the web, and automate development workflows.

**Q: Is OpenCode free?**
A: OpenCode itself is open-source and free. You pay for your own AI provider API usage, or use OpenCode Zen's hosted free models.

**Q: What models does OpenCode support?**
A: OpenAI (GPT-4o, GPT-4o-mini), Anthropic (Claude), Google (Gemini), and many others. See providers.md for the full list.

**Q: Does OpenCode work offline?**
A: No, OpenCode requires an internet connection to communicate with AI providers.

**Q: Can OpenCode access my files?**
A: Yes, OpenCode reads files you explicitly ask it to read or that it discovers while searching. It never uploads your code to third parties — only to the AI provider you've configured.

### Configuration

**Q: Where is the config file?**
A: Default location: `~/.config/opencode/opencode.json` (Linux/macOS) or `%APPDATA%\opencode\opencode.json` (Windows).

**Q: Can I have project-specific config?**
A: Yes, place an `opencode.json` in your project root. Project configs merge with global config.

**Q: How do I add a new provider?**
A: Set the provider's API key as an environment variable or in config, then select the model.

### Troubleshooting

**Q: Why is OpenCode not responding?**
A: Check your API key, provider status, rate limits, and network connection.

**Q: Why is my config not applying?**
A: Run `opencode debug config` to see the resolved configuration.

**Q: How do I reset OpenCode?**
A: Delete the config directory or run `opencode uninstall` and reinstall.

---

## Keybinds (keybinds.md)

### Default Keybind Reference

| Shortcut | Action | Context |
|---|---|---|
| `Enter` | Submit message | Input |
| `Shift+Enter` | New line in input | Input |
| `Ctrl+C` | Cancel current generation | Any |
| `Ctrl+D` | Exit | Any |
| `Ctrl+L` | Clear screen | Any |
| `Ctrl+R` | Regenerate last response | Any |
| `Ctrl+Z` | Undo | Any |
| `Ctrl+Y` | Redo | Any |
| `Ctrl+S` | Save session | Any |
| `Ctrl+F` | Search within output | Output |
| `Ctrl+T` | Cycle thinking depth | Any |
| `Ctrl+E` | Open in editor (`/editor`) | Input |
| `Ctrl+P` | Toggle preview mode | Output |
| `Ctrl+U` | Clear input | Input |
| `Ctrl+W` | Delete word backward | Input |
| `Tab` | Autocomplete / indent | Input |
| `Up/Down` | Navigate history | Input |
| `PgUp/PgDn` | Scroll output | Output |
| `Home/End` | Jump to start/end | Output |
| `Ctrl+A` | Select all | Input/Output |
| `Ctrl+X C` | `/compact` | Any |
| `Ctrl+X S` | `/share` | Any |
| `Ctrl+X E` | `/export` | Any |
| `Ctrl+X I` | `/import` | Any |
| `Ctrl+X M` | `/models` | Any |
| `Ctrl+X H` | `/help` | Any |

### Custom Keybindings

Keybindings can be customized in `opencode.json`:

```json
{
  "keybindings": {
    "compact": "ctrl+k ctrl+c",
    "share": "ctrl+k ctrl+s"
  }
}
```

Each keybinding maps a command name to a key chord. Available commands match the built-in commands list.

---

## Migration (migration.md)

### Version-to-Version Migration

#### v0.x → v1.0

| Change | Action Required |
|---|---|
| Config format changed | Run `opencode upgrade` to auto-migrate config |
| Plugin API v1 | Update custom plugins to new API |
| New `provider` key required | Add provider configuration |
| `model` key moved | Move model setting under provider |
| Session format v2 | Old sessions are auto-converted on open |

#### v1.0 → v1.1

| Change | Action Required |
|---|---|
| `compaction` defaults changed | Review compaction settings if relying on old behavior |
| New `share` key | Add share config or accept default |
| Deprecated `--verbose` flag | Use `--log-level DEBUG` instead |

#### v1.1 → v1.2

| Change | Action Required |
|---|---|
| Plugin manifest v2 | Update plugin metadata format |
| Theme format updated | Rebuild custom themes |
| `experimental` features opt-in | Enable desired experimental features explicitly |

### General Migration Steps

1. **Backup**: Save your config directory
2. **Upgrade**: Run `opencode upgrade`
3. **Check**: Run `opencode debug config` to verify settings
4. **Test**: Run a simple task to confirm everything works
5. **Rollback**: If issues arise, restore backup and downgrade

---

## Prompt Guidelines (prompt-guidelines.md)

### Best Practices

**Be Specific:**
- Bad: "Fix this code"
- Good: "Fix the race condition in `src/scheduler.ts` where concurrent writes to `taskQueue` cause data loss"

**Provide Context:**
- Reference file paths and line numbers
- Mention what you've already tried
- State the expected behavior vs actual behavior

**Ask One Thing at a Time:**
- Break complex requests into sequential steps
- Each turn should have a clear goal
- Use `/new` for unrelated tasks

**Use the Right Thinking Depth:**
- Shallow: quick edits, simple questions, file reads
- Deep: debugging, architecture design, complex refactoring

**Leverage Commands:**
- `/compact` before switching context
- `/undo` when the model goes wrong
- `/details` to expand compacted sections

### Prompt Structure

```
[Context] In src/auth.ts, the login function...
[Goal] I need to add rate limiting...
[Constraints] Must use existing redis client, don't add new deps...
[What I've tried] I added a counter but it doesn't reset...
[Expected] After 5 failed attempts, block for 15 minutes...
```

### Anti-Patterns

| Anti-Pattern | Why | Better |
|---|---|---|
| "Make it work" | Too vague | Specify the exact error and expected fix |
| "Rewrite everything" | Loses context, introduces bugs | Make incremental, targeted changes |
| "Do X and Y and Z" | Context overflow, model loses track | One request per turn |
| No context provided | Model guesses, wastes tokens | Include file paths, error messages |
| Vague error descriptions | Model can't help effectively | Paste exact error output |

---

## Prompt Templates (prompts.md)

### Magic Prompts (Scenario-Based Templates)

OpenCode includes a library of prompt templates for common scenarios. These are called "magic prompts" because they package best-practice prompting into reusable templates.

#### Code Review
```
Review the code in [file path]. Check for:
1. Security vulnerabilities
2. Performance issues
3. Bug patterns
4. Code style adherence
5. Missing edge cases
```

#### Debugging
```
I'm seeing this error: [paste error]
In file: [path]
When I: [steps to reproduce]
What I've tried: [attempted fixes]
Expected behavior: [what should happen]
Actual behavior: [what happens instead]
```

#### Architecture Design
```
Design a solution for: [problem]
Requirements:
- [requirement 1]
- [requirement 2]
Constraints:
- [constraint 1]
Current system: [existing architecture if any]
Please provide: options, trade-offs, recommendation
```

#### Refactoring
```
Refactor [file/module] to improve:
- [maintainability | performance | readability | testability]
Current issues: [known problems]
Keep: [things to preserve]
Target pattern/style: [optional preference]
```

#### Test Generation
```
Write tests for [file/function].
Testing framework: [jest | pytest | etc.]
Coverage targets:
- Happy path
- Error cases
- Edge cases
- [specific cases]
```

#### Documentation
```
Generate documentation for [module/function].
Format: [JSDoc | docstring | Markdown]
Audience: [developers | users | operators]
Include: [parameters | examples | return values | edge cases]
```

#### Commit Message
```
Generate a commit message for these changes.
Style: [conventional commits | angular | custom]
Scope: [affected module]
Include: summary, motivation, affected areas
```

### Custom Templates

Users can define custom prompt templates in config:

```json
{
  "prompts": {
    "security-audit": "Run a security audit on [path]. Check for: OWASP Top 10, hardcoded secrets, dependency vulnerabilities...",
    "onboard": "Explain the codebase structure in [path] for a new developer..."
  }
}
```

Invoked via: `/prompt security-audit src/auth.ts`

---

## Providers (providers.md)

### Supported Providers

| Provider | Models | Config Key | Auth |
|---|---|---|---|
| **OpenAI** | GPT-4o, GPT-4o-mini, o1, o3 | `openai` | `OPENAI_API_KEY` |
| **Anthropic** | Claude 4 Sonnet, Claude 4 Opus, Claude 3.5 Haiku, Claude 3.5 Sonnet | `anthropic` | `ANTHROPIC_API_KEY` |
| **Google** | Gemini 2.5 Pro, Gemini 2.5 Flash | `google` | `GOOGLE_API_KEY` |
| **OpenCode Zen** | Free hosted models (varies) | `zen` | Zen account login |
| **Azure OpenAI** | GPT-4o, GPT-4o-mini | `azure` | `AZURE_OPENAI_KEY` + endpoint |
| **AWS Bedrock** | Claude, Llama, Mistral | `bedrock` | AWS credentials |
| **GCP Vertex AI** | Gemini, Claude | `vertex` | GCP credentials |
| **Ollama** | Any local model | `ollama` | None (localhost) |
| **LM Studio** | Any local model | `lmstudio` | None (localhost) |
| **Together AI** | Various open models | `together` | `TOGETHER_API_KEY` |
| **Groq** | Llama, Mixtral, Gemma | `groq` | `GROQ_API_KEY` |
| **Fireworks** | Various open models | `fireworks` | `FIREWORKS_API_KEY` |
| **Perplexity** | Sonar, Sonar Pro | `perplexity` | `PERPLEXITY_API_KEY` |
| **DeepSeek** | DeepSeek V3, R1 | `deepseek` | `DEEPSEEK_API_KEY` |
| **Mistral** | Mistral Large, Small | `mistral` | `MISTRAL_API_KEY` |
| **OpenRouter** | Multi-provider access | `openrouter` | `OPENROUTER_API_KEY` |
| **Custom** | Any OpenAI-compatible API | `custom` | Varies |

### Provider Configuration Example

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4",
  "anthropic": {
    "apiKey": "sk-ant-...",
    "maxTokens": 8192,
    "thinking": 4096
  },
  "variants": {
    "fast": { "model": "claude-3-5-haiku", "thinking": 0 },
    "deep": { "model": "claude-4-opus", "thinking": 32000 }
  }
}
```

### Provider Selection
- Multiple providers can be configured simultaneously
- Switch between them at any time with `/model`
- Each provider can have multiple model variants
- Fallback: if a provider fails, OpenCode can switch to an alternative provider

---

## Troubleshooting (troubleshoot.md)

### Common Issues and Solutions

#### Installation Issues
| Issue | Solution |
|---|---|
| Permission denied | Reinstall without sudo or use a package manager |
| Command not found | Check PATH, reinstall, or use full path |
| Windows execution policy | Set `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| macOS quarantine | `xattr -d com.apple.quarantine $(which opencode)` |

#### Authentication Issues
| Issue | Solution |
|---|---|
| Invalid API key | Verify key has correct prefix and is not expired |
| Rate limited | Wait, reduce request frequency, or upgrade plan |
| Provider not responding | Check provider status page |
| Unauthorized (401) | Regenerate API key, check permissions |

#### Connection Issues
| Issue | Solution |
|---|---|
| Network timeout | Check proxy/firewall, increase timeout |
| DNS resolution | Check network, try 8.8.8.8 |
| SSL/TLS error | Update CA certificates, check system time |
| Proxy issues | Set `HTTP_PROXY` / `HTTPS_PROXY` environment variables |

#### Performance Issues
| Issue | Solution |
|---|---|
| Slow responses | Switch to faster model, reduce thinking budget, check network |
| High token usage | Enable compaction, use `prune: true`, reduce context |
| Memory issues | Use a smaller model, reduce max output tokens |
| UI lag | Disable animations, use simpler theme |

#### Session Issues
| Issue | Solution |
|---|---|
| Session lost | Check `~/.local/share/opencode/sessions/` for backups |
| Share link broken | Verify `enterprise.url`, or regenerate the link |
| Export fails | Check disk space, write permissions |
| Import fails | Verify file format, check for corruption |

#### Git Integration
| Issue | Solution |
|---|---|
| `opencode github install` fails | Verify `gh` CLI is authenticated, re-auth with `gh auth login` |
| Workflow not triggering | Check Actions permissions, branch protections |
| Secrets not found | Verify secret names match exactly |
| Bot not responding | Check workflow logs for errors |

---

## OpenCode Zen (zen.md)

### Overview
OpenCode Zen is the **hosted service** that provides:
- Free AI models (no API key needed)
- Web-based interface
- Session sharing backend
- Managed infrastructure

### Features

| Feature | Description |
|---|---|
| **Free Models** | Use without any API key or billing setup |
| **Web Interface** | Full OpenCode experience in the browser |
| **Zero Configuration** | No setup required beyond login |
| **Session Sync** | Sessions available across devices |
| **Share Backend** | Powers the `/share` functionality |
| **Custom Domains** | Enterprise self-hosting option |

### Getting Started with Zen

```bash
opencode auth login
# Follow the browser prompt to authenticate
opencode web
# Opens the web interface in your default browser
```

Or use the TUI with Zen as the default provider:
```bash
opencode
# Uses Zen's free models automatically after login
```

### Zen vs Local Setup

| Aspect | Zen | Local (Custom Provider) |
|---|---|---|
| API Key | Not needed | Required |
| Model Access | Free models | Any supported provider |
| Interface | Web + TUI | TUI (web optional) |
| Data Privacy | Shared infrastructure | Your own provider |
| Setup Time | Minutes | Minutes to hours |
| Cost | Free | API usage costs |
| Custom Models | No | Yes (Ollama, etc.) |
| Offline | No | No (except local models) |

### Authentication
- Login via browser-based OAuth flow
- `opencode auth login` opens the Zen login page
- `opencode auth list` shows authenticated sessions
- Tokens are stored locally in the config directory
- Logout: remove the token file from config directory

### Web Interface
- Full feature parity with TUI
- Real-time streaming of responses
- Session management
- File browser (access to permitted directories)
- Theme support
- Keyboard shortcuts (same as TUI)

### Data & Privacy
- Sessions are stored on Zen servers
- Share links are hosted on `opncd.ai`
- Enterprise customers can self-host the backend
- See the privacy policy for full details
- Sessions can be deleted from the Zen dashboard

### Limitations
- Free models have rate limits and lower priority
- Not all experimental features are available on Zen
- Some provider-specific features may not work with Zen models
- Web interface requires a modern browser (Chrome, Firefox, Safari, Edge)
