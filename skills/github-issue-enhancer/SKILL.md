---
name: github-issue-enhancer
description: Enhance GitHub issues with additional information, context, and structure to prepare them for autonomous agent processing. Detects missing information, clarifies requirements, and adds acceptance criteria through interactive Q&A. Use when the user says "enhance this issue", "prepare issue for agent", "make issue more detailed", "add context to issue", or similar.
---

# GitHub Issue Enhancer Workflow

Transform raw GitHub issues into agent-ready specifications by detecting gaps, clarifying requirements, and adding structure through interactive questioning.

## When to Use

Trigger this skill when the user wants to:

- Enhance a GitHub issue with missing details
- Prepare an issue for autonomous agent processing
- Add acceptance criteria and technical context
- Structure an unstructured issue description
- Fill information gaps before handing off to an agent

## Step 1 — Retrieve the Issue

Get the issue content from the user or GitHub API:

**If issue number provided:**

```bash
gh issue view <issue-number> --json title,body,labels,assignees,comments
```

**If issue content provided directly:**
Parse the markdown content to extract:

- Title
- Description/Body
- Labels
- Any existing comments or context

Store the original issue content for comparison.

## Step 2 — Initial Analysis

Analyze the issue for completeness using these criteria:

### Required Elements Checklist

- [ ] Clear title describing the work
- [ ] Problem statement or goal description
- [ ] Expected behavior/outcome
- [ ] Acceptance criteria (explicit or implicit)
- [ ] Technical context or constraints
- [ ] Priority or urgency indication
- [ ] Related issues or dependencies
- [ ] Definition of "done"

### Gap Detection

For each missing element, note:

- What information is absent
- Why it matters for agent execution
- What questions need to be asked

### Quality Assessment

Rate the issue on:

- **Clarity**: Is the goal unambiguous?
- **Completeness**: Can an agent execute without guessing?
- **Actionability**: Are next steps clear?
- **Testability**: Can success be measured?

## Step 3 — Interactive Q&A Session

Based on detected gaps, ask targeted questions to gather missing information. Use `ask_user_question` for structured choices when applicable.

### Common Question Categories

#### 1. Problem Understanding

```text
Question: "What specific problem does this issue address?"
Options:
- Bug fix (unexpected behavior)
- Feature request (new capability)
- Technical debt (refactoring/improvement)
- Documentation (missing or unclear docs)
- Infrastructure (devops, deployment, config)
```

#### 2. Scope Definition

```text
Question: "What should be in scope for this work?"
Options:
- Minimal viable fix only
- Core functionality + basic edge cases
- Full implementation with error handling
- Complete solution with tests and docs
```

#### 3. Technical Constraints

```text
Question: "Are there technical constraints to consider?"
Options:
- Must maintain backward compatibility
- Performance requirements exist
- Security/compliance requirements
- Integration with existing systems
- No constraints, full flexibility
```

#### 4. Success Criteria

```text
Question: "How should success be measured?"
Options:
- All existing tests pass
- New tests added and passing
- Manual verification steps defined
- Performance benchmarks met
- User acceptance criteria satisfied
```

#### 5. Dependencies & Context

```text
Question: "What dependencies or context matter?"
Options:
- Depends on other issues/PRs
- Requires external service changes
- Needs team coordination
- Blocks other work
- Independent, no dependencies
```

**For open-ended gaps**, use free-text questions to gather specific details.

## Step 4 — Enhancement Generation

Combine original issue content with gathered information to create an enhanced version:

### Enhanced Issue Structure

```markdown
# [Original Title]

## Summary

[Brief 1-2 sentence overview]

## Problem Statement

[What problem is being solved, why it matters]

## Goals & Objectives

- [ ] Primary goal
- [ ] Secondary goals
- [ ] Out of scope (explicitly stated)

## Acceptance Criteria

### Functional

- [ ] Criterion 1
- [ ] Criterion 2

### Technical

- [ ] Criterion 1
- [ ] Criterion 2

### Quality

- [ ] Tests passing
- [ ] Documentation updated
- [ ] Performance requirements met

## Technical Context

[Relevant technical details, constraints, patterns]

## Implementation Notes

[Suggested approach, considerations, gotchas]

## Dependencies

[Related issues, blocking work, required changes]

## Definition of Done

- [ ] All acceptance criteria met
- [ ] Code reviewed and merged
- [ ] Tests passing in CI
- [ ] Documentation updated
- [ ] Deployed to [environment]

## Original Issue Reference

[Link to original issue, timestamp of enhancement]
```

