# ses_date — Date of survey administration
# Source: SDAT
# WARNING: codebook_entry missing. Inferred type as 'numeric' from float64 dtype.
# Assumption: All values are valid, mapping is identity as no max value provided for scaling.
df_clean['ses_date'] = df['SDAT'].map({
    20140409.0: 20140409.0,
    20140410.0: 20140410.0,
    20140411.0: 20140411.0,
    20140412.0: 20140412.0,
    20140413.0: 20140413.0,
    20140414.0: 20140414.0,
    20140415.0: 20140415.0,
    20140416.0: 20140416.0,
    20140417.0: 20140417.0,
})
CODEBOOK_VARIABLES['ses_date'] = {
    'original_variable': 'SDAT',
    'question_label': "Date of survey administration (Inferred)",
    'type': 'numeric',
    'value_labels': {},
}