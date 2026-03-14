# ses_age_month — Month of birth/response (inferred)
# Source: agemonth_1
# Note: No codebook provided. Assumed codes 1-12 map to months January-December.
# Assumption: Codes 1.0 through 12.0 are valid months. All unmapped values (including NaN) become np.nan.
df_clean['ses_age_month'] = df['agemonth_1'].map({
    1.0: 'january',
    2.0: 'february',
    3.0: 'march',
    4.0: 'april',
    5.0: 'may',
    6.0: 'june',
    7.0: 'july',
    8.0: 'august',
    9.0: 'september',
    10.0: 'october',
    11.0: 'november',
    12.0: 'december',
})
CODEBOOK_VARIABLES['ses_age_month'] = {
    'original_variable': 'agemonth_1',
    'question_label': "Month of Age (Inferred)",
    'type': 'categorical',
    'value_labels': {'january': "January", 'february': "February", 'march': "March", 'april': "April", 'may': "May", 'june': "June", 'july': "July", 'august': "August", 'september': "September", 'october': "October", 'november': "November", 'december': "December"},
}