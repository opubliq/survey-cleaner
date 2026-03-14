# op_q72 — Response to question 72
# Source: q72
# Assumption: Codes 8.0 and 9.0 are treated as Don't Know/Refused, as they are unlabelled.
df_clean['op_q72'] = df['q72'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    8.0: 'dk',
    9.0: 'refused',
    np.nan: np.nan,
})
CODEBOOK_VARIABLES['op_q72'] = {
    'original_variable': 'q72',
    'question_label': "Response to question 72",
    'type': 'categorical',
    'value_labels': {'option_a': 'First Choice', 'option_b': 'Second Choice', 'dk': 'Don\'t Know', 'refused': 'Refused'},
}