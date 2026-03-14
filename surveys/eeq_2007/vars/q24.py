# op_gov_waste — Perception of government waste of tax money
# Source: q24
# No codebook_entry provided in task; values derived from codebook.json
# Question: "Pensez-vous que les gens au gouvernement gaspillent BEAUCOUP, QUELQUE PEU ou PAS BEAUCOUP nos taxes ?"
df_clean['op_gov_waste'] = df['q24'].map({
    '1': 'waste_much',
    '2': 'waste_some',
    '3': 'waste_little',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_gov_waste'] = {
    'original_variable': 'q24',
    'question_label': "Pensez-vous que les gens au gouvernement gaspillent BEAUCOUP, QUELQUE PEU ou PAS BEAUCOUP nos taxes ?",
    'type': 'categorical',
    'value_labels': {'waste_much': "Gaspillent beaucoup de nos taxes", 'waste_some': "En gaspillent quelque peu", 'waste_little': "N'en gaspillent pas beaucoup"},
}
