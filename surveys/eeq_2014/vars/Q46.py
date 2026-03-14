# op_vote_intention — Vote intention
# Source: Q46
# Assumption: Codes 8 and 9 are treated as missing (Don't know/Refused).
df_clean['op_vote_intention'] = df['Q46'].map({
    1.0: 'choice_one',
    2.0: 'choice_two',
    3.0: 'choice_three',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q46',
    'question_label': "Vote intention",
    'type': 'categorical',
    'value_labels': {'choice_one': "Choice One", 'choice_two': "Choice Two", 'choice_three': "Choice Three"},
}
