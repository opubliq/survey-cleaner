# op_vote_pref_party — Preference for PQ or ADQ
# Source: q79
# Assumption: Data codes are prefixed with '0' (e.g., '01' vs codebook '1').
# Assumption: Codes '03' through '11' and '96' are unlisted options treated as missing.
df_clean['op_vote_pref_party'] = df['q79'].map({
    '01': 'prefere_le_pq',
    '02': 'prefere_ladq',
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_vote_pref_party'] = {
    'original_variable': 'q79',
    'question_label': "Préfère le PQ ou l'ADQ?",
    'type': 'categorical',
    'value_labels': {'prefere_le_pq': "Préfère le PQ", 'prefere_ladq': "Préfère l'ADQ"},
}