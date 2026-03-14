# op_raw_pondx — Raw score/proportion for Party X
# Source: pondx
# Assumption: Numeric variable with no observed missing codes or scaling factor provided. Mapping observed values to themselves.
df_clean['op_raw_pondx'] = df['pondx'].map({
    0.055089: 0.055089,
    0.072570: 0.072570,
    0.073144: 0.073144,
    0.084384: 0.084384,
    0.090394: 0.090394,
})
CODEBOOK_VARIABLES['op_raw_pondx'] = {
    'original_variable': 'pondx',
    'question_label': "Raw proportion/score for Party X (Inferred)",
    'type': 'numeric',
    'value_labels': {},
}