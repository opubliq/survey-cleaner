# op_party_preference — Party preference or group affiliation (Q34BB)
# Source: Q34BB
# Assumption: Codes 98/99 are treated as missing (not explicitly labelled in codebook context)
# Assumption: The 7 distinct codes (1-7) correspond to 7 different parties/groups.
df_clean['op_party_preference'] = df['Q34BB'].map({
    1.0: 'party_1',
    2.0: 'party_2',
    3.0: 'party_3',
    4.0: 'party_4',
    5.0: 'party_5',
    6.0: 'party_6',
    7.0: 'party_7',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_party_preference'] = {
    'original_variable': 'Q34BB',
    'question_label': "Party preference or group affiliation (Q34BB)",
    'type': 'categorical',
    'value_labels': {'party_1': 'Party 1', 'party_2': 'Party 2', 'party_3': 'Party 3', 'party_4': 'Party 4', 'party_5': 'Party 5', 'party_6': 'Party 6', 'party_7': 'Party 7'},
}