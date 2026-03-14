# ses_Q14B — Inferred political data point from Q14B
# Source: Q14B
# Assumption: Codes 1-5 are categories, codes 8, 9, and NaN are missing. Type inferred as categorical.
df_clean['ses_Q14B'] = df['Q14B'].map({
    1.0: 'choice_1',
    2.0: 'choice_2',
    3.0: 'choice_3',
    4.0: 'choice_4',
    5.0: 'choice_5',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_Q14B'] = {
    'original_variable': 'Q14B',
    'question_label': "Inferred data point from Q14B (no codebook entry provided)",
    'type': 'categorical',
    'value_labels': {'choice_1': "Category 1", 'choice_2': "Category 2", 'choice_3': "Category 3", 'choice_4': "Category 4", 'choice_5': "Category 5"},
}