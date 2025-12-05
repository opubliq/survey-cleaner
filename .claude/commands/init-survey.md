---
description: Initialize survey structure by copying files from _SharedFolder_data_produit
argument-hint: [survey_id]
autoApprove:
  - Bash(*)
  - Task(*)
---

Initialize a new survey by copying files from _SharedFolder_data_produit and creating status.json entry.

## Arguments:
- $1: Survey ID (required) - e.g., "test", "ces2019"

## What this does:

1. Validates that `_SharedFolder_data_produit/$1/` exists with data and codebook files
2. Launches **survey-init** agent via Task tool to:
   - Copy files from _SharedFolder_data_produit to surveys/$1/
   - Create entry in surveys/status.json
   - Copy clean.py template
3. Reports initialization summary

## Usage:

```
/init-survey test
/init-survey ces2019
```

## Steps:

1. **Validate arguments**:
   - If $1 is missing, prompt for survey ID and exit
   - If `_SharedFolder_data_produit/$1/` doesn't exist, report error and exit

2. **Launch survey-init agent**:
   - Use Task tool with:
     - subagent_type: "survey-init"
     - description: "Initialize survey $1"
     - prompt: "Initialize survey $1"

3. **Report completion**:
   - Display agent's summary report
   - Confirm files created in surveys/$1/
   - Show status.json entry

## Next steps:

After initialization:
1. Run `/transform-codebook $1` to generate codebook.md
2. Start cleaning variables with `/clean-var $1 variable_name`
