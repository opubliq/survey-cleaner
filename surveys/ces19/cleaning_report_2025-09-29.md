# CES 2019 Survey Cleaning Report

**Survey**: Canadian Election Study 2019
**Date**: 2025-09-29
**Session**: First 10 variables processed
**Total observations**: 37,822
**Original variables**: 634

---

## Processing Summary

### Variables Processed This Session: 10

| # | Original Variable | Cleaned Variable | Type | Transformation |
|---|-------------------|------------------|------|----------------|
| 1 | cps19_StartDate | tech_survey_start_date | character | Kept as Stata timestamp string |
| 2 | cps19_EndDate | tech_survey_end_date | character | Kept as Stata timestamp string |
| 3 | cps19_ResponseId | id_respondent | character | Unique identifier (preserved) |
| 4 | cps19_consent | tech_consent | numeric | All values = 1 (consented) |
| 5 | cps19_citizenship | ses_citizenship | character | 4→canadian_citizen, 5→permanent_resident |
| 6 | cps19_yob | tech_yob_quota | numeric | Technical quota variable (not actual YOB) |
| 7 | cps19_yob_2001_age | tech_age_screening | numeric | Age screening (mostly missing) |
| 8 | cps19_gender | ses_gender | character | 1→male, 2→female, 3→other |
| 9 | cps19_province | ses_province | character | Mapped to descriptive province names |
| 10 | cps19_education | ses_education | character | Mapped to descriptive education levels |

---

## Detailed Transformations

### 1. Timestamp Variables (Technical)
- **tech_survey_start_date**: Survey start timestamp (Stata format)
  - Missing: 0
  - Action: Preserved as string representation

- **tech_survey_end_date**: Survey end timestamp (Stata format)
  - Missing: 0
  - Action: Preserved as string representation

### 2. Identifier
- **id_respondent**: Unique respondent ID
  - Missing: 0
  - Unique values: 37,822 (100%)
  - Action: Preserved original values

### 3. Technical/Control Variables
- **tech_consent**: Consent indicator
  - Missing: 0
  - All values: 1.0 (all respondents consented)

- **tech_yob_quota**: Year of birth quota variable
  - Missing: 0
  - Range: 1-82
  - Note: Technical quota coding, NOT actual year of birth

- **tech_age_screening**: Age screening for 2001-born respondents
  - Missing: 37,529 (99.2%)
  - Valid: 293 (0.8%)
  - Note: Only filled for people born in 2001

### 4. Socioeconomic Variables

#### **ses_citizenship**: Citizenship status
- **canadian_citizen**: 36,480 (96.45%)
- **permanent_resident**: 1,342 (3.55%)
- **other**: 0 (0.00%)
- Missing: 0
- Recoding: 4→canadian_citizen, 5→permanent_resident, 6→other

#### **ses_gender**: Gender
- **female**: 21,980 (58.11%)
- **male**: 15,551 (41.12%)
- **other**: 291 (0.77%)
- Missing: 0
- Recoding: 1→male, 2→female, 3→other

#### **ses_province**: Province/territory of residence
- **province_ontario**: 14,808 (39.15%)
- **province_quebec**: 8,399 (22.21%)
- **province_alberta**: 4,481 (11.85%)
- **province_british_columbia**: 4,354 (11.51%)
- **province_manitoba**: 1,691 (4.47%)
- **province_saskatchewan**: 1,340 (3.54%)
- **province_nova_scotia**: 1,001 (2.65%)
- **province_new_brunswick**: 858 (2.27%)
- **province_newfoundland_and_labrador**: 633 (1.67%)
- **province_prince_edward_island**: 168 (0.44%)
- **territory_yukon**: 38 (0.10%)
- **territory_nunavut**: 26 (0.07%)
- **territory_northwest_territories**: 25 (0.07%)
- Missing: 0
- Recoding: Numeric codes (14-26) → descriptive province names

#### **ses_education**: Highest level of education completed
- **bachelor_degree**: 9,192 (24.30%)
- **completed_technical_college**: 7,702 (20.36%)
- **completed_secondary**: 5,865 (15.51%)
- **some_technical_college**: 4,394 (11.62%)
- **some_university**: 3,716 (9.82%)
- **master_degree**: 3,207 (8.48%)
- **some_secondary**: 1,649 (4.36%)
- **professional_or_doctorate**: 1,575 (4.16%)
- **completed_elementary**: 288 (0.76%)
- **some_elementary**: 87 (0.23%)
- **no_schooling**: 48 (0.13%)
- Missing: 99 (0.26%)
- Recoding: Numeric codes (1-11) → descriptive education levels
- Note: Original value 12 ("Don't know/Prefer not to answer") recoded to missing (NA)

---

## Data Quality Checks

