# 01 - Getting Started

## 1. Introduction

### Vibe Coding

"Speak, don't touch" — describe what you want in natural language; the AI agent writes the code. You review, iterate, and accept/reject changes. The agent handles file creation, refactoring, debugging, and boilerplate.

### IDE-based vs TUI-based Tools

| Aspect | IDE-based (e.g. Copilot, Cursor) | TUI-based (e.g. OpenCode) |
|--------|----------------------------------|---------------------------|
| Interface | Embedded in editor | Standalone terminal app |
| Scope | Inline completions, chat sidebar | Full agent with file system access |
| Multi-project | Tab/sidebar per file | Sessions per project |
| Automation | Limited | Scriptable via CLI, server mode |
| Remote use | Requires IDE | Terminal + SSH, Web UI, attach |

### OpenCode vs Claude Code vs Codex CLI

| Feature | OpenCode | Claude Code | Codex CLI |
|---------|----------|-------------|-----------|
| License | Open source (Apache 2.0) | Proprietary | Proprietary |
| Model support | 75+ providers, any model | Claude only | GPT/Codex only |
| Free models | 6 built-in (no key needed) | None | None |
| TUI | Full terminal UI | Basic terminal | Basic terminal |
| Desktop app | Yes (macOS/Win/Linux) | No | No |
| IDE extension | Yes (VS Code, JetBrains) | No | VS Code only |
| Web UI | Yes (`opencode web`) | No | No |
| Multi-session | Yes (parallel agents) | No | No |
| Share links | Yes | Yes | No |
| MCP support | Full (local + remote) | Yes | No |
| Plugins/Hooks | Yes | No | No |
| Custom tools | Yes (SDK) | No | No |
| Skills (agent instructions) | Yes | Claude.md only | No |
| LSP integration | Auto-loads LSPs | Basic | Basic |
| GitHub agent | Yes (Actions workflow) | No | No |
| GitLab Duo | Yes | No | No |
| Self-hosted | Yes (Docker, binary) | No | No |
| Enterprise config | Remote `.well-known`, MDM | No | No |

### Who OpenCode Is For

- **Developers** who want an AI coding agent in their terminal
- **Teams** needing shareable sessions and consistent agent configs
- **Enterprises** requiring on-premise, air-gapped, or MDM-managed deployments
- **Multi-model users** who switch between Claude, GPT, Gemini, Qwen, DeepSeek, local models
- **Open source enthusiasts** who want full control and auditability

---

## 2. Installation

### Official One-liner

```bash
curl -fsSL https://opencode.ai/install | bash
```

Parameters:
- `--version` — install a specific version (e.g. `... | bash -s -- --version v0.1.48`)
- `--no-modify-path` — skip adding to PATH

### Package Managers

