# ses_weight — Survey sampling weight, normalized
# Source: POND
# Assumption: Max observed value 0.580105 used for normalization.
df_clean['ses_weight'] = df['POND'] / 0.580105
CODEBOOK_VARIABLES['ses_weight'] = {
    'original_variable': 'POND',
    'question_label': "Survey sampling weight (normalized 0-1)",
    'type': 'numeric',
    'value_labels': {'0.0_to_1.0': "Normalized sampling weight (0.0 to 1.0)"},
}