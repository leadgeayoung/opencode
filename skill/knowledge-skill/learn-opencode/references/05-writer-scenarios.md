# Writer Scenarios

---

## 1. Content Workflow (`writer-workflow`)

### Plan → Build Pattern

| Phase | Agent | Action |
|-------|-------|--------|
| **Plan** | Plan Agent (Tab) | Outline, structure, research, topic strategy |
| **Build** | Build Agent (Tab) | Draft, edit, polish, publish-ready output |

Invoke Plan first: `@plan Outline a 10-post series on productivity` → review → Tab → Build: `@build Write post 1 from the outline`.

### File-Based Content Management

- All content lives in **Markdown files** on disk — not a web UI.
- Organize: `content/{type}/{topic}/{slug}.md`
- `@file` references: `@content/blog/my-post.md` to pull existing content into conversation.
- Batch production: process 5, 10, or 20 pieces in a single session.

### `/init` for Content Rules

- Run `/init` in a content project to generate `AGENTS.md`.
- Include writing conventions: tone, audience, formatting, platform specifics.
- `/init Focus on copywriting for B2B SaaS products` — passes custom params.

### Workflow Commands

| Command | Purpose |
|---------|---------|
| `@file` | Reference existing content for continuation or remixing |
| `/init` | Bootstrap AGENTS.md with content rules |
| `!git` | Version control for content files |

---

## 2. Blog / Newsletter (`writer-blog`, `writer-wechat`)

### Batch Topic Planning

```
Prompt: Generate 15 blog post topics about [niche] for the next quarter.
Categorize by: beginner / intermediate / advanced.
Include SEO keywords for each.
```

### Series Management

- Maintain series consistency: part numbers, callbacks, progressive complexity.
- Reference earlier posts via `@content/series/series-name/index.md`.
- AGENTS.md stores style guide:
  ```markdown
  ## Blog Style
  - Tone: Conversational but authoritative
  - Average length: 1500-2000 words
  - H2 for major sections, H3 for subsections
  - Opening hook in first 50 words
  - CTA at end (subscribe, comment, share)
  - Internal links to 2-3 related posts
  ```

### Content Pipeline

```
Topic → Outline → Draft → Polish → Publish
  1       2         3        4         5
```

- **Topic**: batch-generate 10-20 ideas.
- **Outline**: H1 → H2 → H3 structure with key points per section.
- **Draft**: Build Agent writes full post from outline.
- **Polish**: `Polish this post: tighten sentences, improve flow, check tone.`
- **Publish**: `!git add . && !git commit -m "post: [title]"`

### Version Control with `!git`

| Command | When |
|---------|------|
| `!git diff` | Review changes before finalizing |
| `!git add <file>` | Stage specific posts |
| `!git commit -m "post: [slug]"` | Commit with descriptive message |
| `!git push` | Deploy to publishing pipeline |

### WeChat Official Account (公众号)

- Platform-specific formatting: WeChat不允许外链, use `#` for headings.
- WeChat style guide in AGENTS.md:
  ```markdown
  ## WeChat Style
  - Use emoji sparingly in titles
  - Short paragraphs (3-4 sentences max)
  - WeChat reading index optimization
  - Lead image required (16:9 ratio)
  - No external links in body
  - "在看" and "分享" call-to-action at end
  ```
- Batch schedule: generate 7 articles for the week in one session.
- Series continuity across WeChat articles via `#系列名` tags.

---

## 3. Short Social (`writer-xiaohongshu`, `writer-social`)

### Batch Post Generation

```
Prompt: Generate 10 xiaohongshu posts about [topic].
Each post: title (2 lines max), body (200-500 chars), 3-5 hashtags.
Include hook in first line.
```

### Topic Library Management

- Maintain `topics/` directory with category files.
- Example: `topics/beauty.md`:
  ```markdown
  # Beauty Topics
  - Morning routine 5-step skincare
  - Drugstore vs luxury foundation comparison
  - Seasonal lip color recommendations
  - ...
  ```
- Reference via `@topics/beauty.md` when generating.

### Image + Text Pairing

