# op_party_vote_intent — Likely party choice
# Source: Q20
# Assumption: No codebook provided. Codes 6, 96, 98, 99 treated as missing/refused.
df_clean['op_party_vote_intent'] = df['Q20'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    5.0: 'other_party',
    6.0: np.nan,
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_party_vote_intent'] = {
    'original_variable': 'Q20',
    'question_label': "Likely party choice",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'party_d': "Party D", 'other_party': "Other Party"},
}