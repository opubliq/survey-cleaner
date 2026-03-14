# op_q45 — Opinion variable Q45 (label missing)
# Source: q45
# Assumption: Treating as categorical. Codes 98 and 99 are treated as missing.
df_clean['op_q45'] = df['q45'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    6.0: 'response_6',
    7.0: 'response_7',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q45'] = {
    'original_variable': 'q45',
    'question_label': "Opinion variable Q45 (label missing)",
    'type': 'categorical',
    'value_labels': {'response_1': "Response 1", 'response_2': "Response 2", 'response_3': "Response 3", 'response_4': "Response 4", 'response_5': "Response 5", 'response_6': "Response 6", 'response_7': "Response 7"},
}