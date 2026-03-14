# behav_q42b — Response to question Q42B (Inferred as behavioral)
# Source: Q42B
# Assumption: Codes 96, 98, 99 are treated as missing as they are unlabelled in the data exploration.
# Assumption: Codes 1-6 map to generic values. A proper codebook is needed for accurate labels.
df_clean['behav_q42b'] = df['Q42B'].map({
    1.0: 'value_1',
    2.0: 'value_2',
    3.0: 'value_3',
    4.0: 'value_4',
    5.0: 'value_5',
    6.0: 'value_6',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q42b'] = {
    'original_variable': 'Q42B',
    'question_label': "Response to Q42B (Inferred)",
    'type': 'categorical',
    'value_labels': {'value_1': "Response 1", 'value_2': "Response 2", 'value_3': "Response 3", 'value_4': "Response 4", 'value_5': "Response 5", 'value_6': "Response 6"},
}