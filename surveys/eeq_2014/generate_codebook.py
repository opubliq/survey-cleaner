
import json
import re
import pandas as pd
import pyreadstat

def extract_labels_from_markdown(markdown_content, var_name, question_text=None):
    labels = {}
    # Try to find the variable name followed by its question
    # This regex tries to find the variable and then capture options that look like bullet points or numbered lists.
    # It looks for lines starting with '-' or a number followed by '.' and then the label.
    # It stops at the next variable or a blank line.
    
    # Escape var_name for regex if it contains special characters
    escaped_var_name = re.escape(var_name)
    
    # Pattern to find the variable and potentially its question, followed by possible list items
    # It tries to be flexible with "VAR_NAME: Question" or "VAR_NAME Question"
    # and then looks for indented list items
    
    # This pattern aims to capture labels that are indented and start with a hyphen or a number.
    # It looks for the variable name, then potentially its question, then lines that are indented
    # and look like list items.
    
    # Strategy: Find the variable name. Then, look for indented lines immediately following it.
    # This assumes labels are directly below the variable definition.

    # First, try to locate the question text more robustly, if not provided
    search_text = question_text if question_text else ""
    
    # Pattern to find the variable definition line and subsequent potential labels
    # It's flexible with "VAR: Question" or "VAR Question"
    # This is a complex regex and might need iterative refinement.
    # Let's try a simpler approach: find the variable line, then parse subsequent indented lines.

    # Find the block related to the variable
    # Look for variable name (possibly with a colon) and then the question text (if available)
    # The markdown often has "VAR: Question text" or "VAR. Question text"
    
    # We need to consider both "VAR: Question" and "VAR. Question"
    # Also, the labels are often indented with hyphens or numbers.
    
    
    # Let's read the markdown line by line for precise parsing
    lines = markdown_content.split('\\n')
    in_var_block = False
    label_code = 1
    
    # Create a list of potential ways the variable might appear in the markdown
    var_patterns = [
        re.compile(r'^\s*' + escaped_var_name + r':\s*(.*)', re.IGNORECASE),
        re.compile(r'^\s*' + escaped_var_name + r'\.\s*(.*)', re.IGNORECASE),
        re.compile(r'^\s*' + escaped_var_name + r'\s*(.*)', re.IGNORECASE) # Just the variable name
    ]

    for i, line in enumerate(lines):
        # Check if we are at the start of a variable's block
        # The question can span multiple lines, but we are looking for the label definitions
        # after the question.
        
        # Check if this line is the start of the current variable's definition
        for pattern in var_patterns:
            if pattern.match(line):
                in_var_block = True
                # Reset label_code for a new variable
                label_code = 1
                break
        
        if in_var_block:
            # Look for indented list items as labels
            label_match_hyphen = re.match(r'^\s*-\s*(.*)', line)
            label_match_number = re.match(r'^\s*(\d+)\.\s*(.*)', line)
            
            if label_match_hyphen:
                label_text = label_match_hyphen.group(1).strip()
                if label_text and "Entrez l’année" not in label_text and "Entrez le code" not in label_text: # Skip instruction lines
                    labels[str(label_code)] = label_text
                    label_code += 1
            elif label_match_number:
                code = label_match_number.group(1)
                label_text = label_match_number.group(2).strip()
                if label_text and "Entrez l’année" not in label_text and "Entrez le code" not in label_text: # Skip instruction lines
                    labels[str(code)] = label_text
                    # Do not increment label_code if explicit code is provided
            elif line.strip() == "" and labels: # If we see a blank line after finding labels, we might be done with this variable's labels.
                # However, sometimes questions themselves have blank lines. This is tricky.
                # A more robust check might be to see if the next non-blank line is another variable.
                next_non_blank_line_is_var = False
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() != "":
                        for pattern in var_patterns:
                            if pattern.match(lines[j]):
                                next_non_blank_line_is_var = True
                                break
                        break
                if next_non_blank_line_is_var:
                    in_var_block = False # Exit this variable's label block
            elif not line.strip().startswith('-') and not re.match(r'^\s*\d+\.\s*', line) and labels:
                # If we're in a block, have found labels, and the current line is not a label,
                # AND it's not empty, it likely means the labels block ended.
                # This needs refinement to handle questions spanning multiple lines.
                
                # A better heuristic: if the current line is not a label AND is not indented like a label,
                # AND it doesn't appear to be a continuation of the question, then stop.
                # This is a very rough heuristic and might fail.
                pass # For now, keep parsing. Will refine.
            
            # If the current line is a new variable, stop parsing labels for the previous one
            for pattern in var_patterns:
                if pattern.match(line) and line.strip().startswith(var_name) == False: # Make sure it's not itself
                    if labels: # Only stop if we actually found labels for the current var
                        in_var_block = False
                        break
        if not in_var_block and labels: # if we exited the block and have labels, return them
            break # Exit the loop, we got labels for the requested var

    return labels


