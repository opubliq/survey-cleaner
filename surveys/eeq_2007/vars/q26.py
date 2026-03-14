# op_q26_behavior — Assumed Yes/No question (no codebook provided)
# Source: q26
# Assumption: codes 8/9 treated as missing (not documented)
df_clean['op_q26_behavior'] = df['q26'].map({
    '1': 'yes',
    '2': 'no',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_q26_behavior'] = {
    'original_variable': 'q26',
    'question_label': "Unknown question for Q26 (No codebook entry provided)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}