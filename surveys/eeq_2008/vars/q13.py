# op_attitude_q13 — Attitude question q13 (Mapping inferred due to missing codebook entry)
# Source: q13
# Assumption: Codes 1-5 represent a scale, codes 95+ are missing/unlabelled.
df_clean['op_attitude_q13'] = df['q13'].map({
    1.0: 'very_low',
    2.0: 'low',
    3.0: 'medium',
    4.0: 'high',
    5.0: 'very_high',
    95.0: np.nan,
    96.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q13'] = {
    'original_variable': 'q13',
    'question_label': "Question q13 from eeq_2008 (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'very_low': "Code 1 (Inferred)", 'low': "Code 2 (Inferred)", 'medium': "Code 3 (Inferred)", 'high': "Code 4 (Inferred)", 'very_high': "Code 5 (Inferred)"},
}