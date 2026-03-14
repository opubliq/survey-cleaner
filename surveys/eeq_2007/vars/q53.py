# op_vote_intention — Voting intention (assumed)
# Source: q53
# Assumption: Codes 8 and 9 are treated as missing based on common survey practices.
# Assumption: Labels 1-4 map to major/other parties as no codebook was provided.
df_clean['op_vote_intention'] = df['q53'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'other',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'q53',
    'question_label': "Voting intention (Inferred - please verify)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'other': "Other"},
}