# behav_vote_frequency — Frequency of participation in federal elections
# Source: Q31F
# Assumption: Codes 9.0, 98.0, 99.0 are unmapped/missing and will become np.nan.
# Assumption: Likert scale normalized 1.0 (Always) to 0.0 (Never/Not applicable).
df_clean['behav_vote_frequency'] = df['Q31F'].map({
    0.0: 1.0,
    1.0: 0.8,
    2.0: 0.6,
    3.0: 0.4,
    4.0: 0.2,
    5.0: 0.0,
    6.0: 0.0, # N'a pas voté (2011) mapped to lowest frequency bin
    7.0: 0.0, # N'était pas admissible (2011) mapped to lowest frequency bin
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_frequency'] = {
    'original_variable': 'Q31F',
    'question_label': "Fréquence de participation aux élections fédérales",
    'type': 'likert',
    'value_labels': {1.0: "Toujours", 0.8: "Presque toujours", 0.6: "Souvent", 0.4: "Parfois", 0.2: "Rarement", 0.0: "Jamais / Non-parti"},
}