
import pyreadstat
import json

sav_file = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2014/Quebec Election Study 2014.sav"
df, meta = pyreadstat.read_sav(sav_file)

output = {
    "column_names": meta.column_names,
    "column_labels": meta.column_labels,
    "variable_value_labels": meta.variable_value_labels
}

with open("/home/hubcad25/opubliq/repos/survey-cleaner/surveys/eeq_2014/sav_metadata.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print("SAV metadata extracted to sav_metadata.json")
