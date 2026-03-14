# ses_region — Region/Riding of residence
# Source: QREGION
# Note: Lacking codebook_entry.values, codes 1.0-17.0 mapped to generic placeholders based on data exploration.
# Assumption: All observed codes (1.0-17.0) are valid and unlabelled codes are not present (since missing count is 0).
df_clean['ses_region'] = df['QREGION'].map({
    1.0: 'region_01',
    2.0: 'region_02',
    3.0: 'region_03',
    4.0: 'region_04',
    5.0: 'region_05',
    6.0: 'region_06',
    7.0: 'region_07',
    8.0: 'region_08',
    9.0: 'region_09',
    10.0: 'region_10',
    11.0: 'region_11',
    12.0: 'region_12',
    13.0: 'region_13',
    14.0: 'region_14',
    15.0: 'region_15',
    16.0: 'region_16',
    17.0: 'region_17',
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'QREGION',
    'question_label': "Region of residence",
    'type': 'categorical',
    'value_labels': {'region_01': "Placeholder Region 1", 'region_02': "Placeholder Region 2", 'region_03': "Placeholder Region 3", 'region_04': "Placeholder Region 4", 'region_05': "Placeholder Region 5", 'region_06': "Placeholder Region 6 (Most Frequent)", 'region_07': "Placeholder Region 7", 'region_08': "Placeholder Region 8", 'region_09': "Placeholder Region 9", 'region_10': "Placeholder Region 10", 'region_11': "Placeholder Region 11", 'region_12': "Placeholder Region 12", 'region_13': "Placeholder Region 13", 'region_14': "Placeholder Region 14", 'region_15': "Placeholder Region 15", 'region_16': "Placeholder Region 16", 'region_17': "Placeholder Region 17"},
}