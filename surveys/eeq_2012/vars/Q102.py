# op_vote_choice_q102 — Inferred vote choice for Q102
# Source: Q102
# Assumption: Codes 1, 2, 3 mapped to Party A, Party B, and Other based on common patterns.
df_clean['op_vote_choice_q102'] = df['Q102'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'other',
})
CODEBOOK_VARIABLES['op_vote_choice_q102'] = {
    'original_variable': 'Q102',
    'question_label': "Inferred vote choice for Q102 (Codes 1, 2, 3)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'other': "Other"},
}