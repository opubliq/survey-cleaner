# type_inferred — Inferred variable type (1 or 2)
# Source: type
# Note: No codebook entry provided. Codes 1.0 and 2.0 mapped to generic 'one'/'two'.
df_clean['type_inferred'] = df['type'].map({
    1.0: 'one',
    2.0: 'two',
})
CODEBOOK_VARIABLES['type_inferred'] = {
    'original_variable': 'type',
    'question_label': "Inferred type variable",
    'type': 'categorical',
    'value_labels': {'one': "Type One", 'two': "Type Two"},
}