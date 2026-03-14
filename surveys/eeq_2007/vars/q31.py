# op_q31 — Unknown variable q31
# Source: q31
# Assumption: Codes observed in data are mapped to generic strings. Unobserved codes and 99.0 are treated as missing.
df_clean['op_q31'] = df['q31'].map({
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
    12.0: 'code_12',
    15.0: 'code_15',
    19.0: 'code_19',
    20.0: 'code_20',
    24.0: 'code_24',
    25.0: 'code_25',
    29.0: 'code_29',
    30.0: 'code_30',
    33.0: 'code_33',
    35.0: 'code_35',
    40.0: 'code_40',
    41.0: 'code_41',
    45.0: 'code_45',
    50.0: 'code_50',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q31'] = {
    'original_variable': 'q31',
    'question_label': "Unknown variable q31",
    'type': 'categorical',
    'value_labels': {'code_0': "0", 'code_1': "1", 'code_2': "2", 'code_3': "3", 'code_4': "4", 'code_5': "5", 'code_6': "6", 'code_7': "7", 'code_8': "8", 'code_9': "9", 'code_10': "10", 'code_12': "12", 'code_15': "15", 'code_19': "19", 'code_20': "20", 'code_24': "24", 'code_25': "25", 'code_29': "29", 'code_30': "30", 'code_33': "33", 'code_35': "35", 'code_40': "40", 'code_41': "41", 'code_45': "45", 'code_50': "50"},
}