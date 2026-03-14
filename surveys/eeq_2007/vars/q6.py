# op_fiscal_imbalance_importance — Déséquilibre fiscal — importance de l'enjeu
# Source: q6
df_clean['op_fiscal_imbalance_importance'] = df['q6'].map({
    '1': 1.0,
    '2': 0.67,
    '3': 0.33,
    '4': 0.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_fiscal_imbalance_importance'] = {
    'original_variable': 'q6',
    'question_label': "Est-ce que le déséquilibre fiscal ÉTAIT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {'1.0': "très important", '0.67': "assez important", '0.33': "peu important", '0.0': "pas du tout important"},
}
