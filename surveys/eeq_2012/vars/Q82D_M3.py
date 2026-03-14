# op_response_q82d_m3 — Inferred response for question Q82D part 3
# Source: Q82D_M3
# Assumption: Codes 3, 4, 5 mapped as generic options due to missing codebook. All other numeric codes and NA will map to np.nan.
df_clean['op_response_q82d_m3'] = df['Q82D_M3'].map({
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
})
CODEBOOK_VARIABLES['op_response_q82d_m3'] = {
    'original_variable': 'Q82D_M3',
    'question_label': "Inferred response for question Q82D part 3 (Missing Codebook)",
    'type': 'categorical',
    'value_labels': {'option_3': "Option 3", 'option_4': "Option 4", 'option_5': "Option 5"},
}