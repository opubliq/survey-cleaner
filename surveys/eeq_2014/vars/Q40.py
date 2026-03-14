# op_q40 — Unknown question label for Q40
# Source: Q40
# Assumption: Q40 is categorical, mapping 1-5 to generic labels. Codes 8 and 9 are treated as missing.
df_clean['op_q40'] = df['Q40'].map({
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    4.0: 'four',
    5.0: 'five',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q40'] = {
    'original_variable': 'Q40',
    'question_label': "Unknown question label for Q40",
    'type': 'categorical',
    'value_labels': {'one': 'Code 1', 'two': 'Code 2', 'three': 'Code 3', 'four': 'Code 4', 'five': 'Code 5'},
}