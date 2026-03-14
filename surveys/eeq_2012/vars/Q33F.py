# op_party_chance_fed_imp — Importance of party's chance of forming government in federal election
# Source: Q33F
# Note: Mapped 1-4 scale to 0.0-1.0 (Likert). Codes 8/9 treated as missing.
df_clean['op_party_chance_fed_imp'] = df['Q33F'].map({
    1.0: 0.0,
    2.0: 1/3,
    3.0: 2/3,
    4.0: 1.0,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_party_chance_fed_imp'] = {
    'original_variable': 'Q33F',
    'question_label': "When you cast your ballot in Canadian federal elections, how important are each of the following when you make your voting choice? (4 = very important, 3 = fairly important, 2 = not very important, 1 = not at all important) / The party's chances of forming government",
    'type': 'likert',
    'value_labels': {'0.0': "Not at all important (1)", '0.3333333333333333': "2", '0.6666666666666666': "3", '1.0': "Very important (4)"},
}