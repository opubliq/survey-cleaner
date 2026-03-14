# op_q82e — Voting intention (assumed)
# Source: Q82E
# Assumption: Based on numeric codes 1-4, treated as categorical. Codes >= 96 are treated as missing.
df_clean['op_q82e'] = df['Q82E'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: 'refused',
    4.0: 'unsure',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q82e'] = {
    'original_variable': 'Q82E',
    'question_label': "Voting intention (inferred from name/codes)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No", 'refused': "Refused/Don't know", 'unsure': "Unsure"},
}