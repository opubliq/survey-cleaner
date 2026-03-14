# ses_id — Respondent identifier
# Source: respid
# Note: Since no codebook was provided, mapping observed float values directly to themselves to preserve IDs as numeric, following standard numeric variable procedure.
df_clean['ses_id'] = df['respid'].map({
    2.0: 2.0,
    5.0: 5.0,
    7.0: 7.0,
    10.0: 10.0,
    11.0: 11.0,
    18.0: 18.0,
    20.0: 20.0,
    28.0: 28.0,
    29.0: 29.0,
    35.0: 35.0,
    40.0: 40.0,
    44.0: 44.0,
    45.0: 45.0,
    46.0: 46.0,
    50.0: 50.0,
    52.0: 52.0,
    54.0: 54.0,
    63.0: 63.0,
    64.0: 64.0,
    65.0: 65.0,
    70.0: 70.0,
    71.0: 71.0,
    77.0: 77.0,
    81.0: 81.0,
    94.0: 94.0,
})
CODEBOOK_VARIABLES['ses_id'] = {
    'original_variable': 'respid',
    'question_label': "Respondent identifier (inferred)",
    'type': 'numeric',
    'value_labels': {},
}