---
description: Clean one survey variable by generating transformation code
argument-hint: [survey_id] [variable_name]
autoApprove:
  - Bash(*)
  - Task(*)
---

Clean a single survey variable by generating transformation code and metadata.

## Arguments:
- $1: Survey ID (required) - e.g., "test", "ces2019"
- $2: Variable name (required) - e.g., "Q1_province", "satisfaction_gov"

## What this does:

1. Validates that survey is initialized and codebook exists
2. Launches **clean-variable** agent via Task tool to:
   - Explore the raw variable in data
   - Search codebook.md for variable documentation
   - Generate cleaning code in clean.py
   - Generate CODEBOOK_VARIABLES metadata entry
   - Update surveys/status.json (variables.cleaned += 1)
3. Reports cleaning summary

## Usage:

```
/clean-var test Q1_province
/clean-var ces2019 satisfaction_gov
```

## Steps:

1. **Validate arguments**:
   - If $1 or $2 is missing, prompt and exit
   - If `surveys/$1/` doesn't exist, report error and exit
   - If `surveys/$1/codebook.md` missing, suggest running `/transform-codebook` first

2. **Launch clean-variable agent**:
   - Use Task tool with:
     - subagent_type: "clean-variable"
     - description: "Clean variable $2 in $1"
     - prompt: "Clean variable $2 in survey $1"

3. **Report completion**:
   - Display agent's summary report
   - Show progress: X/Y variables cleaned
   - Confirm code added to clean.py

## Next steps:

After cleaning a variable:
1. Review generated code in clean.py
2. Run `/validate-cleaning $1 $2` to test transformation
3. Continue with next variable or run `/finalize-survey $1` when done
