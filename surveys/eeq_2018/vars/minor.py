# ses_minor — Respondent is a minor
# Source: minor
# Assumption: Based on name, assuming binary status where 1 is minor and 2 is not minor.
df_clean['ses_minor'] = df['minor'].map({
    1.0: 1.0,
    2.0: 0.0,
})
CODEBOOK_VARIABLES['ses_minor'] = {
    'original_variable': 'minor',
    'question_label': "Is the respondent a minor?",
    'type': 'binary',
    'value_labels': {'1.0': "Yes (minor)", '0.0': "No (not minor)"},
}