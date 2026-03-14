# ses_sel2 — Binary indicator derived from SEL2
# Source: SEL2
# Assumption: Codes 1.0 and 2.0 represent a binary distinction, mapped to 0.0 and 1.0 respectively. Label unknown.
df_clean['ses_sel2'] = df['SEL2'].map({
    1.0: 0.0,
    2.0: 1.0,
})
CODEBOOK_VARIABLES['ses_sel2'] = {
    'original_variable': 'SEL2',
    'question_label': "Inferred binary variable from SEL2",
    'type': 'binary',
    'value_labels': {0.0: "Category 1 (was 1.0)", 1.0: "Category 2 (was 2.0)"},
}
