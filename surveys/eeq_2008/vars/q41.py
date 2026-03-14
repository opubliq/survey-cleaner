# op_count_q41 — Frequency of activity Q41
# Source: q41
# Assumption: No codebook entry provided. Treating as numeric with explicit mapping of observed codes to strings.
df_clean['op_count_q41'] = df['q41'].map({
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
    14.0: '14',
    15.0: '15',
    20.0: '20',
    25.0: '25',
    30.0: '30',
    33.0: '33',
    35.0: '35',
    37.0: '37',
    40.0: '40',
    41.0: '41',
    43.0: '43',
    45.0: '45',
    np.nan: np.nan,
})
CODEBOOK_VARIABLES['op_count_q41'] = {
    'original_variable': 'q41',
    'question_label': "Frequency of activity Q41 (no codebook labels available)",
    'type': 'numeric',
    'value_labels': {'0': "0", '1': "1", '2': "2", '3': "3", '4': "4", '5': "5", '6': "6", '7': "7", '8': "8", '9': "9", '10': "10", '11': "11", '12': "12", '14': "14", '15': "15", '20': "20", '25': "25", '30': "30", '33': "33", '35': "35", '37': "37", '40': "40", '41': "41", '43': "43", '45': "45"},
}