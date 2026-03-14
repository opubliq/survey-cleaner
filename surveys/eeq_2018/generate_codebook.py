
import pandas as pd
import json
import re

def generate_codebook():
    survey_id = "eeq_2018"
    shared_folder = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2018"
    surveys_dir = f"/home/hubcad25/opubliq/repos/survey-cleaner/surveys/{survey_id}"

    # Load DTA metadata
    dta_file = f"{shared_folder}/Quebec Election Study 2018.dta"
    reader = pd.read_stata(dta_file, iterator=True)
    variable_labels_dta = reader.variable_labels()
    value_labels_dta = reader.value_labels()
    df = pd.read_stata(dta_file, convert_categoricals=False)
    column_names = list(df.columns)

    # Read markdown file
    md_file = f"{shared_folder}/Quebec Election Study 2018 FR.md"
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    codebook = {
        "survey_id": survey_id,
        "variables": {}
    }

    variables_with_labels_from_md = 0
    variables_with_null_labels = 0

    for var_name in column_names:
        question_text = variable_labels_dta.get(var_name, "")
        values = {}
        var_type = "continuous" # Default to continuous

        # Try to get value labels from DTA first
        # DTA stores value labels by label-set name, not variable name directly
        # We need to find which label set, if any, corresponds to the variable.
        # This is a heuristic, as pandas doesn't provide a direct map.
        # For simplicity, we'll iterate through value_labels_dta and check if the var_name
        # is a key in any of the value label sets.
        # A more robust solution might involve examining df.dtypes to see if a variable
        # is a CategoricalDtype and then getting its categories.

        dta_has_labels = False
        for label_set_name, label_map in value_labels_dta.items():
            if var_name in label_set_name or var_name.lower() in label_set_name.lower(): # Heuristic match
                for code, label in label_map.items():
                    values[str(int(code))] = str(label) if label else None
                dta_has_labels = True
                break
        
        # If DTA has no labels or heuristic match failed, try to get from markdown
        if not dta_has_labels and len(df[var_name].unique()) <= 25:
            # Search markdown for value labels if variable appears categorical
            # This is a very basic regex, might need refinement for complex cases
            match = re.search(r'{}[\s\S]*?(?=(?:Q\w+:\s|\Z))'.format(re.escape(var_name)), md_content, re.IGNORECASE)
            if match:
                block = match.group(0)
                # Look for lines starting with '-' followed by a code and label
                md_label_matches = re.findall(r'-\s*(\d+)\s*-\s*(.+)', block)
                if md_label_matches:
                    for code, label in md_label_matches:
                        values[code.strip()] = label.strip()
                    variables_with_labels_from_md += 1
            
            # Fallback for value labels like "1: Yes", "2: No"
            if not values:
                md_label_matches = re.findall(r'(?:{}|{})(?:.*?)(\d+):\s*(.+?)(?=\n\d+:|\n\n|\Z)'.format(re.escape(var_name), re.escape(question_text)), md_content, re.IGNORECASE)
                if md_label_matches:
                    for code, label in md_label_matches:
                        values[code.strip()] = label.strip()
                    if values:
                        variables_with_labels_from_md += 1

        # Determine type
        if len(values) > 0 or len(df[var_name].unique()) <= 25:
            var_type = "categorical"
        elif pd.api.types.is_numeric_dtype(df[var_name]) and len(df[var_name].unique()) > 25:
            var_type = "continuous"
        elif pd.api.types.is_string_dtype(df[var_name]):
            var_type = "text"
        
        # If still no labels and categorical, populate with unique values from data as null
        if not values and var_type == "categorical":
            unique_codes = df[var_name].unique()
            for code in unique_codes:
                if pd.isna(code): # Handle NaN values if they exist
                    continue
                values[str(int(code))] = None
            if values: # Only count if there are actual codes
                variables_with_null_labels += 1
        
        # If question text is empty, try to get it from markdown
        if not question_text:
            question_match = re.search(r'(Q\w+):\s*(.*?)(?=\nQ\w+:|\n\n|\Z)', md_content, re.IGNORECASE)
            if question_match and question_match.group(1).lower() == var_name.lower():
                question_text = question_match.group(2).strip()


        # Filter out variables with no question text (missing labels are fine)
        if question_text:
            codebook["variables"][var_name] = {
                "question": question_text,
                "type": var_type,
                "values": values,
                "missing": [], # Placeholder, to be extracted later if needed
            }
    
    # Save the codebook.json
    output_path = f"{surveys_dir}/codebook.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(codebook, f, indent=2, ensure_ascii=False)

    return len(column_names), variables_with_labels_from_md, variables_with_null_labels, output_path

if __name__ == "__main__":
    total_vars, md_labels, null_labels, output_path = generate_codebook()
    print(f"Script: surveys/eeq_2018/generate_codebook.py")
    print(f"codebook.json written: {output_path}")
    print(f"Variables: {total_vars}")
    print(f"Labels enriched from PDF/DOC: {md_labels}")
    print(f"Labels still null (not found anywhere): {null_labels}")
    print(f"Sources used: Quebec Election Study 2018.dta, Quebec Election Study 2018 FR.md")
