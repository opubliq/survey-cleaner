---
description: Finalize survey by validating completeness and marking as ready
argument-hint: [survey_id]
autoApprove:
  - Bash(*)
  - Task(*)
---

Finalize a survey by validating completeness and marking as ready for upload to AWS.

## Arguments:
- $1: Survey ID (required) - e.g., "test", "ces2019"

## What this does:

1. Validates that survey has cleaned variables
2. Launches **finalize-survey** agent via Task tool to:
   - Check SURVEY_METADATA completeness
   - Check CODEBOOK_VARIABLES completeness
   - Test clean.py execution
   - Generate codebook.json
   - Update surveys/status.json to "completed"
3. Reports finalization results

## Usage:

```
/finalize-survey test
/finalize-survey ces2019
```

## Steps:

1. **Validate arguments**:
   - If $1 is missing, prompt for survey ID and exit
   - If `surveys/$1/` doesn't exist, report error and exit

2. **Launch finalize-survey agent**:
   - Use Task tool with:
     - subagent_type: "finalize-survey"
     - description: "Finalize survey $1"
     - prompt: "Finalize survey $1"

3. **Report results**:
   - Display validation checks
   - Show pass/fail status
   - List files ready for upload

## Next steps:

If finalization passed:
1. Review codebook.json for accuracy
2. Upload to sandbox: `python upload_to_pipeline.py $1 --stage sandbox`
3. Verify results in AWS S3
4. Upload to production when ready

If finalization failed:
- Fix reported issues
- Continue cleaning variables
- Re-run finalization
