# op_response_q73 — Response to question 73
# Source: q73
# Assumption: Codes 96, 97, 98, 99, and 2036 are treated as missing due to unlabelled data.
df_clean['op_response_q73'] = df['q73'].map({
    '01': 'option_1',
    '02': 'option_2',
    '03': 'option_3',
    '04': 'option_4',
    '05': 'option_5',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
    '2036': np.nan,
})
CODEBOOK_VARIABLES['op_response_q73'] = {
    'original_variable': 'q73',
    'question_label': "Response to question 73 (inferred from data exploration)",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4", 'option_5': "Option 5"},
}