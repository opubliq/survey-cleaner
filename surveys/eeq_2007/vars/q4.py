# op_unemployment_importance — Unemployment as election issue importance
# Source: q4
# Assumption: codes 8/9 treated as missing (don't know/refusal)
df_clean['op_unemployment_importance'] = df['q4'].map({
    '1': 1.0,
    '2': 0.667,
    '3': 0.333,
    '4': 0.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_unemployment_importance'] = {
    'original_variable': 'q4',
    'question_label': "Est-ce que le chômage ÉTAIT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {'0.0': 'pas du tout important', '0.333': 'peu important', '0.667': 'assez important', '1.0': 'très important'},
}
