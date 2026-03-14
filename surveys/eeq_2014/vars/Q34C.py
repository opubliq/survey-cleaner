# op_q34c_response — Response to Q34C
# Source: Q34C
# Assumption: Codes 8.0 and 9.0 are unlabelled missing values.
# TODO: Verify question meaning and map to meaningful labels.
df_clean['op_q34c_response'] = df['Q34C'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q34c_response'] = {
    'original_variable': 'Q34C',
    'question_label': "Response to Q34C",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4"},
}