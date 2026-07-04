# Custom Tools, Formatters & LSP

## Custom Tools (13)

### Overview
- Create TypeScript tools that the LLM can call
- Tools are registered via the plugin system
- Full access to OpenCode API via context object

### Tool Definition
```typescript
import { Tool } from 'opencode/tool';

export const myTool: Tool = {
  name: "my_tool",                    // snake_case, unique identifier
  description: "Does something useful", // LLM reads this to decide invocation
  parameters: {                        // JSON Schema for arguments
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query string"
      },
      limit: {
        type: "number",
        default: 10,
        minimum: 1,
        maximum: 100
      }
    },
    required: ["query"]
  },
  handler: async (args, context) => {
    // args: validated parameters matching JSON Schema
    // context: { api, session, logger, config, ... }
    const results = await context.api.search(args.query, args.limit);
    return { results };
  }
};
```

### Parameter Validation
- JSON Schema validation happens automatically before handler runs
- On validation failure, LLM receives a clear error and can retry
- Supports: `type`, `enum`, `pattern`, `minimum`/`maximum`, `minLength`/`maxLength`, `default`

### Error Handling
```typescript
handler: async (args, context) => {
  try {
    const data = await fetchExternalApi(args.url);
    return data;
  } catch (err) {
    // Return structured error — LLM can read and adapt
    return {
      error: true,
      message: `API call failed: ${err.message}`,
      retryable: err.status >= 500
    };
  }
}
```

### Register via Plugin System
```typescript
// plugin/custom-tools.ts
import { myTool } from './tools/my-tool';
import { searchTool } from './tools/search';

export default {
  name: "my-custom-tools",
  tools: [myTool, searchTool]
  // Or register dynamically:
  // hooks: { onSessionCreated: (session) => { session.registerTool(myTool); } }
};
```

### Plugin Config
```json
{
  "plugins": ["my-custom-tools"]
}
```

### Access OpenCode API via Context
| Context Property | Description |
|-----------------|-------------|
| `context.api.readFile(path)` | Read file contents |
| `context.api.writeFile(path, content)` | Write file contents |
| `context.api.searchFiles(pattern)` | Glob search |
| `context.api.grep(pattern)` | Content search |
| `context.api.runCommand(cmd)` | Execute shell command |
| `context.session` | Current session state |
| `context.logger` | Structured logger |
| `context.config` | Resolved config |

### Full Example
```typescript
// tool/summarize.ts
export const summarizeTool = {
  name: "summarize_file",
  description: "Read a file and return a summary of its contents",
  parameters: {
    type: "object",
    properties: {
      path: { type: "string", description: "File path relative to workspace" },
      maxLines: { type: "number", default: 50, description: "Max lines to read" }
    },
    required: ["path"]
  },
  handler: async (args, context) => {
    const content = await context.api.readFile(args.path);
    if (!content) return { error: `File not found: ${args.path}` };
    const lines = content.split('\n').slice(0, args.maxLines);
    return {
      filename: args.path,
      totalLines: content.split('\n').length,
      summary: lines.join('\n')
    };
  }
};
```

---

## Formatters (18)

### Auto-Run Behavior
- Formatters execute automatically after every write/edit operation
- Applies only to modified files
- Non-blocking — user can continue working while formatting runs
- Respects `.prettierrc`, `.editorconfig`, and any existing project formatting config

### Built-in Formatters
| Language | Tool | Extensions |
|----------|------|------------|
| JavaScript/TypeScript | Prettier | `.js`, `.ts`, `.jsx`, `.tsx` |
| CSS/JSON/MD/YAML | Prettier | `.css`, `.json`, `.md`, `.yaml`, `.yml` |
| JS/TS/JSX/TSX/CSS/JSON | Biome | `.js`, `.ts`, `.jsx`, `.tsx`, `.css`, `.json` |
| Go | gofmt | `.go` |
| Rust | rustfmt | `.rs` |
| Python | Ruff | `.py` |
| Ruby | RuboCop | `.rb` |
| Lua | LuaFormatter | `.lua` |
| Shell | shfmt | `.sh`, `.bash` |

### Configuration
```json
{
  "formatter": {
    "prettier": {
      "disabled": false,
      "options": {
        "singleQuote": true,
        "tabWidth": 2,
        "trailingComma": "all",
        "printWidth": 100
      }
    },
    "biome": {
      "disabled": true
    },
    "gofmt": {
      "disabled": false
    }
  }
}
```

### Custom Formatter
```json
{
  "formatter": {
    "custom-sql-formatter": {
      "command": ["npx", "sql-formatter", "--write", "$FILE"],
      "extensions": [".sql", ".pgsql"]
    }
  }
}
```
- `$FILE` is replaced with the absolute path of the file being formatted
- Formatter must exit with code 0 on success
- Stderr is logged for debugging

### Disable All Formatting
```json
{
  "formatter": false
}
```

### Per-Workspace Override
```json
// .opencode/opencode.json (project-local)
{
  "formatter": {
    "prettier": {
      "options": {
        "singleQuote": false  // override for this project
      }
    }
  }
}
```

---

## LSP (19)

### Supported Language Servers (30+)
| Language | LSP Server |
|----------|-----------|
| TypeScript/JavaScript | `typescript-language-server` |
| Python | `pyright` / `pylsp` |
| Go | `gopls` |
| Rust | `rust-analyzer` |
| Java | `eclipse-jdtls` |
| C/C++ | `clangd` |
| C# | `omnisharp` |
| PHP | `intelephense` |
| Ruby | `solargraph` |
| Lua | `lua-language-server` |
| SQL | `sqls` |
| HTML/CSS/JSON/YAML | `vscode-langservers-extracted` |
| Markdown | `marksman` |
| Docker | `docker-langserver` |
| TOML | `taplo` |
| Bash | `bash-language-server` |
| GraphQL | `graphql-language-service` |

### 9 Code Intelligence Operations
| Operation | Description |
|-----------|-------------|
| **Go to Definition** | Navigate to symbol definition |
| **Find References** | All references to a symbol |
| **Hover Info** | Type signature + docstring on hover |
| **Completion** | Auto-complete suggestions |
| **Diagnostics** | Errors, warnings, hints in real-time |
| **Code Action** | Quick fixes, refactoring, auto-import |
| **Signature Help** | Parameter hints for function calls |
| **Document Symbol** | List symbols in current file |
| **Workspace Symbol** | Search symbols across workspace |

### LSP Configuration
```json
{
  "lsp": {
    "typescript": {
      "disabled": false,
      "options": {
        "format": { "semicolons": "insert" }
      }
    },
    "custom-lsp": {
      "command": ["my-lsp-server", "--stdio"],
      "extensions": [".foo", ".bar"],
      "initializationOptions": { "setting1": "value1" }
    }
  }
}
```

### Activation Requirement
- The `lsp` tool requires environment variable:
  ```bash
  export OPENCODE_EXPERIMENTAL_LSP_TOOL=true
  ```
- Without this, LSP features are passive (diagnostics only, no tool invocation)

### Auto-Diagnostics Flow
```
User writes file → Formatter runs → LSP diagnostics trigger
→ Errors/warnings collected → Displayed in output
→ LLM can see diagnostics and auto-fix issues
```

### Disable LSP
```json
{
  "lsp": false   // disable all LSP servers
}
```

### Diagnostics-Only Mode
```json
{
  "lsp": {
    "typescript": { "diagnosticsOnly": true }
    // Workspace symbols, goto def, etc. disabled; only error checking runs
  }
}
```
