# ses_region — Region of residence
# Source: regio
# Assumption: Based on the context of an election study, 1/2/3 are mapped to major regions within the study area.
# TODO: verify mapping for codes 1.0, 2.0, 3.0 against official eeq_2008 codebook.
df_clean['ses_region'] = df['regio'].map({
    1.0: 'montreal',
    2.0: 'quebec_city',
    3.0: 'rest_of_province',
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'regio',
    'question_label': "Region of residence",
    'type': 'categorical',
    'value_labels': {'montreal': "Montreal Area", 'quebec_city': "Quebec City Area", 'rest_of_province': "Rest of Province"},
}