# op_response_q33 — Response to question Q33
# Source: Q33
# Assumption: Codes 8.0 and 9.0 are treated as missing based on common patterns.
# TODO: Verify actual meaning of codes 1.0 and 2.0 and update labels/mapping.
df_clean['op_response_q33'] = df['Q33'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_response_q33'] = {
    'original_variable': 'Q33',
    'question_label': "Response to question Q33",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1 (Check against codebook)", 'option_2': "Option 2 (Check against codebook)"},
}