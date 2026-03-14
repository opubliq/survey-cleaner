# behav_response — Agent response
# Source: agensp
# Assumption: Binary variable mapped to 0/1 for response/no-response.
df_clean['behav_response'] = df['agensp'].map({
    0.0: 0.0,
    1.0: 1.0,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_response'] = {
    'original_variable': 'agensp',
    'question_label': "Agent response indicator (inferred)",
    'type': 'binary',
    'value_labels': {'0.0': "No/Negative", '1.0': "Yes/Positive"},
}