# op_q7 — Attitude toward political parties or leaders
# Source: Q7
# Assumption: Codes 0.0-10.0 are the valid range; 98.0 and 99.0 are treated as missing.
# Assumption: Generic labels assigned due to missing codebook entry.
df_clean['op_q7'] = df['Q7'].map({
    0.0: 'no_response',
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    6.0: 'option_6',
    7.0: 'option_7',
    8.0: 'option_8',
    9.0: 'option_9',
    10.0: 'option_10',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q7'] = {
    'original_variable': 'Q7',
    'question_label': "Attitude toward political parties or leaders",
    'type': 'categorical',
    'value_labels': {'no_response': 'No response/Unknown', 'option_1': 'Option 1', 'option_2': 'Option 2', 'option_3': 'Option 3', 'option_4': 'Option 4', 'option_5': 'Option 5', 'option_6': 'Option 6', 'option_7': 'Option 7', 'option_8': 'Option 8', 'option_9': 'Option 9', 'option_10': 'Option 10'},
}