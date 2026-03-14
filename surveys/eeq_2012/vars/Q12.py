# op_parliament_importance — Importance of Parliament decisions
# Source: Q12
df_clean['op_parliament_importance'] = df['Q12'].map({
    1.0: 'very important',
    2.0: 'quite important',
    3.0: 'not very important',
    4.0: 'not at all important',
    8.0: "i don't know",
    9.0: 'prefer not to answer',
})
CODEBOOK_VARIABLES['op_parliament_importance'] = {
    'original_variable': 'Q12',
    'question_label': "And how important are the decisions made by the Parliament of Canada for you personally?",
    'type': 'categorical',
    'value_labels': {'very important': "Very important", 'quite important': "Quite important", 'not very important': "Not very important", 'not at all important': "Not at all important", "i don't know": "I don't know", 'prefer not to answer': "I prefer not to answer"},
}