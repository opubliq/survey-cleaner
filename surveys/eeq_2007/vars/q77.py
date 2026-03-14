# op_q77 — Unknown question from q77
# Source: q77
# Assumption: Codes 98 and 99 are treated as missing (np.nan) due to lack of codebook information.
df_clean['op_q77'] = df['q77'].map({
    '02': 'cat_02',
    '03': 'cat_03',
    '04': 'cat_04',
    '05': 'cat_05',
    '06': 'cat_06',
    '07': 'cat_07',
    '08': 'cat_08',
    '09': 'cat_09',
    '10': 'cat_10',
    '11': 'cat_11',
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_q77'] = {
    'original_variable': 'q77',
    'question_label': "Unknown categorical variable mapped from q77",
    'type': 'categorical',
    'value_labels': {'cat_02': "Category 02", 'cat_03': "Category 03", 'cat_04': "Category 04", 'cat_05': "Category 05", 'cat_06': "Category 06", 'cat_07': "Category 07", 'cat_08': "Category 08", 'cat_09': "Category 09", 'cat_10': "Category 10", 'cat_11': "Category 11"},
}