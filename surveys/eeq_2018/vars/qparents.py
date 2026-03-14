# ses_parent_status — Parent status proxy
# Source: qparents
# Assumption: Inferred mapping based on variable name 'qparents' and observed codes 1.0, 2.0, 9.0.
# Assumption: Code 9.0 treated as missing (unlabelled in data exploration).
df_clean['ses_parent_status'] = df['qparents'].map({
    1.0: 'present',
    2.0: 'absent',
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_parent_status'] = {
    'original_variable': 'qparents',
    'question_label': "Inferred: Parent status/education category",
    'type': 'categorical',
    'value_labels': {'present': "Present/Category 1", 'absent': "Absent/Category 2"},
}
