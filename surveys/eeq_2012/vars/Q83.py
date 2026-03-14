# op_economic_comparison — Comparison of Quebec's economic situation vs. rest of Canada
# Source: Q83
# Assumption: Codes 8.0 ('I don't know') and 9.0 ('I prefer not to answer') are treated as missing (np.nan)
df_clean['op_economic_comparison'] = df['Q83'].map({
    1.0: 'better',
    2.0: 'worse',
    3.0: 'no_different',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_economic_comparison'] = {
    'original_variable': 'Q83',
    'question_label': "If you compare the economic situation in Quebec with the rest of Canada, do you think that the situation is better in Quebec, worse, or no different?",
    'type': 'categorical',
    'value_labels': {'better': "Better", 'worse': "Worse", 'no_different': "No different"},
}