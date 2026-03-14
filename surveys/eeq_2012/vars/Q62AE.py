# op_q62ae — Follow-up on Q62 regarding provincial election (Quebec 2012)
# Source: Q62AE
# Assumption: No codebook provided. Code 96.0 is present in data but has no label.
# Assumption: Treating observed code 96.0 as missing due to high missing rate and lack of documentation.
df_clean['op_q62ae'] = df['Q62AE'].map({
    96.0: np.nan,
})
CODEBOOK_VARIABLES['op_q62ae'] = {
    'original_variable': 'Q62AE',
    'question_label': "Unknown follow-up question Q62AE",
    'type': 'categorical',
    'value_labels': {},
}