| Element | Specification |
|---------|---------------|
| Cover image | 3:4 ratio, text overlay, high contrast |
| Inline images | 1 per 100 chars, lifestyle aesthetic |
| Image descriptions | Alternative text for accessibility |
| Rich text | Emoji highlight, line breaks, bullet points |

### Platform-Specific Style Guides

| Platform | Tone | Hashtags | Format |
|----------|------|----------|--------|
| **Xiaohongshu** | Friendly, detailed, personal | 3-5 per post, mix broad+niche | Title + body + tags |
| **Weibo** | Punchy, trending | Up to 2, relevant | Short text + image(s) |
| **Douyin** | Script-style, fast | 1-2, broad | Video script format |
| **Bilibili** | Narrative, community | 3-5, detailed | Long-form text + CC |

### Content Calendar Planning

```
Prompt: Plan a content calendar for [platform] covering [month].
- 4 posts per week
- Theme per week: [e.g., Mon=Tips, Wed=Reviews, Fri=Tutorials]
- Seasonal events: [holidays, trends]
- Output as table: Date | Topic | Format | Status
```

### AGENTS.md Style Rules for Social

```markdown
## Short Social Rules
- First 3 words must hook reader
- Every post must include one "save-worthy" takeaway
- Emoji count: max 3 per post (xiaohongshu), max 1 (weibo)
- Use numbered lists for steps/tips
- End with engagement question
```

---

## 4. Marketing Copy (`writer-copywriting`)

### AIDA Model

| Stage | Purpose | Example Prompt |
|-------|---------|----------------|
| **Attention** | Hook, stop scrolling | `Write 5 headlines for [product] that grab attention` |
| **Interest** | Engage, show relevance | `Explain [problem] and why it matters to [audience]` |
| **Desire** | Make them want it | `Describe the transformation [product] enables` |
| **Action** | Call to action | `Generate 3 urgent CTAs for [offer]` |

Full AIDA prompt:
```
Write copy for [product] using AIDA structure:
- Attention: [headline]
- Interest: [2-3 sentences on the problem]
- Desire: [benefits, social proof, features]
- Action: [CTA button text]
Target audience: [persona]
Tone: [brand voice]
```

### A/B Variant Generation

| Variant | Change |
|---------|--------|
| **A** | Original approach |
| **B1** | Different hook angle |
| **B2** | Different emotional appeal (fear vs aspiration) |
| **B3** | Different CTA urgency |
| **B4** | Short vs long form |
| **B5** | Benefit-first vs feature-first |

```
Prompt: Generate 5 A/B variants of this landing page headline.
Original: "The Best Project Management Tool"
Variant angles: 1) Pain point, 2) Social proof, 3) Curiosity gap,
4) Direct benefit, 5) Question format.
```

### Asset Library Management

- `assets/copy/` directory structure:
  ```
  assets/
    copy/
      headlines/       # Bank of 100+ headlines by category
      ctas/            # CTA phrases organized by urgency
      social-proof/    # Testimonials, stats, case study snippets
      product-desc/    # Product descriptions at different lengths
  ```
- Use `@assets/copy/headlines/saas.md` to pull from library.

### Brand Voice Guidelines in AGENTS.md

```markdown
## Brand Voice
- **Personality**: [e.g., Expert, Friendly, Disruptor, Trusted Advisor]
- **Vocabulary**: Use [terms], avoid [terms]
- **Sentence length**: [Short / Varied / Long-form]
- **Emotional range**: [e.g., Optimistic, Urgent, Empathetic]
- **Grammar quirks**: [e.g., Start sentences with "And", Use Oxford comma]
- **Company values**: [Key messaging pillars]
- **Competitors**: Do not mention [brands], differentiate by [X]
```

### Headline Generation Techniques

| Technique | Formula | Example |
|-----------|---------|---------|
| How-to | "How to [benefit] in [timeframe]" | "How to Double Your Email Open Rates in 7 Days" |
| Listicle | "[Number] [adjective] Ways to [goal]" | "7 Proven Ways to Reduce Churn" |
| Question | "Are You Making This [topic] Mistake?" | "Are You Making This SEO Mistake?" |
| Curiosity | "What [authority] Won't Tell You About [topic]" | "What Top Writers Won't Tell You About Productivity" |
| Direct | "[Product]: The [category] for [audience]" | "Notion: The Workspace for Remote Teams" |
| Before/After | "From [pain] to [gain] with [solution]" | "From Overwhelmed to Organized with This System" |
| Social Proof | "[Number] [people] Use [product] to [result]" | "50,000 Writers Use This Tool to Beat Writer's Block" |

