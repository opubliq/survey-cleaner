# op_voter_intention — Assumed voter intention based on data codes
# Source: q37
# Assumption: Missing codebook. Codes '1','2','3' mapped to provincial labels (1=QC, 2=ON, 3=AB). Code '4' is 'other'. Codes '8', '9' treated as missing (unlabelled).
df_clean['op_voter_intention'] = df['q37'].map({
    '1': 'quebec',
    '2': 'ontario',
    '3': 'alberta',
    '4': 'other',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_voter_intention'] = {
    'original_variable': 'q37',
    'question_label': "Unknown: Assumed voter intention based on data codes",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'other': "Other/Unlabelled Response"},
}