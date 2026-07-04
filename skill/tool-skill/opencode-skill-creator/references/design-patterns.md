# Design Patterns

## Pattern 1: Sequential Orchestration

**When**: Multi-step processes with fixed order. Each step depends on previous output.

Structure:
```
## Step 1: Create Account
- Validate email format
- Check for duplicate
- Insert into database

## Step 2: Setup Payment
- Requires: Step 1 (account_id)
- Create billing profile
- Set default payment method

## Failure Rollback
- Step 1 fail: log error, no cleanup needed
- Step 2 fail: rollback Step 1 (delete account), notify admin
```

## Pattern 2: Multi-MCP Coordination

**When**: Workflows span multiple MCP services.

Structure:
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

Phase 4: Notification (Slack MCP)
  → Send handoff summary to team channel
  → Tag relevant developers
```

## Pattern 3: Iterative Optimization

**When**: Output quality requires multiple improvement cycles.

Structure:
```
WHILE quality not met AND iterations < max:
  1. Fix issues
  2. Regenerate output
  3. Validate against quality criteria

Termination: quality_met OR iterations >= max_N
```

Example:
```markdown
1. **Draft**: Generate initial implementation
2. **Validate**: Run linter, type-checker, tests
3. **Fix**: Address all errors and warnings
4. **Re-validate**: Rerun checks
5. **Repeat**: Max 3 iterations or until all checks pass

Termination: all lint/type/test checks pass, no TODO/FIXME remaining
```

## Pattern 4: Context-Aware Tool Selection

**When**: Same goal can be achieved with different tools depending on context.

Structure: Decision tree with transparent choices and fallbacks.

```markdown
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

## Pattern 5: Domain Intelligence

**When**: Skill provides expertise beyond tool access.

Structure: Embed domain knowledge before action, enforce compliance first, maintain audit trail.

Example:
```markdown
### Phase 1: Compliance Check (MANDATORY — run first)
1. **Sanctions Check**: Screen against OFAC/SDN lists
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

### Phase 3: Audit Trail
- Store complete transaction record with timestamps
- Retention: 7 years per regulatory requirements
```
