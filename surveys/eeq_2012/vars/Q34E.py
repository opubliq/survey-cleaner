# prov_party_understands_qc — Importance of party understanding Quebec's needs/issues in provincial elections.
# Source: Q34E
# Assumption: Codes 8/9 are treated as missing as they are 'don't know'/'prefer not to answer'.
# Assumption: Codes 2.0 and 3.0 mapped based on the importance scale implied by 1.0 and 4.0.
df_clean['prov_party_understands_qc'] = df['Q34E'].map({
    1.0: 'not at all important',
    2.0: 'not very important', # Inferred from scale
    3.0: 'fairly important',   # Inferred from scale
    4.0: 'very important',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['prov_party_understands_qc'] = {
    'original_variable': 'Q34E',
    'question_label': "And what about in Quebec provincial elections? How important would each of these things be when you make your voting choice? (4 = very important, 3 = fairly important, 2 = not very important, 1 = not at all important) / How well the party understands Queb",
    'type': 'categorical',
    'value_labels': {'not at all important': "1: not at all important", 'not very important': "2", 'fairly important': "3", 'very important': "4: very important"},
}