# op_q48 — Inferred response to question 48
# Source: q48
# Assumption: Codes 1-4 are valid answers, codes 8 and 9 are missing. Question label is a placeholder.
df_clean['op_q48'] = df['q48'].map({
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_q48'] = {
    'original_variable': 'q48',
    'question_label': "Inferred response for question 48",
    'type': 'categorical',
    'value_labels': {'one': "Answer One", 'two': "Answer Two", 'three': "Answer Three", 'four': "Answer Four"},
}