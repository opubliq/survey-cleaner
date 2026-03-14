# op_q18a — Placeholder for response to question q18a (No codebook provided)
# Source: q18a
# Assumption: codes 96, 98, 99 treated as missing (unlabelled in data exploration)
df_clean['op_q18a'] = df['q18a'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q18a'] = {
    'original_variable': 'q18a',
    'question_label': "Response to question 18a (Labels unknown)",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4", 'option_5': "Option 5"},
}