## Step 5 — Review & Refine

Present the enhanced issue to the user:

1. **Show the enhanced version** in full
2. **Highlight additions** (what was added vs. original)
3. **Request feedback**:
   - "Is anything missing?"
   - "Is anything incorrect?"
   - "Should any criteria be adjusted?"

4. **Iterate** based on feedback until approved

## Step 6 — Update GitHub Issue

Once approved, update the original GitHub issue:

```bash
# Option A: Update issue body directly
gh issue edit <issue-number> --body-file <enhanced-issue.md>

# Option B: Add enhancement as a detailed comment (preserves history)
gh issue comment <issue-number> --body-file <enhanced-issue.md>
```

**Recommendation**: Use Option B (comment) to preserve the original issue history while making the enhanced version available.

## Step 7 — Generate Agent-Ready Output

Create a final version optimized for autonomous agent consumption:

### Agent Prompt Format

```markdown
## Task: [Issue Title]

### Context

[Background, why this matters]

### Objective

[Clear, single-sentence goal]

### Requirements

1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

### Constraints

- [Constraint 1]
- [Constraint 2]

### Acceptance Criteria

[ ] Criterion 1 - measurable, testable
[ ] Criterion 2 - measurable, testable

### Deliverables

- [ ] Code changes
- [ ] Tests
- [ ] Documentation
- [ ] [Other]

### Success Metrics

[How to verify completion]

### Original Issue

[Link to GitHub issue]
```

## Error Handling

- **Issue not found**: Report clearly, ask for correct issue number
- **API authentication failed**: Guide user to authenticate with `gh auth login`
- **Missing critical information**: Flag as blocking, ask user to provide
- **Conflicting requirements**: Surface conflict, ask for resolution

## Best Practices

1. **Preserve original intent**: Don't change the core goal, only clarify and expand
2. **Be specific**: Replace vague terms with measurable criteria
3. **Assume nothing**: If something isn't clear, ask
4. **Document decisions**: Note why certain choices were made
5. **Keep it actionable**: Every criterion should be verifiable
6. **Maintain traceability**: Always link back to original issue

## Example Workflow

### Input Issue

```text
Title: Fix login bug
Body: Users can't login sometimes. Please fix.
```

### Analysis

- ❌ Unclear: "sometimes" - when? how often?
- ❌ Missing: Steps to reproduce
- ❌ Missing: Expected vs actual behavior
- ❌ Missing: Acceptance criteria
- ❌ Missing: Technical context

### Q&A

- When does the login failure occur? (Specific conditions)
- What error message do users see?
- What browser/environment?
- How urgent is this?

### Enhanced Output

```markdown
# Fix Intermittent Login Failures

## Problem Statement

Users experience intermittent login failures in production, occurring approximately 5-10% of login attempts. This impacts user experience and support load.

## Acceptance Criteria

- [ ] Login succeeds 99.9% of attempts under normal load
- [ ] Error messages are clear and actionable
- [ ] Failed attempts are logged with context for debugging
- [ ] No regression in successful login rate

## Technical Context

- Authentication uses JWT tokens
- Issue appears related to rate limiting service
- Affects web and mobile clients

## Definition of Done

- [ ] Root cause identified and fixed
- [ ] Unit tests added for edge cases
- [ ] Load testing confirms 99.9% success rate
- [ ] Monitoring alerts configured
```

## Commands Reference

```bash
# View issue
gh issue view <number> --json title,body,labels

# Edit issue body
gh issue edit <number> --body-file <file.md>

# Add comment
gh issue comment <number> --body-file <file.md>

# List issues
gh issue list --limit <n>
```