| Method | Command |
|--------|---------|
| **npm** | `npm install -g opencode-ai` |
| **Bun** | `bun install -g opencode-ai` |
| **pnpm** | `pnpm install -g opencode-ai` |
| **Yarn** | `yarn global add opencode-ai` |
| **Homebrew** | `brew install anomalyco/tap/opencode` |
| **Scoop** (Windows) | `scoop install opencode` |
| **Chocolatey** (Windows) | `choco install opencode` |
| **Arch Linux** | `sudo pacman -S opencode` (stable) / `paru -S opencode-bin` (AUR latest) |
| **Mise** | `mise use -g github:anomalyco/opencode` |
| **Docker** | `docker run -it --rm ghcr.io/anomalyco/opencode` |
| **Desktop (Homebrew cask)** | `brew install --cask opencode-desktop` |
| **Desktop (Scoop)** | `scoop install extras/opencode-desktop` |
| **Manual** | Download binary from [GitHub Releases](https://github.com/anomalyco/opencode/releases) |

### Binary Locations

| Method | Binary Path |
|--------|-------------|
| Official script | `~/.opencode/bin/opencode` |
| npm/pnpm/bun/yarn | global `node_modules/.bin/opencode` |
| Homebrew | `/opt/homebrew/bin/opencode` (Apple Silicon) / `/usr/local/bin/opencode` (Intel) |
| Scoop | `~/scoop/apps/opencode/current/opencode.exe` |

### Windows

**Recommended**: Use [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install) for best performance.

Install OpenCode inside WSL:
```bash
curl -fsSL https://opencode.ai/install | bash
```

Access Windows files via `/mnt/c/`, `/mnt/d/`, etc.

**Native Windows installation options**: Chocolatey, Scoop, npm.

### Troubleshooting

| Symptom | Solution |
|---------|----------|
| `command not found` | Restart terminal; add to PATH: `export PATH="$HOME/.opencode/bin:$PATH"` (add to `~/.zshrc` / `~/.bashrc`) |
| Network timeout | Use proxy (`HTTP_PROXY`/`HTTPS_PROXY`) or alternative install method (npm, scoop) |
| GitHub rate limiting | Wait or use npm/Homebrew instead of the install script |
| Missing `tar`/`unzip` | Install via package manager: `apt install tar unzip` / `brew install gnu-tar` |
| Windows ExecutionPolicy | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| macOS app won't launch | `xattr -cr /Applications/OpenCode.app` |
| Clean uninstall | `opencode uninstall` or manually delete `~/.opencode/`, `~/.local/share/opencode/`, `~/.cache/opencode/` |

---

## 3. Network Configuration

### Proxy Setup

```bash
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
export NO_PROXY=localhost,127.0.0.1
```

**Important**: The TUI communicates with a local HTTP server. You **must** bypass the proxy for `localhost` and `127.0.0.1` via `NO_PROXY` to prevent routing loops.

### Persist in Shell Profile

```bash
# ~/.zshrc or ~/.bashrc
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
export NO_PROXY=localhost,127.0.0.1
```

### Windows (PowerShell)

```powershell
[Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://127.0.0.1:7890", "User")
[Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://127.0.0.1:7890", "User")
[Environment]::SetEnvironmentVariable("NO_PROXY", "localhost,127.0.0.1", "User")
```

### Authenticated Proxy

```bash
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

### Corporate Firewall

- Use `HTTPS_PROXY` for SSL/TLS inspection proxies
- Configure `NODE_EXTRA_CA_CERTS` for custom CA certificates:
  ```bash
  export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
  ```
- Alternative: use an LLM Gateway that supports your proxy authentication (NTLM, Kerberos)

### NO_PROXY Bypass

Comma-separated list of hosts/IPs to bypass proxy. Always include `localhost,127.0.0.1`.

---

## 4. Connect Models

### Core Concept

The API key is your **identity credential** for AI services. OpenCode stores it locally and uses it to authenticate with the provider.

### Configure via TUI

```
/connect
```

Interactive wizard: select a provider, choose auth method (OAuth or manual API key), enter credentials.

### Configure via CLI

```bash
opencode auth login
opencode auth login --provider anthropic
opencode auth login --provider anthropic --method "Manually enter API Key"
```

### View Credentials

```bash
opencode auth list
opencode auth ls
```

### Auth Priority (highest to lowest)

1. Environment variables (e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`)
2. `~/.local/share/opencode/auth.json` (set via `/connect` or `opencode auth login`)
3. Config file provider settings

### Credentials Storage

All credentials stored in `~/.local/share/opencode/auth.json`. This file contains API keys, OAuth tokens, and provider configurations.

### Switch Models in TUI

```
/models
```

Interactive picker showing all available models from all connected providers.

### Set Default Model in Config

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4"
}
```

Format: `"<providerId>/<modelId>"`

---

## 5. Model Providers (ALL)

### Free Models (No API Key Required)

OpenCode ships with built-in free models. No API key, no billing setup needed.

| Model ID | Provider | Context | Notes |
|----------|----------|---------|-------|
| `glm-5-free` | Zhipu | Standard | Reasoning model |
| `minimax-m2.7-free` | MiniMax | 200K ctx | Good for long context |
| `gpt-5-nano` | OpenAI | Standard | Lightweight, fast |
| `kimi-k2.5-free` | Moonshot | 256K ctx | Large context window |
| `big-pickle` | Hidden | — | Easter egg / hidden model |

### DeepSeek

| Item | Value |
|------|-------|
| Env var | `OPENAI_API_KEY` |
| Base URL | `https://api.deepseek.com/v1` |
| Config provider key | `deepseek` |
| Models | `deepseek-chat`, `deepseek-reasoner` |

Usage:
```json
{
  "provider": {
    "deepseek": {
      "options": {
        "baseURL": "https://api.deepseek.com/v1"
      }
    }
  }
}
```

### Zhipu (GLM)

| Item | Value |
|------|-------|
| Env var | `ZHIPU_API_KEY` |
| Config provider key | `zhipu` |
| Models | `glm-5`, `glm-4-plus`, `glm-4`, and more |

