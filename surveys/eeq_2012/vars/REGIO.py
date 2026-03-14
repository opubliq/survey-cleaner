# ses_region — Province/Region of residence
# Source: REGIO
# Assumption: Codes 1, 2, 3 mapped to major Canadian political regions for the 2012 election context.
df_clean['ses_region'] = df['REGIO'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'other_province',
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'REGIO',
    'question_label': "Province ou région de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'other_province': "Autre province"},
}