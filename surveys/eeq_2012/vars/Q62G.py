# ses_q62g — Unknown categorical variable from Q62G
# Source: Q62G
# Note: Codebook entry was missing, mapping is inferred based on value counts present in data.
# Assumption: Codes 6.0, 8.0, and 9.0 are treated as missing (unlabelled/refused).
df_clean['ses_q62g'] = df['Q62G'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    6.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_q62g'] = {
    'original_variable': 'Q62G',
    'question_label': "Unknown category question (based on Q62G)",
    'type': 'categorical',
    'value_labels': {'option_one': "Category 1", 'option_two': "Category 2"},
}