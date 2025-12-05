---
description: Transform raw codebook into standardized Markdown format
argument-hint: [survey_id]
autoApprove:
  - Bash(*)
  - Task(*)
---

Transform raw codebook (PDF/PPTX/TXT) into standardized Markdown format for Claude processing.

## Arguments:
- $1: Survey ID (required) - e.g., "test", "ces2019"

## What this does:

1. Validates that survey is initialized
2. Launches **transform-codebook** agent via Task tool to:
   - Read codebook.pdf (or .pptx, .txt) from surveys/$1/
   - Extract variable names, questions, and response options
   - Generate surveys/$1/codebook.md in standardized format
3. Reports transformation summary

## Usage:

```
/transform-codebook test
/transform-codebook ces2019
```

## Steps:

1. **Validate arguments**:
   - If $1 is missing, prompt for survey ID and exit
   - If `surveys/$1/` doesn't exist, report error and exit

2. **Launch transform-codebook agent**:
   - Use Task tool with:
     - subagent_type: "transform-codebook"
     - description: "Transform codebook for $1"
     - prompt: "Transform codebook for $1"

3. **Report completion**:
   - Display agent's summary report
   - Show number of variables documented
   - Confirm codebook.md created

## Next steps:

After transformation:
1. Review and edit codebook.md manually if needed
2. Start cleaning variables with `/clean-var $1 variable_name`
