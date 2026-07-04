# 09 — Skills System

---

## 1. Overview: What Are Skills?

Skills are compact, triggerable, on-demand-loaded workflows that encapsulate domain knowledge for OpenCode agents. They are defined through `SKILL.md` files that agents automatically discover and load based on task semantics.

**Key design principles:**
- **Progressive disclosure**: metadata always visible; body loads only after trigger; references/scripts/assets load only as needed
- **On-demand loading**: context window preserved until needed
- **Reusable**: cross-project, cross-team domain knowledge
- **Semantic triggering**: agent decides based on `description` field, not keywords

### Skill vs CLAUDE.md / AGENTS.md

| Feature | CLAUDE.md / AGENTS.md | Skill |
|---------|----------------------|-------|
| Loading Timing | Always loaded to context | Only loaded when task matches |
| Scope | Current project | Reusable across projects |
| Content Type | Pure Markdown | Markdown + code + resource files |
| Platform | Claude Code / OpenCode only | Claude.ai / Code / API |
| Typical Use | Coding conventions, local commands | Domain knowledge, workflows |

**Selection principle**: Project-specific conventions → CLAUDE.md / AGENTS.md. Reusable domain knowledge → Skill.

### Why Skills Exist

Without Skills, the agent starts fresh every conversation — it knows neither your table structures, nor your metric definitions, nor your business rules, nor your team conventions. Skills bridge this gap by wrapping institutional knowledge into loadable units.

---

## 2. SKILL.md Frontmatter

Each `SKILL.md` must start with YAML frontmatter delimited by `---` lines. Unknown frontmatter fields are silently ignored.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier, used for invocation. Must match directory name. |
| `description` | string | Trigger condition description (1-1024 chars). Most important field. |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `license` | string | License information |
| `compatibility` | string | Compatibility markers (e.g. `opencode`) |
| `metadata` | map (string→string) | Custom key-value pairs |
| `homepage` | string | URL for skill home page (local skills only) |
| `allowed-tools` | list | Tool allowlist (local skills only) |
| `user-invocable` | boolean | Whether users can invoke directly (local skills only) |

### name Validation Rules

- 1–64 characters
- Lowercase alphanumeric with single hyphen separators
- Must not start or end with `-`
- Must not contain consecutive `--`
- Must match the directory name containing `SKILL.md`

**Regex**: `^[a-z0-9]+(-[a-z0-9]+)*$`

**Examples:**
```
✓ code-review       ✓ sql-analysis       ✓ git-release
✗ Code_Review       ✗ sql--analysis      ✗ -review
```

### description Writing (Critical for Triggering)

`description` is the **sole factor** determining whether a Skill triggers. The agent uses semantic understanding, not keyword matching.

**Poor**: `description: Help with documents` — too vague.

**Template**:
```yaml
description: |
  [One sentence explaining core capability]
  Provides: [resources this Skill contains, like table structures, formulas, templates]
  Suitable for: [trigger scenario 1], [trigger scenario 2], [trigger scenario 3]
  Not suitable for: [boundary scenario 1], [boundary scenario 2]
```

**Good example**:
```yaml
description: |
  Extract tables from PDFs and convert to CSV format for data analysis workflows.
  Provides: PDF parsing logic, table extraction patterns, CSV formatting rules.
  Suitable for: filling PDF forms, batch processing PDF documents, extracting embedded PDF data.
  Not suitable for: simple PDF viewing, basic format conversion, PDF editing.
```

### Local Skills Additional Frontmatter

Local skills (not remote) may also use:
- `homepage` (string)
- `allowed-tools` (array of strings)
- `user-invocable` (boolean)

---

## 3. Skill Directory Structure

### Basic Structure
```
skill-name/
  SKILL.md    # Required. Markdown with YAML frontmatter
```

### Recommended Complete Structure
```
skill-name/
  SKILL.md          # Main file: workflow and key logic (Layer 2)
  scripts/          # Deterministic helpers (loaded on demand via bash)
  references/       # Detailed docs (loaded only when needed)
    finance.md
    product.md
  assets/           # Templates/media
  agents/           # UI metadata
```

### Nested Directory Support

