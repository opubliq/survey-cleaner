# op_education_importance — Importance of education as an election issue
# Source: q3
# Type: Likert scale (4-point) normalized to 0-1
# Assumption: codes 8 and 9 (missing/refusal) treated as missing
df_clean['op_education_importance'] = df['q3'].astype(float).map({
    1.0: 1.0,
    2.0: 0.67,
    3.0: 0.33,
    4.0: 0.0,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_education_importance'] = {
    'original_variable': 'q3',
    'question_label': "Est-ce que l'éducation ÉTAIT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {'0.0': 'not at all important', '0.33': 'little important', '0.67': 'fairly important', '1.0': 'very important'},
}
