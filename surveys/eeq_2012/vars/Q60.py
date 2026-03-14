# op_vote_intention — Province de résidence (Inferred: Vote intention/actual vote)
# Source: Q60
# Assumption: Codes 1-5 are valid provinces/regions, 8 and 9 are missing values (Refused/DK).
# Assumption: Codes 4 and 5 map to 'other' regions since only 1-3 were provided in typical context.
df_clean['op_vote_intention'] = df['Q60'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'other',
    5.0: 'other',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q60',
    'question_label': "Province/Region de résidence (Inferred)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'other': "Other/Unspecified Region"},
}
