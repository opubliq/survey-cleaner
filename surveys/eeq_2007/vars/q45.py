# op_q45 — Cleaning inferred from codes (Codebook Missing)
# Source: q45
# Assumption: Codes 98/99 treated as missing (unlabelled in codebook)
df_clean['op_q45'] = df['q45'].map({
    '01': 'response_1',
    '02': 'response_2',
    '03': 'response_3',
    '04': 'response_4',
    '05': 'response_5',
    '06': 'response_6',
    '07': 'response_7',
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_q45'] = {
    'original_variable': 'q45',
    'question_label': "Cleaning inferred from codes (Codebook Missing)",
    'type': 'categorical',
    'value_labels': {'response_1': "Option 1", 'response_2': "Option 2", 'response_3': "Option 3", 'response_4': "Option 4", 'response_5': "Option 5", 'response_6': "Option 6", 'response_7': "Option 7"},
}