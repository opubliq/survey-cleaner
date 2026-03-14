# op_q39 — Generic score from Q39
# Source: q39
# Assumption: This is a categorical variable based on observed discrete float values (0.0 to 50.0).
# Assumption: Since no codebook was provided, codes are mapped to generic string labels in lowercase.
df_clean['op_q39'] = df['q39'].map({
    0.0: 'level_0',
    1.0: 'level_1',
    2.0: 'level_2',
    3.0: 'level_3',
    4.0: 'level_4',
    5.0: 'level_5',
    6.0: 'level_6',
    7.0: 'level_7',
    8.0: 'level_8',
    9.0: 'level_9',
    10.0: 'level_10',
    11.0: 'level_11',
    12.0: 'level_12',
    15.0: 'level_15',
    20.0: 'level_20',
    21.0: 'level_21',
    22.0: 'level_22',
    25.0: 'level_25',
    30.0: 'level_30',
    33.0: 'level_33',
    35.0: 'level_35',
    37.0: 'level_37',
    40.0: 'level_40',
    45.0: 'level_45',
    50.0: 'level_50',
})
CODEBOOK_VARIABLES['op_q39'] = {
    'original_variable': 'q39',
    'question_label': "Response to question 39 (No codebook provided)",
    'type': 'categorical',
    'value_labels': {'level_0': 'Code 0', 'level_1': 'Code 1', 'level_2': 'Code 2', 'level_3': 'Code 3', 'level_4': 'Code 4', 'level_5': 'Code 5', 'level_6': 'Code 6', 'level_7': 'Code 7', 'level_8': 'Code 8', 'level_9': 'Code 9', 'level_10': 'Code 10', 'level_11': 'Code 11', 'level_12': 'Code 12', 'level_15': 'Code 15', 'level_20': 'Code 20', 'level_21': 'Code 21', 'level_22': 'Code 22', 'level_25': 'Code 25', 'level_30': 'Code 30', 'level_33': 'Code 33', 'level_35': 'Code 35', 'level_37': 'Code 37', 'level_40': 'Code 40', 'level_45': 'Code 45', 'level_50': 'Code 50'},
}