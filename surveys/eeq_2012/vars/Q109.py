# ses_relationship_status — Relationship status
# Source: Q109
# Assumption: code 9.0 ('I prefer not to answer') treated as missing (np.nan)
df_clean['ses_relationship_status'] = df['Q109'].map({
    1.0: 'married',
    2.0: 'married_separated',
    3.0: 'single',
    4.0: 'divorced',
    5.0: 'widowed',
    6.0: 'civil_partnership',
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_relationship_status'] = {
    'original_variable': 'Q109',
    'question_label': "Which of these applies to you at present?",
    'type': 'categorical',
    'value_labels': {'married': "Married", 'married_separated': "Married, but separated", 'single': "Single", 'divorced': "Divorced", 'widowed': "Widowed", 'civil_partnership': "In a civil partnership"},
}