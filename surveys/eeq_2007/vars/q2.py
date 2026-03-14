# op_health_importance — Importance of health as an election issue (Likert: 4-point scale)
# Source: q2
df_clean['op_health_importance'] = df['q2'].map({
    '1': 1.0,
    '2': 2.0 / 3,
    '3': 1.0 / 3,
    '4': 0.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_health_importance'] = {
    'original_variable': 'q2',
    'question_label': "Est-ce que la santé était un enjeu important pour vous dans cette élection ? Diriez-vous que c'est un enjeu...?",
    'type': 'likert',
    'value_labels': {1.0: "très important", 2.0 / 3: "assez important", 1.0 / 3: "peu important", 0.0: "pas du tout important"},
}
