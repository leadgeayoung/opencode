# Plugins & Hooks

## Plugin Basics (12a)

### What Plugins Are
- Plugins extend OpenCode via the hooks mechanism
- Hook into any part of the OpenCode lifecycle: events, tools, LLM calls, config loading, auth

### Installation
- **npm packages**: `npm install -g opencode-helicone-session`
- **Local files**: place `.ts` or `.js` files in plugin directories
- **Config declaration**:
  ```json
  "plugins": ["opencode-helicone-session"]
  ```

### Plugin Locations (searched in order)
| Path | Scope |
|------|-------|
| `~/.config/opencode/plugin/` | User-global |
| `.opencode/plugin/` | Project-local |
| `node_modules/` | npm-managed |

### Plugin Structure
```typescript
// plugin = npm package OR local file exporting OpenCode plugin interface
export default {
  name: "my-plugin",
  hooks: {
    onSessionCreated: (session) => { ... },
    interceptTool: (toolName, params) => { ... },
    modifyLLMParams: (params) => { ... },
  }
};
```

---

## Plugin Advanced (12b)

### Hook Types Overview

| Hook Type | Purpose | Registration |
|-----------|---------|-------------|
| **Event** | Subscribe to lifecycle events | `on('eventName', handler)` |
| **Tool** | Intercept/modify/override tool calls | `intercept('toolName', handler)` |
| **LLM** | Modify LLM parameters before request | `modifyLLMParams(params)` |
| **Config** | Transform config at load time | `modifyConfig(config)` |
| **Auth** | Custom auth flows + token handling | `authenticate(req)` |

### Event Hooks
```typescript
export default {
  hooks: {
    onSessionCreated: async (session) => {
      console.log(`Session ${session.id} started`);
    },
    onMessageReceived: async (message) => {
      // message: { role, content, toolCalls, ... }
      if (message.role === 'user') trackUsage(message);
    },
    onToolCall: async (toolCall) => {
      // Log every tool invocation
      auditLog.push({ tool: toolCall.name, args: toolCall.args, time: Date.now() });
    },
    onFileWritten: async (filePath, content) => {
      // Post-write hook — e.g., auto-add copyright header
    }
  }
};
```

### Tool Hooks
```typescript
// Intercept any tool call
export const interceptTool = {
  name: "intercept-read",
  toolName: "read",           // target specific tool
  handler: async (args, next) => {
    console.log(`Reading file: ${args.filePath}`);
    // Modify args before passing to original handler
    args.filePath = resolveAlias(args.filePath);
    const result = await next(args);  // pass to next plugin or original
    // Modify result after
    return result;
  }
};

// Block a tool entirely
export const blockTool = {
  name: "block-dangerous",
  toolName: "bash",
  handler: async (args, next) => {
    const blocked = ["rm -rf", "shutdown", "> /dev/sda"];
    if (blocked.some(cmd => args.command.includes(cmd))) {
      throw new Error(`Command blocked by security policy: ${args.command}`);
    }
    return next(args);
  }
};
```

### LLM Hooks
```typescript
export default {
  hooks: {
    modifyLLMParams: (params) => {
      // Force specific model
      params.model = "gpt-4-turbo";
      // Add system prompt prefix
      params.systemPrompt = "[COMPLIANCE MODE]\n" + (params.systemPrompt || "");
      // Set temperature ceiling
      params.temperature = Math.min(params.temperature || 0.7, 1.0);
      // Inject custom stop sequences
      params.stop = [...(params.stop || []), "<END_COMPLIANT>"];
      return params;
    }
  }
};
```

### Config Hooks
```typescript
export default {
  hooks: {
    modifyConfig: (config) => {
      // Enforce org-wide settings
      config.disableTelemetry = true;
      config.models.baseUrl = "https://gateway.internal.company.com/v1";
      // Merge in team overrides from remote
      const teamConfig = await fetchTeamConfig();
      return { ...config, ...teamConfig };
    }
  }
};
```

