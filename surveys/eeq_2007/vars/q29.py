# op_q29 — Unknown question from Q29 (no codebook provided)
# Source: q29
# Assumption: Codes mapped to generic labels since codebook was not provided for this variable.
df_clean['op_q29'] = df['q29'].map({
    0.0: 'response_0',
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    6.0: 'response_6',
    7.0: 'response_7',
    8.0: 'response_8',
    9.0: 'response_9',
    10.0: 'response_10',
    15.0: 'response_15',
    18.0: 'response_18',
    20.0: 'response_20',
    21.0: 'response_21',
    22.0: 'response_22',
    25.0: 'response_25',
    28.0: 'response_28',
    30.0: 'response_30',
    33.0: 'response_33',
    34.0: 'response_34',
    35.0: 'response_35',
    39.0: 'response_39',
    40.0: 'response_40',
    43.0: 'response_43',
})
CODEBOOK_VARIABLES['op_q29'] = {
    'original_variable': 'q29',
    'question_label': "Unknown question from Q29 (no codebook provided)",
    'type': 'categorical',
    'value_labels': {'response_0': "0.0", 'response_1': "1.0", 'response_2': "2.0", 'response_3': "3.0", 'response_4': "4.0", 'response_5': "5.0", 'response_6': "6.0", 'response_7': "7.0", 'response_8': "8.0", 'response_9': "9.0", 'response_10': "10.0", 'response_15': "15.0", 'response_18': "18.0", 'response_20': "20.0", 'response_21': "21.0", 'response_22': "22.0", 'response_25': "25.0", 'response_28': "28.0", 'response_30': "30.0", 'response_33': "33.0", 'response_34': "34.0", 'response_35': "35.0", 'response_39': "39.0", 'response_40': "40.0", 'response_43': "43.0"},
}