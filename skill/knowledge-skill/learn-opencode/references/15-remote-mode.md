# Remote Mode

## Server Basics (`opencode serve`)

**Headless Server**: `opencode serve` starts OpenCode as a background HTTP server without interactive CLI. Accessible via REST API or web interface.

**Web Interface**: `opencode web` starts the server AND opens a browser tab with a full chat UI. Same backend as `serve`, just adds browser frontend.

**Server Configuration** (in `opencode.json` under `server` key):

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `server.port` | Number | `4096` | HTTP listen port. Change if port conflict. |
| `server.hostname` | String | `"0.0.0.0"` | Bind address. `"0.0.0.0"` = all interfaces (LAN accessible). `"127.0.0.1"` = localhost only. |
| `server.mdns` | Boolean | `false` | Enable mDNS (Bonjour/Zeroconf) advertisement. Other devices on LAN see "OpenCode Server" in discovery tools. |
| `server.cors` | Object/Strings | `["*"]` | Allowed CORS origins. Array of origin strings. `["*"]` allows all. Restrict to specific URLs in production. |
| `server.ssl` | Object | `null` | SSL config: `{ "key": "path/to/key.pem", "cert": "path/to/cert.pem" }`. Enables HTTPS. |
| `server.maxBodySize` | String | `"10mb"` | Max request body size. |
| `server.rateLimit` | Object | `null` | Rate limiting: `{ "windowMs": 60000, "max": 100 }`. |

**Example opencode.json**:
```jsonc
{
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": true,
    "cors": ["http://localhost:5173", "https://myapp.com"]
  }
}
```

**mDNS Discovery**:
- Enabled with `server.mdns: true`. OpenCode advertises as `_opcode._tcp` service.
- Clients on same LAN: `opencode scan` lists discovered servers by hostname, IP, port.
- Works across subnets if mDNS gateway configured. Zero configuration required.

**Web Interface Features**:
- Full chat UI: type messages, see streaming responses, view file diffs.
- Session management: create, rename, switch, delete sessions.
- File browser: navigate workspace, preview files.
- Terminal panel: execute commands remotely.
- Settings page: edit opencode.json via form UI.
- Mobile-responsive: works on phones/tablets.

**Remote Terminal**: `opencode remote <server-address>` connects to a running server and provides an SSH-like terminal experience. Supports tab completion, history, file transfer via drag-drop. Authenticated via same token/credentials as API.

---

## HTTP API Reference

**Base URL**: `http://<host>:<port>/api` (default `http://localhost:4096/api`)

**Authentication**: All endpoints except health check require `Authorization: Bearer <token>` header. Token configured via `OP_TOKEN` env var or `opencode.json` (`server.token`).

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check (no auth required). Returns `{ "status": "ok", "version": "x.y.z" }`. |
| `POST` | `/api/messages` | Send a message to a session. Body: `{ "sessionId": "...", "message": "...", "stream": true }`. Returns message response (or SSE stream). |
| `GET` | `/api/sessions` | List all sessions. Returns `{ "sessions": [{ "id": "...", "name": "...", "createdAt": "..." }] }`. |
| `POST` | `/api/sessions` | Create a new session. Body: `{ "name": "optional-name" }`. |
| `GET` | `/api/sessions/:id` | Get session details and message history. |
| `DELETE` | `/api/sessions/:id` | Delete a session. |
| `GET` | `/api/models` | List available models and their capabilities. |
| `POST` | `/api/tools/call` | Execute a tool directly. Body: `{ "tool": "toolName", "args": {...} }`. |
| `GET` | `/api/config` | Get current configuration (redacted secrets). |
| `PATCH` | `/api/config` | Update configuration at runtime. Body: partial opencode.json object. |
| `GET` | `/api/files` | List workspace files (with optional glob filter). |
| `POST` | `/api/files/read` | Read file contents. Body: `{ "path": "relative/path" }`. |
| `POST` | `/api/files/write` | Write file contents. Body: `{ "path": "...", "content": "..." }`. |
| `POST` | `/api/files/edit` | Apply edits to a file. Body: `{ "path": "...", "edits": [{ "oldString": "...", "newString": "..." }] }`. |
| `GET` | `/api/mcp/servers` | List MCP server configurations. |
| `POST` | `/api/mcp/servers` | Add an MCP server. |

### Streaming (SSE)

**Endpoint**: `POST /api/messages` with `"stream": true`

**Response**: `Content-Type: text/event-stream`. Events:

```
event: message.chunk
data: {"content": "partial response text"}

event: message.chunk
data: {"content": "more text"}

event: message.complete
data: {"messageId": "abc123", "fullContent": "complete response"}

event: error
data: {"error": "description", "code": "ERROR_CODE"}
```

**Curl Example** (non-streaming):
```bash
curl -X POST http://localhost:4096/api/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OP_TOKEN" \
  -d '{"message": "List files in project", "stream": false}'
```

**Curl Example** (streaming):
```bash
curl -N -X POST http://localhost:4096/api/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OP_TOKEN" \
  -d '{"message": "Explain this code", "sessionId": "sess_abc", "stream": true}'
```

**JavaScript Fetch**:
```javascript
const response = await fetch('http://localhost:4096/api/messages', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
  body: JSON.stringify({ message: 'Hello', stream: true })
});
const reader = response.body.getReader();
// read SSE chunks...
```

### Error Responses

```json
{ "error": "Session not found", "code": "SESSION_NOT_FOUND", "status": 404 }
{ "error": "Invalid token", "code": "UNAUTHORIZED", "status": 401 }
{ "error": "Rate limit exceeded", "code": "RATE_LIMITED", "status": 429 }
```