OpenCode supports nested skill directories via the glob `{skill,skills}/**/SKILL.md`. The `**` matches subdirectories at any depth. The skill name is determined by the frontmatter `name` field, not the directory hierarchy.

```
.opencode/skill/
  audit/
    security/
      SKILL.md    # name: might be "security-audit" — directory nesting is irrelevant
```

---

## 4. Skill Loading & Discovery

### Search Paths (in order, later overrides earlier)

| Priority | Location | Pattern | Scope |
|----------|----------|---------|-------|
| 1 | `~/.claude/skills/<name>/SKILL.md` | `skills/**/SKILL.md` | Global external |
| 2 | `~/.agents/skills/<name>/SKILL.md` | `skills/**/SKILL.md` | Global external |
| 3 | `.claude/skills/<name>/SKILL.md` | `skills/**/SKILL.md` | Project external (cwd→git root) |
| 4 | `.agents/skills/<name>/SKILL.md` | `skills/**/SKILL.md` | Project external (cwd→git root) |
| 5 | `.opencode/skills/<name>/SKILL.md` | `{skill,skills}/**/SKILL.md` | Project OpenCode (cwd→git root) |
| 6 | `~/.config/opencode/skills/<name>/SKILL.md` | `{skill,skills}/**/SKILL.md` | Global OpenCode |
| 7 | `skills.paths` (extra paths) | `**/SKILL.md` | Custom configured |
| 8 | `skills.urls` (remote URLs) | `**/SKILL.md` | Cached remote |

**Project-local path traversal**: OpenCode walks up from current working directory until it reaches the git worktree root, scanning for skill directories at each level.

### OpenCode Skill Glob Patterns (Source: `skill/skill.ts`)

```typescript
const EXTERNAL_DIRS = [".claude", ".agents"];
const EXTERNAL_SKILL_GLOB = new Bun.Glob("skills/**/SKILL.md");
const OPENCODE_SKILL_GLOB = new Bun.Glob("{skill,skills}/**/SKILL.md");
const SKILL_GLOB = new Bun.Glob("**/SKILL.md");
```

Both `skill/` (singular) and `skills/` (plural) are supported for OpenCode directories.

### Config Schema

```typescript
skills: {
  paths: string[],  // Additional Skill directory paths
  urls: string[]    // Remote Skill index URLs
}
```

### Custom Config Directory via Environment Variable

```bash
export OPENCODE_CONFIG_DIR="/path/to/custom/config"
```

OpenCode scans both the default `~/.config/opencode/skill/` and `$OPENCODE_CONFIG_DIR/skill/`.

### Key API Functions

| Function | Description |
|----------|-------------|
| `Skill.state()` | Returns current skill state (cached via `Instance.state`) |
| `Skill.get(name)` | Returns a single skill by name |
| `Skill.all()` | Returns array of all loaded skills |
| `Skill.dirs()` | Returns array of all skill directories |
| `Discovery.pull(url)` | Fetches index.json from remote URL, downloads files |

### Loading Mechanism

1. At startup, OpenCode scans all skill directories and aggregates `name` + `description` into the `skill` tool description as `<available_skills>` XML
2. When user sends a message, the agent evaluates task semantics against each skill's `description`
3. On match, agent calls `skill({ name: "sql-analysis" })`
4. Full SKILL.md content loads into agent context
5. The base directory path is provided so the agent can read `references/` files on demand

### Duplicate Name Handling

If the same skill name exists in multiple locations, the later-loaded one overrides. A warning is logged:
```
log.warn("duplicate skill name", { name, existing, duplicate });
```

---

## 5. Three-Layer Progressive Disclosure Structure

Skills use layered loading to conserve context window:

```
Layer 1: name + description (~100 words)
  → Always visible in <available_skills>, used to determine if loading is needed

Layer 2: SKILL.md body content
  → Loaded when task matches, contains main instructions, workflows, decision trees

Layer 3: references/ directory (and scripts/, assets/)
  → Loaded only when specific details are needed; agent reads on demand
```

**Principle**: Information should exist in exactly one place — either SKILL.md OR references/, never both.

