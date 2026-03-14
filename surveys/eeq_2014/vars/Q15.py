# op_q15 — Placeholder for Q15 variable
# Source: Q15
# Assumption: Codes 98 and 99 are missing. No question text or labels available; codes 0-10 used directly as categories.
df_clean['op_q15'] = df['Q15'].map({
    0.0: '0',
    1.0: '1',
    2.0: '2',
    3.0: '3',
    4.0: '4',
    5.0: '5',
    6.0: '6',
    7.0: '7',
    8.0: '8',
    9.0: '9',
    10.0: '10',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q15'] = {
    'original_variable': 'Q15',
    'question_label': "Q15 - Unknown question text (check codebook)",
    'type': 'categorical',
    'value_labels': {'0': "Code 0", '1': "Code 1", '2': "Code 2", '3': "Code 3", '4': "Code 4", '5': "Code 5", '6': "Code 6", '7': "Code 7", '8': "Code 8", '9': "Code 9", '10': "Code 10"},
}