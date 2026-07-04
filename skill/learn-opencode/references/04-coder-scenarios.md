# Developer Scenarios (4-scenarios)

---

## B1 Daily Development

### Core Workflow

```
Understand (Plan) → Plan (Plan) → Implement (Build) → Verify (Build)
```

| Phase | Agent | Activity |
|-------|-------|----------|
| Understand | Plan | Read code, explore codebase, analyze requirements |
| Plan | Plan | Design solution, outline steps, identify risks |
| Implement | Build | Write code, create files, apply changes |
| Verify | Build | Run tests, lint, typecheck, manual verification |

### Quick Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `@path` | File reference | `@src/main.ts` |
| `!command` | Execute command | `!npm test` |
| `/undo` | Revert last AI change | `/undo` |

### Magic Prompts

#### 1. Code Explanation Prompt

```
Role: You are a senior tech writer explaining code to junior developers.
Task: Explain the provided code thoroughly.
Input:
  Language: <language>
  Code: @<filepath>
Output:
  1. One-line summary of what the code does
  2. Block-by-block explanation (function signatures, logic flow, data structures, API calls)
  3. Key concepts and patterns used
  4. Potential issues or edge cases
  5. Simple usage example
Constraints:
  - Progressive explanation (high-level first, then dive deeper)
  - Use analogies for complex concepts
  - Assume beginner-to-intermediate developer audience
```

#### 2. Feature Implementation Prompt

```
Role: You are a senior full-stack developer implementing a new feature.
Task: Implement step by step. Wait for confirmation after each step before proceeding.
Input:
  Requirements: <requirements>
  Language: <language>
Output per step:
  - Step goal: what this step accomplishes
  - Code changes with @file references
  - Verification: how to test this step works
  - Next step preview: what the next step will cover
Constraints:
  - Do NOT proceed to the next step until user confirms
  - Keep each step small and testable
```

#### 3. Bug Localization Prompt

```
Role: You are a senior troubleshooting engineer.
Input:
  Problem description: <what user reports>
  Expected behavior: <what should happen>
  Actual behavior: <what actually happens>
  Steps to reproduce: <steps>
  Relevant code: @<filepath>
  Error messages/logs: <paste>
  Environment: <OS, versions, dependencies>
Output:
  1. Problem summary (one paragraph)
  2. Root cause analysis (ranked by likelihood)
  3. Verification approach for most likely cause
  4. Fix solutions with code changes
Constraints:
  - Sort potential root causes by likelihood
  - Verify the most likely cause first before proposing fixes
```

### Agent Switching

| Action | Key |
|--------|-----|
| Build → Plan | Tab |
| Plan → Build | Shift+Tab |
| List agents | `<leader>a` |
| Next sub-session | `<leader>right` or `<leader>→` |
| Previous sub-session | `<leader>left` or `<leader>←` |
| Parent session | `<leader>up` or `<leader>↑` |

---

## B2 Refactoring & Testing

### Workflow

1. **Plan Agent** analyzes code smells first (`@explore` for full codebase understanding)
2. **Build Agent** performs the refactoring
3. AI generates test cases automatically

### Best Practices

- Use `@explore` subagent before refactoring to understand all usages
- Let Plan Agent produce a refactoring plan with risks identified
- Build Agent applies changes incrementally
- AI auto-generates unit/integration tests for refactored code
- Verify with existing test suite after each change

### Code Smells the Plan Agent Can Detect

- Duplicated code
- Long methods / large classes
- God objects / excessive coupling
- Inconsistent naming conventions
- Missing error handling
- Dead code / unused imports
- Overly complex conditionals
- Insufficient test coverage

---

## B3 Docs & Git

### README Generation

```
Role: You are a senior developer creating project documentation.
Task: Generate a professional README.md.
Input:
  - Project analysis via @explore
  - Any specific README requirements
Output sections:
  1. Project name and concise description
  2. Features (bullet list with brief explanations)
  3. Quick start (prerequisites + installation + basic usage)
  4. Usage (common commands/examples with code blocks)
  5. Configuration (environment variables, config files)
  6. Contributing guidelines
  7. License information
```

**Usage**: Use Build Agent with `@explore` to analyze project first, then prompt with the above template.

### Commit Messages

```
Role: You are a developer writing git commit messages.
Input: !git diff (to show staged/unstaged changes)
Output: Single commit message in Conventional Commits format:
  type(scope): description
Constraints:
  - Under 50 characters
  - Imperative mood ("add" not "added")
Types: feat | fix | docs | style | refactor | test | chore
```

**Workflow**: `!git diff` shows changes → AI generates message → `!git commit -m "..."`

### PR Descriptions

```
Role: You are a developer creating a pull request.
Input:
  - !git log --oneline -10 (recent commits)
  - !git diff main...HEAD (changes from base branch, if applicable)
Output:
  ## Summary
  <brief description of what this PR does>
  ## Changes
  - <change 1 with @file links>
  - <change 2 with @file links>
  ## Testing
  <how changes were tested>
  ## Related Issues
  Closes #<issue-number> (if applicable)
```

### Code Comments