### Auth Hooks
```typescript
export default {
  hooks: {
    authenticate: async (req) => {
      const token = req.headers["x-custom-auth"];
      const user = await validateToken(token);
      return { userId: user.id, email: user.email, roles: user.roles };
    },
    onTokenExpiring: async (token) => {
      return refreshToken(token.refreshToken);
    }
  }
};
```

### Multiple Plugin Execution Order
- Plugins run in the order they are declared in config
- Each hook handler receives a `next` function to pass control
- If a handler does NOT call `next()`, subsequent plugins are skipped
- Error in one plugin does not crash others (configurable isolation)

### Error Handling
```typescript
// Graceful degradation
export default {
  hooks: {
    onToolCall: async (toolCall, next) => {
      try {
        return await next(toolCall);
      } catch (err) {
        console.error(`[my-plugin] tool ${toolCall.name} failed:`, err);
        // Return fallback or rethrow
        throw err;
      }
    }
  }
};
```

---

## Hook Tutorial (12c)

### Plugin Hooks vs Config Hooks
- **Plugin hooks**: registered by plugins, run on every matching event
- **Config hooks**: defined in `opencode.json` under `"hooks"`, simpler for one-off modifications
  ```json
  {
    "hooks": {
      "onSessionCreated": "console.log('session started')",
      "modifyLLMParams": "params => ({ ...params, temperature: 0.5 })"
    }
  }
  ```

### Event Subscription
```typescript
import { on } from 'opencode/hooks';

// Subscribe once
on('session.created', (session) => {
  logger.info(`Session: ${session.id}`);
});

// Subscribe with filter
on('message.received', { role: 'user' }, (msg) => {
  // Only user messages
});
```

### Tool Interception
```typescript
import { intercept } from 'opencode/hooks';

intercept('read', async (args, next) => {
  if (!isAllowed(args.filePath)) {
    return { error: 'Access denied' };
  }
  return next(args);
});
```

### LLM Parameter Modification
```typescript
import { modifyLLMParams } from 'opencode/hooks';

modifyLLMParams((params) => {
  return { ...params, maxTokens: 4096 };
});
```

### Permission Control in Hooks
```typescript
intercept('bash', async (args, next) => {
  const policy = await loadSecurityPolicy();
  if (!policy.allowedCommands.some(p => args.command.startsWith(p))) {
    throw new PermissionError(`Command '${args.command}' not allowed`);
  }
  return next(args);
});
```

### Complete Hook Example
```typescript
// plugin/timing-hook.ts
import { on, intercept, modifyLLMParams } from 'opencode/hooks';

export default {
  name: "timing-monitor",
  hooks: {
    onSessionCreated: (session) => {
      session.meta.startTime = Date.now();
    },
    onMessageReceived: (msg) => {
      if (msg.toolCalls?.length) {
        console.log(`Tool calls: ${msg.toolCalls.map(t => t.name).join(', ')}`);
      }
    },
    interceptTool: {
      name: "timing",
      handler: async (toolCall, next) => {
        const start = performance.now();
        const result = await next(toolCall);
        const elapsed = performance.now() - start;
        console.log(`Tool ${toolCall.name}: ${elapsed.toFixed(2)}ms`);
        return result;
      }
    },
    modifyLLMParams: (params) => {
      console.log(`LLM call: model=${params.model}, tokens=${params.maxTokens}`);
      return params;
    }
  }
};
```

### Testing Hooks
```typescript
// test/timing-hook.test.ts
import { describe, it, expect, vi } from 'vitest';
import timingHook from '../plugin/timing-hook';

describe('timing-monitor', () => {
  it('logs tool execution time', async () => {
    const consoleSpy = vi.spyOn(console, 'log');
    const next = vi.fn().mockResolvedValue({ content: 'test' });

    await timingHook.hooks.interceptTool.handler(
      { name: 'read', args: { filePath: '/test' } },
      next
    );

    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringMatching(/Tool read: \d+\.\d+ms/)
    );
  });

  it('modifies LLM params', () => {
    const result = timingHook.hooks.modifyLLMParams({ model: 'gpt-3', maxTokens: 100 });
    expect(result).toEqual({ model: 'gpt-3', maxTokens: 100 });
  });
});
```
