# op_party_support — Party support or issue opinion (Codebook missing)
# Source: Q69
# Assumption: Variable treated as categorical based on numerous codes observed.
# Assumption: Mappings and labels are placeholders due to missing codebook entry for Q69.
df_clean['op_party_support'] = df['Q69'].map({
    0.0: 'code_0',
    1.0: 'code_1',
    2.0: 'code_2',
    3.0: 'code_3',
    4.0: 'code_4',
    5.0: 'code_5',
    6.0: 'code_6',
    7.0: 'code_7',
    8.0: 'code_8',
    10.0: 'code_10',
    12.0: 'code_12',
    13.0: 'code_13',
    15.0: 'code_15',
    20.0: 'code_20',
    22.0: 'code_22',
    24.0: 'code_24',
    25.0: 'code_25',
    30.0: 'code_30',
    33.0: 'code_33',
    35.0: 'code_35',
    37.0: 'code_37',
    40.0: 'code_40',
    44.0: 'code_44',
    45.0: 'code_45',
    49.0: 'code_49',
})
CODEBOOK_VARIABLES['op_party_support'] = {
    'original_variable': 'Q69',
    'question_label': "Unknown/Inferred from context (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'code_0': 'Code 0 (Unknown)', 'code_1': 'Code 1 (Unknown)', 'code_2': 'Code 2 (Unknown)', 'code_3': 'Code 3 (Unknown)', 'code_4': 'Code 4 (Unknown)', 'code_5': 'Code 5 (Unknown)', 'code_6': 'Code 6 (Unknown)', 'code_7': 'Code 7 (Unknown)', 'code_8': 'Code 8 (Unknown)', 'code_10': 'Code 10 (Unknown)', 'code_12': 'Code 12 (Unknown)', 'code_13': 'Code 13 (Unknown)', 'code_15': 'Code 15 (Unknown)', 'code_20': 'Code 20 (Unknown)', 'code_22': 'Code 22 (Unknown)', 'code_24': 'Code 24 (Unknown)', 'code_25': 'Code 25 (Unknown)', 'code_30': 'Code 30 (Unknown)', 'code_33': 'Code 33 (Unknown)', 'code_35': 'Code 35 (Unknown)', 'code_37': 'Code 37 (Unknown)', 'code_40': 'Code 40 (Unknown)', 'code_44': 'Code 44 (Unknown)', 'code_45': 'Code 45 (Unknown)', 'code_49': 'Code 49 (Unknown)'},
}