# ses_province — Province of residence (Inferred mapping)
# Source: Q36E
# Assumption: Codes 8 and 9 are treated as missing (not in inferred codebook).
# TODO: Verify mapping for Q36E as no codebook entry was provided.
df_clean['ses_province'] = df['Q36E'].map({
    1.0: 'value 1',
    2.0: 'value 2',
    3.0: 'value 3',
    4.0: 'value 4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q36E',
    'question_label': "Province of residence (Inferred)",
    'type': 'categorical',
    'value_labels': {'value 1': "Value 1", 'value 2': "Value 2", 'value 3': "Value 3", 'value 4': "Value 4"},
}