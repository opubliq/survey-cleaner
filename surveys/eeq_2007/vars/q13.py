# behav_second_choice — Deuxième choix de parti
# Source: q13
# Note: blank string (433 cases) represents skip logic / non-response
df_clean['behav_second_choice'] = df['q13'].map({
    '01': 'liberal',
    '02': 'pq',
    '03': 'adq',
    '04': 'qs',
    '05': 'vert',
    '95': 'not_voted',
    '96': 'other',
    '97': 'none',
    '98': np.nan,
    '99': np.nan,
    '': np.nan,
})
CODEBOOK_VARIABLES['behav_second_choice'] = {
    'original_variable': 'q13',
    'question_label': "Quel parti était votre deuxième choix ?",
    'type': 'categorical',
    'value_labels': {
        'liberal': "Parti libéral",
        'pq': "Parti québécois",
        'adq': "ADQ",
        'qs': "Québec Solidaire",
        'vert': "Parti vert",
        'not_voted': "N'a pas voté",
        'other': "Autre parti",
        'none': "Aucun",
    },
}
