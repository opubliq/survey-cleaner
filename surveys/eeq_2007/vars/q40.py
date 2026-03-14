# op_q40 — Opinion/Attitude for question 40
# Source: q40
# Assumption: Codes are categorical without explicit labels provided; mapped to generic strings based on observed values.
df_clean['op_q40'] = df['q40'].map({
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
    11.0: '11',
    12.0: '12',
    13.0: '13',
    15.0: '15',
    17.0: '17',
    19.0: '19',
    20.0: '20',
    22.0: '22',
    25.0: '25',
    27.0: '27',
    28.0: '28',
    30.0: '30',
    34.0: '34',
    35.0: '35',
})
CODEBOOK_VARIABLES['op_q40'] = {
    'original_variable': 'q40',
    'question_label': "Opinion/Attitude for question 40 (Unlabelled)",
    'type': 'categorical',
    'value_labels': {'0': "Code 0", '1': "Code 1", '2': "Code 2", '3': "Code 3", '4': "Code 4", '5': "Code 5", '6': "Code 6", '7': "Code 7", '8': "Code 8", '9': "Code 9", '10': "Code 10", '11': "Code 11", '12': "Code 12", '13': "Code 13", '15': "Code 15", '17': "Code 17", '19': "Code 19", '20': "Code 20", '22': "Code 22", '25': "Code 25", '27': "Code 27", '28': "Code 28", '30': "Code 30", '34': "Code 34", '35': "Code 35"},
}