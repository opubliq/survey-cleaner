# ses_region — Inferred region/riding code
# Source: QUEST
# Assumption: Variable is categorical based on integer codes 1003-1031, treated as distinct regions since codebook is missing.
df_clean['ses_region'] = df['QUEST'].map({
    1003.0: 'code_1003', 1004.0: 'code_1004', 1005.0: 'code_1005', 1006.0: 'code_1006', 1007.0: 'code_1007', 
    1008.0: 'code_1008', 1009.0: 'code_1009', 1010.0: 'code_1010', 1011.0: 'code_1011', 1012.0: 'code_1012', 
    1013.0: 'code_1013', 1016.0: 'code_1016', 1017.0: 'code_1017', 1018.0: 'code_1018', 1019.0: 'code_1019', 
    1020.0: 'code_1020', 1021.0: 'code_1021', 1023.0: 'code_1023', 1024.0: 'code_1024', 1026.0: 'code_1026', 
    1027.0: 'code_1027', 1028.0: 'code_1028', 1029.0: 'code_1029', 1030.0: 'code_1030', 1031.0: 'code_1031',
})
CODEBOOK_VARIABLES['ses_region'] = {
    'original_variable': 'QUEST',
    'question_label': "Inferred region/riding code from QUEST",
    'type': 'categorical',
    'value_labels': {'code_1003': 'Code 1003', 'code_1004': 'Code 1004', 'code_1005': 'Code 1005', 'code_1006': 'Code 1006', 'code_1007': 'Code 1007', 'code_1008': 'Code 1008', 'code_1009': 'Code 1009', 'code_1010': 'Code 1010', 'code_1011': 'Code 1011', 'code_1012': 'Code 1012', 'code_1013': 'Code 1013', 'code_1016': 'Code 1016', 'code_1017': 'Code 1017', 'code_1018': 'Code 1018', 'code_1019': 'Code 1019', 'code_1020': 'Code 1020', 'code_1021': 'Code 1021', 'code_1023': 'Code 1023', 'code_1024': 'Code 1024', 'code_1026': 'Code 1026', 'code_1027': 'Code 1027', 'code_1028': 'Code 1028', 'code_1029': 'Code 1029', 'code_1030': 'Code 1030', 'code_1031': 'Code 1031'},
}