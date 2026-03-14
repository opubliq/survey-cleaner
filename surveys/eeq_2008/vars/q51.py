# ses_voting_intention — Placeholder for voting intention (no codebook provided)
# Source: q51
# Assumption: Codes 8.0 and 9.0 treated as missing (unlabelled in data exploration)
df_clean['ses_voting_intention'] = df['q51'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'other',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_voting_intention'] = {
    'original_variable': 'q51',
    'question_label': "Placeholder for Q51 (No label found)",
    'type': 'categorical',
    'value_labels': {'quebec': "Category 1", 'ontario': "Category 2", 'alberta': "Category 3", 'other': "Category 4"},
}