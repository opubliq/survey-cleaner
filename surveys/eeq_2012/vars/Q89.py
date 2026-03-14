# op_rating_q89 — Rating scale or ordered response (Q89)
# Source: Q89
# Note: Codebook entry missing. Treating as categorical based on float dtype and codes 0-10, 98-99.
df_clean['op_rating_q89'] = df['Q89'].map({
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
CODEBOOK_VARIABLES['op_rating_q89'] = {
    'original_variable': 'Q89',
    'question_label': "Question Q89 (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'0': "0", '1': "1", '2': "2", '3': "3", '4': "4", '5': "5", '6': "6", '7': "7", '8': "8", '9': "9", '10': "10"},
}