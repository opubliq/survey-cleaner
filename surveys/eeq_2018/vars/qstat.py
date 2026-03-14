# ses_status — Respondent's political status/leaning
# Source: qstat
# Assumption: Codes 1-6 map to a standard support scale. Code 98 is assumed missing as it's unlabelled.
df_clean['ses_status'] = df['qstat'].map({
    1.0: 'strong_supporter',
    2.0: 'supporter',
    3.0: 'slight_supporter',
    4.0: 'slight_opponent',
    5.0: 'opponent',
    6.0: 'strong_opponent',
    98.0: np.nan,
})
CODEBOOK_VARIABLES['ses_status'] = {
    'original_variable': 'qstat',
    'question_label': "Respondent's political status/leaning (Inferred)",
    'type': 'categorical',
    'value_labels': {'strong_supporter': "Strong Supporter", 'supporter': "Supporter", 'slight_supporter': "Slight Supporter", 'slight_opponent': "Slight Opponent", 'opponent': "Opponent", 'strong_opponent': "Strong Opponent"},
}