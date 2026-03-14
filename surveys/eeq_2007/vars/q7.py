# op_tax_cuts_importance — Importance of tax cuts in election
# Source: q7
# Assumption: codes 8/9 treated as missing (no opinion/refusal, not in importance scale)
df_clean['op_tax_cuts_importance'] = df['q7'].map({
    '1': 1.0,
    '2': 0.667,
    '3': 0.333,
    '4': 0.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_tax_cuts_importance'] = {
    'original_variable': 'q7',
    'question_label': "Est-ce que les baisses d'impôts ÉTAIENT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {'1.0': 'très important', '0.667': 'assez important', '0.333': 'peu important', '0.0': 'pas du tout important'},
}
