# ses_q46 — Generic categorical variable based on q46
# Source: q46
# Assumption: Codes 98 and 99 treated as missing (unlabelled in data exploration)
# Assumption: Codes 01-07 mapped to generic labels as codebook was unavailable
df_clean['ses_q46'] = df['q46'].map({
    '01': 'val_01',
    '02': 'val_02',
    '03': 'val_03',
    '04': 'val_04',
    '05': 'val_05',
    '06': 'val_06',
    '07': 'val_07',
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['ses_q46'] = {
    'original_variable': 'q46',
    'question_label': "Unlabelled categorical question from q46",
    'type': 'categorical',
    'value_labels': {'val_01': "Category 01", 'val_02': "Category 02", 'val_03': "Category 03", 'val_04': "Category 04", 'val_05': "Category 05", 'val_06': "Category 06", 'val_07': "Category 07"},
}