# op_vote_intention — Inferred vote intention (no codebook provided)
# Source: q54
# Assumption: Codes 8 and 9 are treated as missing, and 1-4 map to generic parties.
df_clean['op_vote_intention'] = df['q54'].map({
    '1': 'party_a',
    '2': 'party_b',
    '3': 'party_c',
    '4': 'party_d',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'q54',
    'question_label': "Inferred vote intention based on single-digit response pattern (1-4)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'party_d': "Party D"},
}