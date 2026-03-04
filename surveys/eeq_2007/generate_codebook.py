#!/usr/bin/env python3
"""
Generate codebook.json from eeq_2007 SPSS file
"""
import json
import pyreadstat

# Paths
SAV_FILE = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2007/Quebec Election Study 2007 (SPSS).sav"
OUTPUT_FILE = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2007/codebook.json"

# Read SPSS file
df, meta = pyreadstat.read_sav(SAV_FILE)

# Get value labels from metadata
value_labels = meta.variable_value_labels

# Get variable types
var_types = meta.readstat_variable_types

# Function to determine variable type
def get_var_type(var_name):
    """Determine if variable is categorical, ordinal, continuous, or text"""
    # Check if variable has value labels
    if var_name in value_labels and value_labels[var_name]:
        # Check if it has numeric codes (indicating categorical/ordinal)
        labels = value_labels[var_name]
        # If all keys are numeric, it's likely categorical/ordinal
        numeric_keys = all(
            (isinstance(k, (int, float))) or 
            (isinstance(k, str) and k.lstrip('-').isdigit())
            for k in labels.keys()
        )
        if numeric_keys:
            return "categorical"
        else:
            return "text"
    
    # Check if variable is numeric (continuous)
    if var_name in var_types:
        if var_types[var_name] in ('double', 'float', 'int', 'integer'):
            # Check if it has few unique values (could be ordinal)
            unique_vals = df[var_name].dropna().unique()
            if len(unique_vals) <= 20:
                return "ordinal"
            return "continuous"
    
    return "text"

# Build codebook
codebook = {
    "survey_id": "eeq_2007",
    "variables": {}
}

for var_name in meta.column_names:
    # Get question text
    question = meta.column_labels[meta.column_names.index(var_name)] if meta.column_labels else ""
    
    # Skip variables with no question text
    if not question or question.strip() == "":
        continue
    
    # Get value labels
    values = {}
    if var_name in value_labels:
        raw_values = value_labels[var_name]
        for k, v in raw_values.items():
            # Convert keys to strings
            if isinstance(k, float):
                if k == int(k):
                    key = str(int(k))
                else:
                    key = str(int(k))  # Handle float codes like 995.0 -> "995"
            else:
                key = str(k)
            values[key] = v
    
    # Determine type
    var_type = get_var_type(var_name)
    
    # Build variable entry
    var_entry = {
        "question": question.strip(),
        "type": var_type,
        "values": values,
    }
    
    # Add missing if applicable (based on value labels that indicate missing)
    missing = []
    if values:
        # Common missing value codes in this survey: 98, 99, 997, 998, 999
        for key in values.keys():
            if key in ('98', '99', '997', '998', '999', '995', '996'):
                missing.append(key)
        if missing:
            var_entry["missing"] = missing
    
    # Add to codebook
    codebook["variables"][var_name] = var_entry

# Write codebook.json
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(codebook, f, indent=2, ensure_ascii=False)

print(f"codebook.json written: {OUTPUT_FILE}")
print(f"Variables: {len(codebook['variables'])}")
