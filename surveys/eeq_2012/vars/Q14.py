# op_voting_intention — Intention de vote pour le parti (Inferred)
# Source: Q14
# Assumption: Q14 is about voting intention for parties 1-6. Codes 96, 98, 99 are assumed to be missing codes.
# TODO: verify mapping for codes 1.0 to 6.0 against the actual codebook.
df_clean['op_voting_intention'] = df['Q14'].map({
    1.0: 'parti_a',
    2.0: 'parti_b',
    3.0: 'parti_c',
    4.0: 'parti_d',
    5.0: 'parti_e',
    6.0: 'other',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_voting_intention'] = {
    'original_variable': 'Q14',
    'question_label': "Intention de vote pour le parti (Inferred)",
    'type': 'categorical',
    'value_labels': {'parti_a': "Party A", 'parti_b': "Party B", 'parti_c': "Party C", 'parti_d': "Party D", 'parti_e': "Party E", 'other': "Other Party"},
}