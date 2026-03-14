# ses_q62ad — Unspecified response code from Q62AD
# Source: Q62AD
# Assumption: Only code 96.0 found in data, treated as a unique category. All others are missing.
df_clean['ses_q62ad'] = df['Q62AD'].map({
    96.0: 'unspecified_response',
})
CODEBOOK_VARIABLES['ses_q62ad'] = {
    'original_variable': 'Q62AD',
    'question_label': "Q62AD - No codebook entry available, inferred from data exploration.",
    'type': 'categorical',
    'value_labels': {'unspecified_response': "Code 96 found in data"},
}
