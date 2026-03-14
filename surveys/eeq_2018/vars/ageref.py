# ses_age_ref — Age Reference Group (Inferred)
# Source: ageref
# Assumption: Only code 0.0 exists and represents the reference group. Unmapped values become NaN.
df_clean['ses_age_ref'] = df['ageref'].map({
    0.0: 'reference',
})
CODEBOOK_VARIABLES['ses_age_ref'] = {
    'original_variable': 'ageref',
    'question_label': "Reference age category (Inferred from data)",
    'type': 'categorical',
    'value_labels': {'reference': "Reference Group (Inferred)"},
}
