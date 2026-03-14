# behav_read_news_weekly_or_more — Frequency of reading newspapers (weekly or more)
# Source: Q70C
# Assumption: Data exploration failed, proceeding based on codebook entry values.
df_clean['behav_read_news_weekly_or_more'] = df['Q70C'].map({
    1.0: 1.0,
    2.0: 0.0,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_read_news_weekly_or_more'] = {
    'original_variable': 'Q70C',
    'question_label': "Fréquence de lecture des journaux (hebdomadaire ou plus)",
    'type': 'binary',
    'value_labels': {1.0: "Oui", 0.0: "Non"},
}