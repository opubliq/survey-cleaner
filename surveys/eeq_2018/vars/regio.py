# ses_region — Région de résidence (inferred)
# Source: regio
# Assumption: Codes 1, 2, 3 mapped to major Quebec regions based on context.
df_clean['ses_region'] = df['regio'].map({
    1.0: 'montreal',
    2.0: 'estrie',
    3.0: 'qccapital',
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'regio',
    'question_label': "Région de résidence (Inferred)",
    'type': 'categorical',
    'value_labels': {'montreal': "Montréal", 'estrie': "Estrie", 'qccapital': "Capitale-Nationale"},
}