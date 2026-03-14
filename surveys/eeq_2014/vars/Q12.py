# op_support_q12 — Overall support level for subject of Q12
# Source: Q12
# Assumption: codes 8 and 9 treated as missing (unlabelled in context)
# TODO: verify mapping for codes 1-4, 8, 9 as codebook for Q12 is missing
df_clean['op_support_q12'] = df['Q12'].map({
    1.0: 'strong_support',
    2.0: 'moderate_support',
    3.0: 'moderate_oppose',
    4.0: 'strong_oppose',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_support_q12'] = {
    'original_variable': 'Q12',
    'question_label': "Overall support level for subject of Q12",
    'type': 'categorical',
    'value_labels': {'strong_support': "Strong Support", 'moderate_support': "Moderate Support", 'moderate_oppose': "Moderate Oppose", 'strong_oppose': "Strong Oppose"},
}