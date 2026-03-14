# op_intent_Q10 — Vote intention for Q10
# Source: Q10
# Assumption: Codes 8 and 9 are converted to specific missing value labels based on typical survey practice.
df_clean['op_intent_Q10'] = df['Q10'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'other',
    8.0: 'refused',
    9.0: 'dont_know',
})
CODEBOOK_VARIABLES['op_intent_Q10'] = {
    'original_variable': 'Q10',
    'question_label': "Vote intention (Inferred from codes 1, 2, 3, 8, 9)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'other': "Other/Other Party", 'refused': "Refused", 'dont_know': "Don't Know"},
}