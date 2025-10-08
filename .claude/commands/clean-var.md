---
description: Clean one survey variable using survey-variable-cleaner-agent
argument-hint: [survey_name] [variable_name]
autoApprove:
  - Bash(*)
  - Task(*)
---

Process and clean a single variable from a survey using the survey-variable-cleaner-agent.

## Arguments:
- $1: Survey name (required) - e.g., "test", "ces19"
- $2: Variable name (required) - e.g., "age", "cps19_gender"

## What this does:

1. Validates that survey is initialized (checks `variables_todo.md` exists)
2. Launches **survey-variable-cleaner-agent** to process ONE variable:
   - Explores the variable (frequencies, distributions)
   - Searches codebook (local + cross-survey fuzzy matching)
   - Generates cleaning code following safe patterns
   - Validates transformation
   - Updates `clean.py` with cleaning code
   - Updates `codebook.json` with variable metadata
   - Git commits the changes
   - Marks variable as completed in `variables_todo.md`
3. If variable needs human input (ambiguous), marks it as `[?]` with question
4. Reports completion status

## Usage:

```
/clean-var test age
/clean-var ces19 cps19_gender
```

## Steps:

1. **Validate arguments**:
   - If $1 or $2 is missing, report error and exit
   - Check that `surveys/$1/variables_todo.md` exists

2. **Launch survey-variable-cleaner-agent**:
   - Use Task tool with:
     - subagent_type: "survey-variable-cleaner-agent"
     - description: "Clean variable $2 in $1"
     - prompt: "Process ONLY variable '$2' in surveys/$1"

3. **Report completion**:
   - If successful: "✓ Variable cleaned: $2 → {cleaned_name}"
   - If question: "? Variable $2 needs human input (see variables_todo.md)"
   - If error: "! Variable $2 failed (check logs)"

## Notes:

- Agent works autonomously, no approval required
- Variable is committed immediately after cleaning
- Safe to run multiple times on same variable (will skip if already done)
- Questions are marked as `[?]` in `variables_todo.md` for later review
- This command is designed to be called in a loop by shell script
