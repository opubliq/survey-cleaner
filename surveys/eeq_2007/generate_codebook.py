#!/usr/bin/env python3
"""
Generate codebook.json for eeq_2007 survey from SPSS file.
"""

import json
import subprocess
import os
import re

# Survey configuration
SURVEY_ID = "eeq_2007"
SHARED_FOLDER = "/home/hubcad25/Dropbox/_SharedFolder_data_produit/eeq_2007"
SAV_FILE = os.path.join(SHARED_FOLDER, "Quebec Election Study 2007 (SPSS).sav")
OUTPUT_FILE = os.path.join(SHARED_FOLDER, "codebook.json")

def get_variable_info():
    """Extract variable labels and value labels from SPSS file using R."""
    
    r_script = '''
library(haven)
library(jsonlite)

sav_path <- "{sav_path}"
df <- haven::read_sav(sav_path)

# Get all variable info
var_info <- list()

for (var_name in names(df)) {{
    attrs <- attributes(df[[var_name]])
    
    # Get variable label (question text)
    label <- attrs$label
    if (is.null(label)) {{
        label <- NA
    }}
    
    # Get value labels
    value_labels <- attrs$labels
    if (is.null(value_labels)) {{
        value_labels <- NA
    }} else {{
        # Convert to named list
        value_labels <- as.list(value_labels)
    }}
    
    # Get class to determine type
    var_class <- class(df[[var_name]])[1]
    
    var_info[[var_name]] <- list(
        label = label,
        value_labels = value_labels,
        class = var_class
    )
}}

# Output as JSON
writeLines(toJSON(var_info, auto_unbox = TRUE, na = "null"))
'''.format(sav_path=SAV_FILE)
    
    result = subprocess.run(
        ["Rscript", "-e", r_script],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        print(f"R error: {result.stderr}")
        raise Exception("Failed to extract variable info from SPSS file")
    
    return json.loads(result.stdout)


def determine_type(var_class, value_labels, var_name):
    """Determine the variable type."""
    if var_class == "character":
        return "text"
    
    # Check if it's numeric (continuous)
    if var_class == "numeric" or var_class == "double":
        return "continuous"
    
    # For labelled variables, check if it has many unique values (continuous-like)
    if isinstance(value_labels, dict) and value_labels:
        num_values = len(value_labels)
        # If more than 30 values, treat as continuous
        if num_values > 30:
            return "continuous"
    
    # For Likert scales and similar, it's ordinal
    ordinal_patterns = ['agree', 'désaccord', 'important', 'satisfait', 'proche', 'échelle']
    if isinstance(value_labels, dict):
        labels_str = ' '.join(str(v).lower() for v in value_labels.values())
        for pattern in ordinal_patterns:
            if pattern in labels_str.lower():
                return "ordinal"
    
    return "categorical"


def format_value_labels(value_labels, var_name):
    """Format value labels for codebook.json.
    
    In R, the named list has labels as names and codes as values.
    We need to swap them so codes are keys and labels are values.
    """
    if not value_labels or value_labels == "NA" or value_labels is None:
        return {}
    
    if isinstance(value_labels, dict):
        result = {}
        for label, code in value_labels.items():
            # The label is the key, code is the value in R's named list
            # We need to swap: code becomes key, label becomes value
            code_str = str(code).strip('"').strip("'")
            label_str = str(label).strip()
            result[code_str] = label_str
        return result
    
    return {}


def main():
    print(f"Generating codebook for {SURVEY_ID}...")
    
    # Get variable information from SPSS file
    var_info = get_variable_info()
    
    # Build codebook structure
    codebook = {
        "survey_id": SURVEY_ID,
        "variables": {}
    }
    
    for var_name, info in var_info.items():
        label = info.get("label")
        
        # Skip variables without question text (except those with value labels)
        if label is None or (isinstance(label, float) and str(label) == 'nan'):
            # Check if it has value labels anyway
            if not isinstance(info.get("value_labels"), dict):
                continue
            label = f"[Variable: {var_name}]"
        
        value_labels = info.get("value_labels")
        var_class = info.get("class", "haven_labelled")
        
        # Determine variable type
        var_type = determine_type(var_class, value_labels, var_name)
        
        # Format value labels
        formatted_labels = format_value_labels(value_labels, var_name)
        
        # Determine missing values based on common patterns in labels
        # (now values in the dictionary, keys are codes)
        missing_values = []
        if formatted_labels:
            for code, val_label in formatted_labels.items():
                label_lower = str(val_label).lower()
                if 'ne sais pas' in label_lower or 'nsp' in label_lower or 'refus' in label_lower:
                    if code not in missing_values:
                        missing_values.append(code)
        
        # Build variable entry
        var_entry = {
            "question": label,
            "type": var_type,
            "values": formatted_labels if formatted_labels else {}
        }
        
        if missing_values:
            var_entry["missing"] = missing_values
        
        codebook["variables"][var_name] = var_entry
    
    # Write codebook.json
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(codebook, f, ensure_ascii=False, indent=2)
    
    print(f"Codebook written to: {OUTPUT_FILE}")
    print(f"Total variables: {len(codebook['variables'])}")


if __name__ == "__main__":
    main()
