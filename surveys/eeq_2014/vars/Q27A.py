# op_choice_party — Vote intention/Preferred party
# Source: Q27A
# Assumption: Codes 1-4 are mapped to specific parties. Codes 8 and 9 are treated as missing.
df_clean['op_choice_party'] = df['Q27A'].map({
    1.0: 'caq',
    2.0: 'liberal',
    3.0: 'pqc',
    4.0: 'conservateur',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_choice_party'] = {
    'original_variable': 'Q27A',
    'question_label': "Preferred political party (Inferred)",
    'type': 'categorical',
    'value_labels': {'caq': "CAQ", 'liberal': "Liberal", 'pqc': "PQC", 'conservateur': "Conservative"},
}