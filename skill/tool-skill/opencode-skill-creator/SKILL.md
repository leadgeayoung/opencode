---
name: opencode-skill-creator
description: |
  Create, edit, audit, and validate SKILL.md files for opencode's skill system.
  Provides: description writing templates, design pattern selection guide, directory structure rules, frontmatter schema, trigger test methodology.
  Suitable for: building new skills from scratch, revising existing skills, auditing skills for security, validating frontmatter and trigger behavior.
  Not suitable for: configuring MCP servers, writing project-specific AGENTS.md/CLAUDE.md, installing plugins.
compatibility: opencode
---

# opencode Skill Creator

## Skill Design Principles

Skills use 3-layer progressive disclosure to conserve context:

| Layer | Content | When Loaded |
|-------|---------|-------------|
| 1 | `name` + `description` (~100 words) | Always visible in `<available_skills>` |
| 2 | SKILL.md body | On task match via `skill({ name })` |
| 3 | `references/`, `scripts/`, `assets/` | On demand by agent |

Information exists in exactly one place — either SKILL.md or references/, never both.

## Quick Creation Flow

```
1. Clarify Requirements → 2. Name → 3. Description → 4. Instructions → 5. Test
```

Detailed process → `references/creation-test.md`

## Description Writing (Critical for Triggering)

Template:
```yaml
description: |
  [One sentence: core capability]
  Provides: [resources like table structures, formulas, templates]
  Suitable for: [trigger scenario 1], [trigger scenario 2]
  Not suitable for: [boundary scenario 1], [boundary scenario 2]
```

Good:
```yaml
description: |
  Extract tables from PDFs and convert to CSV for data analysis workflows.
  Provides: PDF parsing logic, table extraction patterns, CSV formatting rules.
  Suitable for: filling PDF forms, batch processing PDF documents, extracting embedded PDF data.
  Not suitable for: simple PDF viewing, basic format conversion, PDF editing.
```

Bad: `description: "Help with documents"` — too vague, won't trigger reliably.

## Directory Structure

```
skill-name/
  SKILL.md              # Required: frontmatter + workflow
  scripts/              # Deterministic helpers (loaded via bash)
  references/           # Detailed docs (loaded on demand)
  assets/               # Templates/output resources
  agents/               # UI metadata
```

### name Validation

- `^[a-z0-9]+(-[a-z0-9]+)*$`
- 1–64 chars, lowercase, hyphen-separated
- Must match directory name containing SKILL.md

## Design Pattern Decision Tree

Task involves multi-step fixed-order process?
  └── Yes → Sequential Orchestration → `references/design-patterns.md`
  └── No → Spans multiple MCP services?
          ├── Yes → Multi-MCP Coordination → `references/design-patterns.md`
          └── No → Output quality needs iteration?
                  ├── Yes → Iterative Optimization → `references/design-patterns.md`
                  └── No → Tool choice depends on context?
                          ├── Yes → Context-Aware Tool Selection → `references/design-patterns.md`
                          └── No → Domain expertise beyond tools?
                                  ├── Yes → Domain Intelligence → `references/design-patterns.md`
                                  └── No → Simple workflow: just list steps inline

## Validation Checklist

- [ ] YAML frontmatter has `name` + `description` + `compatibility`
- [ ] `name` matches regex and directory name
- [ ] `description` follows Provides/Suitable/Not suitable template
- [ ] Trigger test: 3+ positive cases activate (e.g. "Use [skill]", semantic match)
- [ ] Negative test: 3+ boundary cases don't activate
- [ ] All `references/` files exist and are referenced in SKILL.md
- [ ] Permission config exists if needed (allow/deny/ask)

## Frontmatter Schema

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Skill identifier, matches dir name |
| `description` | yes | 3-part template |
| `license` | no | License info |
| `compatibility` | no | e.g. `opencode` |
| `metadata` | no | Custom key-value pairs |
| `homepage` | no | URL (local skills only) |
| `allowed-tools` | no | Tool allowlist (local skills only) |
| `user-invocable` | no | Direct user invocation (local skills only) |

Distribution methods and permission configuration → `references/distribution.md`
