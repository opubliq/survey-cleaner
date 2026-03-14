# op_q33e_response — Response to question 33E
# Source: Q33E
# Assumption: Codes 8.0 and 9.0 treated as missing (unlabelled in input context)
df_clean['op_q33e_response'] = df['Q33E'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    3.0: 'option_c',
    4.0: 'option_d',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q33e_response'] = {
    'original_variable': 'Q33E',
    'question_label': "Response to question 33E",
    'type': 'categorical',
    'value_labels': {'option_a': "Option A", 'option_b': "Option B", 'option_c': "Option C", 'option_d': "Option D"},
}