**Example SKILL.md (Layer 2)**:
```markdown
---
name: sql-analysis
description: For analyzing business data: revenue, ARR, customer segmentation, product usage.
---

## Workflow

1. Clarify analysis requirements
2. Choose the correct data source
3. Apply standard filters
4. Validate results

## Data Source Selection

| Analysis Type | Recommended Table | Detailed Docs |
|--------------|-------------------|---------------|
| Revenue Analysis | monthly_revenue | `references/finance.md` |
| Product Usage | daily_usage | `references/product.md` |

## Required Filters

All queries must:
- Exclude test accounts: `account != 'Test'`
- Use only complete periods

Read corresponding files in references/ when specific table structures or query examples are needed.
```

**Example references/finance.md (Layer 3)**:
```markdown
# Financial Tables

## monthly_revenue

| Field | Type | Description |
|-------|------|-------------|
| account_id | STRING | Account ID |
| month | DATE | Month (first day) |
| mrr | FLOAT | Monthly Recurring Revenue |
| arr | FLOAT | Annual Recurring Revenue |

## Common Queries

### Monthly Revenue by Segment
```sql
SELECT segment, DATE_TRUNC(month, MONTH) as period, SUM(mrr) as total_mrr
FROM monthly_revenue
WHERE account_id != 'Test'
GROUP BY 1, 2 ORDER BY 2 DESC, 3 DESC
```
```

---

## 6. Skill + MCP Collaboration (Kitchen & Recipe)

MCP and Skills are complementary:

| Component | Analogy | Role |
|-----------|---------|------|
| **MCP** | Kitchen | Provides tools/services (stove, fridge, knives) |
| **Skill** | Recipe | Best practices for using tools, multi-step orchestration, domain expertise |

- **MCP without Skill** = "kitchen without recipes" — tools exist but no guidance on using them
- **Skill without MCP** = "recipes without a kitchen" — instructions exist but no tools to execute

Skills provide:
- Best practices for using MCP tools
- Multi-step workflow orchestration across MCP services
- Domain expertise that tool descriptions alone cannot convey

---

## 7. Three Use Case Categories

| Category | Characteristics | Skill Focus |
|----------|----------------|-------------|
| **1. Document/Asset Creation** | Output quality priority | Embed style guides, templates, quality checklists |
| **2. Workflow Automation** | Multi-step consistency | Step definitions, validation gates, error handling |
| **3. MCP Enhancement** | Tool usage optimization | Coordinate MCP calls, embed domain knowledge |

### Category 1: Document/Asset Creation
- Output quality is the top priority
- Embed style guides, brand guidelines, templates, quality checklists directly
- Examples: DOCX creation skill, brand guidelines skill, frontend design skill

### Category 2: Workflow Automation
- Multi-step processes must execute consistently
- Define step dependencies, validation gates, rollback procedures, error handling
- Examples: CI/CD pipeline skill, release management skill

### Category 3: MCP Enhancement
- Optimize how tools from MCP servers are used
- Coordinate calls across multiple MCP services
- Embed domain knowledge that tool descriptions cannot convey
- Examples: Design→Dev handoff across Figma→Drive→Linear→Slack MCPs

---

## 8. Five Skill Workflow Design Patterns

### Pattern 1: Sequential Orchestration

**Use when**: Multi-step processes with a fixed order. Each step depends on previous step output.

**Key techniques**:
- Explicit step ordering
- Dependencies between steps
- Validation at each stage
- Rollback instructions for failures

**Example**:
```markdown
## Step 1: Create Account
- Validate email format
- Check for duplicate
- Insert into database

## Step 2: Setup Payment
- Requires: Step 1 (account_id)
- Create billing profile
- Set default payment method

## Step 3: Create Subscription
- Requires: Step 2 (billing_profile_id)
- Choose plan tier
- Set billing cycle

## Step 4: Send Welcome Email
- Requires: Step 3 (subscription_id)
- Compose welcome template
- Send via email service

## Failure Rollback
- Step 1 fail: log error, no cleanup needed
- Step 2 fail: rollback Step 1 (delete account), notify admin
- Step 3 fail: rollback Step 2 (delete billing profile), log
- Step 4 fail: subscription active but email pending, retry
```

### Pattern 2: Multi-MCP Coordination

**Use when**: Workflows span multiple services. Clear phase separation with data passing between phases and validation gates.

