# behav_response_q74 — Response to question Q74
# Source: Q74
# Assumption: Codes 8.0 and 9.0 are treated as missing as they are unlabelled and likely represent 'Don't Know' or 'Refused'.
df_clean['behav_response_q74'] = df['Q74'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_response_q74'] = {
    'original_variable': 'Q74',
    'question_label': "Response to question Q74",
    'type': 'categorical',
    'value_labels': {'response_1': "Category 1", 'response_2': "Category 2", 'response_3': "Category 3", 'response_4': "Category 4"},
}