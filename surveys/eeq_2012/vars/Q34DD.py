# op_satisfaction_level — Level of satisfaction
# Source: Q34DD
# Assumption: Codes 5.0, 6.0, 96.0 treated as missing (unlabelled in codebook)
# Assumption: Codes 98.0, 99.0 treated as missing (explicitly listed in codebook)
df_clean['op_satisfaction_level'] = df['Q34DD'].map({
    1.0: 'very satisfied',
    2.0: 'satisfied',
    3.0: 'not satisfied',
    4.0: 'not at all satisfied',
    5.0: np.nan,
    6.0: np.nan,
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_satisfaction_level'] = {
    'original_variable': 'Q34DD',
    'question_label': "Q34DD",
    'type': 'categorical',
    'value_labels': {'very satisfied': "Very satisfied", 'satisfied': "Satisfied", 'not satisfied': "Not satisfied", 'not at all satisfied': "Not at all satisfied"},
}