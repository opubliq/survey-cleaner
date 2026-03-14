# ses_political_proxy — Proxy for political response/vote choice (Assumed mapping due to missing codebook)
# Source: q71
# Assumption: Codes 8.0 and 9.0 treated as missing (unlabelled in provided context)
df_clean['ses_political_proxy'] = df['q71'].map({
    1.0: 'response_a',
    2.0: 'response_b',
    3.0: 'response_c',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_political_proxy'] = {
    'original_variable': 'q71',
    'question_label': "Unknown: Political response proxy based on data exploration",
    'type': 'categorical',
    'value_labels': {'response_a': "Response A", 'response_b': "Response B", 'response_c': "Response C"},
}