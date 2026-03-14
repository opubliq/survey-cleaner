# op_aid_families_importance — Importance of family aid as election issue
# Source: q10
df_clean['op_aid_families_importance'] = df['q10'].map({
    '1': 1.0,
    '2': 0.667,
    '3': 0.333,
    '4': 0.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_aid_families_importance'] = {
    'original_variable': 'q10',
    'question_label': "Est-ce que l'aide aux familles ÉTAIT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {'1.0': 'très important', '0.667': 'assez important', '0.333': 'peu important', '0.0': 'pas du tout important'},
}
