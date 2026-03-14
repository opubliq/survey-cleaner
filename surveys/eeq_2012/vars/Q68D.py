# op_q68d — Unknown categorical variable, proceeding with observed codes
# Source: Q68D
# WARNING: Codebook mapping and label information is missing for this variable.
# The map keys are based on observed float values, mapped to generic string labels.
df_clean['op_q68d'] = df['Q68D'].map({
    0.0: 'code_0',
    1.0: 'code_1',
    2.0: 'code_2',
    3.0: 'code_3',
    4.0: 'code_4',
    5.0: 'code_5',
    6.0: 'code_6',
    8.0: 'code_8',
    9.0: 'code_9',
    10.0: 'code_10',
    15.0: 'code_15',
    20.0: 'code_20',
    25.0: 'code_25',
    26.0: 'code_26',
    29.0: 'code_29',
    30.0: 'code_30',
    33.0: 'code_33',
    34.0: 'code_34',
    35.0: 'code_35',
    36.0: 'code_36',
    40.0: 'code_40',
    45.0: 'code_45',
    49.0: 'code_49',
    50.0: 'code_50',
})
CODEBOOK_VARIABLES['op_q68d'] = {
    'original_variable': 'Q68D',
    'question_label': "Q68D - Unlabeled categorical variable",
    'type': 'categorical',
    'value_labels': {'code_0': "Code 0 (Unlabeled)", 'code_1': "Code 1 (Unlabeled)", 'code_2': "Code 2 (Unlabeled)", 'code_3': "Code 3 (Unlabeled)", 'code_4': "Code 4 (Unlabeled)", 'code_5': "Code 5 (Unlabeled)", 'code_6': "Code 6 (Unlabeled)", 'code_8': "Code 8 (Unlabeled)", 'code_9': "Code 9 (Unlabeled)", 'code_10': "Code 10 (Unlabeled)", 'code_15': "Code 15 (Unlabeled)", 'code_20': "Code 20 (Unlabeled)", 'code_25': "Code 25 (Unlabeled)", 'code_26': "Code 26 (Unlabeled)", 'code_29': "Code 29 (Unlabeled)", 'code_30': "Code 30 (Unlabeled)", 'code_33': "Code 33 (Unlabeled)", 'code_34': "Code 34 (Unlabeled)", 'code_35': "Code 35 (Unlabeled)", 'code_36': "Code 36 (Unlabeled)", 'code_40': "Code 40 (Unlabeled)", 'code_45': "Code 45 (Unlabeled)", 'code_49': "Code 49 (Unlabeled)", 'code_50': "Code 50 (Unlabeled)"},
}