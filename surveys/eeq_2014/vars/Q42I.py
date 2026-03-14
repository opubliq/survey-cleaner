# ses_q42i — Province de résidence
# Source: Q42I
# Assumption: Codes 96, 98, 99 are treated as missing (unlabelled in data/codebook)
# TODO: Verify question label and map actual values for 1.0-6.0
df_clean['ses_q42i'] = df['Q42I'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    6.0: 'response_6',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_q42i'] = {
    'original_variable': 'Q42I',
    'question_label': "Question Q42I - Needs Label Update",
    'type': 'categorical',
    'value_labels': {'response_1': "Response 1", 'response_2': "Response 2", 'response_3': "Response 3", 'response_4': "Response 4", 'response_5': "Response 5", 'response_6': "Response 6"},
}