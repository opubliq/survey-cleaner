# ses_code — Classification code
# Source: CODE1
# Assumption: No codebook provided; codes G, H, J interpreted as distinct groups, '9' as a category.
df_clean['ses_code'] = df['CODE1'].map({
    '9': 'nine',
    'G': 'group_g',
    'H': 'group_h',
    'J': 'group_j',
})
CODEBOOK_VARIABLES['ses_code'] = {
    'original_variable': 'CODE1',
    'question_label': "Classification code (No label available)",
    'type': 'categorical',
    'value_labels': {'nine': "Code 9", 'group_g': "Group G", 'group_h': "Group H", 'group_j': "Group J"},
}
