# ses_region_g — Region G (Best guess due to missing codebook)
# Source: Q29G
# Assumption: All observed codes mapped to generic region labels as codebook is missing.
df_clean['ses_region_g'] = df['Q29G'].map({
    0.0: 'region_0',
    1.0: 'region_1',
    2.0: 'region_2',
    3.0: 'region_3',
    4.0: 'region_4',
    5.0: 'region_5',
    6.0: 'region_6',
    9.0: 'region_9',
    10.0: 'region_10',
    11.0: 'region_11',
    13.0: 'region_13',
    15.0: 'region_15',
    16.0: 'region_16',
    18.0: 'region_18',
    20.0: 'region_20',
    23.0: 'region_23',
    25.0: 'region_25',
    30.0: 'region_30',
    32.0: 'region_32',
    35.0: 'region_35',
    39.0: 'region_39',
    40.0: 'region_40',
    44.0: 'region_44',
    45.0: 'region_45',
    49.0: 'region_49',
})
CODEBOOK_VARIABLES['ses_region_g'] = {
    'original_variable': 'Q29G',
    'question_label': "Q29G - Unknown Region/Category",
    'type': 'categorical',
    'value_labels': {
        'region_0': 'Category 0', 'region_1': 'Category 1', 'region_2': 'Category 2', 
        'region_3': 'Category 3', 'region_4': 'Category 4', 'region_5': 'Category 5', 
        'region_6': 'Category 6', 'region_9': 'Category 9', 'region_10': 'Category 10', 
        'region_11': 'Category 11', 'region_13': 'Category 13', 'region_15': 'Category 15', 
        'region_16': 'Category 16', 'region_18': 'Category 18', 'region_20': 'Category 20', 
        'region_23': 'Category 23', 'region_25': 'Category 25', 'region_30': 'Category 30', 
        'region_32': 'Category 32', 'region_35': 'Category 35', 'region_39': 'Category 39', 
        'region_40': 'Category 40', 'region_44': 'Category 44', 'region_45': 'Category 45', 
        'region_49': 'Category 49'
    }
}