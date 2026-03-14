# ses_occupation — Occupation principale
# Source: OCCUP
# Assumption: codes 96 and 99 treated as missing (unlabelled in codebook)
df_clean['ses_occupation'] = df['OCCUP'].map({
    1.0: 'employed_full_time',
    2.0: 'employed_part_time',
    3.0: 'self_employed',
    4.0: 'unemployed',
    5.0: 'student',
    6.0: 'retired',
    7.0: 'homemaker',
    8.0: 'not_in_labour_force',
    9.0: 'employed_other',
    10.0: 'other_unspecified',
    11.0: 'not_stated_or_refused',
    96.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_occupation'] = {
    'original_variable': 'OCCUP',
    'question_label': "Occupation principale",
    'type': 'categorical',
    'value_labels': {'employed_full_time': "Employed (Full-Time)", 'employed_part_time': "Employed (Part-Time)", 'self_employed': "Self-Employed", 'unemployed': "Unemployed", 'student': "Student", 'retired': "Retired", 'homemaker': "Homemaker", 'not_in_labour_force': "Not in Labour Force", 'employed_other': "Employed (Other)", 'other_unspecified': "Other/Unspecified", 'not_stated_or_refused': "Not Stated/Refused"},
}