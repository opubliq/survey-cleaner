# op_support_party — Support for main political parties
# Source: q62
# Assumption: Codes 01-05 are valid parties, codes 96-99 are treated as missing (unlabelled in codebook)
df_clean['op_support_party'] = df['q62'].map({
    '01': 'party_a',
    '02': 'party_b',
    '03': 'party_c',
    '04': 'party_d',
    '05': 'party_e',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_support_party'] = {
    'original_variable': 'q62',
    'question_label': "Support for main political parties (Inferred)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A (01)", 'party_b': "Party B (02)", 'party_c': "Party C (03)", 'party_d': "Party D (04)", 'party_e': "Party E (05)"},
}