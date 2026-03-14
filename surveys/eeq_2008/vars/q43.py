# op_q43_inferred — Inferred categorical variable from q43
# Source: q43
# Assumption: No labels provided; mapping floats to lowecase string versions of themselves as placeholder labels.
# Missing codes are np.nan (817 explicit NAs + any unmapped values).
df_clean['op_q43_inferred'] = df['q43'].map({
    0.0: 'zero',
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    5.0: 'five',
    7.0: 'seven',
    10.0: 'ten',
    12.0: 'twelve',
    15.0: 'fifteen',
    20.0: 'twenty',
    24.0: 'twenty_four',
    25.0: 'twenty_five',
    30.0: 'thirty',
    35.0: 'thirty_five',
    40.0: 'forty',
    45.0: 'forty_five',
    50.0: 'fifty',
    55.0: 'fifty_five',
    60.0: 'sixty',
    65.0: 'sixty_five',
    70.0: 'seventy',
    75.0: 'seventy_five',
    80.0: 'eighty',
    85.0: 'eighty_five',
    90.0: 'ninety',
})
CODEBOOK_VARIABLES['op_q43_inferred'] = {
    'original_variable': 'q43',
    'question_label': "Inferred categorical response for Q43 (No original label)",
    'type': 'categorical',
    'value_labels': {'zero': "0.0", 'one': "1.0", 'two': "2.0", 'three': "3.0", 'five': "5.0", 'seven': "7.0", 'ten': "10.0", 'twelve': "12.0", 'fifteen': "15.0", 'twenty': "20.0", 'twenty_four': "24.0", 'twenty_five': "25.0", 'thirty': "30.0", 'thirty_five': "35.0", 'forty': "40.0", 'forty_five': "45.0", 'fifty': "50.0", 'fifty_five': "55.0", 'sixty': "60.0", 'sixty_five': "65.0", 'seventy': "70.0", 'seventy_five': "75.0", 'eighty': "80.0", 'eighty_five': "85.0", 'ninety': "90.0"},
}