# op_vote_intention — Inferred vote intention
# Source: Q17
# Assumption: Codes 1, 2 are parties, 9 is refused. All unmapped/NaN treated as missing.
df_clean['op_vote_intention'] = df['Q17'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    9.0: 'refused',
    np.nan: np.nan
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q17',
    'question_label': "Inferred: Vote intention for party A or B (Q17)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'refused': "Refused"},
}