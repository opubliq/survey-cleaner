# op_q36 — Unknown categorical variable Q36
# Source: Q36
# Assumption: Codes 8.0 and 9.0 are treated as missing (unlabelled in data exploration)
# TODO: Verify mapping labels for codes 1.0 through 4.0 as codebook entry was unavailable.
df_clean['op_q36'] = df['Q36'].map({
    1.0: 'value_one',
    2.0: 'value_two',
    3.0: 'value_three',
    4.0: 'value_four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q36'] = {
    'original_variable': 'Q36',
    'question_label': "Unknown question label for Q36 in eeq_2012",
    'type': 'categorical',
    'value_labels': {'value_one': "Mapped value 1", 'value_two': "Mapped value 2", 'value_three': "Mapped value 3", 'value_four': "Mapped value 4"},
}