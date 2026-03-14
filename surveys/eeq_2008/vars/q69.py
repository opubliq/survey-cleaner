# ses_region — Province/Region of residence (Inferred)
# Source: q69
# Assumption: Codes 8.0 and 9.0 observed in data but not in initial (missing) codebook entry are treated as missing. Code 4.0 is inferred.
df_clean['ses_region'] = df['q69'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'british columbia',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'q69',
    'question_label': "Province/Region of residence (Inferred from data exploration)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'british columbia': "British Columbia"},
}