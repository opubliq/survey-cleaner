# op_canadian_identity — How respondent identifies (Quebec vs Canada)
# Source: q18a
# Note: 1093 blank values (empty strings) treated as missing
df_clean['op_canadian_identity'] = df['q18a'].map({
    '01': 'quebec_only',
    '02': 'quebec_first',
    '03': 'equal',
    '04': 'canada_first',
    '05': 'canada_only',
    '96': 'other',
    '98': np.nan,
    '99': np.nan,
    '': np.nan,
})
CODEBOOK_VARIABLES['op_canadian_identity'] = {
    'original_variable': 'q18a',
    'question_label': "Les gens ont différentes façons de se définir. Diriez-vous que vous vous considérez...?",
    'type': 'categorical',
    'value_labels': {
        'quebec_only': "...uniquement comme Québécois(e)",
        'quebec_first': "...d'abord comme Québécois(e), puis comme Canadien(ne)",
        'equal': "...également comme Canadien(ne) et comme Québécois(e)",
        'canada_first': "...d'abord comme Canadien(ne), puis comme Québécois(e)",
        'canada_only': "...ou uniquement comme Canadien(ne)?",
        'other': "autres (précisez)",
    },
}
