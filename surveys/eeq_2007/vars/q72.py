# op_q72 — Question 72 response
# Source: q72
# Assumption: Codes '8' and '9' are treated as missing as no codebook was provided.
df_clean['op_q72'] = df['q72'].map({
    '1': 'yes',
    '2': 'no',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_q72'] = {
    'original_variable': 'q72',
    'question_label': "Question 72 (Unknown Text)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}