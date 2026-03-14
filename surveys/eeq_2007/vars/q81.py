# op_q81 — Unknown question, codes 01-05 observed
# Source: q81
# CRITICAL: Codebook entry was missing. Mapping codes based on observed string values (01-05) and treating 98/99 as missing.
# TODO: Verify question label, standard name, and value_labels against the full codebook.
df_clean['op_q81'] = df['q81'].map({
    '01': 'response_1',
    '02': 'response_2',
    '03': 'response_3',
    '04': 'response_4',
    '05': 'response_5',
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_q81'] = {
    'original_variable': 'q81',
    'question_label': "Unknown question - codebook missing",
    'type': 'categorical',
    'value_labels': {'response_1': "Response 1 (Unknown)", 'response_2': "Response 2 (Unknown)", 'response_3': "Response 3 (Unknown)", 'response_4': "Response 4 (Unknown)", 'response_5': "Response 5 (Unknown)"},
}