**Key techniques**:
- Clear phase separation
- Data passing between MCPs
- Validation before moving to next phase
- Centralized error handling

**Example: Design→Dev Handoff**
```
Phase 1: Design Review (Figma MCP)
  → Extract design specs, assets, style guides
  → Validate design completeness

Phase 2: Asset Management (Drive MCP)
  → Upload finalized assets
  → Organize by component category
  → Generate asset URLs

Phase 3: Task Creation (Linear MCP)
  → Create development tickets
  → Attach design specs and assets
  → Set priority and assignee

Phase 4: Notification (Slack MCP)
  → Send handoff summary to team channel
  → Tag relevant developers
  → Include links to tickets and assets
```

### Pattern 3: Iterative Optimization

**Use when**: Output quality requires multiple improvement cycles. Define a Draft → Validate → Fix → Re-validate loop with a clear termination condition.

**Key techniques**:
- Explicit quality criteria
- Iterative improvement loop
- Validation scripts
- Know when to stop iterating

**Structure**:
```
WHILE quality not met AND iterations < max:
  1. Fix issues
  2. Regenerate output
  3. Validate against quality criteria

Termination: quality_met OR iterations >= max_N
```

**Example**:
```markdown
## Code Review Optimization Loop

1. **Draft**: Generate initial implementation
2. **Validate**: Run linter, type-checker, tests
3. **Fix**: Address all errors and warnings
4. **Re-validate**: Rerun checks
5. **Repeat**: Max 3 iterations or until all checks pass

## Termination Condition
- All lint/type/test checks pass
- Code coverage >= 80%
- No TODO/FIXME comments remaining
```

### Pattern 4: Context-Aware Tool Selection

**Use when**: Same goal can be achieved with different tools depending on context. Define a decision tree with transparent choices and fallback options.

**Key techniques**:
- Clear decision criteria
- Fallback options
- Transparency about choices

**Example: File Storage Selection**
```markdown
## Choose Storage Location

| Context | Tool | Rationale |
|---------|------|-----------|
| Large files (>10MB) | Cloud Storage | Context window limitation |
| Collaborative editing | Notion/Drive | Team access required |
| Code snippets | GitHub Gist | Version control, sharing |
| Temporary/scratch data | Local filesystem | Speed, no network |

## Decision Tree

Is the file >10MB?
  ├── Yes → Use Cloud Storage MCP
  │         Fallback: Split file, upload parts
  └── No → Does it need collaboration?
            ├── Yes → Use Notion MCP
            │         Fallback: Local file + share link
            └── No → Is it code?
                      ├── Yes → Use GitHub Gist MCP
                      └── No → Use Local filesystem
```

### Pattern 5: Domain Intelligence

**Use when**: The skill provides expertise beyond tool access. Embed domain knowledge before action, enforce compliance first, maintain an audit trail.

**Key techniques**:
- Domain expertise embedded in logic
- Compliance before action
- Comprehensive documentation
- Clear governance

**Example: Payment Compliance**
```markdown
## Payment Processing Workflow

### Phase 1: Compliance Check (MANDATORY — run first)
1. **Sanctions Check**: Screen against OFAC/SDN lists
   - API: sanctions-mcp.check(entity_name)
   - If matched → BLOCK, notify compliance team
2. **Jurisdiction Verify**: Determine applicable regulations
   - EU → GDPR + PSD2
   - US → State-specific money transmitter laws
3. **Risk Assessment**: Score transaction risk (1-100)
   - >80 → manual review required
   - 50-80 → enhanced due diligence
   - <50 → proceed

### Phase 2: Processing
- Only execute if Phase 1 passes all checks
- Log every step with timestamps

### Phase 3: Audit Trail
- Store complete transaction record
- Include risk score, checks performed, timestamps
- Retention: 7 years per regulatory requirements
```

---

## 9. Permission Configuration

### Global Permissions (`opencode.json`)

```jsonc
{
  "permission": {
    "skill": {
      "*": "allow",            // Default: allow all
      "pr-review": "allow",    // Load immediately
      "internal-*": "deny",    // Hidden, access rejected
      "experimental-*": "ask"  // User prompted before loading
    }
  }
}
```

