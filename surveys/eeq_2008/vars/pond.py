# wgt_respondent — Respondent sampling weight
# Source: pond
# Note: Variable is a continuous numeric weight; no explicit transformation (divide by max) or code mapping was performed as max value is unknown and no missing codes were documented.
df_clean['wgt_respondent'] = df['pond']
CODEBOOK_VARIABLES['wgt_respondent'] = {
    'original_variable': 'pond',
    'question_label': "Respondent sampling weight",
    'type': 'numeric',
    'value_labels': {},
}