# ses_region_code — Unknown region code
# Source: q59
# Assumption: Codes 96-99 are treated as missing due to lack of codebook.
# Assumption: Codes 01-05 mapped to generic placeholders.
df_clean['ses_region_code'] = df['q59'].map({
    '01': 'code_01',
    '02': 'code_02',
    '03': 'code_03',
    '04': 'code_04',
    '05': 'code_05',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['ses_region_code'] = {
    'original_variable': 'q59',
    'question_label': "Unknown - Based on exploration (q59)",
    'type': 'categorical',
    'value_labels': {'code_01': "Code 01", 'code_02': "Code 02", 'code_03': "Code 03", 'code_04': "Code 04", 'code_05': "Code 05"},
}