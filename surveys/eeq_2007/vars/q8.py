# op_issue_quebec_status — Importance of Quebec political status as election issue
# Source: q8
# Likert scale (1–4) normalized to 0–1; codes 8–9 treated as missing
df_clean['op_issue_quebec_status'] = df['q8'].map({
    '1': 1.0,
    '2': 0.67,
    '3': 0.33,
    '4': 0.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_issue_quebec_status'] = {
    'original_variable': 'q8',
    'question_label': "Est-ce que le statut politique du Québec ÉTAIT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {'1.0': 'très important', '0.67': 'assez important', '0.33': 'peu important', '0.0': 'pas du tout important'},
}
