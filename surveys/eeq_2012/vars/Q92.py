# op_q92 — Opinion/Attitude question 92 (Best guess)
# Source: Q92
# Assumption: Codes 1.0-6.0 mapped to generic options due to missing codebook.
# Assumption: Codes 97.0, 98.0, 99.0 are treated as missing (unlabelled in data).
df_clean['op_q92'] = df['Q92'].map({
    1.0: 'opt1',
    2.0: 'opt2',
    3.0: 'opt3',
    4.0: 'opt4',
    5.0: 'opt5',
    6.0: 'opt6',
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q92'] = {
    'original_variable': 'Q92',
    'question_label': "Unknown question (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'opt1': "Option 1 (Code 1.0)", 'opt2': "Option 2 (Code 2.0)", 'opt3': "Option 3 (Code 3.0)", 'opt4': "Option 4 (Code 4.0)", 'opt5': "Option 5 (Code 5.0)", 'opt6': "Option 6 (Code 6.0)"},
}