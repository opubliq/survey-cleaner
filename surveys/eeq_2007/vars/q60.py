# op_vote_intention — Voting intention (01-05 coded, 96-99 missing/other)
# Source: q60
# Assumption: Invented schema based on value counts, as codebook entry was for Q2_province.
# Codes 01-05 are assumed to be parties, 96-98 are assumed to be non-response, 99 is missing.
df_clean['op_vote_intention'] = df['q60'].map({
    '01': 'vote_pc',
    '02': 'vote_lib',
    '03': 'vote_bq',
    '04': 'vote_ndp',
    '05': 'vote_other',
    '96': 'refused',
    '97': 'don_t_know',
    '98': 'non_eligible',
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'q60',
    'question_label': "Voting intention (inferred)",
    'type': 'categorical',
    'value_labels': {'vote_pc': "PC", 'vote_lib': "Liberal", 'vote_bq': "Bloc Québécois", 'vote_ndp': "NDP", 'vote_other': "Other", 'refused': "Refused", 'don_t_know': "Don't Know", 'non_eligible': "Non-eligible"},
}