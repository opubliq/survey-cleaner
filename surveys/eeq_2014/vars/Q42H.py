# ses_q42h — Q42H from eeq_2014, type inferred from data exploration
# Source: Q42H
# Assumption: Codes 96.0, 98.0, 99.0 treated as missing (not explicitly documented)
df_clean['ses_q42h'] = df['Q42H'].map({
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    4.0: 'four',
    5.0: 'five',
    6.0: 'six',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_q42h'] = {
    'original_variable': 'Q42H',
    'question_label': "Q42H (Label unknown, inferred from data)",
    'type': 'categorical',
    'value_labels': {'one': "1 (Inferred)", 'two': "2 (Inferred)", 'three': "3 (Inferred)", 'four': "4 (Inferred)", 'five': "5 (Inferred)", 'six': "6 (Inferred)"},
}