# IDE Integration

## VS Code Extension

**Installation**: Open VS Code → Extensions sidebar → search "OpenCode" → Install. Or via CLI: `code --install-extension opencode-ai.opencode-vscode`.

**Features**:
- Inline code actions: highlight code → right-click → "Ask OpenCode" for explain, refactor, fix, or custom prompts. Results appear as hover or diff view.
- Diagnostics display: OpenCode linting/suggestions shown inline as editor diagnostics (squiggly underlines). Click to see AI reasoning and apply fixes.
- Integrated terminal: `opencode` command available directly in VS Code terminal without separate window. Terminal pane shows raw OpenCode output.
- Separate pane: View → OpenCode to open dedicated chat panel alongside editor. Supports file context, multi-turn conversations, and code insertion.
- Keybindings: configurable shortcuts for common actions (default: `Ctrl+Shift+I` to open chat, `Ctrl+Shift+M` for diagnostics panel).

**VS Code + Cursor**:
- Cursor IDE users: OpenCode can run in Cursor's integrated terminal (`opencode` command). No dedicated extension needed.
- Cursor AI provider configuration: Settings → AI → Provider → Add custom → point to OpenCode server URL (`http://localhost:4096`). Enables OpenCode as a model provider within Cursor's native AI features.

---

## ACP Protocol (Agent Communication Protocol)

**What ACP Is**: ACP is a standardized protocol allowing editors/IDEs to communicate with OpenCode without native extensions. Communication flows over stdio (local subprocess) or TCP (network). Messages use JSON-RPC 2.0.

**Supported Editors**:

| Editor | Integration Method | Configuration |
|--------|-------------------|---------------|
| **Zed** | Built-in ACP support | `~/.config/zed/settings.json`: `{ "assistant": { "provider": { "type": "acp", "command": "opencode", "args": ["acp"] } } }` |
| **JetBrains** | ACP plugin (JetBrains Marketplace) | Install plugin → Settings → Tools → ACP → set OpenCode executable path. Supports all JetBrains IDEs (IntelliJ, PyCharm, WebStorm, GoLand, etc.). |
| **Neovim** | Plugin (`opencode.nvim`) or manual | Via plugin: `Plug 'opencode-ai/opencode.nvim'` → `require('opencode').setup({ acp = true })`. Manual: `opencode acp --stdio` piped through Neovim's `jobstart()`. |
| **Other editors** | Manual ACP client | Launch `opencode acp --port 8080` (TCP mode), write JSON-RPC messages per spec. |

**ACP Commands**:
- `opencode acp` — start ACP server (default stdio)
- `opencode acp --port <port>` — TCP mode on given port
- `opencode acp --stdio` — force stdio mode

**ACP Message Flow**:
1. Editor sends `initialize` request → OpenCode responds with protocol version, capabilities.
2. Editor sends `textDocument/didOpen`, `didChange`, `didClose` notifications.
3. Editor sends `textDocument/codeAction` for inline actions.
4. OpenCode responds with diagnostics, code actions, completions.
5. Editor sends `shutdown` → `exit` to terminate.

**Configuration in opencode.json**:
```jsonc
{
  "acp": {
    "enabled": true,
    "port": 8080,              // TCP port (omit for stdio)
    "allowedOrigins": ["*"],   // CORS for browser-based editors
    "maxMessageSize": 1048576  // 1MB limit
  }
}
```
