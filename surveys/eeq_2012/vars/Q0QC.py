# ses_region_code — Preliminary response code (1-17 observed)
# Source: Q0QC
# Assumption: Variable mapped to string representation of float codes 1.0-17.0 due to missing codebook labels.
# TODO: verify mapping for codes 1.0 through 17.0 against actual codebook.
df_clean['ses_region_code'] = df['Q0QC'].map({
    1.0: '1',
    2.0: '2',
    3.0: '3',
    4.0: '4',
    5.0: '5',
    6.0: '6',
    7.0: '7',
    8.0: '8',
    9.0: '9',
    10.0: '10',
    11.0: '11',
    12.0: '12',
    13.0: '13',
    14.0: '14',
    15.0: '15',
    16.0: '16',
    17.0: '17',
})
CODEBOOK_VARIABLES['ses_region_code'] = {
    'original_variable': 'Q0QC',
    'question_label': "Preliminary response code (1-17 observed)",
    'type': 'categorical',
    'value_labels': {'1': "Code 1", '2': "Code 2", '3': "Code 3", '4': "Code 4", '5': "Code 5", '6': "Code 6", '7': "Code 7", '8': "Code 8", '9': "Code 9", '10': "Code 10", '11': "Code 11", '12': "Code 12", '13': "Code 13", '14': "Code 14", '15': "Code 15", '16': "Code 16", '17': "Code 17"},
}