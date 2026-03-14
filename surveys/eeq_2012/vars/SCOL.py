# ses_education — Level of schooling attainment
# Source: SCOL
# Assumption: Codes 1.0-12.0 map to increasing levels of education. Codes 98.0 and 99.0 are treated as missing.
df_clean['ses_education'] = df['SCOL'].map({
    1.0: 'primary_school',
    2.0: 'secondary_school_level_1',
    3.0: 'secondary_school_level_2',
    4.0: 'secondary_school_level_3',
    5.0: 'secondary_school_level_4',
    6.0: 'secondary_school_level_5',
    7.0: 'post_secondary_level_1',
    8.0: 'post_secondary_level_2',
    9.0: 'post_secondary_level_3',
    10.0: 'university_level_1',
    11.0: 'university_level_2',
    12.0: 'university_level_3_or_higher',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_education'] = {
    'original_variable': 'SCOL',
    'question_label': "Level of schooling attainment (Inferred)",
    'type': 'categorical',
    'value_labels': {'primary_school': "Primary School", 'secondary_school_level_1': "Secondary School Level 1", 'secondary_school_level_2': "Secondary School Level 2", 'secondary_school_level_3': "Secondary School Level 3", 'secondary_school_level_4': "Secondary School Level 4", 'secondary_school_level_5': "Secondary School Level 5", 'post_secondary_level_1': "Post-Secondary Level 1", 'post_secondary_level_2': "Post-Secondary Level 2", 'post_secondary_level_3': "Post-Secondary Level 3", 'university_level_1': "University Level 1", 'university_level_2': "University Level 2", 'university_level_3_or_higher': "University Level 3 or Higher"},
}