# id_respondent — Questionnaire identifier / Numéro de questionnaire
# Source: quest
# Note: Sequential numeric ID (1-2175), stored as string in SPSS file
df_clean['id_respondent'] = pd.to_numeric(df['quest'], errors='coerce')
CODEBOOK_VARIABLES['id_respondent'] = {
    'original_variable': 'quest',
    'question_label': "Questionnaire identifier",
    'type': 'numeric',
    'value_labels': {},
}
