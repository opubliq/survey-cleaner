# op_coded_response — Coded categorical response for Q70D
# Source: Q70D
# Assumption: Codes 0-10 are valid categories. Codes 98 and 99 are treated as missing as they are unlabelled in data/codebook.
df_clean['op_coded_response'] = df['Q70D'].map({
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
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_coded_response'] = {
    'original_variable': 'Q70D',
    'question_label': "Coded response for Q70D (label unknown, mapping derived from data exploration)",
    'type': 'categorical',
    'value_labels': {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10'},
}