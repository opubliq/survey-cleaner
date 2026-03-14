# op_q77 — Placeholder label for Q77
# Source: q77
# Assumption: Codes 2.0-11.0 mapped to generic labels as specific labels are unknown. Code 99.0 treated as missing.
df_clean['op_q77'] = df['q77'].map({
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    6.0: 'option_6',
    7.0: 'option_7',
    8.0: 'option_8',
    9.0: 'option_9',
    10.0: 'option_10',
    11.0: 'option_11',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q77'] = {
    'original_variable': 'q77',
    'question_label': "Unknown question text for Q77",
    'type': 'categorical',
    'value_labels': {'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4", 'option_5': "Option 5", 'option_6': "Option 6", 'option_7': "Option 7", 'option_8': "Option 8", 'option_9': "Option 9", 'option_10': "Option 10", 'option_11': "Option 11"},
}