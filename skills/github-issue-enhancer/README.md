# GitHub Issue Enhancer

A skill to enhance GitHub issues with additional information, context, and structure to prepare them for autonomous agent processing.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated

  ```bash
  brew install gh
  gh auth login
  ```

## Usage

### Basic Usage

When you want to enhance a GitHub issue, simply say:

```text
"Enhance issue #123 for agent processing"
"Prepare this issue for an autonomous agent"
"Add more details to issue #456"
```

### Workflow

1. **Issue Retrieval**: The skill fetches the issue from GitHub
2. **Analysis**: Detects missing information and gaps
3. **Interactive Q&A**: Asks targeted questions to fill gaps
4. **Enhancement**: Generates a structured, detailed issue
5. **Review**: You review and approve the enhancements
6. **Update**: The GitHub issue is updated (as a comment to preserve history)
7. **Agent Output**: Generates an agent-ready prompt format

### Example

**Before** (original issue):

```text
Title: Fix login bug
Body: Users can't login sometimes. Please fix.
```

**After** (enhanced):

```markdown
# Fix Intermittent Login Failures

## Problem Statement

Users experience intermittent login failures in production...

## Acceptance Criteria

- [ ] Login succeeds 99.9% of attempts
- [ ] Error messages are clear and actionable
      ...
```

## Features

- **Gap Detection**: Automatically identifies missing information
- **Interactive Q&A**: Structured questions to gather details
- **Agent-Ready Output**: Format optimized for autonomous agents
- **Preserves History**: Updates via comment to maintain original issue
- **Traceability**: Links back to original issue and enhancement timestamp

## Output Formats

The skill produces:

1. **Enhanced GitHub Issue** (comment on original issue)
2. **Agent-Ready Prompt** (structured format for agent consumption)
3. **Change Summary** (what was added/modified)

## Best Practices

- Be specific about requirements
- Define measurable acceptance criteria
- Include technical context and constraints
- Document dependencies and blockers
- Make success criteria testable
