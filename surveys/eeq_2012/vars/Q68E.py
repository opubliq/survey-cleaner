# ses_q68e — Unknown question, treated as categorical (no codebook provided)
# Source: Q68E
# WARNING: No codebook provided for variable Q68E. Mapping is based on observed values and uses generic labels.
# Note: Original data has 0 explicit missing values. Unseen float values in data will map to np.nan.
df_clean['ses_q68e'] = df['Q68E'].map({
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
    10.0: 'code_10',
    11.0: 'code_11',
    12.0: 'code_12',
    15.0: 'code_15',
    20.0: 'code_20',
    23.0: 'code_23',
    24.0: 'code_24',
    25.0: 'code_25',
    26.0: 'code_26',
    30.0: 'code_30',
    33.0: 'code_33',
    34.0: 'code_34',
    35.0: 'code_35',
    40.0: 'code_40',
    43.0: 'code_43',
})
CODEBOOK_VARIABLES['ses_q68e'] = {
    'original_variable': 'Q68E',
    'question_label': "Q68E - Label Missing/Unknown",
    'type': 'categorical',
    'value_labels': {'code_0': "Code 0", 'code_1': "Code 1", 'code_2': "Code 2", 'code_3': "Code 3", 'code_4': "Code 4", 'code_5': "Code 5", 'code_6': "Code 6", 'code_7': "Code 7", 'code_8': "Code 8", 'code_9': "Code 9", 'code_10': "Code 10", 'code_11': "Code 11", 'code_12': "Code 12", 'code_15': "Code 15", 'code_20': "Code 20", 'code_23': "Code 23", 'code_24': "Code 24", 'code_25': "Code 25", 'code_26': "Code 26", 'code_30': "Code 30", 'code_33': "Code 33", 'code_34': "Code 34", 'code_35': "Code 35", 'code_40': "Code 40", 'code_43': "Code 43"},
}