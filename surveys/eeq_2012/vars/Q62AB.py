# op_vote_preference — Primary vote intention
# Source: Q62AB
# Assumption: Observed code 96.0 is unlabelled and treated as missing. Codebook missing code 99 is also treated as missing.
df_clean['op_vote_preference'] = df['Q62AB'].map({
    1.0: 'parti libéral',
    2.0: 'parti conservateur',
    3.0: 'parti québécois',
    4.0: 'parti québécois',
    5.0: 'parti vert',
    6.0: 'n.d.a.',
    99.0: np.nan,
    96.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_preference'] = {
    'original_variable': 'Q62AB',
    'question_label': "Candidat principal de votre choix",
    'type': 'categorical',
    'value_labels': {'parti libéral': "Parti libéral", 'parti conservateur': "Parti conservateur", 'parti québécois': "Parti québécois", 'parti vert': "Parti vert", 'n.d.a.': "N.D.A."},
}
