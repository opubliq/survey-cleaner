# op_q73g — Opinion on statement Q73G
# Source: Q73G
# Assumption: No codebook provided; assuming 1-4 scale + 8/9 for missing/refused. Type is categorical.
df_clean['op_q73g'] = df['Q73G'].map({
    1.0: 'strongly disagree',
    2.0: 'disagree',
    3.0: 'agree',
    4.0: 'strongly agree',
    8.0: "don't know",
    9.0: 'refused',
})
CODEBOOK_VARIABLES['op_q73g'] = {
    'original_variable': 'Q73G',
    'question_label': "Opinion on statement Q73G (Codebook entry missing)",
    'type': 'categorical',
    'value_labels': {'strongly disagree': "1", 'disagree': "2", 'agree': "3", 'strongly agree': "4", "don't know": "8", 'refused': "9"},
}
