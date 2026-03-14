# ses_self_rating — Inferred self-rating scale, 2 categories
# Source: SEL4
# Assumption: Codes 1.0 and 2.0 map to placeholder labels as no codebook was provided.
df_clean['ses_self_rating'] = df['SEL4'].map({
    1.0: 'option_a',
    2.0: 'option_b',
})
CODEBOOK_VARIABLES['ses_self_rating'] = {
    'original_variable': 'SEL4',
    'question_label': "Inferred self-rating scale category (1.0/2.0)",
    'type': 'categorical',
    'value_labels': {'option_a': "Option A", 'option_b': "Option B"},
}