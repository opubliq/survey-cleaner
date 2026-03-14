# op_vote_intention_q61a — Inferred voting intention or party choice
# Source: q61a
# Assumption: Codes 01-05 are valid responses, codes 96, 97, 98, 99 are missing.
# TODO: Verify variable meaning and correct standard name/labels.
df_clean['op_vote_intention_q61a'] = df['q61a'].map({
    '01': 'party_a',
    '02': 'party_b',
    '03': 'party_c',
    '04': 'other',
    '05': 'none',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention_q61a'] = {
    'original_variable': 'q61a',
    'question_label': "Inferred voting intention or party choice (Variable Q61a)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'other': "Other party", 'none': "None"},
}