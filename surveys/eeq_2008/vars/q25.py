# op_q25 — Response category for Q25
# Source: q25
# Assumption: Codes 8 and 9 treated as missing (not explicitly labelled in codebook context)
df_clean['op_q25'] = df['q25'].map({
    1.0: 'category_1',
    2.0: 'category_2',
    3.0: 'category_3',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q25'] = {
    'original_variable': 'q25',
    'question_label': "Response category for Q25",
    'type': 'categorical',
    'value_labels': {'category_1': "Category 1", 'category_2': "Category 2", 'category_3': "Category 3"},
}