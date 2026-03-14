# op_political_efficacy — Political efficacy belief (government cares about people)
# Source: q21
# Note: Statement is negative ("I don't believe governments care..."), so scale is reversed
# 1 = strongly agree with negative statement → 0.0 (low efficacy)
# 4 = strongly disagree with negative statement → 1.0 (high efficacy)
df_clean['op_political_efficacy'] = df['q21'].map({
    '1': 0.0,
    '2': 0.33,
    '3': 0.67,
    '4': 1.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_political_efficacy'] = {
    'original_variable': 'q21',
    'question_label': "Je ne crois pas que les gouvernements se soucient beaucoup de ce que les gens comme moi pensent.",
    'type': 'likert',
    'value_labels': {0.0: 'strongly disagree (government cares)', 0.33: 'somewhat disagree', 0.67: 'somewhat agree', 1.0: 'strongly agree (government does not care)'},
}
