# op_q47 — Unknown variable Q47 response
# Source: Q47
# Assumption: Codes 1.0/2.0 are mapped to 1.0/0.0 respectively for binary scaling. Code 9.0 is treated as missing (np.nan).
df_clean['op_q47'] = df['Q47'].map({
    1.0: 1.0,
    2.0: 0.0,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q47'] = {
    'original_variable': 'Q47',
    'question_label': "Unknown variable Q47 response",
    'type': 'binary',
    'value_labels': {'1.0': 'Response 1 (Mapped to 1.0)', '0.0': 'Response 2 (Mapped to 0.0)'},
}
