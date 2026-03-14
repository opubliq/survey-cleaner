# op_party_choice — Inferred party choice
# Source: q48
# Assumption: codes 8.0 and 9.0 treated as missing (unlabelled in codebook)
df_clean['op_party_choice'] = df['q48'].map({
    1.0: 'party_1',
    2.0: 'party_2',
    3.0: 'party_3',
    4.0: 'party_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_party_choice'] = {
    'original_variable': 'q48',
    'question_label': "Inferred party choice from q48",
    'type': 'categorical',
    'value_labels': {'party_1': "Party 1", 'party_2': "Party 2", 'party_3': "Party 3", 'party_4': "Party 4"},
}