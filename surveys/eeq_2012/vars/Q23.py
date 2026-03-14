# op_q23 — Unlabelled categorical opinion question
# Source: Q23
# Assumption: codes 8.0 and 9.0 treated as missing (unlabelled in provided context)
df_clean['op_q23'] = df['Q23'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q23'] = {
    'original_variable': 'Q23',
    'question_label': "Question 23 (Label missing)",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3"},
}