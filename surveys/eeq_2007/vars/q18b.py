# op_identity_qc_can — National identity orientation (Quebec-Canada)
# Source: q18b
# Note: value 1082 appears to be SPSS system missing (not in codebook), treated as np.nan
df_clean['op_identity_qc_can'] = df['q18b'].map({
    '01': 'canadian',
    '02': 'canadian_first',
    '03': 'both_equally',
    '04': 'quebec_first',
    '05': 'quebec',
    '96': 'other',
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_identity_qc_can'] = {
    'original_variable': 'q18b',
    'question_label': "Les gens ont différentes façons de se définir. Diriez-vous que vous vous considérez...? / LIRE LES 5 CHOIX",
    'type': 'categorical',
    'value_labels': {
        'canadian': "uniquement comme Canadien(ne)",
        'canadian_first': "d'abord comme Canadien(ne), puis comme Québécois(e)",
        'both_equally': "également comme Canadien(ne) et comme Québécois(e)",
        'quebec_first': "d'abord comme Québécois(e), puis comme Canadien(ne)",
        'quebec': "uniquement comme Québécois(e)",
        'other': "autre (précisez)",
    },
}
