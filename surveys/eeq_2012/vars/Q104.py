# op_vote_choice — Unknown vote choice variable
# Source: Q104
# Assumption: Codes 8.0 and 9.0 are treated as missing based on value_counts (not in main codebook).
# Note: Value labels are placeholders as no codebook was provided for Q104.
df_clean['op_vote_choice'] = df['Q104'].map({
    1.0: 'choice_1',
    2.0: 'choice_2',
    3.0: 'choice_3',
    4.0: 'choice_4',
    5.0: 'choice_5',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_choice'] = {
    'original_variable': 'Q104',
    'question_label': "Unknown question label for Q104",
    'type': 'categorical',
    'value_labels': {'choice_1': "Observed Code 1", 'choice_2': "Observed Code 2", 'choice_3': "Observed Code 3", 'choice_4': "Observed Code 4", 'choice_5': "Observed Code 5"},
}
