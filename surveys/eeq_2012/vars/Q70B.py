# op_q70b — Opinion variable Q70B (codebook missing)
# Source: Q70B
# Note: No codebook provided. Mapping codes 0-10 to generic labels. Codes 98 and 99 treated as missing based on data observation.
df_clean['op_q70b'] = df['Q70B'].map({
    0.0: 'code 0',
    1.0: 'code 1',
    2.0: 'code 2',
    3.0: 'code 3',
    4.0: 'code 4',
    5.0: 'code 5',
    6.0: 'code 6',
    7.0: 'code 7',
    8.0: 'code 8',
    9.0: 'code 9',
    10.0: 'code 10',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q70b'] = {
    'original_variable': 'Q70B',
    'question_label': "Q70B",
    'type': 'categorical',
    'value_labels': {'code 0': 'Code 0', 'code 1': 'Code 1', 'code 2': 'Code 2', 'code 3': 'Code 3', 'code 4': 'Code 4', 'code 5': 'Code 5', 'code 6': 'Code 6', 'code 7': 'Code 7', 'code 8': 'Code 8', 'code 9': 'Code 9', 'code 10': 'Code 10'},
}