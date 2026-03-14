# op_vote_intent — Expressed voting intention (inferred from codes)
# Source: q70
# Note: No codebook provided for q70. Codes 96, 97, 98, 99 assumed missing.
df_clean['op_vote_intent'] = df['q70'].map({
    '01': 'support_party_a',
    '02': 'support_party_b',
    '03': 'support_party_c',
    '04': 'support_party_d',
    '05': 'support_party_e',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_vote_intent'] = {
    'original_variable': 'q70',
    'question_label': "Expressed voting intention (inferred from codes)",
    'type': 'categorical',
    'value_labels': {'support_party_a': "Party A", 'support_party_b': "Party B", 'support_party_c': "Party C", 'support_party_d': "Party D", 'support_party_e': "Party E"},
}