| Permission | Behavior |
|------------|----------|
| `allow` | Skill loads immediately |
| `deny` | Skill hidden from agent, access rejected |
| `ask` | User prompted for approval before loading |

Patterns support wildcards: `internal-*` matches `internal-docs`, `internal-tools`, etc.

### Override Per Agent

**Custom agent frontmatter**:
```yaml
---
permission:
  skill:
    "documents-*": "allow"
---
```

**Built-in agents in `opencode.json`**:
```jsonc
{
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow"
        }
      }
    }
  }
}
```

### Disable Skill Tool Entirely

**Custom agent frontmatter**:
```yaml
---
tools:
  skill: false
---
```

**Built-in agents**:
```jsonc
{
  "agent": {
    "plan": {
      "tools": {
        "skill": false
      }
    }
  }
}
```

When disabled, the `<available_skills>` section is omitted entirely from the agent's tool description.

---

## 10. Distribution Methods

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Local Directory** | Personal use | Simple and direct | Not easy to share |
| **Extra Paths** | Team sharing (NAS) | Configure once, use everywhere | Requires filesystem sharing |
| **Remote URL** | Enterprise/Community | Auto-update, version management | Requires server setup |
| **Git Repository** | Open Source/Team | Version control, easy collaboration | Requires manual pull updates |

### Method 1: Local Directory Placement

Place skills directly in one of the supported search paths (`.opencode/skills/`, `~/.config/opencode/skills/`, etc.).

### Method 2: Configure Extra Paths

Specify additional skill directories in `opencode.json`:

```jsonc
{
  "skills": {
    "paths": [
      "~/my-skills",
      "../shared-team-skills",
      "/opt/company-skills",
      "C:\\Team\\Skills"
    ]
  }
}
```

Path resolution:
- `~/` expands to home directory
- Absolute paths used as-is
- Relative paths resolved from project root

The configured path must contain a `skill/` or `skills/` subdirectory with skills inside. Scanned with `**/SKILL.md` glob.

### Method 3: Remote URL Discovery (Recommended for Teams/Community)

OpenCode supports automatic skill downloads from remote servers:

```jsonc
{
  "skills": {
    "urls": [
      "https://company.com/.well-known/skills/",
      "https://skills.example.com/index.json"
    ]
  }
}
```

**Server must serve `index.json`**:
```json
{
  "skills": [
    {
      "name": "git-release",
      "description": "Create consistent releases and changelogs",
      "files": ["SKILL.md", "template.md", "references/release-checklist.md"]
    },
    {
      "name": "code-review",
      "description": "Review code for issues and security vulnerabilities",
      "files": ["SKILL.md", "checklist.md"]
    }
  ]
}
```

**Server directory structure**:
```
.well-known/skills/
  index.json
  git-release/
    SKILL.md
    template.md
    references/
      release-checklist.md
  code-review/
    SKILL.md
    checklist.md
```

**OpenCode download process**:
1. Fetches `index.json` from the remote URL
2. For each skill in the index, downloads its listed files
3. Caches everything to `~/.cache/opencode/skills/`
4. Loads cached skills automatically on subsequent launches

### Method 4: Git Repository Sharing

Combine Git repository with extra path configuration:

```bash
# Clone to a fixed location
git clone https://github.com/yourcompany/opencode-skills.git ~/opencode-skills
```

```jsonc
{
  "skills": {
    "paths": ["~/opencode-skills/skills"]
  }
}
```

Team workflow: `git pull` to get the latest skills.

---

## 11. Complete SKILL.md Example

```markdown
---
name: git-release
description: Create consistent releases and changelogs. Drafts release notes from merged PRs, proposes version bumps, provides gh release create commands.
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

# Git Release Skill

## Workflow

1. Determine version bump (major/minor/patch) based on commit history
2. Generate changelog from merged PRs since last tag
3. Create annotated git tag
4. Draft release notes
5. Provide `gh release create` command

## Version Bump Rules

| Change Type | Bump |
|-------------|------|
| Breaking changes | major |
| New features | minor |
| Bug fixes | patch |

## Changelog Format

### [version] - YYYY-MM-DD
- Feature: [description] (#PR)
- Fix: [description] (#PR)
- Chore: [description] (#PR)

## References

- Commit convention details → `references/commit-conventions.md`
- Release checklist → `references/release-checklist.md`
```

