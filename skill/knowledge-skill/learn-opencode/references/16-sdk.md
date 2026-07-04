# OpenCode SDK

## Basics

**Installation**:
```bash
npm install @opencode-ai/sdk
# or
yarn add @opencode-ai/sdk
# or
pnpm add @opencode-ai/sdk
```

**Quick Start**:
```typescript
import { OpenCode } from '@opencode-ai/sdk';

const client = new OpenCode({ apiKey: process.env.OP_API_KEY });

// Create a session and send a message
const session = await client.sessions.create({ name: 'my-session' });
const response = await client.messages.send({
  sessionId: session.id,
  message: 'Hello, what can you do?'
});
console.log(response.content);
```

**Streaming**:
```typescript
const stream = client.messages.stream({
  sessionId: session.id,
  message: 'Write a React component'
});

for await (const chunk of stream) {
  process.stdout.write(chunk.content); // incremental response
}
```

**Connection Options**:
```typescript
const client = new OpenCode({
  apiKey: '...',
  baseUrl: 'http://localhost:4096/api',  // default: env.OP_API_URL
  timeout: 60000,                         // request timeout ms
  maxRetries: 3                           // auto-retry on transient errors
});
```

---

## SDK Reference (21 API Modules)

### Session Module
```typescript
client.sessions.create({ name?: string })              // Promise<Session>
client.sessions.list()                                 // Promise<Session[]>
client.sessions.get(id: string)                        // Promise<Session>
client.sessions.switch(id: string)                     // Promise<void>
client.sessions.delete(id: string)                     // Promise<void>
client.sessions.rename(id: string, name: string)       // Promise<Session>
client.sessions.clearHistory(id: string)               // Promise<void>
```

### Message Module
```typescript
client.messages.send({ sessionId, message, files?, tools?, model?, stream? })
  // Promise<Message> | Stream<MessageChunk>
client.messages.stream({ sessionId, message, ... })    // AsyncIterable<MessageChunk>
client.messages.list(sessionId)                        // Promise<Message[]>
client.messages.get(messageId)                         // Promise<Message>
client.messages.delete(messageId)                      // Promise<void>
client.messages.edit(messageId, { content })           // Promise<Message>
client.messages.fork(messageId)                        // Promise<Session> (branch off)
```

### File Module
```typescript
client.file.read(path: string)                         // Promise<string>
client.file.write(path: string, content: string)       // Promise<void>
client.file.edit(path: string, edits: Edit[])          // Promise<void>
client.file.search(pattern: string, path?: string)     // Promise<SearchResult[]>
client.file.glob(pattern: string)                      // Promise<string[]>
client.file.delete(path: string)                       // Promise<void>
client.file.exists(path: string)                       // Promise<boolean>
client.file.info(path: string)                         // Promise<FileInfo>
client.file.watch(path: string)                        // AsyncIterable<FileEvent>
```

### Config Module
```typescript
client.config.get()                                    // Promise<Config>
client.config.set(partial: Partial<Config>)            // Promise<Config>
client.config.getKey(key: string)                      // Promise<any>
client.config.setKey(key: string, value: any)          // Promise<void>
client.config.reset()                                  // Promise<void>
```

### MCP Module
```typescript
client.mcp.servers.list()                              // Promise<MCPServer[]>
client.mcp.servers.add(config: MCPServerConfig)        // Promise<MCPServer>
client.mcp.servers.remove(name: string)                // Promise<void>
client.mcp.servers.start(name: string)                 // Promise<void>
client.mcp.servers.stop(name: string)                  // Promise<void>
client.mcp.tools.list(serverName?: string)             // Promise<MCPTool[]>
client.mcp.tools.call(serverName: string, tool: string, args: any) // Promise<any>
client.mcp.resources.list(serverName?: string)         // Promise<MCPResource[]>
```

### LSP Module
```typescript
client.lsp.didOpen(uri: string, languageId: string, text: string)  // Promise<void>
client.lsp.didChange(uri: string, text: string)                    // Promise<void>
client.lsp.didClose(uri: string)                                   // Promise<void>
client.lsp.completions(uri: string, position: Position)            // Promise<Completion[]>
client.lsp.hover(uri: string, position: Position)                  // Promise<Hover>
client.lsp.definition(uri: string, position: Position)             // Promise<Location[]>
client.lsp.references(uri: string, position: Position)             // Promise<Location[]>
client.lsp.diagnostics(uri: string)                                // Promise<Diagnostic[]>
client.lsp.codeActions(uri: string, range: Range)                  // Promise<CodeAction[]>
client.lsp.formatting(uri: string, options?: FormatOptions)         // Promise<TextEdit[]>
```

