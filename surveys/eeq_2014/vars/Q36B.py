# op_Q36B — Response to question Q36B (Best effort mapping)
# Source: Q36B
# Assumption: Codes 8.0 and 9.0 are treated as missing (not labelled in context)
df_clean['op_Q36B'] = df['Q36B'].map({
    1.0: 'choice_1',
    2.0: 'choice_2',
    3.0: 'choice_3',
    4.0: 'choice_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_Q36B'] = {
    'original_variable': 'Q36B',
    'question_label': "Response to question Q36B",
    'type': 'categorical',
    'value_labels': {'choice_1': "Choice 1", 'choice_2': "Choice 2", 'choice_3': "Choice 3", 'choice_4': "Choice 4"},
}