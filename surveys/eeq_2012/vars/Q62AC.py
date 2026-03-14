# op_province_code_outlier — Outlier province code from data that conflicts with codebook
# Source: Q62AC
# Assumption: Observed code 96.0 is treated as missing as it is not in the expected set {1, 2, 3} from codebook.
df_clean['op_province_code_outlier'] = df['Q62AC'].map({
    96.0: np.nan,
})
CODEBOOK_VARIABLES['op_province_code_outlier'] = {
    'original_variable': 'Q62AC',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {},
}