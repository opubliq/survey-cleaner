# op_q42e — General opinion/behavior question Q42E
# Source: Q42E
# Assumption: No codebook provided. Codes 1-6 treated as categories. Codes >= 96 treated as missing.
df_clean['op_q42e'] = df['Q42E'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    6.0: 'option_6',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q42e'] = {
    'original_variable': 'Q42E',
    'question_label': "Q42E",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4", 'option_5': "Option 5", 'option_6': "Option 6"},
}