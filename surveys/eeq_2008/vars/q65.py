# op_q65 — Opinion/Attitude variable - mapping based on data counts due to missing codebook
# Source: q65
# Assumption: Codes are mapped to placeholders as codebook is unavailable. Unmapped codes (including missing) become np.nan.
df_clean['op_q65'] = df['q65'].map({
    0.0: 'code_0',
    1.0: 'code_1',
    5.0: 'code_5',
    7.0: 'code_7',
    8.0: 'code_8',
    10.0: 'code_10',
    20.0: 'code_20',
    25.0: 'code_25',
    30.0: 'code_30',
    33.0: 'code_33',
    35.0: 'code_35',
    38.0: 'code_38',
    39.0: 'code_39',
    40.0: 'code_40',
    45.0: 'code_45',
    50.0: 'code_50',
    51.0: 'code_51',
    55.0: 'code_55',
    59.0: 'code_59',
    60.0: 'code_60',
    65.0: 'code_65',
    66.0: 'code_66',
    67.0: 'code_67',
    70.0: 'code_70',
    75.0: 'code_75',
})
CODEBOOK_VARIABLES['op_q65'] = {
    'original_variable': 'q65',
    'question_label': "Opinion/Attitude variable (q65) - mapping is a best-effort guess due to missing codebook",
    'type': 'categorical',
    'value_labels': {'code_0': "Code 0 placeholder", 'code_1': "Code 1 placeholder", 'code_5': "Code 5 placeholder", 'code_7': "Code 7 placeholder", 'code_8': "Code 8 placeholder", 'code_10': "Code 10 placeholder", 'code_20': "Code 20 placeholder", 'code_25': "Code 25 placeholder", 'code_30': "Code 30 placeholder", 'code_33': "Code 33 placeholder", 'code_35': "Code 35 placeholder", 'code_38': "Code 38 placeholder", 'code_39': "Code 39 placeholder", 'code_40': "Code 40 placeholder", 'code_45': "Code 45 placeholder", 'code_50': "Code 50 placeholder", 'code_51': "Code 51 placeholder", 'code_55': "Code 55 placeholder", 'code_59': "Code 59 placeholder", 'code_60': "Code 60 placeholder", 'code_65': "Code 65 placeholder", 'code_66': "Code 66 placeholder", 'code_67': "Code 67 placeholder", 'code_70': "Code 70 placeholder", 'code_75': "Code 75 placeholder"},
}
