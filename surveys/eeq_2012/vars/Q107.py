# behav_q107 — Inferred behavioral question response
# Source: Q107
# Assumption: Codes 1.0-12.0, 16.0 are categories; 96.0 is missing/refused.
# NOTE: Complete mapping and question text must be verified by the 'validate-cleaning' step.
df_clean['behav_q107'] = df['Q107'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    6.0: 'option_6',
    7.0: 'option_7',
    8.0: 'option_8',
    10.0: 'option_10',
    11.0: 'option_11',
    12.0: 'option_12',
    16.0: 'option_16',
    96.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q107'] = {
    'original_variable': 'Q107',
    'question_label': "Inferred: Response to question Q107",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4", 'option_5': "Option 5", 'option_6': "Option 6", 'option_7': "Option 7", 'option_8': "Option 8", 'option_10': "Option 10", 'option_11': "Option 11", 'option_12': "Option 12", 'option_16': "Option 16"},
}