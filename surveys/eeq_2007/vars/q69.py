# op_vote_intent — Voter intention at time of survey
# Source: q69
# Assumption: Codes 4, 8, 9 treated as missing (inferred from common survey practice, as no codebook was provided)
df_clean['op_vote_intent'] = df['q69'].map({
    '1': 'party_a',
    '2': 'party_b',
    '3': 'party_c',
    '4': np.nan,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_vote_intent'] = {
    'original_variable': 'q69',
    'question_label': "Voter intention (Inferred)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C"},
}