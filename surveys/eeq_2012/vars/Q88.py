# op_vote_Q88 — Inferred: Voting intention/behavior for Q88
# Source: Q88
# Assumption: No codebook provided. Inferring structure based on value counts:
# 1-4 are response codes, 8/9 are missing/refused. Treating as categorical.
df_clean['op_vote_Q88'] = df['Q88'].map({
    1.0: 'choice_1',
    2.0: 'choice_2',
    3.0: 'choice_3',
    4.0: 'undecided',
    8.0: np.nan,  # Refused
    9.0: np.nan,  # Don't Know
})
CODEBOOK_VARIABLES['op_vote_Q88'] = {
    'original_variable': 'Q88',
    'question_label': "Inferred: Voting intention/behavior for Q88",
    'type': 'categorical',
    'value_labels': {'choice_1': "Primary choice", 'choice_2': "Secondary choice", 'choice_3': "Other choice", 'undecided': "Undecided"},
}