### Missing Values
- **Total missing value count**: 37,628 (0.99% of all cleaned cells)
- **Variables with missing values**:
  - tech_age_screening: 37,529 missing (99.2%) - Expected, only for 2001-born respondents
  - ses_education: 99 missing (0.26%) - Recoded from "Don't know/Prefer not to answer"

### Value Distributions
- All categorical recodings verified against raw data
- No unexpected values found
- All transformations preserved frequency distributions

### Data Integrity
- Unique respondent IDs: 37,822 (100% unique)
- No duplicate records
- All transformations completed successfully

---

## Encoding Standards Applied

### Nomenclature
- **Prefixes**:
  - `ses_` = Socioeconomic variables
  - `tech_` = Technical/metadata variables
  - `id_` = Identifier variables
- **Case**: snake_case throughout
- **Language**: English for all variable and value names
- **Categories**: Descriptive lowercase with underscores (e.g., "canadian_citizen", "province_ontario")

### Missing Values
- Numeric "Don't know/Prefer not to answer" codes converted to NA
- Original missing values preserved as NA/NaN

### Character Variables
- All categorical variables use descriptive string values
- No numeric codes retained (all mapped to meaningful labels)

---

## Output Files

### Generated Files
1. **clean.py** (`surveys/ces19/clean.py`)
   - Dual-mode cleaning script (AWS + local)
   - Function: `clean_data(df)` - AWS entry point
   - Status: Ready for AWS deployment

2. **data_cleaned.csv** (`surveys/ces19/processed/data_cleaned.csv`)
   - Size: 4.3 MB
   - Rows: 37,822
   - Columns: 10 (cleaned variables)

3. **codebook.json** (`surveys/ces19/processed/codebook.json`)
   - Size: 5.8 KB
   - Format: Standardized JSON schema
   - Contains: Variable labels, types, value distributions, missing counts

4. **variables_todo.md** (`surveys/ces19/variables_todo.md`)
   - Tracks processing status of all 634 variables
   - Completed: 10 variables
   - Remaining: 624 variables

---

## Next Steps

### Variables Remaining: 624

The following variable categories remain to be processed:

1. **Opinion Variables** (majority of remaining variables):
   - Democracy satisfaction (cps19_demsat)
   - Issue importance (cps19_imp_iss)
   - Vote choice and intentions
   - Party ratings
   - Leader ratings
   - Policy positions
   - Economic evaluations

2. **Behavioral Variables**:
   - Political participation
   - Voting behavior
   - News consumption
   - Campaign attention

3. **Additional Demographics**:
   - Age (cps19_age - computed variable)
   - Religion
   - Ethnicity
   - Language
   - Employment
   - Income
   - Household composition

4. **Post-Election Survey Variables** (pes19_* prefix):
   - 336 post-election variables to process

5. **Weight Variables**:
   - Survey weights (4 variables)

### Recommended Processing Order
1. Continue with core demographics (age, income, employment)
2. Process vote choice and political behavior variables
3. Process opinion/attitude scales (with 0-1 normalization)
4. Process post-election survey variables
5. Process weights and technical variables

### Processing Rate
- **This session**: 10 variables processed
- **Estimated remaining sessions**: ~62 sessions (at 10 variables per session)
- **Recommendation**: Prioritize most analytically important variables first

---

## Technical Notes

### Encoding Issues Resolved
- SAV file had encoding issues (invalid byte sequence)
- Successfully loaded using fallback encoding (latin1/cp1252)

### Timestamp Format
- Stata timestamp format encountered (seconds since 1960-01-01)
- Preserved as string representation due to conversion complexity
- Future work: Proper datetime conversion if needed

### Variable Naming Discovery
- `cps19_yob` is NOT year of birth (technical quota variable)
- Actual age available in `cps19_age` (to be processed later)

---

## Git Commits

All work committed incrementally:
1. Clean variable: cps19_StartDate → tech_survey_start_date
2. Clean variable: cps19_EndDate → tech_survey_end_date
3. Clean variable: cps19_ResponseId → id_respondent
4. Clean variable: cps19_consent → tech_consent
5. Clean variable: cps19_citizenship → ses_citizenship
6. Clean variables: cps19_yob → tech_yob_quota, cps19_yob_2001_age → tech_age_screening
7. Clean variable: cps19_gender → ses_gender
8. Clean variable: cps19_province → ses_province
9. Clean variable: cps19_education → ses_education

---

## Conclusion

Successfully processed the first 10 variables of the CES 2019 dataset, establishing:
- Dual-mode cleaning script architecture (AWS + local)
- Standardized nomenclature (ses_, tech_, id_ prefixes)
- Complete codebook with descriptive labels
- Variable tracking system (variables_todo.md)
- Incremental git commit workflow

The cleaning script is ready for AWS deployment and can process all variables incrementally using the same workflow established in this session.