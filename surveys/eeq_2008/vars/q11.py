# op_q11 — Opinion question 11 (inferred)
# Source: q11
# Note: Codebook not provided. Inferring 'op' type as it is likely an opinion question.
# Assumption: Codes 9.0 are treated as missing.
df_clean['op_q11'] = df['q11'].map({
    1.0: 'yes',
    2.0: 'no',
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q11'] = {
    'original_variable': 'q11',
    'question_label': "Opinion question 11 (inferred from context)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}