# op_opinion_29a — Unknown: Inferring from many numeric codes (0-44+)
# Source: Q29A
# Assumption: Codes 0-10 mapped to generic categories due to missing codebook. All other observed codes (11, 12, 15, 17, 20, 25, 30, 32, 34, 35, 40, 41, 42, 44, etc.) are treated as missing/unmappable.
df_clean['op_opinion_29a'] = df['Q29A'].map({
    0.0: 'none',
    1.0: 'low_1',
    2.0: 'low_2',
    3.0: 'low_3',
    4.0: 'low_4',
    5.0: 'low_5',
    6.0: 'low_6',
    7.0: 'low_7',
    8.0: 'low_8',
    9.0: 'low_9',
    10.0: 'low_10',
})
CODEBOOK_VARIABLES['op_opinion_29a'] = {
    'original_variable': 'Q29A',
    'question_label': "Unknown: Inferring from many numeric codes (0-44+)",
    'type': 'categorical',
    'value_labels': {'none': "None/Missing", 'low_1': "Category 1", 'low_2': "Category 2", 'low_3': "Category 3", 'low_4': "Category 4", 'low_5': "Category 5", 'low_6': "Category 6", 'low_7': "Category 7", 'low_8': "Category 8", 'low_9': "Category 9", 'low_10': "Category 10"},
}