# op_turnout_intention — Turnout intention
# Source: q39
# Assumption: Variable treated as categorical due to missing codebook. Observed float codes mapped to string equivalents.
df_clean['op_turnout_intention'] = df['q39'].map({
    0.0: '0',
    1.0: '1',
    2.0: '2',
    3.0: '3',
    4.0: '4',
    5.0: '5',
    6.0: '6',
    7.0: '7',
    8.0: '8',
    9.0: '9',
    10.0: '10',
    12.0: '12',
    15.0: '15',
    17.0: '17',
    20.0: '20',
    25.0: '25',
    26.0: '26',
    30.0: '30',
    32.0: '32',
    35.0: '35',
    40.0: '40',
    45.0: '45',
    47.0: '47',
    49.0: '49',
    50.0: '50',
})
CODEBOOK_VARIABLES['op_turnout_intention'] = {
    'original_variable': 'q39',
    'question_label': "Turnout intention (Inferred)",
    'type': 'categorical',
    'value_labels': {'0': "Code 0", '1': "Code 1", '2': "Code 2", '3': "Code 3", '4': "Code 4", '5': "Code 5", '6': "Code 6", '7': "Code 7", '8': "Code 8", '9': "Code 9", '10': "Code 10", '12': "Code 12", '15': "Code 15", '17': "Code 17", '20': "Code 20", '25': "Code 25", '26': "Code 26", '30': "Code 30", '32': "Code 32", '35': "Code 35", '40': "Code 40", '45': "Code 45", '47': "Code 47", '49': "Code 49", '50': "Code 50"},
}