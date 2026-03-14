# op_q64 — Unlabeled categorical variable from question 64
# Source: q64
# Assumption: Missing codebook entry. Codes mapped to their string equivalent.
df_clean['op_q64'] = df['q64'].map({
    0.0: '0',
    1.0: '1',
    2.0: '2',
    3.0: '3',
    4.0: '4',
    5.0: '5',
    6.0: '6',
    7.0: '7',
    9.0: '9',
    10.0: '10',
    12.0: '12',
    15.0: '15',
    20.0: '20',
    25.0: '25',
    29.0: '29',
    30.0: '30',
    33.0: '33',
    35.0: '35',
    39.0: '39',
    40.0: '40',
    45.0: '45',
    49.0: '49',
    50.0: '50',
    51.0: '51',
    55.0: '55',
})
CODEBOOK_VARIABLES['op_q64'] = {
    'original_variable': 'q64',
    'question_label': "Unlabeled/Missing Codebook: q64",
    'type': 'categorical',
    'value_labels': {'0': "Code 0", '1': "Code 1", '2': "Code 2", '3': "Code 3", '4': "Code 4", '5': "Code 5", '6': "Code 6", '7': "Code 7", '9': "Code 9", '10': "Code 10", '12': "Code 12", '15': "Code 15", '20': "Code 20", '25': "Code 25", '29': "Code 29", '30': "Code 30", '33': "Code 33", '35': "Code 35", '39': "Code 39", '40': "Code 40", '45': "Code 45", '49': "Code 49", '50': "Code 50", '51': "Code 51", '55': "Code 55"},
}