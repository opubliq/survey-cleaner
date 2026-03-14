# ses_region — Region of residence (inferred from codebook/name)
# Source: REGIO
# Assumption: Codes 1, 2, 3 mapped to generic region labels as codebook was unavailable.
# Assumption: All values are treated as categorical.
df_clean['ses_region'] = df['REGIO'].map({
    1.0: 'region_1',
    2.0: 'region_2',
    3.0: 'region_3',
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'REGIO',
    'question_label': "Region de résidence (unknown mapping)",
    'type': 'categorical',
    'value_labels': {'region_1': "Region 1 (Code 1)", 'region_2': "Region 2 (Code 2)", 'region_3': "Region 3 (Code 3)"},
}