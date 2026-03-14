# op_q7f — Response to question Q7F (assuming 4-point scale)
# Source: Q7F
# Assumption: Codes 8.0 and 9.0 are treated as missing/refused as they lack labels and 1.0-4.0 appear to be the main responses.
df_clean['op_q7f'] = df['Q7F'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q7f'] = {
    'original_variable': 'Q7F',
    'question_label': "Response to question Q7F",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4"},
}