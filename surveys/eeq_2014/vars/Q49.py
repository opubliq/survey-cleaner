# op_q49 — General question 49 response
# Source: Q49
# Assumption: Codes 8.0 and 9.0 are 'Don't Know'/'Refused' and will be mapped to missing.
df_clean['op_q49'] = df['Q49'].map({
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    4.0: 'four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q49'] = {
    'original_variable': 'Q49',
    'question_label': "Question 49 response",
    'type': 'categorical',
    'value_labels': {'one': "Category 1", 'two': "Category 2", 'three': "Category 3", 'four': "Category 4"},
}