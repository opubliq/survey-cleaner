# op_attitude_q56 — General attitude or opinion question 56
# Source: q56
# Assumption: Codes 01-05 are substantive responses. Codes 96, 97, 98, 99 are treated as missing (not in codebook).
df_clean['op_attitude_q56'] = df['q56'].map({
    '01': 'response_1',
    '02': 'response_2',
    '03': 'response_3',
    '04': 'response_4',
    '05': 'response_5',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q56'] = {
    'original_variable': 'q56',
    'question_label': "Inferred: General attitude/opinion for question 56",
    'type': 'categorical',
    'value_labels': {'response_1': "Substantive response 1", 'response_2': "Substantive response 2", 'response_3': "Substantive response 3", 'response_4': "Substantive response 4", 'response_5': "Substantive response 5"},
}