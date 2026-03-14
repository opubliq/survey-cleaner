# op_q70a — Opinion item on a scale (missing codebook labels)
# Source: Q70A
# Assumption: Codes 0.0-10.0 are distinct categories. Codes 98.0/99.0 treated as missing.
df_clean['op_q70a'] = df['Q70A'].map({
    0.0: 'not_applicable',
    1.0: 'level_1',
    2.0: 'level_2',
    3.0: 'level_3',
    4.0: 'level_4',
    5.0: 'level_5',
    6.0: 'level_6',
    7.0: 'level_7',
    8.0: 'level_8',
    9.0: 'level_9',
    10.0: 'level_10',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q70a'] = {
    'original_variable': 'Q70A',
    'question_label': "Opinion item Q70A (Labels assumed due to missing codebook data)",
    'type': 'categorical',
    'value_labels': {'not_applicable': "Not Applicable/Unknown", 'level_1': "Level 1", 'level_2': "Level 2", 'level_3': "Level 3", 'level_4': "Level 4", 'level_5': "Level 5", 'level_6': "Level 6", 'level_7': "Level 7", 'level_8': "Level 8", 'level_9': "Level 9", 'level_10': "Level 10"},
}