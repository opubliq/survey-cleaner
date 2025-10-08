---
description: Initialize survey structure and create tracking files
argument-hint: [survey_name]
autoApprove:
  - Bash(*)
  - Task(*)
---

Initialize a survey directory structure using the survey-init-agent.

## Arguments:
- $1: Survey name (required) - e.g., "test", "ces19"

## What this does:

1. Validates that survey directory exists at `surveys/$1/`
2. Launches **survey-init-agent** via Task tool to:
   - Create `raw/` and `processed/` directories
   - Move data and codebook files to `raw/`
   - Extract all column names from data file
   - Create `variables_todo.md` with all variables listed as pending
   - Create `pending_vars.txt` with one variable per line (for shell loop)
   - Copy and customize `clean.py` template
3. Reports initialization summary

## Usage:

```
/init-survey test
/init-survey ces19
```

## Steps:

1. **Validate arguments**:
   - If $1 is missing, list available surveys and exit
   - If `surveys/$1/` doesn't exist, report error and exit

2. **Launch survey-init-agent**:
   - Use Task tool with:
     - subagent_type: "survey-init-agent"
     - description: "Initialize survey $1"
     - prompt: "Initialize survey surveys/$1"

3. **Report completion**:
   - Display agent's summary report
   - Confirm files created:
     - `variables_todo.md` ✓
     - `pending_vars.txt` ✓
     - `clean.py` ✓

## Notes:

- Agent will create structure if it doesn't exist
- Safe to run on already-initialized surveys (will skip existing files)
- Next step: Use `/clean-var` to process variables one by one
