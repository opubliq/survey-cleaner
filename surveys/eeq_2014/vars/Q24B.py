# behav_q24b — Response to question Q24B (Unlabelled in context)
# Source: Q24B
# TODO: Verify mapping and label against codebook for Q24B. Assuming 1, 2, 3 are responses and 8, 9 are missing.
df_clean['behav_q24b'] = df['Q24B'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q24b'] = {
    'original_variable': 'Q24B',
    'question_label': "Response to question Q24B (Requires Codebook Verification)",
    'type': 'categorical',
    'value_labels': {'response_1': "Response Code 1", 'response_2': "Response Code 2", 'response_3': "Response Code 3"},
}