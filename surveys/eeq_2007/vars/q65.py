# behav_q65 — Response category for Q65
# Source: q65
# Assumption: No codebook available. Mapping speculative based on value_counts().
# Codes 50.0, 60.0, 70.0, 40.0, 30.0 mapped to distinct categories. All others (including 0.0) are treated as missing.
df_clean['behav_q65'] = df['q65'].map({
    50.0: 'cat_50',
    60.0: 'cat_60',
    70.0: 'cat_70',
    40.0: 'cat_40',
    30.0: 'cat_30',
})
CODEBOOK_VARIABLES['behav_q65'] = {
    'original_variable': 'q65',
    'question_label': "Q65 (Label unknown - speculative cleaning based on data exploration)",
    'type': 'categorical',
    'value_labels': {'cat_50': "Category 50", 'cat_60': "Category 60", 'cat_70': "Category 70", 'cat_40': "Category 40", 'cat_30': "Category 30"},
}
