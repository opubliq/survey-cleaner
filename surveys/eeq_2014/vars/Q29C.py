# behav_transit_frequency — Frequency of using public transit in your area (Inferred: No codebook provided)
# Source: Q29C
# Assumption: Codes are categorical/ordinal frequencies; mapping float keys to string labels derived from the code itself.
df_clean['behav_transit_frequency'] = df['Q29C'].map({
    0.0: 'freq_0_none',
    1.0: 'freq_1_rare',
    2.0: 'freq_2_low',
    3.0: 'freq_3_medium',
    4.0: 'freq_4_high',
    5.0: 'freq_5',
    6.0: 'freq_6',
    7.0: 'freq_7',
    8.0: 'freq_8',
    9.0: 'freq_9',
    10.0: 'freq_10',
    11.0: 'freq_11',
    12.0: 'freq_12',
    15.0: 'freq_15',
    20.0: 'freq_20',
    22.0: 'freq_22',
    24.0: 'freq_24',
    25.0: 'freq_25',
    30.0: 'freq_30',
    31.0: 'freq_31',
    35.0: 'freq_35',
    36.0: 'freq_36',
    40.0: 'freq_40',
    44.0: 'freq_44',
    45.0: 'freq_45',
})
CODEBOOK_VARIABLES['behav_transit_frequency'] = {
    'original_variable': 'Q29C',
    'question_label': "Frequency of using public transit in your area (Inferred)",
    'type': 'categorical',
    'value_labels': {'freq_0_none': "Code 0 (None)", 'freq_1_rare': "Code 1 (Rarely)", 'freq_2_low': "Code 2 (Low)", 'freq_3_medium': "Code 3 (Medium)", 'freq_4_high': "Code 4 (High)", 'freq_5': "Code 5", 'freq_6': "Code 6", 'freq_7': "Code 7", 'freq_8': "Code 8", 'freq_9': "Code 9", 'freq_10': "Code 10", 'freq_11': "Code 11", 'freq_12': "Code 12", 'freq_15': "Code 15", 'freq_20': "Code 20", 'freq_22': "Code 22", 'freq_24': "Code 24", 'freq_25': "Code 25", 'freq_30': "Code 30", 'freq_31': "Code 31", 'freq_35': "Code 35", 'freq_36': "Code 36", 'freq_40': "Code 40", 'freq_44': "Code 44", 'freq_45': "Code 45"},
}