---

## 5. Translation & Polish (`writer-translate`)

### Batch Translation Workflow

```
Steps:
1. @file source/content.md — load source file
2. Translate all content to [target language]
3. Maintain formatting (headings, lists, links, code blocks)
4. Output to translations/[lang]/[filename].md
```

For multi-file batch:
```
Prompt: Translate all files in content/ to Spanish.
- Preserve frontmatter
- Adapt cultural references for [region]
- Output to content/es/ maintaining directory structure
- Report any terms requiring manual review
```

### Glossary Management

Terms glossary in `glossary/[lang-pair].md`:
```markdown
# EN → ZH Glossary

| English | 中文 | Notes |
|---------|------|-------|
| dashboard | 仪表盘 | Product UI term |
| onboarding | 上手引导 | Not "入职" |
| engagement | 参与度 | User metric context |
| feature flag | 功能开关 | Engineering term |
```

Reference: `@glossary/en-zh.md` before translation.

### Tone / Register Adjustment

| Source Tone | Target Tone | Prompt Addition |
|-------------|-------------|-----------------|
| Formal | Casual | `Make this sound like a friendly blog post` |
| Technical | General | `Simplify for a general audience, explain terms` |
| Marketing | Educational | `Change from persuasive to informative tone` |
| Corporate | Conversational | `Rewrite in first-person, use contractions` |
| Literal | Natural | `Make this sound like native [language] writing` |

### Multi-Format Output

| Format | Extension | Considerations |
|--------|-----------|---------------|
| Markdown | `.md` | Preserve all Markdown syntax |
| HTML | `.html` | Preserve tags, escape content |
| Plain text | `.txt` | Strip formatting, keep structure |
| JSON/i18n | `.json` | Maintain key-value structure, nested keys |
| SRT/CAPTIONS | `.srt` | Timecode preservation, line length limits |

### Quality Checklist

- [ ] All headings translated (check H1-H6)
- [ ] Links preserved and functional (update locale-specific URLs)
- [ ] Images: alt text translated, locale-appropriate images swapped
- [ ] Code blocks: comments translated, code untouched
- [ ] Frontmatter fields translated (title, description, tags)
- [ ] Cultural adaptation: idioms, references, examples localized
- [ ] Glossary terms consistent across all files
- [ ] Character count / reading time within spec
- [ ] Numbers, dates, currency formatted for locale
- [ ] Right-to-left support if applicable

---

## 6. Novel Writing (`writer-novel`)

### Multi-File Management

```
novels/
  my-novel/
    chapters/
      01-opening.md
      02-inciting-incident.md
      03-first-plot-point.md
      ...
    characters/
      protagonist.md
      antagonist.md
      supporting-cast.md
    world/
      geography.md
      magic-system.md
      history-timeline.md
    outline.md
    style-guide.md
```

### Character Cards

Prototype in `characters/protagonist.md`:
```markdown
# Character: [Name]

## Basic
- Role: [Protagonist / Antagonist / Love Interest / Mentor]
- Age: [age]
- Occupation: [job]

## Personality
- MBTI / Archetype: [e.g., INTJ / The Hero]
- Core motivation: [What drives them?]
- Fear: [What holds them back?]
- Flaw: [Internal weakness]
- Arc: [What do they learn?]

## Backstory
- Key event that shaped them: [event]
- Secret: [something only the reader (eventually) knows]
- Lie they believe: [misbelief that drives conflict]

## Relationships
- [Char A]: [rival, ally, love interest]
- [Char B]: [mentor, antagonist]

## Voice
- Speech patterns: [formal/slang/regional]
- Internal monologue style: [reflective/impulsive]

## Physical
- Appearance: [key traits]
- Mannerism: [repeated gesture or habit]
- Wardrobe: [signature style]

## Notes
- [Spoilers, planned developments, unresolved threads]
```

