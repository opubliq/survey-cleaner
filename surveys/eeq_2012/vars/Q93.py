# ses_province_q93 — Inferred province of residence question
# Source: Q93
# Assumption: Codes 8.0 and 9.0 are missing codes not specified in the codebook.
df_clean['ses_province_q93'] = df['Q93'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province_q93'] = {
    'original_variable': 'Q93',
    'question_label': "Inferred province of residence question (Q93)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}