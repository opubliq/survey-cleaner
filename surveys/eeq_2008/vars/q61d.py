# behav_q61d — Unknown variable Q61d from eeq_2008 (No codebook provided)
# Source: q61d
# Assumption: codes 96-99 treated as missing (unlabelled)
df_clean['behav_q61d'] = df['q61d'].map({
    1.0: 'code_1',
    2.0: 'code_2',
    3.0: 'code_3',
    4.0: 'code_4',
    5.0: 'code_5',
    96.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q61d'] = {
    'original_variable': 'q61d',
    'question_label': "Unknown variable Q61d from eeq_2008 (No codebook provided)",
    'type': 'categorical',
    'value_labels': {'code_1': "Code 1", 'code_2': "Code 2", 'code_3': "Code 3", 'code_4': "Code 4", 'code_5': "Code 5"},
}