### MiniMax

| Item | Value |
|------|-------|
| Env var | `MINIMAX_API_KEY` |
| Config provider key | `minimax` |
| Models | `minimax-m2.7`, `minimax-m2.1`, `minimax-m2.5` |

### Claude (Anthropic)

| Item | Value |
|------|-------|
| Env var | `ANTHROPIC_API_KEY` |
| Config provider key | `anthropic` |
| Models | `claude-sonnet-4`, `claude-opus-4`, `claude-opus-4-5-thinking`, `claude-haiku-4-5`, etc. |
| Prompt caching | `"setCacheKey": true` in provider options |
| Auth methods | API key or OAuth (Claude Pro/Max) |

Note: Anthropic prohibits using Claude Pro/Max subscription in external tools. OpenCode removed bundled plugins for this as of v1.3.0.

Config with caching:
```json
{
  "provider": {
    "anthropic": {
      "options": {
        "setCacheKey": true,
        "timeout": 600000,
        "chunkTimeout": 30000
      }
    }
  }
}
```

Built-in variants: `high` (default high thinking), `max` (maximum thinking budget)

### Claude Code Relay

Use the Claude Code API via an OpenAI-compatible relay:

| Item | Value |
|------|-------|
| Env var | `OPENAI_API_KEY` |
| Base URL | `https://claudecode-relay.example.com/v1` |
| Config provider key | Custom (any key) |

```json
{
  "provider": {
    "claude-code-relay": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Claude Code Relay",
      "options": {
        "baseURL": "https://claudecode-relay.example.com/v1"
      },
      "models": {
        "claude-sonnet-4-20250514": {}
      }
    }
  }
}
```

### Ollama (Local Models)

| Item | Value |
|------|-------|
| Env var | `OLLAMA_API_KEY` (optional) |
| Base URL | `http://localhost:11434/v1` |
| Config provider key | `ollama` |
| Prefix env var | `OPENCODE_OLLAMA_MODEL_PREFIX` |

```json
{
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "llama2": { "name": "Llama 2" },
        "qwen3-coder:a3b": { "name": "Qwen3-Coder (local)" }
      }
    }
  }
}
```

Tip: If tool calls aren't working, increase `num_ctx` in Ollama (start at 16k–32k). Ollama can auto-configure itself for OpenCode — see [Ollama integration docs](https://docs.ollama.com/integrations/opencode).

### OpenAI

| Item | Value |
|------|-------|
| Env var | `OPENAI_API_KEY` |
| Config provider key | `openai` |
| Models | `gpt-4o`, `gpt-5`, `gpt-5-nano`, `o3`, `o4-mini`, etc. |
| Reasoning format | `o*` models support `reasoningEffort`, `textVerbosity`, `reasoningSummary` |
| Auth methods | API key or OAuth (ChatGPT Plus/Pro) |

Built-in variants: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`

Recommended models: GPT 5.2, GPT 5.1 Codex

```json
{
  "provider": {
    "openai": {
      "models": {
        "gpt-5": {
          "options": {
            "reasoningEffort": "high",
            "textVerbosity": "low",
            "reasoningSummary": "auto",
            "include": ["reasoning.encrypted_content"]
          }
        }
      }
    }
  }
}
```

### Alibaba (Qwen)

| Item | Value |
|------|-------|
| Env var | `DASHSCOPE_API_KEY` or `QWEN_API_KEY` |
| Base URL | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Config provider key | `dashscope` or `qwen` |
| Models | `qwen-plus`, `qwen-max`, `qwen-turbo`, `qwen3-235b-a22b`, `qwen3-coder-480b` |

```json
{
  "provider": {
    "dashscope": {
      "options": {
        "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1"
      }
    }
  }
}
```

### GitHub Copilot

| Item | Value |
|------|-------|
| Auth | OAuth device flow (`https://github.com/login/device`) or `GITHUB_TOKEN` |
| Config provider key | `github-copilot` |
| Web search | Enabled (automatic) |
| Models | `gpt-4o`, `claude-sonnet-4`, `gemini-2.5-pro` (some require Pro+ subscription) |

Connection: `/connect` → select GitHub Copilot → enter device code at `https://github.com/login/device`.

### Google / Gemini

| Item | Value |
|------|-------|
| Env var | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| Config provider key | `google` or `gemini` |
| Models | `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-3-pro` |

