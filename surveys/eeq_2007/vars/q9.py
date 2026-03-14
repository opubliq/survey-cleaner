# op_poverty_importance — Importance of poverty as election issue
# Source: q9
df_clean['op_poverty_importance'] = df['q9'].map({
    '1': 0.0,
    '2': 0.33,
    '3': 0.67,
    '4': 1.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_poverty_importance'] = {
    'original_variable': 'q9',
    'question_label': "Est-ce que la pauvreté ÉTAIT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {'0.0': 'pas du tout important', '0.33': 'peu important', '0.67': 'assez important', '1.0': 'très important'},
}
