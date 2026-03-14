# op_q68b — Unknown opinion variable Q68B
# Source: Q68B
# Assumption: Codes derived from value_counts are the only valid categories.
df_clean['op_q68b'] = df['Q68B'].map({
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
    13.0: '13',
    15.0: '15',
    16.0: '16',
    17.0: '17',
    20.0: '20',
    25.0: '25',
    30.0: '30',
    33.0: '33',
    35.0: '35',
    37.0: '37',
    38.0: '38',
    40.0: '40',
    43.0: '43',
})
CODEBOOK_VARIABLES['op_q68b'] = {
    'original_variable': 'Q68B',
    'question_label': "Unknown variable Q68B, codes derived from data exploration.",
    'type': 'categorical',
    'value_labels': {'0': "Category 0", '1': "Category 1", '2': "Category 2", '3': "Category 3", '4': "Category 4", '5': "Category 5", '6': "Category 6", '7': "Category 7", '8': "Category 8", '9': "Category 9", '10': "Category 10", '12': "Category 12", '13': "Category 13", '15': "Category 15", '16': "Category 16", '17': "Category 17", '20': "Category 20", '25': "Category 25", '30': "Category 30", '33': "Category 33", '35': "Category 35", '37': "Category 37", '38': "Category 38", '40': "Category 40", '43': "Category 43"},
}