---

## 12. Executable Script Integration

### Why Scripts

Some operations are more efficient as code than as generated tokens:
- Sorting/filtering (milliseconds vs many tokens)
- PDF parsing (direct file processing vs loading into context)
- Format conversion (deterministic vs error-prone)

### Structure

```
skill/
  pdf-skill/
    SKILL.md
    scripts/
      extract_form_fields.py
      merge_pdfs.py
```

### Script Writing Principles

1. **Independently executable** — no complex environment dependencies
2. **Clear input/output** — explicit parameters and return formats
3. **Error handling** — gracefully handle exceptions
4. **Minimal dependencies** — only use necessary libraries

### Referencing Scripts in SKILL.md

```markdown
## Extract Form Fields

Run directly:
```bash
python scripts/extract_form_fields.py input.pdf
```

Output:
```json
{"fields": [{"name": "full_name", "type": "text", "value": ""}]}
```

## Merge PDFs
```bash
python scripts/merge_pdfs.py file1.pdf file2.pdf -o output.pdf
```

See `references/scripts-guide.md` for detailed parameter descriptions.
```

### Example Script (`scripts/extract_form_fields.py`)

```python
#!/usr/bin/env python3
"""Extract PDF form field information"""
import sys, json

def extract_fields(pdf_path: str) -> dict:
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        fields = reader.get_fields() or {}
        result = [{"name": n, "type": str(f.get("/FT","unknown")), "value": str(f.get("/V",""))} for n, f in fields.items()]
        return {"fields": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: extract_form_fields.py <pdf_path>"}))
        sys.exit(1)
    print(json.dumps(extract_fields(sys.argv[1]), indent=2))
```

---

## 13. 5-Step Skill Creation Process

### Step 1: Clarify Requirements

| Question | Purpose |
|----------|---------|
| What specific problem does this solve? | Clarify value |
| When should it be triggered? | Design description |
| What does successful output look like? | Acceptance criteria |
| What are the edge cases? | Avoid omissions |

**Good candidates**: Reusable knowledge, multi-person processes, stable patterns.
**Not suitable**: One-time tasks, frequently changing content, project-specific conventions (use AGENTS.md).

### Step 2: Write name

Short, clear, lowercase, hyphen-separated. Reflect core functionality.

### Step 3: Write description (Most Critical)

Must include: specific capability, trigger scenarios, target use case, boundary limits.

### Step 4: Write main instructions

Structure with Markdown — headers, lists, tables. Be actionable. Provide concrete examples. State what it can't do. Reference detailed docs.

### Step 5: Test and Validate

#### Test Matrix

| Test Type | Content | Expected | Priority |
|-----------|---------|----------|----------|
| Trigger Test | "Help me query last quarter's revenue" | Skill activates | P0 |
| Boundary Test | "Query revenue" (no time range) | Asks then executes | P1 |
| Negative Test | "Help me write an email" | Doesn't activate | P0 |
| Output Test | Verify output format | Format correct | P1 |
| Error Test | Wrong input parameters | Graceful error | P2 |

#### Trigger Test Cases
```
# Should activate
"Use sql-analysis skill"              → Explicit request
"Help me check last quarter's ARR"    → Semantic match
"Revenue trend analysis"              → Keyword match

# Should NOT activate
"Help me write a SQL tutorial"        → Teaching, not analysis
"Database performance tuning"         → Out of scope
"Create new table"                    → DDL operation, not applicable
```

#### Manual Test Checklist
- [ ] Trigger test: all 3+ positive cases activate
- [ ] Negative test: all 3+ boundary cases don't activate
- [ ] Output test: format matches expectations
- [ ] Novice test: non-experts can successfully use
- [ ] Reference test: all `references/` files exist
- [ ] Error test: clear messages on wrong input

---

## 14. Real-World Examples

### Example: DOCX Creation Skill (Anthropic)

