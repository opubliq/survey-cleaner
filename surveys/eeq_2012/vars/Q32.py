# op_vote_choice — Assumed vote intention or party preference
# Source: Q32
# Assumption: Codes 1-5 are valid choices, codes 96-99 and NaN are missing/refusals.
df_clean['op_vote_choice'] = df['Q32'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    5.0: 'other',
    96.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_choice'] = {
    'original_variable': 'Q32',
    'question_label': "Assumed Vote Intention/Party Preference (Codes 1-5 mapped)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'party_d': "Party D", 'other': "Other party"},
}