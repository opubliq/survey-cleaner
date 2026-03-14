# op_attitude_q4 — Attitude question 4 (Inferred from data values)
# Source: Q4
# Assumption: No codebook provided. Codes 1.0 and 2.0 mapped generically. Code 9.0 treated as missing.
df_clean['op_attitude_q4'] = df['Q4'].map({
    1.0: 'option 1',
    2.0: 'option 2',
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q4'] = {
    'original_variable': 'Q4',
    'question_label': "Attitude question 4 (Inferred from data values)",
    'type': 'categorical',
    'value_labels': {'option 1': "Option 1", 'option 2': "Option 2"},
}