# ses_q19_response — Inferred response to Question 19
# Source: Q19
# WARNING: Codebook entry was missing. Mapping based on data exploration (values 1.0-5.0 mapped, 96/98/99 treated as missing).
# TODO: Verify mapping and question label for ses_q19_response
df_clean['ses_q19_response'] = df['Q19'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_q19_response'] = {
    'original_variable': 'Q19',
    'question_label': "Inferred: Response to Question 19",
    'type': 'categorical',
    'value_labels': {'response_1': 'Code 1', 'response_2': 'Code 2', 'response_3': 'Code 3', 'response_4': 'Code 4', 'response_5': 'Code 5'},
}
