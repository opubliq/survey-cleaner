# op_q43a — Inferred categorical variable
# Source: Q43A
# CRITICAL: Codebook entry was missing. Mapping labels are generic placeholders derived from observed values in data exploration.
df_clean['op_q43a'] = df['Q43A'].map({
    0.0: 'no_response',
    1.0: 'cat_1',
    2.0: 'cat_2',
    3.0: 'cat_3',
    4.0: 'cat_4',
    5.0: 'cat_5',
    6.0: 'cat_6',
    8.0: 'cat_8',
    10.0: 'cat_10',
    15.0: 'cat_15',
    19.0: 'cat_19',
    20.0: 'cat_20',
    25.0: 'cat_25',
    30.0: 'cat_30',
    33.0: 'cat_33',
    35.0: 'cat_35',
    37.0: 'cat_37',
    40.0: 'cat_40',
    42.0: 'cat_42',
    45.0: 'cat_45',
    49.0: 'cat_49',
    50.0: 'cat_50',
    51.0: 'cat_51',
    55.0: 'cat_55',
    60.0: 'cat_60',
})
CODEBOOK_VARIABLES['op_q43a'] = {
    'original_variable': 'Q43A',
    'question_label': "Q43A (Label missing in context)",
    'type': 'categorical',
    'value_labels': {'no_response': "No Response (Inferred)", 'cat_1': "Category 1 (Inferred)", 'cat_2': "Category 2 (Inferred)", 'cat_3': "Category 3 (Inferred)", 'cat_4': "Category 4 (Inferred)", 'cat_5': "Category 5 (Inferred)", 'cat_6': "Category 6 (Inferred)", 'cat_8': "Category 8 (Inferred)", 'cat_10': "Category 10 (Inferred)", 'cat_15': "Category 15 (Inferred)", 'cat_19': "Category 19 (Inferred)", 'cat_20': "Category 20 (Inferred)", 'cat_25': "Category 25 (Inferred)", 'cat_30': "Category 30 (Inferred)", 'cat_33': "Category 33 (Inferred)", 'cat_35': "Category 35 (Inferred)", 'cat_37': "Category 37 (Inferred)", 'cat_40': "Category 40 (Inferred)", 'cat_42': "Category 42 (Inferred)", 'cat_45': "Category 45 (Inferred)", 'cat_49': "Category 49 (Inferred)", 'cat_50': "Category 50 (Inferred)", 'cat_51': "Category 51 (Inferred)", 'cat_55': "Category 55 (Inferred)", 'cat_60': "Category 60 (Inferred)"}
}