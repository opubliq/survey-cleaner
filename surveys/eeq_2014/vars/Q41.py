# op_response_q41 — Response to question 41
# Source: Q41
# Assumption: Codes 8 and 9 are treated as missing based on data exploration (not present in hypothetical codebook)
df_clean['op_response_q41'] = df['Q41'].map({
    1.0: 'yes',
    2.0: 'no',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_response_q41'] = {
    'original_variable': 'Q41',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}