# op_response_q82 — Response to question 82 (Inferred mapping)
# Source: Q82
# Assumption: Codes 8/9 treated as explicit missing values based on common survey practice.
df_clean['op_response_q82'] = df['Q82'].map({
    1.0: 'yes',
    2.0: 'no',
    8.0: 'refused',
    9.0: 'dont_know',
})
CODEBOOK_VARIABLES['op_response_q82'] = {
    'original_variable': 'Q82',
    'question_label': "Response to question 82 (Inferred mapping)",
    'type': 'categorical',
    'value_labels': {'yes': 'Yes', 'no': 'No', 'refused': 'Refused', 'dont_know': 'Don\'t know'},
}