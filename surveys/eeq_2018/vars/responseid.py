# id_response — Response Identifier
# Source: responseid
# Note: As this is an ID, it is passed through using an identity map based on observed values.
df_clean['id_response'] = df['responseid'].map({
    3.0: 3.0,
    4.0: 4.0,
    5.0: 5.0,
    6.0: 6.0,
    7.0: 7.0,
    8.0: 8.0,
    9.0: 9.0,
    10.0: 10.0,
    11.0: 11.0,
    12.0: 12.0,
    13.0: 13.0,
    14.0: 14.0,
    15.0: 15.0,
    16.0: 16.0,
    17.0: 17.0,
    18.0: 18.0,
    19.0: 19.0,
    20.0: 20.0,
    21.0: 21.0,
    22.0: 22.0,
    23.0: 23.0,
    24.0: 24.0,
    25.0: 25.0,
    26.0: 26.0,
    27.0: 27.0,
})
CODEBOOK_VARIABLES['id_response'] = {
    'original_variable': 'responseid',
    'question_label': "Response Identifier",
    'type': 'numeric',
    'value_labels': {},
}