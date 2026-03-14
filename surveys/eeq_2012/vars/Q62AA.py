# behav_q62aa — Unknown variable, likely categorical/numeric with only code 96 observed
# Source: Q62AA
# WARNING: Codebook entry was missing. Mapping based only on data exploration (code 96.0 observed).
df_clean['behav_q62aa'] = df['Q62AA'].map({
    96.0: 'code_96',
    # Assumption: All other non-96 values are missing and will map to np.nan
})
CODEBOOK_VARIABLES['behav_q62aa'] = {
    'original_variable': 'Q62AA',
    'question_label': "Unknown (Missing Codebook)",
    'type': 'categorical',
    'value_labels': {'code_96': "Observed code 96"},
}
