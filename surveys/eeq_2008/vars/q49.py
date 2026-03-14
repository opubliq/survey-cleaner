# op_q49 — Inferred: Question 49
# Source: q49
# Assumption: Variable type is categorical based on float dtype with discrete values.
# Assumption: Codes 8 and 9 are treated as missing/refused.
# TODO: verify mapping for codes 1, 2, 3, 8, 9 as no codebook entry was provided.
df_clean['op_q49'] = df['q49'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: 'not sure',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q49'] = {
    'original_variable': 'q49',
    'question_label': "Inferred: Question 49",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No", 'not sure': "Not Sure"},
}