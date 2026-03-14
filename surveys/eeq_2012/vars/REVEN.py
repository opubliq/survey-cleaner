# ses_income — Household income before taxes for 2011
# Source: REVEN
# Note: Step 1 failed due to missing data file, mapping based solely on codebook.
df_clean['ses_income'] = df['REVEN'].map({
    1.0: 'less than 8k',
    2.0: '8k to 15.9k',
    3.0: '16k to 23.9k',
    4.0: '24k to 39.9k',
    5.0: '40k to 55.9k',
    6.0: '56k to 71.9k',
    7.0: '72k to 87.9k',
    8.0: '88k to 103.9k',
    9.0: '104k or more',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_income'] = {
    'original_variable': 'REVEN',
    'question_label': "And now your total household income before taxes for 2011.  That includes income from all sources such as savings, pensions, rent, as well as wages.   Was it:",
    'type': 'categorical',
    'value_labels': {'less than 8k': 'Less than $8,000', '8k to 15.9k': '$8000 - $15,999', '16k to 23.9k': '$16,000 - $23,999', '24k to 39.9k': '$24,000 - $39,999', '40k to 55.9k': '$40,000 - $55,999', '56k to 71.9k': '$56,000 - $71,999', '72k to 87.9k': '$72,000 - $87,999', '88k to 103.9k': '$88,000 -  $103,999', '104k or more': '$104,000 or more'},
}
