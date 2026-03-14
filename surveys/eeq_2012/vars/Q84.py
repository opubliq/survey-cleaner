# op_Q84 — Inferred response category for Q84
# Source: Q84
# Assumption: Codes 8.0 and 9.0 are treated as missing based on exploration.
# TODO: Verify actual question label and specific meaning of codes 1.0, 2.0, 3.0.
df_clean['op_Q84'] = df['Q84'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    3.0: 'option_three',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_Q84'] = {
    'original_variable': 'Q84',
    'question_label': "Inferred response category for Q84 (Mapping derived from value counts 1, 2, 3, 8, 9)",
    'type': 'categorical',
    'value_labels': {'option_one': 'Option 1', 'option_two': 'Option 2', 'option_three': 'Option 3'},
}