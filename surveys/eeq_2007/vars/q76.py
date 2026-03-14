# behav_intent_vote — Intent to vote
# Source: q76
# Assumption: Based on observation of values '1' and '2', treating as binary intent (1=Yes, 2=No).
df_clean['behav_intent_vote'] = df['q76'].map({
    '1': 1.0,
    '2': 0.0,
})
CODEBOOK_VARIABLES['behav_intent_vote'] = {
    'original_variable': 'q76',
    'question_label': "Intent to vote (Hypothetical Label)",
    'type': 'binary',
    'value_labels': {1.0: "Yes", 0.0: "No"},
}
