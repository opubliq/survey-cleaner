# op_behavior_m2 — Likelihood of a specific behavior (M2)
# Source: Q82D_M2
# Assumption: Treating as categorical based on observed float values [2.0, 3.0, 4.0, 5.0].
# Assumption: Missing values are represented by NaN in the data.
df_clean['op_behavior_m2'] = df['Q82D_M2'].map({
    2.0: 'less_likely',
    3.0: 'somewhat_less_likely',
    4.0: 'somewhat_more_likely',
    5.0: 'more_likely',
})
CODEBOOK_VARIABLES['op_behavior_m2'] = {
    'original_variable': 'Q82D_M2',
    'question_label': "Likelihood of behavior M2 (Assumed)",
    'type': 'categorical',
    'value_labels': {'less_likely': "Less Likely", 'somewhat_less_likely': "Somewhat Less Likely", 'somewhat_more_likely': "Somewhat More Likely", 'more_likely': "More Likely"},
}