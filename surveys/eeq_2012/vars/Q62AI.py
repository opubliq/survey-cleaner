# behav_q62ai — Observed response
# Source: Q62AI
# Assumption: Only code 96.0 observed, treated as a single response category. All others are missing.
df_clean['behav_q62ai'] = df['Q62AI'].map({
    96.0: 'response',
})
CODEBOOK_VARIABLES['behav_q62ai'] = {
    'original_variable': 'Q62AI',
    'question_label': "Response to Q62AI",
    'type': 'categorical',
    'value_labels': {'response': 'Observed Response'},
}