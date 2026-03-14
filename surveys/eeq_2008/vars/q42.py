# op_attitude_q42 — Attitude towards an unspecified topic in Q42
# Source: q42
# Note: No codebook provided; mapping based on observed values from data exploration.
df_clean['op_attitude_q42'] = df['q42'].map({
    0.0: 'no_opinion',
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
    12.0: 'level_12',
    13.0: 'level_13',
    15.0: 'level_15',
    19.0: 'level_19',
    20.0: 'level_20',
    25.0: 'level_25',
    27.0: 'level_27',
    29.0: 'level_29',
    30.0: 'level_30',
    33.0: 'level_33',
    35.0: 'level_35',
    40.0: 'level_40',
    45.0: 'level_45',
    50.0: 'level_50',
})
CODEBOOK_VARIABLES['op_attitude_q42'] = {
    'original_variable': 'q42',
    'question_label': "Q42 (Unlabelled)",
    'type': 'categorical',
    'value_labels': {'no_opinion': "No Opinion/Refused", 'level_1': "Level 1", 'level_2': "Level 2", 'level_3': "Level 3", 'level_4': "Level 4", 'level_5': "Level 5", 'level_6': "Level 6", 'level_7': "Level 7", 'level_8': "Level 8", 'level_9': "Level 9", 'level_10': "Level 10", 'level_12': "Level 12", 'level_13': "Level 13", 'level_15': "Level 15", 'level_19': "Level 19", 'level_20': "Level 20", 'level_25': "Level 25", 'level_27': "Level 27", 'level_29': "Level 29", 'level_30': "Level 30", 'level_33': "Level 33", 'level_35': "Level 35", 'level_40': "Level 40", 'level_45': "Level 45", 'level_50': "Level 50"},
}