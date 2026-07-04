# MCP (Model Context Protocol) Reference

> Covers: `07a-mcp-basics`, `07b-mcp-advanced`, `07c-mcp-chrome-devtools`

---

## 1. Overview

MCP = **Model Context Protocol**. A standard that connects external services to AI assistants so they can call databases, search engines, monitoring platforms, browsers, and other tools in real time.

---

## 2. MCP Configuration

Configure MCP servers under the `"mcp"` key in `opencode.json` / `opencode.jsonc`:

```jsonc
{
  "mcp": {
    "context7": {
      "type": "local",
      "command": ["npx", "-y", "@upstash/context7-mcp"]
    },
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "headers": {
        "Authorization": "Bearer <token>"
      },
      "oauth": {
        "clientId": "xxx",
        "clientSecret": "xxx",
        "scope": "read write"
      }
    },
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    },
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxx"
      }
    },
    "brave-search": {
      "type": "local",
      "command": ["npx", "-y", "@anthropic/brave-search-mcp"],
      "env": {
        "BRAVE_API_KEY": "xxx"
      }
    }
  }
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | `"local"` \| `"remote"` | How the MCP server runs |
| `command` | `string[]` | **Local only** — executable + arguments |
| `url` | `string` | **Remote only** — HTTP endpoint |
| `headers` | `Record<string,string>` | **Remote only** — HTTP headers (e.g. `Authorization`) |
| `oauth` | `object \| false` | **Remote only** — OAuth 2.0 credentials; set `false` to disable auto-detection |
| `env` | `Record<string,string>` | **Local only** — environment variables |
| `enabled` | `boolean` | Set `false` to disable a server without removing its config |
| `disabled` | `boolean` | Alias for disabling |

### Local MCP Servers

Run as a **subprocess** of OpenCode. The `command` array specifies the executable and its arguments.

**Via npx (recommended for npm packages):**
```jsonc
"my-tool": {
  "type": "local",
  "command": ["npx", "-y", "some-mcp-package"]
}
```

**Via direct binary:**
```jsonc
"my-tool": {
  "type": "local",
  "command": ["node", "path/to/server.js"]
}
```

**Passing environment variables:**
```jsonc
"postgres": {
  "type": "local",
  "command": ["npx", "-y", "@anthropic/server-postgres"],
  "env": {
    "PGHOST": "localhost",
    "PGPORT": "5432",
    "PGUSER": "user",
    "PGPASSWORD": "pass",
    "PGDATABASE": "mydb"
  }
}
```

### Remote MCP Servers

Connect over **HTTP(S)**. Supports optional headers and OAuth 2.0.

**Minimal remote:**
```jsonc
"my-remote": {
  "type": "remote",
  "url": "https://mcp.example.com/mcp"
}
```

**With headers:**
```jsonc
"my-remote": {
  "type": "remote",
  "url": "https://mcp.example.com/mcp",
  "headers": {
    "Authorization": "Bearer sk-xxx"
  }
}
```

**Disabling OAuth auto-detection:**
```jsonc
"my-remote": {
  "type": "remote",
  "url": "https://mcp.example.com/mcp",
  "oauth": false
}
```

### Disabling MCP Servers

```jsonc
{
  "mcp": {
    "some-server": {
      "enabled": false,
      "type": "local",
      "command": ["npx", "-y", "some-package"]
    }
  }
}
```

---

## 3. OAuth Authentication (07b)

Remote MCP servers support the **OAuth 2.0** flow.

- Auto-detects whether an endpoint requires OAuth
- Use the `"oauth"` config block to provide credentials:

```jsonc
{
  "mcp": {
    "my-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret",
        "scope": "read write"
      }
    }
  }
}
```

- Set `"oauth": false` to skip OAuth auto-detection entirely (useful for servers that return confusing OAuth headers)

---

## 4. Permission Integration

MCP tools integrate with OpenCode's **permission system**. Every MCP tool is addressable as:

```
mcp.<server_name>.<tool_name>
```

### Granular Permission Rules

```jsonc
{
  "permission": {
    "mcp.filesystem.read_file": "allow",
    "mcp.filesystem.write_file": "ask",
    "mcp.github.create_issue": "ask",
    "mcp.postgres.query": "ask",
    "mcp.sentry.*": "deny"
  }
}
```

### Wildcard Permissions

```jsonc
{
  "permission": {
    "mcp.myserver_*": "allow"
  }
}
```

This pattern-matches any tool from servers whose name starts with `myserver`.

### Permission Levels

| Level | Behavior |
|-------|----------|
| `"allow"` | Auto-approved, no prompt |
| `"deny"` | Blocked, no prompt |
| `"ask"` | Prompts user for approval each time |

---

## 5. Context Cost

- MCP tools become available to the AI, but **consume context window**
- More MCP servers / tools → **faster context limit hit**
- Be selective: only enable servers you actually need for the current task
- Consider disabling rarely-used servers to preserve context budget

---

## 6. Common MCP Servers

| Server | Package | Use Case |
|--------|---------|----------|
| **Filesystem** | `@modelcontextprotocol/server-filesystem` | Read/write files, directory listing |
| **GitHub** | `@modelcontextprotocol/server-github` | Issues, PRs, repos, search |
| **PostgreSQL** | `@anthropic/server-postgres` | Query PostgreSQL databases |
| **SQLite** | `@anthropic/server-sqlite` | Query SQLite databases |
| **Puppeteer** | `@anthropic/server-puppeteer` | Browser automation |
| **Brave Search** | `@anthropic/brave-search-mcp` | Web search via Brave |
| **Fetch** | `@modelcontextprotocol/server-fetch` | HTTP fetching |
| **Sentry** | `@sentry/mcp` | Error monitoring, issue triage |
| **Cloudflare** | `@cloudflare/mcp-server` | Cloudflare API management |
| **Context7** | `@upstash/context7-mcp` | Context retrieval |
| **Chrome DevTools** | `@anthropic/chrome-devtools-mcp-server` | Chrome debugging (see §7) |

### Example Configurations

**Filesystem:**
```jsonc
{
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\projects", "C:\\docs"]
    }
  }
}
```

**GitHub:**
```jsonc
{
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Brave Search:**
```jsonc
{
  "mcp": {
    "brave-search": {
      "type": "local",
      "command": ["npx", "-y", "@anthropic/brave-search-mcp"],
      "env": {
        "BRAVE_API_KEY": "your_brave_api_key"
      }
    }
  }
}
```

---

## 7. Chrome DevTools MCP (07c)

### 7.1 Setup

**Step 1 — Launch Chrome with remote debugging:**

```
chrome --remote-debugging-port=9222
```

Or on Windows:
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**Step 2 — Configure MCP server:**

```jsonc
{
  "mcp": {
    "chrome-devtools": {
      "type": "local",
      "command": ["npx", "-y", "@anthropic/chrome-devtools-mcp-server"],
      "env": {
        "CHROME_URL": "http://localhost:9222/json/version"
      }
    }
  }
}
```

### 7.2 Verification

After configuration, restart OpenCode. The MCP server connects via the Chrome DevTools Protocol (CDP). You should see `chrome-devtools` listed in the available MCP servers.

### 7.3 Available Tools

| Tool | Function |
|------|----------|
| `chrome-devtools_new_page` | Open a new tab to a URL |
| `take_snapshot` | Capture a page snapshot |
| `fill` | Fill a form field (by selector) |
| `click` | Click an element (by selector) |
| `wait_for` | Wait for text or element to appear |
| `evaluate_script` | Execute arbitrary JavaScript in page context |
| `inspect_network_requests` | View network request logs |
| `analyze_performance` | Run performance profiling |
| `debug_css` | Inspect and debug CSS |
| `debug_dom` | Inspect and debug DOM structure |

### 7.4 Use Cases

- **Web scraping** — Navigate, wait for content, take snapshots, extract data
- **Automated form filling** — Open pages, fill fields, click buttons
- **Image generation automation** — Automate Jimeng, Gemini, or other AI image tools in the browser
- **Performance analysis** — Profile page load, network requests, rendering
- **Debugging** — Inspect CSS/DOM, run JS, capture network activity

### 7.5 Practical Workflow Example

```
# Conceptual sequence (prompt-based):
1. "Open https://example.com"          → chrome-devtools_new_page
2. "Wait for 'Welcome' to appear"      → wait_for
3. "Fill '#search' with 'test query'"  → fill
4. "Click '#submit-button'"            → click
5. "Take a snapshot"                   → take_snapshot
6. "Run JS to get page title"          → evaluate_script("document.title")
7. "Show network requests"             → inspect_network_requests
```

### 7.6 Wait Times

| Scenario | Typical Wait |
|----------|-------------|
| Jimeng image generation | 30–60 seconds |
| Gemini image generation | 15–30 seconds |
| Standard page load | 2–5 seconds |

### 7.7 Content Moderation Notes

Some services (especially image-generation platforms) use **sensitive-word filters**. When automating these:
- Use **alternative descriptions** to avoid triggering content moderation
- Rephrase prompts that may contain blocked terms
- Test variations if a tool call fails due to moderation

### 7.8 Limitations & Tips

- Chrome must already be running with `--remote-debugging-port=9222` before starting OpenCode
- Only one DevTools session can connect at a time
- Use `chrome://inspect` to verify the debugging endpoint is active
- Close unused tabs to reduce memory usage during automation
- For headless automation, launch Chrome with: `chrome --headless --remote-debugging-port=9222`
