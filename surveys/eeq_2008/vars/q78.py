# op_q78 — Likelihood to support party (10-point scale)
# Source: q78
# Assumption: Codes 1-10 are ordered likelihood. Codes 98, 99 mapped to missing.
df_clean['op_q78'] = df['q78'].map({
    1.0: 'not_at_all', 2.0: 'low', 3.0: 'low', 4.0: 'low_mid',
    5.0: 'neutral', 6.0: 'high_mid', 7.0: 'high', 8.0: 'high',
    9.0: 'very_high', 10.0: 'extremely_high',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q78'] = {
    'original_variable': 'q78',
    'question_label': "Likelihood to support party (10-point scale)",
    'type': 'likert',
    'value_labels': {'not_at_all': "Not at all likely", 'extremely_high': "Extremely likely"},
}