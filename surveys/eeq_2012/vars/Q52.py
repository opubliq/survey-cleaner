# op_party_support — Assumed party support based on frequency
# Source: Q52
# Assumption: Codes 8.0 and 9.0 are missing values as no labels were provided.
# TODO: Verify mapping for codes 1.0 and 2.0 against the actual codebook.
df_clean['op_party_support'] = df['Q52'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_party_support'] = {
    'original_variable': 'Q52',
    'question_label': "Assumed party support question",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B"},
}