**Prompt**: `@file add JSDoc comments to exported functions with params, returns, examples`

---

## B4 CI/CD (GitHub Agent)

### Core Approach

- Use **GitHub Agent** (not glue/script code)
- Trigger via `/oc` or `/opencode` in Issue/PR comments

### Installation

```bash
opencode github install
```

**Wizard does**:
1. Installs OpenCode GitHub App to the repository
2. Generates `.github/workflows/opencode.yml` workflow file
3. Configures `OPENCODE_API_KEY` and other secrets in GitHub Secrets

### Triggering

Comment on any Issue or PR:
- `/oc summarize` — AI summarizes the issue/PR
- `/opencode summarize` — same as above
- Any command: `/oc <instruction>`

### Secrets Management

- Provider API keys are stored in **GitHub Secrets**
- Workflow reads secrets and passes them to OpenCode as environment variables
- No hardcoded secrets in the repository

### Generated Workflow (`.github/workflows/opencode.yml`)

```yaml
name: OpenCode
on:
  issue_comment:
    types: [created]
jobs:
  opencode:
    if: ${{ github.event.comment.body.startsWith('/oc') || github.event.comment.body.startsWith('/opencode') }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anomalyco/opencode-action@v1
        with:
          command: ${{ github.event.comment.body }}
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
```

---

## B5 Custom Development Agents

### Agent Locations

| Scope | Path |
|-------|------|
| Global | `~/.config/opencode/agent/` |
| Project | `.opencode/agent/` |

### Invocation

- Filename without `.md` extension = agent name
- Example: `code-reviewer.md` → `@code-reviewer`

### Code Reviewer Agent

**File**: `~/.config/opencode/agent/code-reviewer.md` or `.opencode/agent/code-reviewer.md`

```markdown
---
description: Performs thorough code review on provided files or code changes
edit: deny
bash: deny
---

You are a senior code reviewer. Analyze the provided code and produce a structured review.

## Review Checklist

For each file, evaluate:
1. **Code Quality** — readability, naming, structure, DRY, single responsibility
2. **Potential Issues** — logic errors, race conditions, memory leaks, edge cases
3. **Maintainability** — testability, documentation, coupling, cohesion

## Output Format

| File | Line(s) | Severity | Issue |
|------|---------|----------|-------|
| `@file.ts` | 42-55 | High | Description |

**Severity levels**: High (must fix), Medium (should fix), Low (nice to have)
```

### Security Auditor Agent

**File**: `.opencode/agent/security-auditor.md`

```markdown
---
description: Security audit of code for vulnerabilities and best practices
edit: deny
bash: deny
---

You are a security engineer performing a code security audit.

## Check Items

- Input validation / SQL injection / XSS
- Authentication / authorization bypass
- Hardcoded secrets (API keys, passwords, tokens)
- Dependency vulnerabilities
- Insecure deserialization
- Path traversal
- CSRF / SSRF
- Insecure direct object references (IDOR)

## Output Format

| File | Line(s | Issue | OWASP Category | Risk Level |
|------|--------|-------|----------------|------------|
| `@file.ts` | 15 | SQL injection via string concat | A1: Injection | Critical |

**Risk Levels**: Critical, High, Medium, Low
```

### Test Writer Agent

**File**: `.opencode/agent/test-writer.md`

```markdown
---
description: Analyzes code and generates comprehensive test suites
edit: deny
bash: deny
---

You are a QA engineer. Analyze the provided code and generate a test strategy.

## Test Strategy

For each function/module:
1. **Unit tests** — test each function in isolation
2. **Integration tests** — test component interactions
3. **Boundary tests** — edge cases, min/max values, empty/null inputs
4. **Exception tests** — error handling, expected failures

## Coverage Requirements

- Aim for >80% line coverage
- Cover all public API surfaces
- Test both happy path and error paths
```

### Workflow Command (Multi-Agent Orchestration)

**File**: `.opencode/command/comprehensive-review.md`

```markdown
---
description: Comprehensive code review
---
Execute in order:
1. @code-reviewer
2. @security-auditor
3. @test-writer
Target: $ARGUMENTS
```

**Usage**: Create the command file, then write `.opencode/command/comprehensive-review.md` and invoke with something like `@comprehensive-review @src/main.ts`.

---

## B6 Air-gapped / On-premise

### Environment Variables to Disable External Access

| # | Variable | Value | Purpose |
|---|----------|-------|---------|
| 1 | `OPENCODE_DISABLE_MODELS_FETCH` | `true` | Skip fetching model list from models.dev |
|   | `OPENCODE_MODELS_PATH` | `~/.cache/opencode/models.json` | Local path to pre-downloaded models.json |
| 2 | `OPENCODE_MODELS_URL` | `https://internal-mirror/...` | Alternative: internal mirror (do NOT set DISABLE) |
| 3 | `OPENCODE_DISABLE_DEFAULT_PLUGINS` | `true` | Skip downloading default plugins |
| 4 | `OPENCODE_DISABLE_AUTOUPDATE` | `true` | Disable auto-update checks |
| 5 | `OPENCODE_DISABLE_LSP_DOWNLOAD` | `true` | Disable LSP binary downloads |