```markdown
---
name: docx
description: "Document creation, editing, and analysis, supporting revisions, comments, format preservation, and text extraction."
license: Proprietary
---

## Workflow Decision Tree

### Read/Analyze → Use "Text Extraction" or "Raw XML Access"
### Create New → Use "Create New Word Document" workflow
### Edit Existing
- Own doc + simple changes → "Basic OOXML Editing"
- Someone else's doc → "Revision Workflow" (recommended default)
- Legal/academic/business/government → Must use revision workflow

## Text Extraction
```bash
pandoc --track-changes=all path-to-file.docx -o output.md
```

## Detailed Docs
- OOXML editing → `ooxml.md`
- docx-js syntax → `docx-js.md`
```

### Example: Frontend Design Skill (Anthropic Engineering Blog)

```markdown
---
name: frontend-design
description: Create unique, production-grade frontend interfaces. Avoids generic AI aesthetics.
---

## Design Thinking

Before coding, understand:
- **Purpose**: What problem? Who's using it?
- **Style**: Minimalism, maximalism, retro-futuristic, etc.
- **Differentiation**: What makes it memorable?

## Typography
Avoid Arial, Inter, Roboto. Use JetBrains Mono, Playfair Display, IBM Plex.

## Color
Unified palette with CSS variables. Bold accent > evenly distributed muted.

## Motion
Staggered page loads, purposeful micro-interactions.

## Absolutely Avoid
- Inter, Roboto, Arial, system fonts
- White bg + purple gradient
- Predictable layout patterns
```

### Example: Brand Guidelines Skill

```markdown
---
name: brand-guidelines
description: Apply company official brand colors and typography for documents, presentations, interfaces.
---

## Colors
- Dark: `#141413`
- Light: `#faf9f5`
- Medium Gray: `#b0aea5`
- Orange: `#d97757`
- Blue: `#6a9bcc`
- Green: `#788c5d`

## Typography
- Headlines: Poppins (24pt+) / Arial fallback
- Body: Lora / Georgia fallback
```

---

## 15. Common Pitfalls & Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Skill won't load | SKILL.md case incorrect | Must be uppercase `SKILL.md` |
| Skill not showing | Missing frontmatter | Must include `name` and `description` |
| Task matches but doesn't trigger | description too vague | Add capabilities, scenarios, boundaries |
| Same-name conflict | Same name in multiple places | Later loaded overrides earlier; check logs |
| Access denied | Permission set to deny | Check permission configuration |
| Directory not recognized | Spelling | Both `skill/` and `skills/` supported |
| Remote download fails | index.json format error | Verify JSON structure |
| MCP call fails but Skill loads | MCP not connected | Configure MCP in `opencode.json` |
| Wrong MCP order | No explicit ordering | Use "Step 1/2/3" to define sequence |
| Infinite optimization loop | Missing termination condition | Add `max N iterations` or quality threshold |

### Troubleshoot Loading Checklist

1. Verify `SKILL.md` is spelled in ALL CAPS
2. Check frontmatter includes both `name` and `description`
3. Ensure skill names are unique across all locations
4. Check permissions — skills with `deny` are hidden from agents
5. Restart agent if needed to rescan directories

---

## 16. Security Audit

### Why Auditing Matters

Skills can contain executable code and instructions that guide the agent to access network resources. Malicious skills could cause data leaks or system damage.

### Audit Checklist

| Check Item | Check Content | Risk |
|-----------|---------------|------|
| File Content | Read all .md files | Suspicious instructions |
| Script Code | Review .py/.js files | Malicious code execution |
| Network Requests | Check URLs and API calls | Data exfiltration |
| File Operations | Check read/write paths | Unauthorized access |
| Environment Variables | Check env var usage | Credential leakage |

---

## 17. Continuous Optimization

1. **Use the skill in real work** — discover gaps and edge cases
2. **Record successes and failures** — what triggered correctly? What didn't?
3. **Periodically review and update** — reflect learnings back into the skill
4. **Share with team** — gather feedback from other users
5. **Iterate with Claude** — use the agent to collaboratively refine the skill

### Collaborative Creation

```
User: Help me create a data warehouse skill. I'll describe our tables and business logic.
Claude: Sure, tell me:
  1. What are your main data tables?
  2. What business terms need definition?
  3. What rules must be followed when querying?
```

### Learning from Failures

When a skill-produced output is wrong, reflect the fix back into the skill:
- Was the instruction not clear enough?
- Was an edge case not covered?
- Was a constraint not emphasized?
