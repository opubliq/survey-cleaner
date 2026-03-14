# op_vote_intention — Intention de vote
# Source: Q20
# Assumption: Codes 8.0 (Refused) and 9.0 (Don't Know) are treated as missing.
df_clean['op_vote_intention'] = df['Q20'].map({
    1.0: 'liberal',
    2.0: 'conservative',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q20',
    'question_label': "Intention de vote (Synthetic Label)",
    'type': 'categorical',
    'value_labels': {'liberal': "Liberal Party", 'conservative': "Conservative Party"},
}