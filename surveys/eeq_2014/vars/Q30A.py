# ses_voting_intention_party — Intention de vote (parti)
# Source: Q30A
# Assumption: Missing codes 97, 98, 99 treated as missing (unlabelled in codebook)
df_clean['ses_voting_intention_party'] = df['Q30A'].map({
    1.0: 'caq',
    2.0: 'plr',
    3.0: 'liberal',
    4.0: 'pqc',
    5.0: 'union_nationale',
    6.0: 'autre',
    95.0: np.nan, # Mentionné mais non dans codebook (probablement "other")
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_voting_intention_party'] = {
    'original_variable': 'Q30A',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'caq': "CAQ", 'plr': "PLQ", 'liberal': "Libéral", 'pqc': "PQC", 'union_nationale': "Union nationale", 'autre': "Autre"},
}
