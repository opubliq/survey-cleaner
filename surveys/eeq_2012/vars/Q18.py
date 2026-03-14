# op_q18_response — Response to Q18 (Assumed behavior/opinion)
# Source: Q18
# Assumption: Codes 96, 98, 99 treated as missing (unlabelled in provided context)
df_clean['op_q18_response'] = df['Q18'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    5.0: 'party_e',
    6.0: 'party_f',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q18_response'] = {
    'original_variable': 'Q18',
    'question_label': "Response to Q18 (Assumed election behavior/opinion)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'party_d': "Party D", 'party_e': "Party E", 'party_f': "Party F"},
}
