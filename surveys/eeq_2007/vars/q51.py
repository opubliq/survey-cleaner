# op_q51 — Placeholder for Q51 response, assumed categorical
# Source: q51
# Assumption: Codes 8/9 are treated as missing (no labels provided)
df_clean['op_q51'] = df['q51'].map({
    '1': 'option_1',
    '2': 'option_2',
    '3': 'option_3',
    '4': 'option_4',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_q51'] = {
    'original_variable': 'q51',
    'question_label': "Q51 (Label unknown - using placeholder)",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4"},
}