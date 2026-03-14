# ses_q77c — Unnamed variable, mapping based on observed values
# Source: Q77C
# Assumption: Codes 8 and 9 are treated as 'refused' and 'dont_know' respectively, as they were not explicitly labelled in the provided context.
df_clean['ses_q77c'] = df['Q77C'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    3.0: 'option_c',
    4.0: 'option_d',
    8.0: 'refused',
    9.0: 'dont_know',
})
CODEBOOK_VARIABLES['ses_q77c'] = {
    'original_variable': 'Q77C',
    'question_label': "Response to question 77, category C (Inferred)",
    'type': 'categorical',
    'value_labels': {'option_a': "Option A", 'option_b': "Option B", 'option_c': "Option C", 'option_d': "Option D", 'refused': "Refused", 'dont_know': "Don't know"},
}
