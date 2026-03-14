# behav_q53 — Generic categorical response for question 53
# Source: q53
# Assumption: Codes 8.0 and 9.0 are treated as missing per standard practice.
df_clean['behav_q53'] = df['q53'].map({
    1.0: 'response_one',
    2.0: 'response_two',
    3.0: 'response_three',
    4.0: 'response_four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q53'] = {
    'original_variable': 'q53',
    'question_label': "Response to question 53 (Label unknown, using placeholder)",
    'type': 'categorical',
    'value_labels': {'response_one': "Option One", 'response_two': "Option Two", 'response_three': "Option Three", 'response_four': "Option Four"},
}