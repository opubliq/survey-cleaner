# op_q82d_m1 — Inferred Q82D part 1 opinion/attitude
# Source: Q82D_M1
# Assumption: Likert scale normalized 0.0 to 1.0. Code 9.0 treated as missing (unlabelled in codebook/data exploration).
df_clean['op_q82d_m1'] = df['Q82D_M1'].map({
    1.0: 0.0,
    2.0: 0.2,
    3.0: 0.4,
    4.0: 0.6,
    5.0: 0.8,
    7.0: 1.0,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q82d_m1'] = {
    'original_variable': 'Q82D_M1',
    'question_label': "Inferred Q82D part 1 opinion/attitude",
    'type': 'likert',
    'value_labels': {0.0: "Label 1", 0.2: "Label 2", 0.4: "Label 3", 0.6: "Label 4", 0.8: "Label 5", 1.0: "Label 6"},
}