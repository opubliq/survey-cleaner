# op_q73 — Unknown variable q73, all values mapped to NaN due to missing codebook
# Source: q73
# Assumption: No codebook entry available for eeq_2008/q73. All observed codes (1.0-5.0, 98.0, 99.0) are treated as missing (np.nan)
df_clean['op_q73'] = df['q73'].map({
    1.0: np.nan,
    2.0: np.nan,
    3.0: np.nan,
    4.0: np.nan,
    5.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q73'] = {
    'original_variable': 'q73',
    'question_label': "q73 (No codebook available to translate)",
    'type': 'categorical',
    'value_labels': {},
}