# op_q0qc — Cleaned Q0QC (Missing Codebook)
# Source: q0qc
# Assumption: Since no codebook was provided, codes 1.0-17.0 are mapped to generic labels.
df_clean['op_q0qc'] = df['q0qc'].map({
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
    11.0: 'code_11',
    12.0: 'code_12',
    13.0: 'code_13',
    14.0: 'code_14',
    15.0: 'code_15',
    16.0: 'code_16',
    17.0: 'code_17',
})
CODEBOOK_VARIABLES['op_q0qc'] = {
    'original_variable': 'q0qc',
    'question_label': "Cleaned Q0QC (Missing Codebook)",
    'type': 'categorical',
    'value_labels': {'code_1': 'Label 1', 'code_2': 'Label 2', 'code_3': 'Label 3', 'code_4': 'Label 4', 'code_5': 'Label 5', 'code_6': 'Label 6', 'code_7': 'Label 7', 'code_8': 'Label 8', 'code_9': 'Label 9', 'code_10': 'Label 10', 'code_11': 'Label 11', 'code_12': 'Label 12', 'code_13': 'Label 13', 'code_14': 'Label 14', 'code_15': 'Label 15', 'code_16': 'Label 16', 'code_17': 'Label 17'},
}