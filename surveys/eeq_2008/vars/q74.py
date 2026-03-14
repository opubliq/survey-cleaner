# op_q74 — Likert scale response
# Source: q74
# Assumption: Codes 96 (Don't know/Refused) and 98 (Refused) are treated as missing (np.nan), as they are not explicitly defined in a provided codebook.
df_clean['op_q74'] = df['q74'].map({
    1.0: 'strong_agree',
    2.0: 'agree',
    3.0: 'neutral',
    4.0: 'disagree',
    5.0: 'strong_disagree',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q74'] = {
    'original_variable': 'q74',
    'question_label': "Likert scale response (Based on values 1-5)",
    'type': 'categorical',
    'value_labels': {'strong_agree': "Strongly Agree", 'agree': "Agree", 'neutral': "Neutral", 'disagree': "Disagree", 'strong_disagree': "Strongly Disagree"},
}