Built-in variants: `low`, `high`

### Other Providers (Quick Reference)

| Provider | Env Var(s) | Config Key | Notes |
|----------|-----------|------------|-------|
| 302.AI | via `/connect` | `302ai` | Multi-model gateway |
| Amazon Bedrock | `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` / `AWS_PROFILE` / `AWS_BEARER_TOKEN_BEDROCK` | `amazon-bedrock` | Supports VPC endpoints, custom inference profiles |
| Atomic Chat | — | custom | Local models, endpoint `http://127.0.0.1:1337/v1` |
| Azure OpenAI | `AZURE_RESOURCE_NAME` | `azure` | Deployment name must match model name |
| Azure Cognitive Services | `AZURE_COGNITIVE_SERVICES_RESOURCE_NAME` | `azure-cognitive-services` | |
| Baseten | via `/connect` | `baseten` | |
| Cerebras | via `/connect` | `cerebras` | Models include Qwen 3 Coder 480B |
| Cloudflare AI Gateway | `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_GATEWAY_ID` + `CLOUDFLARE_API_TOKEN` | `cloudflare-ai-gateway` | Unified billing, multi-provider |
| Cloudflare Workers AI | `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_KEY` | `cloudflare-workers-ai` | |
| Cortecs | via `/connect` | `cortecs` | |
| Deep Infra | via `/connect` | `deepinfra` | |
| DigitalOcean | OAuth or Model Access Key + `DIGITALOCEAN_ACCESS_TOKEN` | `digitalocean` | Inference Routers (OAuth only) |
| Fireworks AI | via `/connect` | `fireworks` | |
| FrogBot | via `/connect` | `frogbot` | |
| GitLab Duo | `GITLAB_TOKEN` / OAuth | `gitlab` | Experimental; requires Premium/Ultimate; models: `duo-chat-haiku-4-5`, `duo-chat-sonnet-4-5`, `duo-chat-opus-4-5`; DAP workflow models |
| GMI Cloud | via `/connect` | `gmicloud` | |
| Google Vertex AI | `GOOGLE_CLOUD_PROJECT` + `GOOGLE_APPLICATION_CREDENTIALS` / `gcloud auth` | `google-vertex` | `VERTEX_LOCATION` (default `global`) |
| Groq | via `/connect` | `groq` | |
| Helicone | via `/connect` | `helicone` | LLM observability + gateway; custom headers for caching, sessions |
| Hugging Face | HF token with inference permission | `huggingface` | 17+ provider backends |
| IO.NET | via `/connect` | `ionet` | 17 optimized models |
| llama.cpp | — | custom | Local, endpoint `http://127.0.0.1:8080/v1` |
| LLM Gateway | via `/connect` | `llmgateway` | |
| LM Studio | — | custom | Local, endpoint `http://127.0.0.1:1234/v1` |
| Moonshot AI | via `/connect` | `moonshot` | Kimi K2 |
| NVIDIA | `NVIDIA_API_KEY` | `nvidia` | Nemotron models; on-prem NIM supported |
| Nebius Token Factory | via `/connect` | `nebius` | |
| Ollama Cloud | via `/connect` | `ollamacloud` | Must `ollama pull` cloud models first |
| OpenCode Zen | API key from `https://opencode.ai/auth` | `opencode` | Tested/verified models; recommended for beginners |
| OpenCode Go | Subscription from `https://opencode.ai/auth` | `opencode-go` | Low-cost subscription for open coding models |
| OpenRouter | via `/connect` | `openrouter` | Multi-model router; `provider.order` for fallback |
| Together AI | via `/connect` | `together` | |
| Venice AI | via `/connect` | `venice` | |
| Vercel AI Gateway | via `/connect` | `vercel-ai-gateway` | |
| xAI | via `/connect` | `xai` | Grok models |
| Z.AI | via `/connect` | `zai` | |
| ZenMux | via `/connect` | `zenmux` | |

### Provider Config Options (Common)

```json
{
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 300000,
        "chunkTimeout": 30000,
        "setCacheKey": true,
        "baseURL": "https://api.anthropic.com/v1"
      },
      "blacklist": ["claude-opus-4-20250514"],
      "whitelist": ["claude-sonnet-4-20250514"]
    }
  }
}
```

