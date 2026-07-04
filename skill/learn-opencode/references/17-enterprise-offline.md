# Enterprise & Air-Gapped Deployment

## Enterprise Features (11)

### Deployment Options
- **Self-hosted**: Full control on own infrastructure
- **Cloud**: Managed OpenCode cloud instance
- **Hybrid**: Mix of cloud + on-prem components

### Data Security
- All data stays within enterprise network perimeter
- No data exfiltration to external services
- Encrypted at rest and in transit
- Configurable data retention policies

### Team Management
- Shared configuration across organization via `.opencode/` in repos
- Role-based access control (admin, developer, viewer)
- Per-team configuration overrides
- Centralized usage policies

### Audit Logging
- Every AI operation is logged: prompt sent, response received, files modified
- Logs include: timestamp, user identity, action type, resource accessed
- Exportable to SIEM systems (Splunk, ELK, etc.)
- Tamper-evident log storage option

### Compliance
- **SOC2**: Supports SOC2 Type II requirements (security, availability, confidentiality)
- **GDPR**: Data processing records, right to erasure, data portability
- **HIPAA**: Business associate agreement (BAA) support available
- **FedRAMP**: Moderate/High impact level readiness

---

## Enterprise Auth Integration (11a)

### SSO Integration
- **SAML 2.0**: Connect to Okta, Azure AD, OneLogin, ADFS
- **OIDC**: Connect to Google Workspace, Azure AD, Keycloak, Auth0
- **LDAP**: Direct bind to Active Directory / OpenLDAP
- JIT (Just-In-Time) provisioning on first login

### Token Injection Flow
```
User Login → SSO Provider → OpenCode receives JWT/SAML token
→ Token injected into OpenCode process via environment variables
→ OPENCODE_AUTH_TOKEN, OPENCODE_USER_EMAIL, OPENCODE_USER_GROUPS
→ All AI requests authenticated via process identity
```

### Organization Config Distribution
- Hosted at `https://<org>.opencode.ai/.well-known/opencode`
- Contains: allowed models, plugin list, formatter config, LSP config
- Auto-fetched by clients on startup
- Can be self-hosted at internal URL

### Token Renewal
- Short-term tokens (15-60 min) auto-renewed via plugin
- Plugin hook `onTokenExpiring()` triggers refresh before expiry
- Seamless renewal without interrupting user sessions

### Plugin-Based Auth
- Custom auth flows implemented as plugins
- Hook into login, token validation, permission checks
- Support for mTLS, custom headers, API key rotation
- Example: `export const authPlugin = { authenticate: async (req) => { ... } }`

---

## Air-Gapped / On-Premise Deployment

### Disable External Access (5 env vars)
| Env Var | Effect |
|---------|--------|
| `OPENCODE_DISABLE_MODELS_FETCH=true` | Prevents fetching model list from remote |
| `OPENCODE_DISABLE_TELEMETRY=true` | Disables all telemetry/usage reporting |
| `OPENCODE_DISABLE_UPDATES=true` | Skips update checks |
| `OPENCODE_DISABLE_PLUGIN_INSTALL=true` | Blocks npm install of remote plugins |
| `OPENCODE_DISABLE_LSP_FETCH=true` | Prevents downloading LSP binaries |

### Dependency Hang Fix
```bash
# Prevents node_modules resolution hanging on network timeout
mkdir -p ~/.config/opencode/node_modules
# Or system-wide:
mkdir -p /etc/opencode/node_modules
```

### Internal AI Gateway
```json
{
  "models": {
    "provider": "internal-gateway",
    "baseUrl": "https://ai-gateway.internal.company.com/v1",
    "apiKey": "env:INTERNAL_AI_KEY"
  }
}
```
- Route all LLM calls through internal gateway for auditing, rate limiting, model governance
- Supports OpenAI-compatible API, Anthropic, and custom endpoints

### Model List Download
```bash
# Download models manifest from internal registry
curl -o ~/.config/opencode/models.json https://models.internal.company.com/api.json
# Verify with checksum
sha256sum ~/.config/opencode/models.json > ~/.config/opencode/models.json.sha256
```

### One-Click Setup Script
```bash
#!/bin/bash
# airgap-setup.sh — run once on each developer machine
set -euo pipefail
mkdir -p ~/.config/opencode/node_modules
curl -s https://internal.company.com/opencode/models.json -o ~/.config/opencode/models.json
cat >> ~/.config/opencode/opencode.json <<'EOF'
{
  "disableModelsFetch": true,
  "disableTelemetry": true,
  "disableUpdates": true,
  "disablePluginInstall": true,
  "models": {
    "baseUrl": "https://ai-gateway.internal.company.com/v1",
    "apiKey": "env:INTERNAL_GATEWAY_KEY"
  },
  "auth": {
    "provider": "saml",
    "ssoUrl": "https://sso.internal.company.com/saml"
  }
}
EOF
echo "Air-gap setup complete."
```

### Offline Plugin Installation
```bash
# On air-gapped machine, install plugins from local tarball
npm pack opencode-helicone-session  # on internet machine
# Copy .tgz file via USB/SCP
npm install --prefix ~/.config/opencode ./opencode-helicone-session-1.0.0.tgz
```
