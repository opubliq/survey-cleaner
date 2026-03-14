# op_vote_intention_2012 — Vote intention for the 2012 federal election
# Source: Q34A
# Assumption: Codes 1-4 are parties; 8 (Don't Know) and 9 (Refused) treated as missing.
df_clean['op_vote_intention_2012'] = df['Q34A'].map({
    1.0: 'bloc_quebecois',
    2.0: 'liberal',
    3.0: 'conservative',
    4.0: 'ndp',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention_2012'] = {
    'original_variable': 'Q34A',
    'question_label': "Si l'élection avait lieu dimanche prochain, quel parti voteriez-vous? (Inferred from context)",
    'type': 'categorical',
    'value_labels': {'bloc_quebecois': "Bloc Québécois (Inferred)", 'liberal': "Liberal Party (Inferred)", 'conservative': "Conservative Party (Inferred)", 'ndp': "NDP (Inferred)"},
}