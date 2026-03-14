# op_vote_intention — Inferred vote intention
# Source: Q9
# Assumption: Based on common structure for Quebec election studies; 1-6 are party choices, 96/98/99 are missing codes.
df_clean['op_vote_intention'] = df['Q9'].map({
    1.0: 'pc',
    2.0: 'lib',
    3.0: 'pqc',
    4.0: 'caq',
    5.0: 'ops',
    6.0: 'none',
    96.0: 'refused',
    98.0: 'dont_know',
    99.0: 'missing',
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q9',
    'question_label': "Vote intention (Inferred from 1-6 codes)",
    'type': 'categorical',
    'value_labels': {'pc': "Parti Conservateur", 'lib': "Parti Libéral", 'pqc': "Parti Québécois", 'caq': "CAQ", 'ops': "Other party", 'none': "None", 'refused': "Refused", 'dont_know': "Don't know", 'missing': "Missing"},
}