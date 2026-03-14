# ses_ethnicity — Ethnicity of respondent
# Source: ethn1
# Assumption: Codes 96 and 99 are treated as missing (not in assumed codebook)
# Assumption: Codes 1.0 through 13.0 are mapped to generic string labels as actual labels are unavailable.
df_clean['ses_ethnicity'] = df['ethn1'].map({
    1.0: 'category_1',
    2.0: 'category_2',
    3.0: 'category_3',
    4.0: 'category_4',
    5.0: 'category_5',
    6.0: 'category_6',
    7.0: 'category_7',
    8.0: 'category_8',
    9.0: 'category_9',
    10.0: 'category_10',
    11.0: 'category_11',
    12.0: 'category_12',
    13.0: 'category_13',
    96.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_ethnicity'] = {
    'original_variable': 'ethn1',
    'question_label': "Ethnicity of respondent (mapped generically)",
    'type': 'categorical',
    'value_labels': {'category_1': "Category 1", 'category_2': "Category 2", 'category_3': "Category 3", 'category_4': "Category 4", 'category_5': "Category 5", 'category_6': "Category 6", 'category_7': "Category 7", 'category_8': "Category 8", 'category_9': "Category 9", 'category_10': "Category 10", 'category_11': "Category 11", 'category_12': "Category 12", 'category_13': "Category 13"},
}