### Plot Consistency Checking

```
Prompt: Check my novel for consistency issues:
- Character ages and timelines
- Plot holes across chapters 1-10
- Unresolved foreshadowing
- Continuity errors (objects, locations, character knowledge)
- Pacing: are there slow stretches?
Reference: @novels/my-novel/ (full directory)
```

### Chapter-by-Chapter Generation

```
Plan → Build cycle:

Phase 1 (Plan Agent):
  Analyze: @novels/my-novel/outline.md
  Task: "Plan chapter 12. What POV? What scenes? What emotional beat?
         What setup/payoff does it need to tie to chapters 8-11?"

Phase 2 (Build Agent):
  Output: "Write chapter 12 from the plan. Write 2000-3000 words.
          Match POV style from chapter 11 (@novels/my-novel/chapters/11.md)."

Phase 3 (Polish):
  "Polish chapter 12: tighten prose, vary sentence rhythm, check dialogue tags."
```

### World-Building Documentation

`world/` directory files:

| File | Contents |
|------|----------|
| `geography.md` | Maps, climate, regions, key locations |
| `magic-system.md` | Rules, limitations, costs, user types |
| `history-timeline.md` | Major events, eras, wars, discoveries |
| `culture.md` | Social norms, taboos, festivals, food, clothing |
| `politics.md` | Factions, power structures, alliances, conflicts |
| `technology.md` | Tech level, inventions, limitations |
| `religion.md` | Gods, beliefs, rituals, organized religion |
| `economy.md` | Currency, trade routes, class system |
| `language.md` | Names, phrases, idioms, naming conventions |

Reference world files during generation:
```
Prompt: Write a scene set in the Northern Wastes. Use @world/geography.md
for environmental details and @world/culture.md for the nomadic tribes' customs.
```

---

## 7. Script Writing (`writer-script`)

### Scene Library Management

```
scripts/
  feature-film/
    scenes/
      01-opening-image.md
      02-theme-stated.md
      03-setup.md
      ...
    characters/
    acts/
      act-1.md
      act-2.md
      act-3.md
    production/
      shot-list.md
      locations.md
      props.md
```

Scene card format:
```markdown
# Scene: [Scene Name]

- **Scene #**: [Number]
- **Location**: [Where]
- **Time**: [When]
- **Characters**: [Who]
- **Summary**: [1-2 sentence description]

## Action
[Blocking, movement, visual description]

## Dialogue
[Character lines and delivery notes]

## Notes
[Director's notes, effects, special requirements]
```

### Format Automation

| Format | Description | Prompt |
|--------|-------------|--------|
| **Screenplay** | Industry standard (Final Draft format) | `Format as screenplay: Scene headings in CAPS, character names centered, dialogue indented, parentheticals italic` |
| **Stage Play** | Stage directions, character entrances | `Format as stage play: Character names bold, stage directions italic, dialogue centered` |
| **TV Script** | Televised format, act breaks | `Format for 30-min TV episode: teaser, 3 acts, tag` |
| **Audio Drama** | Sound cues, voice direction | `Format: [SFX:] for sound effects, (V.O.) for voiceover parentheticals` |
| **Video Script** | Visual + Audio dual column | `Format: LEFT column video description, RIGHT column audio/dialogue` |

### Character Dialogue Tracking

```
Prompt: Analyze dialogue in my script:
- Does each character have a distinct voice?
- Word choice patterns per character
- Dialogue-to-action ratio by scene
- Check for exposition dumps
- Identify overused phrases per character
Generate a "dialogue fingerprint" for each major character.
```

### Three-Act Structure Planning

| Act | Function | Page Count (Feature) | Key Beats |
|-----|----------|---------------------|-----------|
| **Act 1** | Setup | 1-25 | Opening image, inciting incident, first plot point |
| **Act 2** | Confrontation | 25-85 | Rising action, midpoint, all is lost, dark night of the soul |
| **Act 3** | Resolution | 85-110 | Climax, falling action, final image |

Prompt for act planning:
```
Outline Act 2 of my screenplay using Save the Cat beats:
- B Story (page 30)
- Fun and Games (page 35-55)
- Midpoint (page 55)
- Bad Guys Close In (page 55-75)
- All Is Lost (page 75)
- Dark Night of the Soul (page 75-85)
Reference: @scripts/feature-film/acts/act-1.md
```

