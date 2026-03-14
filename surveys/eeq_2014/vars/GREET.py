# ses_simple_binary — Inferred: Simple binary indicator
# Source: GREET
# Assumption: Only code 1.0 exists in data and is mapped to 1.0 (binary)
df_clean['ses_simple_binary'] = df['GREET'].map({
    1.0: 1.0,
})
CODEBOOK_VARIABLES['ses_simple_binary'] = {
    'original_variable': 'GREET',
    'question_label': "Inferred: Simple binary indicator (No codebook provided)",
    'type': 'binary',
    'value_labels': {'1.0': 'Observed value 1.0'},
}