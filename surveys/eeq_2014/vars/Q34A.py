# op_liberal_approval — Approuvez-vous ou non le gouvernement du Parti Libéral du Québec?
# Source: Q34A
# Note: Likert scale normalized to 0.0 (most negative) to 1.0 (most positive) based on 4 levels (1, 2, 3, 4).
# Assumption: Codes 8.0, 9.0, and unmapped codes treated as missing (np.nan).
df_clean['op_liberal_approval'] = df['Q34A'].map({
    1.0: 1.0,
    2.0: 2/3,
    3.0: 1/3,
    4.0: 0.0,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_liberal_approval'] = {
    'original_variable': 'Q34A',
    'question_label': "Approuvez-vous ou non le gouvernement du Parti Libéral du Québec?",
    'type': 'likert',
    'value_labels': {1.0: "Approuve fortement", round(2/3, 4): "Approuve", round(1/3, 4): "Approuve peu", 0.0: "Désapprouve"},
}