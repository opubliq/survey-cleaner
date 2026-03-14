# op_q61d — Opinion/Attitude question from Q61 (Mapping based on observed codes as codebook was missing)
# Source: q61d
# Assumption: Codes 01-05 are distinct categories; 96=Don't Know; 97=Refused; 98=No Answer; 99=Missing
df_clean['op_q61d'] = df['q61d'].map({
    '01': 'response_01',
    '02': 'response_02',
    '03': 'response_03',
    '04': 'response_04',
    '05': 'response_05',
    '96': 'dont_know',
    '97': 'refused',
    '98': 'no_answer',
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_q61d'] = {
    'original_variable': 'q61d',
    'question_label': "Opinion/Attitude question from Q61 (Codebook missing, mapping inferred)",
    'type': 'categorical',
    'value_labels': {'response_01': "Response Category 01", 'response_02': "Response Category 02", 'response_03': "Response Category 03", 'response_04': "Response Category 04", 'response_05': "Response Category 05", 'dont_know': "Don't Know", 'refused': "Refused to Answer", 'no_answer': "No Answer Recorded"},
}
