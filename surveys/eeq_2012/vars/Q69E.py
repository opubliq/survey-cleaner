# op_interest — Level of interest in the election
# Source: Q69E
# Assumption: Codes 1-6 are response categories, 95, 97, 98, 99 are treated as missing.
# TODO: The labels for codes 1-6 and the nature of codes 95, 97, 98 need verification against the full codebook.
df_clean['op_interest'] = df['Q69E'].map({
    1.0: 'very low',
    2.0: 'low',
    3.0: 'neutral',
    4.0: 'high',
    5.0: 'very high',
    6.0: 'refused',
    95.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_interest'] = {
    'original_variable': 'Q69E',
    'question_label': "Level of interest in the election",
    'type': 'categorical',
    'value_labels': {'very low': "Very low interest", 'low': "Low interest", 'neutral': "Neutral interest", 'high': "High interest", 'very high': "Very high interest", 'refused': "Refused"},
}
