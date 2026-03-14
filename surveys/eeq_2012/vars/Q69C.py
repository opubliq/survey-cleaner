# op_attitude_q69c — Opinion/Attitude question Q69C
# Source: Q69C
# Assumption: Observed float codes mapped to generic string levels.
df_clean['op_attitude_q69c'] = df['Q69C'].map({
    0.0: 'level_0',
    1.0: 'level_1',
    4.0: 'level_4',
    5.0: 'level_5',
    6.0: 'level_6',
    7.0: 'level_7',
    8.0: 'level_8',
    9.0: 'level_9',
    10.0: 'level_10',
    15.0: 'level_15',
    20.0: 'level_20',
    25.0: 'level_25',
    27.0: 'level_27',
    30.0: 'level_30',
    33.0: 'level_33',
    35.0: 'level_35',
    40.0: 'level_40',
    44.0: 'level_44',
    45.0: 'level_45',
    46.0: 'level_46',
    48.0: 'level_48',
    49.0: 'level_49',
    50.0: 'level_50',
    51.0: 'level_51',
    55.0: 'level_55',
})
CODEBOOK_VARIABLES['op_attitude_q69c'] = {
    'original_variable': 'Q69C',
    'question_label': "Placeholder for Q69C: Unknown question text",
    'type': 'categorical',
    'value_labels': {'level_0': "Level 0 (Observed 0.0)", 'level_1': "Level 1 (Observed 1.0)", 'level_4': "Level 4 (Observed 4.0)", 'level_5': "Level 5 (Observed 5.0)", 'level_6': "Level 6 (Observed 6.0)", 'level_7': "Level 7 (Observed 7.0)", 'level_8': "Level 8 (Observed 8.0)", 'level_9': "Level 9 (Observed 9.0)", 'level_10': "Level 10 (Observed 10.0)", 'level_15': "Level 15 (Observed 15.0)", 'level_20': "Level 20 (Observed 20.0)", 'level_25': "Level 25 (Observed 25.0)", 'level_27': "Level 27 (Observed 27.0)", 'level_30': "Level 30 (Observed 30.0)", 'level_33': "Level 33 (Observed 33.0)", 'level_35': "Level 35 (Observed 35.0)", 'level_40': "Level 40 (Observed 40.0)", 'level_44': "Level 44 (Observed 44.0)", 'level_45': "Level 45 (Observed 45.0)", 'level_46': "Level 46 (Observed 46.0)", 'level_48': "Level 48 (Observed 48.0)", 'level_49': "Level 49 (Observed 49.0)", 'level_50': "Level 50 (Observed 50.0)", 'level_51': "Level 51 (Observed 51.0)", 'level_55': "Level 55 (Observed 55.0)"},
}
