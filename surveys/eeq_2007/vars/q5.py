# op_env_importance — Environmental importance in election
# Source: q5
df_clean['op_env_importance'] = df['q5'].astype(float).map({
    1.0: 1.0,
    2.0: 0.667,
    3.0: 0.333,
    4.0: 0.0,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_env_importance'] = {
    'original_variable': 'q5',
    'question_label': "Est-ce que l'environnement ÉTAIT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {'very_important': 'très important', 'somewhat_important': 'assez important', 'little_important': 'peu important', 'not_important': 'pas du tout important'},
}
