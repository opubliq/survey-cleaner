# op_q76 — Placeholder for question 76 response
# Source: q76
# Assumption: Variable is binary, mapping 1.0 to 1.0 (True/Yes) and 2.0 to 0.0 (False/No).
# TODO: verify mapping and update question_label/value_labels once codebook is available.
df_clean['op_q76'] = df['q76'].map({
    1.0: 1.0,
    2.0: 0.0,
})
CODEBOOK_VARIABLES['op_q76'] = {
    'original_variable': 'q76',
    'question_label': "Placeholder: Question 76 Text Missing",
    'type': 'binary',
    'value_labels': {1.0: "True/Yes", 0.0: "False/No"},
}