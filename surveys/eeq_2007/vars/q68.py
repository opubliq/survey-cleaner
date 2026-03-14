# op_attitude_q68 — General attitude question 68
# Source: q68
# Assumption: Treat values 1-4 as a 4-point scale and 8/9 as missing, as no labels were provided.
df_clean['op_attitude_q68'] = df['q68'].map({
    1.0: 'low',
    2.0: 'medium_low',
    3.0: 'medium_high',
    4.0: 'high',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q68'] = {
    'original_variable': 'q68',
    'question_label': "Attitude question 68 (No labels provided in context)",
    'type': 'categorical',
    'value_labels': {'low': "Low", 'medium_low': "Medium Low", 'medium_high': "Medium High", 'high': "High"},
}