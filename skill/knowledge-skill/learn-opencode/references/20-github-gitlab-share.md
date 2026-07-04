# GitHub, GitLab, and Share Integration

## GitHub Integration (14-github.md)

### GitHub App Installation
- `opencode github install` — installs the OpenCode GitHub App into your account/organization
- Requires GitHub CLI (`gh`) to be authenticated
- The app requests permissions for: issues, pull requests, checks, contents (read), metadata

### Triggering OpenCode on GitHub
- Comment `/oc` or `/opencode` on any Issue or Pull Request to invoke OpenCode
- OpenCode responds inline as a GitHub user (the bot)
- Works in public and private repositories

### Auto-generated Workflow
- Upon installation, OpenCode auto-creates `.github/workflows/opencode.yml`
- This workflow handles the communication bridge between GitHub and OpenCode
- The workflow listens for `issue_comment` events

### Secrets Configuration
- Provider API keys are stored in **GitHub Secrets** (not in code)
- Required secrets vary by provider (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- The workflow reads secrets at runtime and passes them to OpenCode

### Capabilities
| Feature | Description |
|---|---|
| **Issue Triage** | Automatically label, categorize, and respond to issues |
| **Auto-Fix** | OpenCode can propose fixes via PR comments or direct commits |
| **PR Review** | Analyze PR diffs, suggest improvements, catch bugs |
| **Code Analysis** | Deep codebase understanding via OpenCode's agent loop |
| **Scripted Automation** | `opencode run` in Actions for fully automated pipelines |

### `opencode run` in GitHub Actions
```yaml
- name: Run OpenCode
  run: opencode run "review this PR" --print-logs
  env:
    PROVIDER_API_KEY: ${{ secrets.PROVIDER_API_KEY }}
```

### Multi-repo Support
- The GitHub App can be installed across multiple repositories
- Each repo gets its own workflow file
- Organization-level installation covers all repos in the org

### Security Considerations
- The bot only responds when explicitly mentioned (`/oc` or `/opencode`)
- Secrets are never exposed in logs or output
- Permissions are scoped to the minimum required set
- The workflow can be audited like any other GitHub Actions workflow

---

## GitLab Integration (15-gitlab.md)

OpenCode supports GitLab via two complementary approaches:

### Approach 1: GitLab CI/CD Pipelines (Runner-based)

OpenCode runs directly on your **GitLab Runner** as part of your CI/CD pipeline.

**Configuration** (`.gitlab-ci.yml`):
```yaml
opencode-review:
  image: opencode/opencode:latest
  script:
    - opencode run "review this merge request" --print-logs
  only:
    - merge_requests
```

**Features:**
- Full access to your repository and runner environment
- Can review MR diffs, run code analysis, suggest fixes
- Results appear as pipeline output and can be posted as MR comments
- Uses GitLab CI/CD variables for API keys (masked in logs)
- Supports `opencode run` for any automation script

**Variable Setup:**
- Go to Settings > CI/CD > Variables
- Add provider keys (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- Mark as "Masked" to prevent log exposure

### Approach 2: GitLab Duo Integration

GitLab Duo provides chat-based AI interactions within the GitLab UI.

- OpenCode can integrate with Duo for conversational interactions
- Enables `/oc` or `/opencode` commands in GitLab comments
- Similar interaction model to GitHub but tailored for GitLab's ecosystem
- Leverages GitLab's existing AI tooling and UI

### Comparison: GitHub vs GitLab

| Aspect | GitHub | GitLab |
|---|---|---|
| Installation | GitHub App via CLI | CI/CD config or Duo integration |
| Trigger | `/oc` in comments | Runner pipeline or Duo chat |
| Workflow File | `.github/workflows/opencode.yml` | `.gitlab-ci.yml` |
| Secrets Storage | GitHub Secrets | GitLab CI/CD Variables |
| Execution | Actions workflow | GitLab Runner |
| Chat Integration | Issue/PR comments | GitLab Duo |

### Best Practices
- Use **CI/CD approach** for automated, scripted workflows (review, lint, fix)
- Use **Duo approach** for interactive, chat-based assistance
- Combine both for maximum coverage
- Always mask API keys in CI/CD variables
- Pin OpenCode image version for reproducible builds

---

## Session Sharing (16-share.md)

### The `/share` Command

- `/share` creates a publicly accessible link to the current session
- Format: `https://opncd.ai/share/<unique-slug>`
- The slug is auto-generated and URL-safe
- Shared sessions are **read-only** snapshots

### Share Configuration

Configured via `"share"` key in `opencode.json`:

| Value | Behavior |
|---|---|
| `"manual"` (default) | Only share when `/share` is explicitly invoked |
| `"auto"` | Automatically share every session on exit |
| `"disabled"` | Sharing completely disabled |

**Example config:**
```json
{
  "share": "auto"
}
```

### Content of a Shared Session
- Full conversation history between user and OpenCode
- All tool calls and their outputs
- File contents viewed during the session
- Error messages and diagnostics
- **NOT included:** Secrets, API keys, environment variables, tokens

### Importing Shared Sessions

```bash
opencode import https://opncd.ai/share/xxx
opencode import opencode_share_xxx.json
```

- `opencode import <url>` — download and import a shared session
- `opencode import <file>` — import from a local JSON file
- Creates a local session file that can be resumed
- Useful for reproducing bugs, reviewing past work, onboarding

### Enterprise: Custom Domains

For enterprise deployments with `enterprise.url` config:
```json
{
  "enterprise": {
    "url": "https://opencode.example.com"
  }
}
```
- Shared links use the custom domain instead of `opncd.ai`
- Self-hosted sharing backend
- Full control over data residency and access

### Use Cases

| Use Case | Description |
|---|---|
| **Team Collaboration** | Share a debugging session with a teammate |
| **Getting Help** | Share a session link when asking for support (in Discord, GitHub Issues, etc.) |
| **Documentation** | Create walkthroughs by sharing sessions that demonstrate workflows |
| **Code Review** | Share the analysis OpenCode performed on a codebase |
| **Bug Reproduction** | Share the exact steps and context that led to a bug |
| **Onboarding** | Share sessions that teach new team members about the codebase |

### Export/Import Comparison

| Command | Format | Visibility | Use Case |
|---|---|---|---|
| `/export` | Local JSON file | Private (local filesystem) | Backup, local transfer |
| `/share` | URL on opncd.ai | Public (anyone with link) | Collaboration, support |
| `opencode import` | URL or file | N/A | Resume or inspect |

### Privacy Considerations
- Shared links are **unlisted** (not indexed by search engines)
- Anyone with the exact URL can view the session
- No authentication required to view a shared session
- Sessions can be deleted from the sharing backend (if self-hosted)
- For sensitive code, use enterprise self-hosting or stick to local export
