# ses_code2 — Inferred categorical code 2
# Source: CODE2
# WARNING: Codebook mapping is missing. Assuming categorical variable based on data exploration (codes 0.0-9.0).
df_clean['ses_code2'] = df['CODE2'].map({
    0.0: 'code_0',
    1.0: 'code_1',
    2.0: 'code_2',
    3.0: 'code_3',
    4.0: 'code_4',
    5.0: 'code_5',
    6.0: 'code_6',
    7.0: 'code_7',
    8.0: 'code_8',
    9.0: 'code_9',
})
CODEBOOK_VARIABLES['ses_code2'] = {
    'original_variable': 'CODE2',
    'question_label': "Inferred Code 2 (Label unknown)",
    'type': 'categorical',
    'value_labels': {'code_0': 'Category 0', 'code_1': 'Category 1', 'code_2': 'Category 2', 'code_3': 'Category 3', 'code_4': 'Category 4', 'code_5': 'Category 5', 'code_6': 'Category 6', 'code_7': 'Category 7', 'code_8': 'Category 8', 'code_9': 'Category 9'},
}