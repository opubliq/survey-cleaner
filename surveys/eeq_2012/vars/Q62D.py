# op_candidate_choice — Candidate choice
# Source: Q62D
# WARNING: Codebook mapping is speculative as actual codebook entry was unavailable for Q62D in this invocation.
# Assumption: Codes 8.0 (DK) and 9.0 (Refused) are treated as missing.
df_clean['op_candidate_choice'] = df['Q62D'].map({
    1.0: 'choice_one',
    2.0: 'choice_two',
    6.0: 'other_choice',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_candidate_choice'] = {
    'original_variable': 'Q62D',
    'question_label': "Placeholder: Choice of candidate/party in the 2012 Quebec Election Study",
    'type': 'categorical',
    'value_labels': {'choice_one': "Choice One (Placeholder)", 'choice_two': "Choice Two (Placeholder)", 'other_choice': "Other Choice (Placeholder)"},
}