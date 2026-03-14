# behav_party_vote — Parti pour lequel le répondant a voté
# Source: q12
# Note: variable contains 185 empty strings treated as missing
df_clean['behav_party_vote'] = df['q12'].map({
    '01': 'liberal',
    '02': 'pq',
    '03': 'adq',
    '04': 'qs',
    '05': 'green',
    '95': 'no_vote',
    '96': 'other_party',
    '97': 'none',
    '98': 'dont_know',
    '99': 'refusal',
    '': np.nan,
})
CODEBOOK_VARIABLES['behav_party_vote'] = {
    'original_variable': 'q12',
    'question_label': "Pour quel parti avez-vous voté ? Le Parti libéral, le Parti québécois, l'ADQ, Québec solidaire, le Parti vert ou un autre parti ?",
    'type': 'categorical',
    'value_labels': {
        'liberal': "Parti libéral",
        'pq': "Parti québécois",
        'adq': "ADQ (Action démocratique du Québec)",
        'qs': "Québec Solidaire",
        'green': "Parti vert",
        'no_vote': "n'a pas voté",
        'other_party': "autre parti (spécifiez)",
        'none': "aucun",
        'dont_know': "ne sais pas",
        'refusal': "Refus",
    },
}
