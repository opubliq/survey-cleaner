# op_q30 — Attitude/Opinion question 30 (Mapping placeholders due to missing codebook)
# Source: q30
# Assumption: All observed codes (0.0 to 39.0) are treated as distinct categories. No explicit missing codes observed.
df_clean['op_q30'] = df['q30'].map({
    0.0: 'none',
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
    15.0: 'code_15',
    16.0: 'code_16',
    18.0: 'code_18',
    20.0: 'code_20',
    21.0: 'code_21',
    22.0: 'code_22',
    25.0: 'code_25',
    27.0: 'code_27',
    30.0: 'code_30',
    31.0: 'code_31',
    33.0: 'code_33',
    35.0: 'code_35',
    37.0: 'code_37',
    39.0: 'code_39',
})
CODEBOOK_VARIABLES['op_q30'] = {
    'original_variable': 'q30',
    'question_label': "Question 30 label missing, requires review",
    'type': 'categorical',
    'value_labels': {'none': "None", 'code_1': "Code 1 Label", 'code_2': "Code 2 Label", 'code_3': "Code 3 Label", 'code_4': "Code 4 Label", 'code_5': "Code 5 Label", 'code_6': "Code 6 Label", 'code_7': "Code 7 Label", 'code_8': "Code 8 Label", 'code_9': "Code 9 Label", 'code_10': "Code 10 Label", 'code_15': "Code 15 Label", 'code_16': "Code 16 Label", 'code_18': "Code 18 Label", 'code_20': "Code 20 Label", 'code_21': "Code 21 Label", 'code_22': "Code 22 Label", 'code_25': "Code 25 Label", 'code_27': "Code 27 Label", 'code_30': "Code 30 Label", 'code_31': "Code 31 Label", 'code_33': "Code 33 Label", 'code_35': "Code 35 Label", 'code_37': "Code 37 Label", 'code_39': "Code 39 Label"},
}
# TODO: verify mapping for q30 — codebook entry missing, labels are placeholders.
