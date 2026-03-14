# ses_n_children — Number of children in the household (inferred)
# Source: qenfan2
# Assumption: This mapping is inferred as no codebook was provided in the input JSON.
# Codes 1.0 and 2.0 are mapped to strings, 9.0 is treated as missing (np.nan).
df_clean['ses_n_children'] = df['qenfan2'].map({
    1.0: 'one',
    2.0: 'two',
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_n_children'] = {
    'original_variable': 'qenfan2',
    'question_label': "Number of children in household (INFERRED)",
    'type': 'categorical',
    'value_labels': {'one': "One child", 'two': "Two children"},
}