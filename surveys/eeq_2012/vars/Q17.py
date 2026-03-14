# op_q17 — Opinion/Attitude variable Q17
# Source: Q17
# Assumption: Codes 96, 98, 99 treated as missing. Labels are based on observed value counts.
df_clean['op_q17'] = df['Q17'].map({
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    4.0: 'four',
    5.0: 'five',
    6.0: 'six',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q17'] = {
    'original_variable': 'Q17',
    'question_label': "Unknown - derived from Q17 data exploration",
    'type': 'categorical',
    'value_labels': {'one': '1.0', 'two': '2.0', 'three': '3.0', 'four': '4.0', 'five': '5.0', 'six': '6.0'},
}