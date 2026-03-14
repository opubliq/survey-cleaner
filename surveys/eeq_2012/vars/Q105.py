# op_vote_intention — Inferred vote intention/party support
# Source: Q105
# Assumption: Codes 1, 2, 3 map to Party A, B, C respectively; code 9 is unlabelled and mapped to 'not_applicable' due to lack of codebook.
df_clean['op_vote_intention'] = df['Q105'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    9.0: 'not_applicable',
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q105',
    'question_label': "Inferred: Vote intention or party support for Q105",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'not_applicable': "Not Applicable"},
}
