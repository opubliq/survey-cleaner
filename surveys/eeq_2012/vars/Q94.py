# op_opinion_q94 — Opinion or rating question Q94
# Source: Q94
# Assumption: 5-point scale normalized 0.0-1.0. Codes 97, 98, 99 treated as missing.
df_clean['op_opinion_q94'] = df['Q94'].map({
    1.0: 0.0,
    2.0: 0.25,
    3.0: 0.5,
    4.0: 0.75,
    5.0: 1.0,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_opinion_q94'] = {
    'original_variable': 'Q94',
    'question_label': "Opinion or rating question Q94 (Codebook label unknown)",
    'type': 'likert',
    'value_labels': {'0.0': "Lowest/Most Negative", '0.25': "Second Level", '0.5': "Neutral/Midpoint", '0.75': "Fourth Level", '1.0': "Highest/Most Positive"},
}