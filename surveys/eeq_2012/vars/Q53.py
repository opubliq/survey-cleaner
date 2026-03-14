# op_vote_intention — Intention de vote
# Source: Q53
# Assumption: codes 8 and 9 treated as missing/unlabelled
df_clean['op_vote_intention'] = df['Q53'].map({
    1.0: 'pq',
    2.0: 'other_party',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q53',
    'question_label': "Intention de vote (Inferred)",
    'type': 'categorical',
    'value_labels': {'pq': "Parti Québécois", 'other_party': "Other Major Party"},
}