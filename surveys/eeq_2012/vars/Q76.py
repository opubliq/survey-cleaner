# op_attitude — Opinion on main parties (inferred)
# Source: Q76
# Assumption: Codes 8.0 and 9.0 treated as missing (not in assumed mapping 1-4)
df_clean['op_attitude'] = df['Q76'].map({
    1.0: 'support_party_1',
    2.0: 'support_party_2',
    3.0: 'support_party_3',
    4.0: 'support_party_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude'] = {
    'original_variable': 'Q76',
    'question_label': "Opinion on main parties (inferred)",
    'type': 'categorical',
    'value_labels': {'support_party_1': "Party 1", 'support_party_2': "Party 2", 'support_party_3': "Party 3", 'support_party_4': "Party 4"},
}