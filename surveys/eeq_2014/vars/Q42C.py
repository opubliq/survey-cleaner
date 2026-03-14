# op_q42c — Response to question Q42C (Codebook entry missing, mapping inferred from data)
# Source: Q42C
# Assumption: codes 96, 98, 99 treated as missing (unlabelled in data exploration)
df_clean['op_q42c'] = df['Q42C'].map({
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
CODEBOOK_VARIABLES['op_q42c'] = {
    'original_variable': 'Q42C',
    'question_label': "Response to question Q42C (Codebook entry missing, mapping inferred from data)",
    'type': 'categorical',
    'value_labels': {'option_1': 'Option 1', 'option_2': 'Option 2', 'option_3': 'Option 3', 'option_4': 'Option 4', 'option_5': 'Option 5', 'option_6': 'Option 6'},
}