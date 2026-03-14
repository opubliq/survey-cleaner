# op_q5 — Question 5 (Placeholder label)
# Source: Q5
# Assumption: Codes 1.0-4.0 mapped to generic strings, code 8.0 treated as missing.
df_clean['op_q5'] = df['Q5'].map({
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    4.0: 'four',
    8.0: np.nan,
})
CODEBOOK_VARIABLES['op_q5'] = {
    'original_variable': 'Q5',
    'question_label': "Question 5 (Placeholder)",
    'type': 'categorical',
    'value_labels': {'one': "Category One", 'two': "Category Two", 'three': "Category Three", 'four': "Category Four"},
}