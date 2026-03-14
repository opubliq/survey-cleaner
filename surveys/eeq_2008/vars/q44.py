# op_q44 — Unknown categorical variable related to Q44
# Source: q44
# Assumption: Codes 1.0 through 7.0 are valid categories, and 98.0/99.0 are missing values.
# TODO: verify mapping for codes 1.0-7.0 and provide descriptive labels for mapped values.
df_clean['op_q44'] = df['q44'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    6.0: 'response_6',
    7.0: 'response_7',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q44'] = {
    'original_variable': 'q44',
    'question_label': "Unknown question text for Q44",
    'type': 'categorical',
    'value_labels': {'response_1': 'Response 1 Label', 'response_2': 'Response 2 Label', 'response_3': 'Response 3 Label', 'response_4': 'Response 4 Label', 'response_5': 'Response 5 Label', 'response_6': 'Response 6 Label', 'response_7': 'Response 7 Label'},
}