### Tool Module
```typescript
// Register a custom tool for OpenCode to use
client.tool.register(name: string, definition: ToolDefinition, handler: ToolHandler)
  // => Promise<void>

// ToolDefinition: { description: string, parameters: JSONSchema }
// ToolHandler: (args: any) => Promise<any>

// List registered tools
client.tool.list()                                     // Promise<ToolDefinition[]>

// Unregister
client.tool.unregister(name: string)                   // Promise<void>
```

### Other Modules
| Module | Key Methods |
|--------|-------------|
| `client.system` | `info()`, `ping()`, `version()`, `stats()` |
| `client.context` | `addFile(path)`, `addDirectory(path)`, `addText(name, content)`, `clear()` |
| `client.template` | `list()`, `get(name)`, `create(def)`, `apply(name, vars)` |
| `client.snapshot` | `create()`, `list()`, `restore(id)`, `diff(id)` |
| `client.history` | `list(sessionId)`, `search(query)`, `export(format)` |
| `client.env` | `get(key)`, `set(key, value)`, `list()`, `delete(key)` |
| `client.auth` | `login(provider)`, `logout()`, `status()`, `refresh()` |
| `client.cache` | `get(key)`, `set(key, value, ttl?)`, `delete(key)`, `clear()` |
| `client.health` | `check()`, `subscribe()` |
| `client.remote` | `connect(address)`, `disconnect()`, `status()` |
| `client.embedding` | `create(texts)`, `search(query, limit?)`, `delete(id)` |
| `client.web` | `fetch(url)`, `scrape(url)`, `screenshot(url)` |

---

## Event System (35+ Event Types)

```typescript
// Subscribe to events
client.events.on('session.created', (session) => { ... });
client.events.on('message.received', (message) => { ... });
client.events.on('message.streaming', (chunk) => { ... });
client.events.on('tool.called', (call) => { ... });
client.events.on('tool.result', (result) => { ... });
client.events.on('file.changed', (event) => { ... });
client.events.on('error', (error) => { ... });

// Unsubscribe
client.events.off('session.created', handler);

// One-time
client.events.once('connection.ready', () => { ... });
```

**Event Categories**:
| Category | Events |
|----------|--------|
| **Session** | `session.created`, `session.deleted`, `session.renamed`, `session.switched` |
| **Message** | `message.sent`, `message.received`, `message.streaming`, `message.edited`, `message.deleted`, `message.forked` |
| **Tool** | `tool.called`, `tool.result`, `tool.error`, `tool.registered`, `tool.unregistered` |
| **File** | `file.created`, `file.changed`, `file.deleted`, `file.saved` |
| **Config** | `config.changed`, `config.reset` |
| **MCP** | `mcp.server.started`, `mcp.server.stopped`, `mcp.server.error`, `mcp.tool.called` |
| **LSP** | `lsp.diagnostics`, `lsp.completions.ready` |
| **Connection** | `connection.ready`, `connection.closed`, `connection.error`, `connection.reconnecting` |
| **System** | `system.warning`, `system.error`, `system.shutdown`, `system.memory` |

---

## Usage Examples

**Automated Code Review**:
```typescript
import { OpenCode } from '@opencode-ai/sdk';

const client = new OpenCode({ apiKey: process.env.OP_API_KEY });
const file = await client.file.read('src/app.ts');
const session = await client.sessions.create({ name: 'code-review' });
const review = await client.messages.send({
  sessionId: session.id,
  message: `Review this code for bugs and style issues:\n\n\`\`\`typescript\n${file}\n\`\`\``
});
console.log(review.content);
```

**Bulk File Refactor**:
```typescript
const client = new OpenCode({ apiKey: '...' });
const files = await client.file.glob('src/**/*.ts');

for (const file of files) {
  const content = await client.file.read(file);
  if (content.includes('deprecatedFn')) {
    await client.file.edit(file, [{
      oldString: 'deprecatedFn(',
      newString: 'newFn('
    }]);
  }
}
```

**Custom Tool Registration**:
```typescript
client.tool.register('get_weather', {
  description: 'Get current weather for a city',
  parameters: {
    type: 'object',
    properties: {
      city: { type: 'string', description: 'City name' }
    },
    required: ['city']
  }
}, async ({ city }) => {
  const res = await fetch(`https://api.weather.com/${city}`);
  return res.json();
});
```

**Reactive Session Monitor**:
```typescript
client.events.on('session.created', async (session) => {
  console.log(`New session: ${session.name} (${session.id})`);
  const msg = await client.messages.send({
    sessionId: session.id,
    message: 'Welcome! How can I help you today?'
  });
  console.log(`Auto-reply: ${msg.content}`);
});
```

**TypeScript Types**:
All types exported from `@opencode-ai/sdk`:
```typescript
import type { Session, Message, FileInfo, Position, Range, Edit, Config,
  MCPServer, MCPTool, ToolDefinition, Diagnostic, Completion, Hover,
  Location, TextEdit, CodeAction, EventType, StreamChunk, SearchResult,
  ConnectionOptions } from '@opencode-ai/sdk';
```
