# ses_province — Province/Territory of residence
# Source: Q2
# Assumption: Codes 8 and 9 are unlabelled missing values.
df_clean['ses_province'] = df['Q2'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'bc', # Best guess for 4th province
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q2',
    'question_label': "Province/Territory of residence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'bc': "British Columbia"},
}
