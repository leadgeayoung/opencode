# Distribution & Permissions

## Distribution Methods

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Local Directory** | Personal use | Simple and direct | Not easy to share |
| **Extra Paths** | Team sharing (NAS) | Configure once, use everywhere | Requires filesystem sharing |
| **Remote URL** | Enterprise/Community | Auto-update, version management | Requires server setup |
| **Git Repository** | Open Source/Team | Version control, easy collaboration | Requires manual pull updates |

### Method 1: Local Directory

Place directly in a supported search path:
- `~/.config/opencode/skill/<name>/SKILL.md`
- `.opencode/skill/<name>/SKILL.md`

### Method 2: Extra Paths

```jsonc
{
  "skills": {
    "paths": [
      "~/team-skills",
      "../shared-skills",
      "/opt/company-skills"
    ]
  }
}
```

Path resolution: `~/` expands to home, absolute paths used as-is, relative paths resolved from project root. The configured path must contain a `skill/` subdirectory.

### Method 3: Remote URL

Server serves `index.json`:
```json
{
  "skills": [
    {
      "name": "git-release",
      "description": "Create consistent releases and changelogs",
      "files": ["SKILL.md", "template.md", "references/release-checklist.md"]
    }
  ]
}
```

Cached to `~/.cache/opencode/skills/` on first fetch.

### Method 4: Git Repository

```bash
git clone https://github.com/company/opencode-skills.git ~/opencode-skills
```

```jsonc
{
  "skills": {
    "paths": ["~/opencode-skills/skills"]
  }
}
```

Team workflow: `git pull` to get latest skills.

## Permission Configuration

### Global Permissions

```jsonc
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

| Permission | Behavior |
|------------|----------|
| `allow` | Skill loads immediately |
| `deny` | Skill hidden from agent, access rejected |
| `ask` | User prompted for approval before loading |

Patterns support wildcards: `internal-*` matches `internal-docs`, etc.

### Override Per Agent

```yaml
# Custom agent frontmatter
---
permission:
  skill:
    "documents-*": "allow"
---
```

### Disable Skill Tool

```yaml
# Custom agent frontmatter
---
tools:
  skill: false
---
```
