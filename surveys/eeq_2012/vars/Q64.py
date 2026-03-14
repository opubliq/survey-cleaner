# op_Q64 — Response to Q64
# Source: Q64
# Assumption: Codes 96, 98, 99 treated as missing (unlabelled in data exploration)
# Assumption: Codes 1, 2, 3, 4 mapped to generic options due to missing codebook
df_clean['op_Q64'] = df['Q64'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_Q64'] = {
    'original_variable': 'Q64',
    'question_label': "Response to Q64",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4"},
}