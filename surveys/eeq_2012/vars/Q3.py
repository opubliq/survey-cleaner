# op_q3 — General opinion question 3
# Source: Q3
# Assumption: Codes 1.0-5.0 are distinct options. Codes 8.0 and 9.0 treated as missing (unlabelled in codebook).
df_clean['op_q3'] = df['Q3'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    3.0: 'option_three',
    4.0: 'option_four',
    5.0: 'option_five',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q3'] = {
    'original_variable': 'Q3',
    'question_label': "Unknown question text for Q3 - Mapped based on observed data.",
    'type': 'categorical',
    'value_labels': {'option_one': "Option 1", 'option_two': "Option 2", 'option_three': "Option 3", 'option_four': "Option 4", 'option_five': "Option 5"},
}