- `timeout` — Request timeout in ms (default 300000; `false` to disable)
- `chunkTimeout` — Timeout between stream chunks (default 30000)
- `setCacheKey` — Always set a cache key for the provider
- `baseURL` — Custom endpoint URL
- `blacklist` — Array of model IDs to hide from the picker
- `whitelist` — Array of model IDs to keep (hides all others)
- `models` — Map of model ID → config for per-model overrides

### Disable / Enable Providers

```json
{
  "disabled_providers": ["openai", "gemini"],
  "enabled_providers": ["anthropic", "opencode"]
}
```

`disabled_providers` takes priority over `enabled_providers`.

### Custom Provider

For any OpenAI-compatible API not listed above:

```json
{
  "provider": {
    "my-custom-provider": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "My Provider",
      "options": {
        "baseURL": "https://api.example.com/v1",
        "apiKey": "{env:MY_API_KEY}"
      },
      "models": {
        "my-model-1": { "name": "My Model 1" }
      }
    }
  }
}
```

---

## 6. Auto Update

### Default Behavior

OpenCode automatically downloads updates on startup.

### Disable Auto Update

```json
{
  "autoupdate": false
}
```

### Notify Only

```json
{
  "autoupdate": "notify"
}
```

Shows a notification when a new version is available without auto-downloading. Only works when not installed via a package manager (Homebrew, npm, etc.).

### Environment Variable

```bash
export OPENCODE_DISABLE_AUTOUPDATE=true
```

### Manual Upgrade

```bash
opencode upgrade
opencode upgrade v0.1.48
opencode upgrade --method npm
opencode upgrade --method brew
```

Available `--method` values: `curl`, `npm`, `pnpm`, `bun`, `brew`

---

## 7. Desktop App

### Availability

Beta on macOS, Windows, and Linux.

### Installation

- **Download**: [GitHub Releases](https://github.com/anomalyco/opencode/releases)
- **Homebrew cask**: `brew install --cask opencode-desktop`
- **Scoop**: `scoop install extras/opencode-desktop`

### Terminal vs Desktop

| Feature | Terminal (TUI) | Desktop App |
|---------|---------------|-------------|
| Window management | Single terminal window | Multi-window |
| Notifications | Terminal bell + attention config | OS-level notifications |
| Start server | `opencode` (built-in) | Background sidecar (`opencode-cli`) |
| File dropping | Drag to terminal | Native drag-and-drop |
| WebView | No | Embedded WebView2 (Windows) |

### Desktop App Troubleshooting

| Issue | Solution |
|-------|----------|
| Won't start / blank window | Fully quit and relaunch; macOS: `OpenCode` menu → Reload Webview |
| Crashing on launch | Disable plugins: clear `plugin` from `~/.config/opencode/opencode.json(c)` and check `~/.config/opencode/plugins/` |
| Corrupted cache | Delete `~/.cache/opencode` |
| Connection failed | Clear default server URL in Server picker; remove `server.port`/`server.hostname` from config; unset `OPENCODE_PORT` |
| Linux Wayland blank | Launch with `OC_ALLOW_WAYLAND=1` or switch to X11 session |
| Windows WebView2 | Install/update Microsoft Edge WebView2 Runtime |
| Notifications not showing | Enable OS notifications for OpenCode; window must not be focused |
| Last resort reset | Delete `opencode.settings.dat`, `opencode.global.dat`, `opencode.workspace.*.dat` from app data directory |

### WSL + Desktop

1. In WSL: `opencode serve --hostname 0.0.0.0 --port 4096`
2. Connect Desktop to `http://localhost:4096`
3. Secure with: `OPENCODE_SERVER_PASSWORD=your-password opencode serve --hostname 0.0.0.0`

### Storage Locations

| Data | Path |
|------|------|
| Config | `~/.config/opencode/opencode.json` |
| TUI config | `~/.config/opencode/tui.json` |
| Auth credentials | `~/.local/share/opencode/auth.json` |
| Logs | `~/.local/share/opencode/log/` |
| Cache | `~/.cache/opencode/` |
| Session data | `~/.local/share/opencode/project/` |
| Install binary | `~/.opencode/bin/opencode` |
| Desktop app data (macOS) | `~/Library/Application Support/` |
| Desktop app data (Linux) | `~/.local/share/` |
| Desktop app data (Windows) | `%APPDATA%` |
| Managed config (macOS) | `/Library/Application Support/opencode/` |
| Managed config (Linux) | `/etc/opencode/` |
| Managed config (Windows) | `%ProgramData%\opencode` |
