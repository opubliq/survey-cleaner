# op_opinion_q62i — Deduced categorical opinion variable Q62I
# Source: Q62I
# Assumption: Mapping is a placeholder as codebook entry was not provided for Q62I.
# Assumption: Codes 6.0, 8.0, 9.0 are treated as missing/unspecified.
df_clean['op_opinion_q62i'] = df['Q62I'].map({
    1.0: 'level_one',
    2.0: 'level_two',
    6.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_opinion_q62i'] = {
    'original_variable': 'Q62I',
    'question_label': "Q62I (Label Missing - Deduced Categorical)",
    'type': 'categorical',
    'value_labels': {'level_one': "Level One", 'level_two': "Level Two"},
}