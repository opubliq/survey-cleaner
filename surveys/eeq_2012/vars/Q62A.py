# behav_q62a — Response to question 62A
# Source: Q62A
# Assumption: Codes 6, 8, 9 are unlabelled and treated as missing (np.nan)
df_clean['behav_q62a'] = df['Q62A'].map({
    1.0: 'yes',
    2.0: 'no',
    6.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q62a'] = {
    'original_variable': 'Q62A',
    'question_label': "Response to question 62A (Unlabelled)",
    'type': 'categorical',
    'value_labels': {'yes': "1.0 (Yes)", 'no': "2.0 (No)"},
}