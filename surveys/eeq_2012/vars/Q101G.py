# op_voting_intent_G — Voting intention for party G
# Source: Q101G
# Assumption: Codes 1.0 and 2.0 mapped to placeholder parties 'party_a'/'party_b'.
# Assumption: Codes 8.0 (Don't know) and 9.0 (Refused) mapped to np.nan.
df_clean['op_voting_intent_G'] = df['Q101G'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_voting_intent_G'] = {
    'original_variable': 'Q101G',
    'question_label': "Voting intention for Party G (PLACEHOLDER MAPPING)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B"},
}