### Production Notes

- `production/` directory:
  ```
  production/
    shot-list.md       # Scene-by-scene shot requirements
    locations.md       # Location descriptions, availability, permits
    props.md           # Prop list per scene
    costumes.md        # Character costume breakdown
    budget.md          # Estimated costs
    schedule.md        # Shooting schedule (by location, not chrono)
  ```
- Generate call sheets: `Prompt: Create a call sheet for Day 2 using @production/schedule.md and @scenes/ that we're shooting that day.`

---

## 8. Web Novel (`writer-webnovel`)

### Daily Update Workflow

```
Daily session:
1. Review: @webnovels/my-series/chapters/ — check last published chapter
2. Recall plot threads: @webnovels/my-series/outline.md
3. Generate next chapter (1500-3000 words)
4. Polish and format for platform
5. Schedule or publish
6. Document reader engagement in tracking file
```

### Batch Stockpile Content

- Maintain a `stockpile/` buffer of 10-20 pre-written chapters.
- Strategy: write 5 chapters in one session → queue 1/day.
- Allows time-sensitive edits based on reader feedback without breaking daily schedule.

```
Prompt: Write 5 stockpile chapters for my web novel.
Use @webnovels/my-series/outline.md for plot direction.
Chapters should be self-contained with hooks but advance the main arc.
Target: 2000 words each, publishable as standalone episodes.
```

### Serialization Management

- Episode metadata format in frontmatter:
  ```yaml
  ---
  title: "Chapter 42: The Descent"
  arc: "Shadow Arc"
  word_count: 2450
  publish_date: 2026-07-04
  status: draft | edited | queued | published
  cliffhanger: true
  notes: "Follow up on the letter reveal in ch 40"
  ---
  ```

- Arc tracking file `arcs.md`:
  ```markdown
  # Story Arcs
  | Arc | Chapters | Status | Notes |
  |-----|----------|--------|-------|
  | Introduction | 1-10 | Complete | Good pacing |
  | Shadow Arc | 11-25 | In Progress | Needs more tension in ch 18 |
  | Revelation | 26-35 | Planned | Key reveals: parentage, betrayal |
  | Finale | 36-45 | Drafting | Ensure all threads resolve |
  ```

### Reader Engagement Tracking

Tracking file `engagement.md`:
```markdown
# Reader Engagement Dashboard

| Chapter | Views | Comments | Rating | Key Feedback |
|---------|-------|----------|--------|--------------|
| 40 | 12.5K | 89 | 4.7 | "Best chapter yet!" |
| 41 | 11.2K | 72 | 4.5 | "Pacing felt slow in middle" |
| 42 | 14.1K | 105 | 4.8 | "That cliffhanger!" |

## Trends
- Engagement spike on chapters with romantic subplot
- Dip on lore-heavy exposition chapters
- Comments mention wanting more antagonist POV
```

### Chapter Cliffhanger Techniques

| Technique | Formula | Example |
|-----------|---------|---------|
| **Revelation** | Reveal shocking information | "The letter was signed by someone I thought was dead." |
| **Interruption** | Cut at peak action | "The door flew open — and then everything went dark." |
| **Question** | End on unanswered question | "If he wasn't my father… then who was?" |
| **Arrival** | New character/force appears | "A figure stepped out of the shadows, and my blood ran cold." |
| **Choice** | Protagonist forced into impossible decision | "Save her — or save the world. I had three seconds to choose." |
| **Betrayal** | Trusted character revealed as traitor | "His smile never wavered as the blade slid between my ribs." |

Format for generating cliffhangers:
```
Prompt: Write 3 alternative cliffhanger endings for chapter [N].
Current situation: [brief context]
Each option should: create urgency, raise stakes, make readers click "next".
```

### Platform Publishing

| Platform | Format | Update Cadence | Monetization |
|----------|--------|----------------|--------------|
| Webnovel | 1500-3000 words/chapter | Daily | Paid chapters, ads |
| Royal Road | 2000-4000 words/chapter | 3x/week | Patreon, ads |
| Wattpad | 1500-2500 words/chapter | Weekly | Paid stories, brand deals |
| AO3 | Variable | Flexible | Free, donation-based |
| Self-publish | Novel-length volumes | Per volume | Amazon KDP, Kindle |

