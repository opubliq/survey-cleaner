# op_choice_q45 — Inferred voting choice for Q45
# Source: Q45
# Assumption: Codes 1-5 are inferred party choices. Codes 8.0 and 9.0 are treated as missing (np.nan).
df_clean['op_choice_q45'] = df['Q45'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    5.0: 'other',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_choice_q45'] = {
    'original_variable': 'Q45',
    'question_label': "Inferred: Response to Q45",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'party_d': "Party D", 'other': "Other"},
}