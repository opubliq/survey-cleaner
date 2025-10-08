---
description: Run final clean.py and validate survey outputs
argument-hint: [survey_name]
autoApprove:
  - Bash(*)
---

Finalize a survey by running the complete clean.py script and validating outputs.

## Arguments:
- $1: Survey name (required) - e.g., "test", "ces19"

## What this does:

1. Verifies that `clean.py` exists and has cleaning code
2. Runs `python surveys/$1/clean.py` to generate final outputs:
   - `processed/data_cleaned.csv` - All cleaned variables
   - `processed/codebook.json` - Complete metadata
3. Validates outputs exist and are non-empty
4. Generates final report with statistics

## Usage:

```
/finalize-survey test
/finalize-survey ces19
```

## Steps:

1. **Validate arguments**:
   - If $1 is missing, report error and exit
   - Check that `surveys/$1/clean.py` exists

2. **Check variables_todo.md status**:
   - Count completed variables
   - Count pending variables
   - Count questions needing human input
   - Warn if there are pending variables

3. **Run clean.py**:
   - Activate venv: `source venv/bin/activate`
   - Execute: `python surveys/$1/clean.py`
   - Capture output and errors

4. **Validate outputs**:
   - Check `processed/data_cleaned.csv` exists
   - Check `processed/codebook.json` exists
   - Verify file sizes are non-zero
   - If codebook.json exists, count variables in it

5. **Generate report**:
   ```
   ✓ Survey finalized: $1

   Variables processed: X/Y
   - Completed: X
   - Questions: Y
   - Pending: Z

   Outputs:
   - processed/data_cleaned.csv (N rows, M columns)
   - processed/codebook.json (M variables)

   Ready for deployment!
   ```

## Notes:

- Safe to run multiple times (overwrites outputs)
- Will warn if pending variables exist but still runs
- Questions in variables_todo.md should be reviewed manually
- This is the final step after all variables are processed
