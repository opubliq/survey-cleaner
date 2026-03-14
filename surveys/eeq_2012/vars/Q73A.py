# op_vote_intention — Vote intention
# Source: Q73A
# Assumption: Codes 8.0 ('Aucun') and 9.0 ('Refus de répondre') treated as missing.
df_clean['op_vote_intention'] = df['Q73A'].map({
    1.0: 'bq',
    2.0: 'conservateur',
    3.0: 'liberal',
    4.0: 'npd',
    5.0: 'caq',
    6.0: 'autre_parti',
    7.0: 'vert',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q73A',
    'question_label': "Vote intention",
    'type': 'categorical',
    'value_labels': {'bq': "Bloc Québécois", 'conservateur': "Conservateur", 'liberal': "Libéral", 'npd': "NPD", 'caq': "CAQ", 'autre_parti': "Autre parti", 'vert': "Parti vert"},
}