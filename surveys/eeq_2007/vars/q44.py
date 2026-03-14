# op_q44 — Unlabeled question from Q44
# Source: q44
# Assumption: variable has no explicit codebook entry; inferred as categorical based on data.
# Assumption: codes 98 and 99 treated as missing (unlabelled in data exploration).
df_clean['op_q44'] = df['q44'].map({
    '01': 'code_01',
    '02': 'code_02',
    '03': 'code_03',
    '04': 'code_04',
    '05': 'code_05',
    '06': 'code_06',
    '07': 'code_07',
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_q44'] = {
    'original_variable': 'q44',
    'question_label': "Unlabeled question from Q44",
    'type': 'categorical',
    'value_labels': {'code_01': "Code 01", 'code_02': "Code 02", 'code_03': "Code 03", 'code_04': "Code 04", 'code_05': "Code 05", 'code_06': "Code 06", 'code_07': "Code 07"},
}