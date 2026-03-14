# behav_disposition — Unspecified response category, likely "Did not answer" or similar
# Source: Q62AF
# Assumption: No codebook provided. Code 96.0 is the only observed non-missing value. Mapped to an uninformative label due to lack of context.
df_clean['behav_disposition'] = df['Q62AF'].map({
    96.0: 'unspecified_response',
})
CODEBOOK_VARIABLES['behav_disposition'] = {
    'original_variable': 'Q62AF',
    'question_label': "Q62AF (No codebook provided)",
    'type': 'categorical',
    'value_labels': {'unspecified_response': "Unspecified Code 96.0"},
}