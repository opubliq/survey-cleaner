# op_party_vote_intent — Vote intention (Party 1/2)
# Source: Q90
# Assumption: Codes 8.0 (Refused) and 9.0 (Don't know) are treated as missing.
df_clean['op_party_vote_intent'] = df['Q90'].map({
    1.0: 'liberal',
    2.0: 'conservative',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_party_vote_intent'] = {
    'original_variable': 'Q90',
    'question_label': "Vote intention for major parties",
    'type': 'categorical',
    'value_labels': {'liberal': "Liberal", 'conservative': "Conservative"},
}
