# op_vote_intention — Intentions de vote pour la prochaine élection
# Source: Q23
# Assumption: Codes 8/9 are missing based on observation and standard practice
df_clean['op_vote_intention'] = df['Q23'].map({
    1.0: 'liberal',
    2.0: 'conservative',
    3.0: 'ndp',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q23',
    'question_label': "Intentions de vote pour la prochaine élection",
    'type': 'categorical',
    'value_labels': {'liberal': "Liberal Party", 'conservative': "Conservative Party", 'ndp': "NDP"},
}