---

## 9. Content Workstation (`writer-workstation`)

### Custom Agent Creation for Writers

**Agent locations:**

| Scope | Path |
|-------|------|
| Global | `~/.config/opencode/agent/<name>.md` |
| Project | `.opencode/agent/<name>.md` |

**Example writer-style Agent (Markdown):**

```markdown
---
description: Blog post writing expert
mode: subagent
temperature: 0.7
permission:
  edit: deny
  bash: deny
---
# Role
You are a professional blog writer specializing in [niche].
You write engaging, well-researched, SEO-optimized blog posts.

# Style
- Hook in first paragraph
- H2/H3 structure with clear transitions
- Data-backed claims with sources
- Conversational but authoritative tone
- 1500-2000 words target length

# Instructions
- Ask clarifying questions before writing if brief is ambiguous
- Propose 3 angles for the post before drafting
- Include meta description, SEO keywords, and suggested featured image
- End with discussion question and CTA
```

**Example JSON agent config (in opencode.json):**

```jsonc
{
  "agent": {
    "translator": {
      "mode": "subagent",
      "temperature": 0.3,
      "description": "Professional translator: technical docs, marketing, literary",
      "permission": {
        "edit": { "*": "deny", "translations/**": "allow" },
        "bash": { "*": "deny", "ls": "allow" }
      }
    },
    "copywriter": {
      "mode": "subagent",
      "temperature": 0.8,
      "description": "Marketing copywriter: AIDA, headlines, landing pages, email campaigns",
      "permission": {
        "edit": "deny",
        "bash": "deny"
      }
    }
  }
}
```

### Custom Commands for Writers

**Command locations:**

| Scope | Path |
|-------|------|
| Global | `~/.config/opencode/command/<name>.md` |
| Project | `.opencode/command/<name>.md` |

**Example command `.opencode/command/write-post.md`:**

```markdown
---
description: Write a blog post on $ARGUMENTS
---
Write a blog post about $ARGUMENTS following our style guide.
Structure: H1 title, engaging hook, 3-5 H2 sections, conclusion, CTA.
Target length: 1500 words.
Include meta description and SEO keywords at the end.
```

**Example command `.opencode/command/translate-chapter.md`:**

```markdown
---
description: Translate a novel chapter to $ARGUMENTS
---
Translate @file to $ARGUMENTS.
- Use glossary from @glossary/en-es.md
- Preserve narrative voice and style
- Adapt cultural references for [target audience]
- Output to translations/$ARGUMENTS/ with same filename
```

**Example command `.opencode/command/generate-series.md`:**

```markdown
---
description: Plan a content series with N posts
---
Generate a content series plan with $ARGUMENTS posts.
For each post: title, target keyword, key takeaway, CTA.
Ensure posts build on each other sequentially.
Output as a table with status column.
```

**Or define commands in opencode.json:**

```jsonc
{
  "command": {
    "write-post": {
      "template": "Write a blog post about $ARGUMENTS following our style guide. Target 1500 words, include SEO keywords, end with CTA.",
      "description": "Create new blog post"
    },
    "draft-chapter": {
      "template": "Draft the next chapter of my web novel. Reference @webnovels/my-series/outline.md. Target 2000 words, end with cliffhanger.",
      "description": "Draft next web novel chapter"
    },
    "polish": {
      "template": "Polish @file: tighten prose, fix passive voice, vary sentence length, check dialogue tags. Preserve all content.",
      "description": "Polish and edit a draft"
    },
    "translate-batch": {
      "template": "Translate all files in @source/ to $ARGUMENTS using @glossary. Maintain markdown structure and frontmatter.",
      "description": "Batch translate content directory"
    }
  }
}
```

### Custom Skills for Writers

**Skill directory structure:**

```
skill/
  my-writing-skill/
    SKILL.md            # Main skill definition
    references/         # Style guides, templates, examples
    scripts/            # Content processing automation
```

