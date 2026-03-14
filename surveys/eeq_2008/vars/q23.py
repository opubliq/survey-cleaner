# op_trust_government — Confiance envers les gouvernements (Likert 0-1)
# Source: q23
df_clean['op_trust_government'] = df['q23'].map({
    1.0: 1.0,    # Presque toujours
    2.0: 0.667,  # La plupart du temps
    3.0: 0.333,  # Parfois seulement
    4.0: 0.0,    # Presque jamais
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_trust_government'] = {
    'original_variable': 'q23',
    'question_label': "Dans quelle mesure faites-vous confiance aux gouvernements pour faire ce qui doit être fait ?",
    'type': 'likert',
    'value_labels': {
        1.0: "Presque toujours",
        0.667: "La plupart du temps",
        0.333: "Parfois seulement",
        0.0: "Presque jamais",
    },
}
