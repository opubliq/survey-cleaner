# ses_children — Has children (Yes/No/Refused)
# Source: qenfan
# Assumption: Codes 1/2 are Yes/No, Code 9 is Refused, Type is categorical.
df_clean['ses_children'] = df['qenfan'].map({
    1.0: 'yes',
    2.0: 'no',
    9.0: 'refused',
})
CODEBOOK_VARIABLES['ses_children'] = {
    'original_variable': 'qenfan',
    'question_label': "Variable related to having children (Inferred from values)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No", 'refused': "Refused"},
}