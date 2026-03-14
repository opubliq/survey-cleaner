# behav_response_q73c — Unlabeled categorical response for Q73C
# Source: Q73C
# Assumption: Codes 1-4 map to specific responses; 8 (DK) and 9 (Refused) treated as missing.
df_clean['behav_response_q73c'] = df['Q73C'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: 'other',
    4.0: 'maybe',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_response_q73c'] = {
    'original_variable': 'Q73C',
    'question_label': "Response to question Q73C (Label not provided, derived from data)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No", 'other': "Other", 'maybe': "Maybe"},
}