**Note**: For option 2 (internal mirror), do NOT set `OPENCODE_DISABLE_MODELS_FETCH=true`. Set `OPENCODE_MODELS_URL` instead.

### Critical: Dependency Hang Fix

**Symptom**: OpenCode hangs at startup trying to install `@opencode-ai/plugin`.

**Root cause**: `src/config/config.ts:237-257` runs `bun add @opencode-ai/plugin`. In air-gapped environments this hangs waiting for network.

**Fix**:

```bash
mkdir -p ~/.config/opencode/node_modules
```

An empty `node_modules` directory at the config path makes OpenCode skip the install step entirely, because it checks for existing `node_modules` before attempting to run `bun add`.

### Internal AI Gateway Configuration

```jsonc
{
  "provider": {
    "corp-gateway": {
      "api": "https://ai-gateway.company.internal/v1",
      "models": {
        "qwen2.5-72b": {
          "tool_call": true,
          "reasoning": true,
          "limit": {
            "context": 128000,
            "output": 8192
          }
        }
      }
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `api` | Internal gateway URL (OpenAI-compatible) |
| `tool_call` | Whether model supports function/tool calling |
| `reasoning` | Whether model supports reasoning/thinking |
| `limit.context` | Max context window in tokens |
| `limit.output` | Max output tokens |

### grep Tool: ripgrep Requirement

- OpenCode's `grep` tool requires **ripgrep (`rg`)** pre-installed on the system
- In air-gapped environments, `rg` cannot be downloaded automatically
- **Must be pre-installed** via system package manager or bundled with the deployment

**Verification**:
```bash
rg --version
```

### Ollama (Local) Configuration

```jsonc
{
  "provider": {
    "ollama": {
      "api": "http://localhost:11434/v1"
    }
  }
}
```

### Verification Commands

```bash
# Test the internal gateway works
opencode run -m corp-gateway/qwen2.5-72b "1+1=?" --print-logs

# Debug mode with full logs
opencode run "test" --print-logs --log-level DEBUG
```

**Look for in DEBUG logs**:
- `service=models.dev` — if present, fetch is happening (may hang in air-gap)
- `service=bun` — if present, plugin install is happening (may hang in air-gap)
- These should be absent if DISABLE flags are correctly set

### One-Click Setup Scripts

#### Basic (Fully Offline)

```bash
#!/bin/bash
# Fully offline setup - no external network access required

# 1. Set environment variables
export OPENCODE_DISABLE_MODELS_FETCH=true
export OPENCODE_DISABLE_DEFAULT_PLUGINS=true
export OPENCODE_DISABLE_AUTOUPDATE=true
export OPENCODE_DISABLE_LSP_DOWNLOAD=true
export OPENCODE_MODELS_PATH=/opt/opencode/models.json

# 2. Prevent dependency install hang
mkdir -p ~/.config/opencode/node_modules

# 3. Verify ripgrep is installed
if ! command -v rg &> /dev/null; then
  echo "ERROR: ripgrep (rg) is required. Install it first."
  exit 1
fi

echo "OpenCode air-gap setup complete."
```

#### Advanced (Internal Mirror)

```bash
#!/bin/bash
# Advanced setup with internal mirror support

# 1. Use internal mirror (do NOT set DISABLE_MODELS_FETCH)
export OPENCODE_MODELS_URL=https://internal-mirror.company.internal/models.json
export OPENCODE_DISABLE_DEFAULT_PLUGINS=true
export OPENCODE_DISABLE_AUTOUPDATE=true
export OPENCODE_DISABLE_LSP_DOWNLOAD=true

# 2. Configure internal AI gateway
mkdir -p ~/.config/opencode
cat > ~/.config/opencode/opencode.json << 'EOF'
{
  "provider": {
    "corp-gateway": {
      "api": "https://ai-gateway.company.internal/v1",
      "models": {
        "qwen2.5-72b": {
          "tool_call": true,
          "reasoning": true,
          "limit": { "context": 128000, "output": 8192 }
        }
      }
    }
  }
}
EOF

# 3. Verify
echo "Verifying gateway connectivity..."
opencode run -m corp-gateway/qwen2.5-72b "1+1=?" --print-logs
```

### Enterprise Environment Variable Reference

| Variable | Value | Effect |
|----------|-------|--------|
| `OPENCODE_DISABLE_MODELS_FETCH` | `true` | Disables fetching model list from models.dev |
| `OPENCODE_MODELS_PATH` | `~/.cache/opencode/models.json` | Local path for models list |
| `OPENCODE_MODELS_URL` | `https://internal-mirror/...` | Internal mirror for models.dev |
| `OPENCODE_DISABLE_DEFAULT_PLUGINS` | `true` | Disables default plugin installation |
| `OPENCODE_DISABLE_AUTOUPDATE` | `true` | Disables auto-update |
| `OPENCODE_DISABLE_LSP_DOWNLOAD` | `true` | Disables LSP download |
| `OPENCODE_DISABLE_PROJECT_CONFIG` | `true` | Disables scanning project-level config |
