# ses_age — Age of respondent
# Source: agecalc
# Assumption: Numeric age variable scaled by dividing by 100.0 to fit [0, 1] range.
# Assumption: No missing codes present based on exploration (0 missing / 3072 total).
df_clean['ses_age'] = df['agecalc'] / 100.0
CODEBOOK_VARIABLES['ses_age'] = {
    'original_variable': 'agecalc',
    'question_label': "Calculated age",
    'type': 'numeric',
    'value_labels': {}, # No explicit value labels for numeric, continuous variable
}