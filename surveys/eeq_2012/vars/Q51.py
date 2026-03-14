# op_attitude — Inferred: Attitude toward a topic
# Source: Q51
# Note: Codebook entry was missing for Q51. Assuming categorical scale 1-5, with 8/9 as missing.
df_clean['op_attitude'] = df['Q51'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude'] = {
    'original_variable': 'Q51',
    'question_label': "Inferred: Attitude toward a topic (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'response_1': 'Response 1', 'response_2': 'Response 2', 'response_3': 'Response 3', 'response_4': 'Response 4', 'response_5': 'Response 5'},
}