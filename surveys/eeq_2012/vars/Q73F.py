# op_opinion_q73f — Opinion on question 73, part F
# Source: Q73F
# Assumption: Codes 8 and 9 are treated as missing (not explicitly defined in codebook)
df_clean['op_opinion_q73f'] = df['Q73F'].map({
    1.0: 'value_1',
    2.0: 'value_2',
    3.0: 'value_3',
    4.0: 'value_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_opinion_q73f'] = {
    'original_variable': 'Q73F',
    'question_label': "Opinion on question 73, part F (Codebook mapping unknown)",
    'type': 'categorical',
    'value_labels': {'value_1': "Category 1", 'value_2': "Category 2", 'value_3': "Category 3", 'value_4': "Category 4"},
}