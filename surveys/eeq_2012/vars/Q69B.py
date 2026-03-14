# op_q69b — Categorical response to question Q69B
# Source: Q69B
# Assumption: This is a categorical variable, mapping all observed numeric codes to string options as the codebook is unavailable.
df_clean['op_q69b'] = df['Q69B'].map({
    0.0: 'option_0',
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    6.0: 'option_6',
    8.0: 'option_8',
    10.0: 'option_10',
    12.0: 'option_12',
    15.0: 'option_15',
    20.0: 'option_20',
    22.0: 'option_22',
    25.0: 'option_25',
    30.0: 'option_30',
    33.0: 'option_33',
    35.0: 'option_35',
    36.0: 'option_36',
    40.0: 'option_40',
    43.0: 'option_43',
    44.0: 'option_44',
    45.0: 'option_45',
    46.0: 'option_46',
    48.0: 'option_48',
    49.0: 'option_49',
})
CODEBOOK_VARIABLES['op_q69b'] = {
    'original_variable': 'Q69B',
    'question_label': "Unknown: Categorical response to Q69B",
    'type': 'categorical',
    'value_labels': {'option_0': "Code 0.0", 'option_1': "Code 1.0", 'option_2': "Code 2.0", 'option_3': "Code 3.0", 'option_4': "Code 4.0", 'option_5': "Code 5.0", 'option_6': "Code 6.0", 'option_8': "Code 8.0", 'option_10': "Code 10.0", 'option_12': "Code 12.0", 'option_15': "Code 15.0", 'option_20': "Code 20.0", 'option_22': "Code 22.0", 'option_25': "Code 25.0", 'option_30': "Code 30.0", 'option_33': "Code 33.0", 'option_35': "Code 35.0", 'option_36': "Code 36.0", 'option_40': "Code 40.0", 'option_43': "Code 43.0", 'option_44': "Code 44.0", 'option_45': "Code 45.0", 'option_46': "Code 46.0", 'option_48': "Code 48.0", 'option_49': "Code 49.0"},
}