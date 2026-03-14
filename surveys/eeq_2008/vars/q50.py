# op_q50 — Inferred opinion variable q50
# Source: q50
# Assumption: Codes 8.0 and 9.0 treated as missing (unlabelled in provided context)
# TODO: verify mapping for codes 1.0-4.0 as labels are missing from context
df_clean['op_q50'] = df['q50'].map({
    1.0: 'level_1',
    2.0: 'level_2',
    3.0: 'level_3',
    4.0: 'level_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q50'] = {
    'original_variable': 'q50',
    'question_label': "Inferred: Question 50",
    'type': 'categorical',
    'value_labels': {'level_1': "Level 1", 'level_2': "Level 2", 'level_3': "Level 3", 'level_4': "Level 4"},
}