**SKILL.md example for a writing skill:**

```markdown
---
name: blog-production
description: "Weekly blog newsletter production: generate, edit, publish"
---
# Blog Production Workflow

## Process
1. Monday: batch topic generation
2. Tuesday: outline refinement
3. Wednesday: draft primary post
4. Thursday: edit and polish
5. Friday: publish and promote

## Style Guide
See `references/blog-style-guide.md`

## Templates
See `references/templates/`

## Automation
Run `scripts/check-consistency.ps1` before publishing to verify:
- All links work
- No placeholder text
- Consistent heading hierarchy
- Correct file naming convention
```

**References directory examples:**

```
skill/my-writing-skill/
  references/
    blog-style-guide.md       # Tone, voice, formatting rules
    aida-template.md          # AIDA copy structure template
    headline-formulas.md      # 50 headline templates
    chapter-template.md       # Novel chapter template
    social-calendar.md        # Content calendar template
    seo-checklist.md          # On-page SEO checklist
    brand-voice-matrix.md     # Brand voice by channel
```

**Scripts directory examples for content processing:**

```
skill/my-writing-skill/
  scripts/
    check-word-count.ps1     # Validate word counts across chapters
    build-toc.ps1            # Auto-generate table of contents
    find-inconsistencies.ps1 # Cross-reference character/plot details
    format-for-platform.ps1  # Convert Markdown to platform format
    batch-translate.ps1      # Batch translation pipeline
```

Example script `check-word-count.ps1`:
```powershell
param([string]$Path = ".")
Get-ChildItem -Path $Path -Recurse -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $words = $content -split '\s+' | Where-Object { $_ -ne '' }
    [PSCustomObject]@{
        File = $_.Name
        Path = $_.FullName
        Words = $words.Count
    }
} | Format-Table -AutoSize
```

### Complete Writer Workstation Config Example

`opencode.json` for a full writing setup:

```jsonc
{
  "agent": {
    "editor": {
      "mode": "subagent",
      "temperature": 0.4,
      "description": "Line-level editor: grammar, style, clarity, tone",
      "permission": { "edit": "deny", "bash": "deny" }
    },
    "planner": {
      "mode": "subagent",
      "temperature": 0.2,
      "description": "Content strategist: outlines, series planning, calendars",
      "permission": { "edit": "deny", "bash": "deny" }
    }
  },
  "command": {
    "write": {
      "template": "Write about $ARGUMENTS. Reference style from AGENTS.md.",
      "description": "Write on any topic"
    },
    "edit-piece": {
      "template": "Edit @file for clarity, flow, grammar, and tone consistency.",
      "description": "Edit a piece of content"
    },
    "outline": {
      "template": "Create a detailed outline for $ARGUMENTS. Include thesis, 5-7 sections, key points per section.",
      "description": "Create a content outline"
    }
  },
  "skill": [
    "./skill/blog-production",
    "./skill/copywriting"
  ]
}
```

---

## Skill Directory Reference

When loading a writing skill, agents gain access to its `references/` and `scripts/`. Use `@skill` or agent auto-selection to invoke skill-based workflows. Skills can be layered: a blog-production skill shares AGENTS.md rules with a copywriting skill. Merge order is defined by the `skill` array in `opencode.json`.

---

## Quick Reference: Tooling by Scenario

| Scenario | Key Agent | Key Command | Key File Pattern |
|----------|-----------|-------------|------------------|
| Workflow | Plan + Build | `/init`, `@file` | `content/**/*.md` |
| Blog | Build | `write-post` | `content/blog/` |
| WeChat | Build | `write-post` | `content/wechat/` |
| Xiaohongshu | Build | custom social | `content/social/xhs/` |
| Copywriting | Build (0.8 temp) | `write`, `polish` | `assets/copy/` |
| Translation | Build (0.3 temp) | `translate-batch` | `translations/` |
| Novel | Plan + Build (0.7) | `draft-chapter` | `novels/*/chapters/` |
| Script | Plan + Build | custom | `scripts/*/scenes/` |
| Web Novel | Build | `draft-chapter` | `webnovels/*/chapters/` |
| Workstation | Custom agents | custom commands | `skill/*/`, `agent/*` |
