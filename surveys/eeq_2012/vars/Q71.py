# op_q71_attitude — Attitude toward the election (Likert scale)
# Source: Q71
# Assumption: This is a 0-10 Likert scale question. Values 98 and 99 are assumed to be missing/refused based on data exploration.
# Mapping is normalized 0.0 (min) to 1.0 (max) corresponding to codes 0.0 to 10.0.
df_clean['op_q71_attitude'] = df['Q71'].map({
    0.0: 0.0,
    1.0: 0.1,
    2.0: 0.2,
    3.0: 0.3,
    4.0: 0.4,
    5.0: 0.5,
    6.0: 0.6,
    7.0: 0.7,
    8.0: 0.8,
    9.0: 0.9,
    10.0: 1.0,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q71_attitude'] = {
    'original_variable': 'Q71',
    'question_label': "Attitude toward the election (Normalized 0-10)",
    'type': 'likert',
    'value_labels': {'0.0': "Min Intensity/Agreement", '1.0': "Max Intensity/Agreement"},
}