def determine_variable_type(values, unique_data_values):
    if values:
        return "categorical" # If explicit labels exist, it's categorical
    
    if unique_data_values is not None:
        # Filter out non-numeric values for count, assuming they are missing codes for now
        numeric_unique_data_values = [v for v in unique_data_values if isinstance(v, (int, float)) and not pd.isna(v)]
        if 0 < len(numeric_unique_data_values) <= 25:
            return "categorical"
        elif len(numeric_unique_data_values) > 25:
            return "continuous"
    
    # Default to text if no other type can be determined (e.g., if unique_data_values is None)
    return "text"


def generate_codebook(survey_id, shared_folder, surveys_dir):
    codebook = {"survey_id": survey_id, "variables": {}}

    sav_metadata_path = f"{surveys_dir}/sav_metadata.json"
    markdown_path = f"{surveys_dir}/Quebec Election Study 2014 FR.md" # Assuming this is the only markdown file

    with open(sav_metadata_path, 'r', encoding='utf-8') as f:
        sav_metadata = json.load(f)

    with open(markdown_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    column_names = sav_metadata["column_names"]
    # column_labels from SAV metadata is a list, not a dict. Map it by index.
    column_names_from_sav = sav_metadata["column_names"]
    column_labels_list = sav_metadata["column_labels"]
    
    column_labels_map = {col_name: col_label for col_name, col_label in zip(column_names_from_sav, column_labels_list)}
    variable_value_labels = sav_metadata["variable_value_labels"]
    
    # Read the SAV file again to get unique values for type determination
    sav_file = f"{shared_folder}/Quebec Election Study 2014.sav"
    df, _ = pyreadstat.read_sav(sav_file)

    labels_from_sav_only = 0
    labels_enriched_from_pdf = 0
    labels_still_null = 0

    for var_name in column_names:
        question = column_labels_map.get(var_name, "")
        values = variable_value_labels.get(var_name, {})
        notes = "" # Initialize notes

        # If question is empty from SAV, try to extract from markdown
        if not question:
            # Look for "VAR_NAME: Question text" or "VAR_NAME. Question text"
            # This regex is more specific for question extraction
            question_match = re.search(r'^\s*' + re.escape(var_name) + r'[:\.]?\s*(.*)', markdown_content, re.IGNORECASE | re.MULTILINE)
            if question_match:
                # Get the rest of the line as potential question
                potential_question = question_match.group(1).strip()
                # Clean up if it contains just a variable name or junk
                if potential_question and len(potential_question.split()) > 1: # Avoid single word or empty questions
                    question = potential_question

        # Get unique values from the DataFrame for type determination and null labels
        unique_data_values = None
        if var_name in df.columns:
            # Convert to a list of unique values, handling pandas Series and potential non-numeric types
            unique_data_values = df[var_name].dropna().unique().tolist()
            # Ensure unique_data_values are hashable if they are to be used as dict keys (e.g., convert floats to ints if they represent integer codes)
            unique_data_values = [int(x) if isinstance(x, float) and x.is_integer() else x for x in unique_data_values]


        markdown_labels = {} # Initialize to an empty dictionary
        # If SAV has no labels for this variable, try to get from markdown
        if not values:
            markdown_labels = extract_labels_from_markdown(markdown_content, var_name, question)
            if markdown_labels:
                values.update(markdown_labels)
                labels_enriched_from_pdf += 1

        # If still no labels, and it's a categorical type based on unique data values,
        # use unique numeric codes with null labels.
        if not values and unique_data_values is not None:
            # Determine if it's categorical based on unique_data_values count.
            # Only consider numeric values for this count for now.
            numeric_unique_data_values = [v for v in unique_data_values if isinstance(v, (int, float)) and not pd.isna(v)]

            if 0 < len(numeric_unique_data_values) <= 25: # Assuming categorical if <= 25 unique numeric values
                for code in sorted(numeric_unique_data_values):
                    values[str(code)] = None
                if len(numeric_unique_data_values) > 0: # Only count if some values were added
                    labels_still_null += 1
            # For non-numeric unique values (e.g., text), they will not get null labels here
            # and will be handled by the default "text" type.

        # Determine type
        var_type = determine_variable_type(values, unique_data_values)

        # Skip variables with no question text.
        if not question:
            continue

        variable_entry = {
            "question": question,
            "type": var_type,
            "values": values,
        }
        
        # Add notes if found in markdown (e.g., skip patterns)
        # This is a very basic attempt to get notes. Needs refinement for complex skip patterns.
        # For now, let's look for bracketed text right after the question.
        notes_match = re.search(r'^\s*' + re.escape(var_name) + r'[:\.]?\s*' + re.escape(question) + r'\s*\[([^\]]+)\]', markdown_content, re.IGNORECASE | re.MULTILINE)
        if notes_match:
            notes = notes_match.group(1).strip()
            if notes:
                variable_entry["notes"] = notes

        codebook["variables"][var_name] = variable_entry
        
        if variable_value_labels.get(var_name, {}): # If original SAV had labels
            if not markdown_labels and var_name in variable_value_labels:
                labels_from_sav_only += 1
        # labels_enriched_from_pdf is already incremented in the logic above
        # labels_still_null is also already incremented

    # Re-evaluate labels_still_null: count variables where `values` is empty and not enriched from markdown
    final_labels_still_null_count = 0
    for var_name, var_data in codebook["variables"].items():
        if not var_data["values"] and var_data["type"] != "continuous" and var_data["type"] != "text":
            final_labels_still_null_count += 1
    
    # Adjust labels_from_sav_only and labels_enriched_from_pdf counts
    # The previous logic was slightly off because labels_enriched_from_pdf was incremented whenever markdown_labels were found,
    # regardless of whether SAV had labels or not. Let's fix this for reporting.
    
    final_labels_from_sav_only = 0
    final_labels_enriched_from_pdf = 0

    for var_name in column_names:
        sav_had_labels = bool(variable_value_labels.get(var_name, {}))
        markdown_found_labels = bool(extract_labels_from_markdown(markdown_content, var_name, column_labels_map.get(var_name, "")))
        
        if sav_had_labels and not markdown_found_labels:
            final_labels_from_sav_only += 1
        elif not sav_had_labels and markdown_found_labels:
            final_labels_enriched_from_pdf += 1


    with open(f"{surveys_dir}/codebook.json", 'w', encoding='utf-8') as f:
        json.dump(codebook, f, ensure_ascii=False, indent=4)

    print(f"Script: {surveys_dir}/generate_codebook.py")
    print(f"codebook.json written: {surveys_dir}/codebook.json")
    print(f"Variables: {len(codebook['variables'])}")
    print(f"Labels from SAV only: {final_labels_from_sav_only}")
    print(f"Labels enriched from PDF/DOC: {final_labels_enriched_from_pdf}")
    print(f"Labels still null (not found anywhere): {final_labels_still_null_count}")
    print(f"Sources used: {sav_metadata_path}, {markdown_path}")

if __name__ == "__main__":
    survey_id = "eeq_2014"
    shared_folder = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2014"
    surveys_dir = "/home/hubcad25/opubliq/repos/survey-cleaner/surveys/eeq_2014"
    generate_codebook(survey_id, shared_folder, surveys_dir)
