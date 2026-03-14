# op_q30b — Inferred 6-point opinion scale (1=very negative, 6=very positive)
# Source: Q30B
# Assumption: Codes 1.0-6.0 mapped linearly to 0.0-1.0. Codes 95.0, 97.0, 98.0, 99.0 treated as missing.
df_clean['op_q30b'] = df['Q30B'].map({
    1.0: 0.0,
    2.0: 0.2,
    3.0: 0.4,
    4.0: 0.6,
    5.0: 0.8,
    6.0: 1.0,
    95.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q30b'] = {
    'original_variable': 'Q30B',
    'question_label': "Inferred: Opinion on topic (6-point scale)",
    'type': 'likert',
    'value_labels': {0.0: "very negative", 1.0: "very positive"},
}