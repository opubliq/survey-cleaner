# ses_child_status — Status/count of children in household
# Source: QENFAN
# Assumption: Codebook was missing. Inferring mapping based on codes 1, 2, 9.
# Assumption: Code 9 is treated as missing/refused.
df_clean['ses_child_status'] = df['QENFAN'].map({
    1.0: 'one',
    2.0: 'two',
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_child_status'] = {
    'original_variable': 'QENFAN',
    'question_label': "Status or count of children in household (Inferred)",
    'type': 'categorical',
    'value_labels': {'one': "One child", 'two': "Two children"},
}