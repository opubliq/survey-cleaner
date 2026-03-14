# op_attitude_81 — Assumed 5-point attitude scale (no question text available)
# Source: q81
# Assumption: 5-point Likert scale (1=min, 5=max) normalized 0-1. Codes 98/99 treated as missing.
df_clean['op_attitude_81'] = df['q81'].map({
    1.0: 0.0,
    2.0: 0.25,
    3.0: 0.5,
    4.0: 0.75,
    5.0: 1.0,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_81'] = {
    'original_variable': 'q81',
    'question_label': "Question 81 (Type: Likert, unlabelled)",
    'type': 'likert',
    'value_labels': {'0.0': "Min (Code 1)", '0.25': "Code 2", '0.5': "Code 3", '0.75': "Code 4", '1.0': "Max (Code 5)"},
}