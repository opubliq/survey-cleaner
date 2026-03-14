# ses_age — Age of respondent, grouped
# Source: age
# Assumption: Codes 1-5 represent 5 distinct age groups (18-29, 30-44, 45-59, 60-74, 75+ respectively), due to limited integer values observed.
df_clean['ses_age'] = df['age'].map({
    1.0: '18-29',
    2.0: '30-44',
    3.0: '45-59',
    4.0: '60-74',
    5.0: '75+',
})
CODEBOOK_VARIABLES['ses_age'] = {
    'original_variable': 'age',
    'question_label': "Age of respondent",
    'type': 'categorical',
    'value_labels': {'18-29': "18-29 years", '30-44': "30-44 years", '45-59': "45-59 years", '60-74': "60-74 years", '75+': "75+ years"},
}