# behav_vote_leader — Vote pour le chef du parti
# Source: Q34CC
# Assumption: Data access failed; proceeding with mapping based on codebook values.
# Assumption: Codes 98 and 99 are treated as missing (explicitly listed in codebook).
df_clean['behav_vote_leader'] = df['Q34CC'].map({
    1.0: 'jean charest',
    2.0: 'pauline marois',
    3.0: 'françois legault',
    4.0: 'gabriel nadeau-dubois',
    5.0: 'richard martineau',
    6.0: 'other leader',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_leader'] = {
    'original_variable': 'Q34CC',
    'question_label': "Vote pour le chef du parti",
    'type': 'categorical',
    'value_labels': {'jean charest': "Jean Charest (Parti libéral du Québec)", 'pauline marois': "Pauline Marois (Parti québécois)", 'françois legault': "François Legault (Coalition avenir Québec)", 'gabriel nadeau-dubois': "Gabriel Nadeau-Dubois (Québec solidaire)", 'richard martineau': "Richard Martineau (Parti conservateur du Québec)", 'other leader': "Autre chef"},
}