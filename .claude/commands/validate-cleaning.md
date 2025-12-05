---
description: Validate variable transformation by comparing raw vs cleaned data
argument-hint: [survey_id] [variable_name]
autoApprove:
  - Bash(*)
  - Task(*)
---

Validate that a variable transformation is correct by comparing distributions.

## Arguments:
- $1: Survey ID (required) - e.g., "test", "ces2019"
- $2: Variable name (required) - Variable that was cleaned

## What this does:

1. Validates that variable has been cleaned
2. Launches **validate-cleaning** agent via Task tool to:
   - Load raw data and execute transformation
   - Compare raw vs cleaned distributions
   - Check for unmapped values, data loss, errors
   - Report validation results
3. Reports pass/fail status

## Usage:

```
/validate-cleaning test ses_province
/validate-cleaning ces2019 op_satisfaction_gov
```

## Steps:

1. **Validate arguments**:
   - If $1 or $2 is missing, prompt and exit
   - If `surveys/$1/clean.py` doesn't exist, report error and exit

2. **Launch validate-cleaning agent**:
   - Use Task tool with:
     - subagent_type: "validate-cleaning"
     - description: "Validate $2 in $1"
     - prompt: "Validate cleaning of $2 in survey $1"

3. **Report results**:
   - Display validation checks
   - Show pass/fail status
   - Flag warnings if any

## Next steps:

If validation passed:
- Continue to next variable

If validation failed:
- Review and fix transformation code in clean.py
- Re-run `/clean-var` to regenerate code
- Re-validate
