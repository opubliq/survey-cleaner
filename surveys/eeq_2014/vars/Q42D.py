# op_q42d — Response to question 42D (Inferred)
# Source: Q42D
# Assumption: Codes 1.0-6.0 are valid responses. Codes 96.0, 98.0, 99.0 are treated as missing due to lack of documentation.
df_clean['op_q42d'] = df['Q42D'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    6.0: 'response_6',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q42d'] = {
    'original_variable': 'Q42D',
    'question_label': "Response to question 42D (Inferred)",
    'type': 'categorical',
    'value_labels': {'response_1': "Response 1", 'response_2': "Response 2", 'response_3': "Response 3", 'response_4': "Response 4", 'response_5': "Response 5", 'response_6': "Response 6"},
}