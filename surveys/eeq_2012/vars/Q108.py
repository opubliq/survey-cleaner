# ses_vote_intention — Intention de vote
# Source: Q108
# Assumption: codes 96, 98, 99 are unlabelled missing codes and will be treated as missing (np.nan)
df_clean['ses_vote_intention'] = df['Q108'].map({
    1.0: 'caq',
    2.0: 'liberal',
    3.0: 'péquiste',
    4.0: 'ca',
    5.0: 'onto_liberal',
    6.0: 'onto_caq',
    7.0: 'onto_péquiste',
    8.0: np.nan,
    9.0: np.nan,
    10.0: 'other',
    11.0: np.nan,
    12.0: np.nan,
    13.0: np.nan,
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_vote_intention'] = {
    'original_variable': 'Q108',
    'question_label': "Quelle est votre intention de vote actuelle?",
    'type': 'categorical',
    'value_labels': {'caq': "CAQ", 'liberal': "Libéral", 'péquiste': "Péquiste", 'ca': "Conservateur", 'onto_liberal': "Ontarien Libéral", 'onto_caq': "Ontarien CAQ", 'onto_péquiste': "Ontarien Péquiste", 'other': "Autre"},
}