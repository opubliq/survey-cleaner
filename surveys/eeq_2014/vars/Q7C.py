# behav_vote_intention_q7c — Vote intention (Inferred from Q7C codes)
# Source: Q7C
# Assumption: Only code 1.0 is mapped as a positive intention. All other codes (2.0, 3.0, 4.0, 8.0, 9.0) are treated as missing due to lack of codebook.
df_clean['behav_vote_intention_q7c'] = df['Q7C'].map({
    1.0: 'yes',
})
CODEBOOK_VARIABLES['behav_vote_intention_q7c'] = {
    'original_variable': 'Q7C',
    'question_label': "Vote intention (Inferred from Q7C)",
    'type': 'categorical',
    'value_labels': {'yes': "Intention to vote for Party/Candidate 1 (Inferred)"},
}