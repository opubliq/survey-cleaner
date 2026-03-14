# op_q26_behavior — Behavioral question on Q26 (Inferred from eeq_2007 structure)
# Source: q26
# Assumption: Data file exploration failed. Mapping, dtype, and value labels are inferred from eeq_2007/q26 cleaning script.
# TODO: Verify data file access and confirm mapping (1='yes', 2='no') and that 8/9 are missing codes.
df_clean['op_q26_behavior'] = df['q26'].map({
    1.0: 'yes',
    2.0: 'no',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q26_behavior'] = {
    'original_variable': 'q26',
    'question_label': "Question 26 (Inferred Label)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}