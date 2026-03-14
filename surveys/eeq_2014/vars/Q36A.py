# ses_region — Région de résidence
# Source: Q36A
# Assumption: 8/9 treated as missing, as they are not explicitly labelled in the codebook for this variable.
# Note: Values are float, mapping to string for categorical variable.
df_clean['ses_region'] = df['Q36A'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'manitoba_sask', # Inferring from other surveys, as 4 is unlabelled here
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'Q36A',
    'question_label': "Région de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'manitoba_sask': "Manitoba/Saskatchewan"},
}
