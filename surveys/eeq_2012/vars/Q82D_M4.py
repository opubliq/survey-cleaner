# know_q82dm4 — Unknown question part M4 from Q82D
# Source: Q82D_M4
# Note: No codebook provided. Mapping based on observed data (4.0, 5.0). All unmapped/NaN values become np.nan.
df_clean['know_q82dm4'] = df['Q82D_M4'].map({
    4.0: 'code_4',
    5.0: 'code_5',
})
CODEBOOK_VARIABLES['know_q82dm4'] = {
    'original_variable': 'Q82D_M4',
    'question_label': "Unknown question part M4 from Q82D (requires codebook)",
    'type': 'categorical',
    'value_labels': {'code_4': "Observed code 4", 'code_5': "Observed code 5"},
}