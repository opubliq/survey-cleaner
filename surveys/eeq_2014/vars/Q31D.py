# behav_q31d — Specific survey item Q31D (Likelihood scale)
# Source: Q31D
# Assumption: Codes 0.0-10.0 are a scale, 98.0/99.0 are missing (unlabelled in codebook)
df_clean['behav_q31d'] = df['Q31D'].map({
    0.0: 'not at all likely',
    1.0: 'unlikely_1',
    2.0: 'unlikely_2',
    3.0: 'unlikely_3',
    4.0: 'unlikely_4',
    5.0: 'neutral',
    6.0: 'likely_6',
    7.0: 'likely_7',
    8.0: 'likely_8',
    9.0: 'likely_9',
    10.0: 'very likely',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q31d'] = {
    'original_variable': 'Q31D',
    'question_label': "Likelihood item Q31D (0-10 scale)",
    'type': 'categorical',
    'value_labels': {'not at all likely': "Not at all likely", 'unlikely_1': "Unlikely 1", 'unlikely_2': "Unlikely 2", 'unlikely_3': "Unlikely 3", 'unlikely_4': "Unlikely 4", 'neutral': "Neutral", 'likely_6': "Likely 6", 'likely_7': "Likely 7", 'likely_8': "Likely 8", 'likely_9': "Likely 9", 'very likely': "Very likely"},
}