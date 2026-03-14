# op_attitude_q14a — Inferred 5-point attitude scale for Q14A
# Source: Q14A
# Assumption: Codes 8.0 and 9.0 treated as missing (not in provided codebook)
df_clean['op_attitude_q14a'] = df['Q14A'].map({
    1.0: 'strongly_disagree',
    2.0: 'disagree',
    3.0: 'neither',
    4.0: 'agree',
    5.0: 'strongly_agree',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q14a'] = {
    'original_variable': 'Q14A',
    'question_label': "Province de résidence (Inferred from context)",
    'type': 'categorical',
    'value_labels': {'strongly_disagree': "Strongly Disagree", 'disagree': "Disagree", 'neither': "Neither Agree nor Disagree", 'agree': "Agree", 'strongly_agree': "Strongly Agree"},
}