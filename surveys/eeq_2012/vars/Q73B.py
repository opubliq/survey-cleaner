# ses_votemode — Mode de scrutin
# Source: Q73B
# Assumption: codes 8 and 9 are missing based on typical survey practice (not in codebook)
df_clean['ses_votemode'] = df['Q73B'].map({
    1.0: 'main_residence',
    2.0: 'another_municipality',
    3.0: 'another_riding',
    4.0: 'in_person_outside_riding',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_votemode'] = {
    'original_variable': 'Q73B',
    'question_label': "Mode de scrutin",
    'type': 'categorical',
    'value_labels': {'main_residence': "Vote à la circonscription de résidence", 'another_municipality': "Vote dans une autre municipalité", 'another_riding': "Vote dans une autre circonscription", 'in_person_outside_riding': "Vote en personne en dehors de la circonscription"},
}