# op_q65 — Response to Question 65 (Codebook label missing)
# Source: Q65
# Note: Codebook entry was missing. Mapped observed values 1.0-25.0 to generic labels.
df_clean['op_q65'] = df['Q65'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    6.0: 'option_6',
    7.0: 'option_7',
    8.0: 'option_8',
    9.0: 'option_9',
    10.0: 'option_10',
    11.0: 'option_11',
    12.0: 'option_12',
    13.0: 'option_13',
    14.0: 'option_14',
    15.0: 'option_15',
    16.0: 'option_16',
    17.0: 'option_17',
    18.0: 'option_18',
    19.0: 'option_19',
    20.0: 'option_20',
    21.0: 'option_21',
    22.0: 'option_22',
    23.0: 'option_23',
    24.0: 'option_24',
    25.0: 'option_25',
})
CODEBOOK_VARIABLES['op_q65'] = {
    'original_variable': 'Q65',
    'question_label': "Response to Question 65 (Codebook label missing)",
    'type': 'categorical',
    'value_labels': {'option_1': 'Option 1 (Label Unknown)', 'option_2': 'Option 2 (Label Unknown)', 'option_3': 'Option 3 (Label Unknown)', 'option_4': 'Option 4 (Label Unknown)', 'option_5': 'Option 5 (Label Unknown)', 'option_6': 'Option 6 (Label Unknown)', 'option_7': 'Option 7 (Label Unknown)', 'option_8': 'Option 8 (Label Unknown)', 'option_9': 'Option 9 (Label Unknown)', 'option_10': 'Option 10 (Label Unknown)', 'option_11': 'Option 11 (Label Unknown)', 'option_12': 'Option 12 (Label Unknown)', 'option_13': 'Option 13 (Label Unknown)', 'option_14': 'Option 14 (Label Unknown)', 'option_15': 'Option 15 (Label Unknown)', 'option_16': 'Option 16 (Label Unknown)', 'option_17': 'Option 17 (Label Unknown)', 'option_18': 'Option 18 (Label Unknown)', 'option_19': 'Option 19 (Label Unknown)', 'option_20': 'Option 20 (Label Unknown)', 'option_21': 'Option 21 (Label Unknown)', 'option_22': 'Option 22 (Label Unknown)', 'option_23': 'Option 23 (Label Unknown)', 'option_24': 'Option 24 (Label Unknown)', 'option_25': 'Option 25 (Label Unknown)'},
}