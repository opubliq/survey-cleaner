# ses_weight — Survey weight variable
# Source: pond
# Assumption: Treating as numeric weight variable, normalized by maximum observed value (5.990714).
df_clean['ses_weight'] = df['pond'] / 5.990714
CODEBOOK_VARIABLES['ses_weight'] = {
    'original_variable': 'pond',
    'question_label': "Survey weight (inferred)",
    'type': 'numeric',
    'value_labels': {'normalized_range': 'Normalized to range [0, 1]'},
}