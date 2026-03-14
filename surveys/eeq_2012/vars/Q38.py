# ses_region — Region of residence (inferred)
# Source: Q38
# Assumption: This is a categorical variable based on float codes. Codes 8.0 and 9.0 are treated as missing since no codebook was provided.
df_clean['ses_region'] = df['Q38'].map({
    1.0: 'montreal',
    2.0: 'quebec_other',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'Q38',
    'question_label': "Region of residence (Inferred)",
    'type': 'categorical',
    'value_labels': {'montreal': "Montreal Area", 'quebec_other': "Rest of Quebec"},
}