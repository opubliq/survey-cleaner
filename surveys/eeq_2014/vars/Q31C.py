# behav_Q31C — Q31C from eeq_2014 (Missing original labels)
# Source: Q31C
# Assumption: Codes 0.0-10.0 are distinct categories. Codes 98.0 and 99.0 are treated as missing.
# TODO: Verify actual meaning of codes 0-10 and labels for 98/99.
df_clean['behav_Q31C'] = df['Q31C'].map({
    0.0: 'option_0',
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
CODEBOOK_VARIABLES['behav_Q31C'] = {
    'original_variable': 'Q31C',
    'question_label': "Q31C from eeq_2014 (Manual Map)",
    'type': 'categorical',
    'value_labels': {'option_0': "Option 0", 'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4", 'option_5': "Option 5", 'option_6': "Option 6", 'option_7': "Option 7", 'option_8': "Option 8", 'option_9': "Option 9", 'option_10': "Option 10"},
}