# op_Q101E — Opinion variable 101E
# Source: Q101E
# Assumption: Codes 1/2 are affirmative/negative response; 8/9 are missing.
# TODO: Verify actual question text and meaning of codes 1/2/8/9.
df_clean['op_Q101E'] = df['Q101E'].map({
    1.0: 'support',
    2.0: 'oppose',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_Q101E'] = {
    'original_variable': 'Q101E',
    'question_label': "Placeholder: Q101E Label - NEEDS MANUAL VERIFICATION",
    'type': 'categorical',
    'value_labels': {'support': "Support/Yes", 'oppose': "Oppose/No"},
}