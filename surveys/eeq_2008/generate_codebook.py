
import json
import re
import pyreadstat
from collections import defaultdict

survey_id = "eeq_2008"
shared_folder = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2008"
surveys_dir = "/home/hubcad25/opubliq/repos/survey-cleaner/surveys/eeq_2008"

# Load SAV metadata
with open(f"{surveys_dir}/sav_metadata.json", "r") as f:
    sav_meta = json.load(f)

# Read SAV data to get unique values for type inference and null labels
sav_file = f"{shared_folder}/Quebec Election Study 2008 (SPSS).sav"
df, _ = pyreadstat.read_sav(sav_file) # Removed disable_conversion_on_float_variables

# Load markdown content
markdown_files = [
    f"{shared_folder}/Quebec Election study 2008 ENG.md",
    f"{shared_folder}/Quebec Election study 2008 ENG.pdf.converted.md",
    f"{shared_folder}/Quebec Election Study 2008 FR.doc.converted.md",
    f"{shared_folder}/Quebec Election Study 2008 FR.md"
]

markdown_content = ""
for md_file in markdown_files:
    try:
        with open(md_file, "r", encoding='utf-8') as f:
            markdown_content += f.read() + "\n\n"
    except FileNotFoundError:
        print(f"Warning: Markdown file not found: {md_file}")
    except UnicodeDecodeError:
        print(f"Warning: UnicodeDecodeError reading {md_file}, trying latin-1")
        with open(md_file, "r", encoding='latin-1') as f:
            markdown_content += f.read() + "\n\n"

codebook = {
    "survey_id": survey_id,
    "variables": {}
}

variables_with_sav_labels = 0
variables_enriched_from_md = 0
variables_still_null = 0

for i, var_name in enumerate(sav_meta["column_names"]):
    question_text = sav_meta["column_labels"][i] if sav_meta["column_labels"] and sav_meta["column_labels"][i] else None
    sav_value_labels = sav_meta["variable_value_labels"].get(var_name, {})

    values = {}
    var_type = "continuous" # Default to continuous
    search_block = "" # Initialize search_block

    # 1. Question text
    if not question_text:
        # Try to find question text in markdown
        # Look for patterns like "VAR_NAME: Question text" or "VAR_NAME\nQuestion text"
        match = re.search(rf"(?:^|\n)\s*{re.escape(var_name)}[.:]?\s*(.*?)(?:\n|$)", markdown_content, re.IGNORECASE | re.DOTALL)
        if match:
            # Take the first line as question if it seems reasonable
            candidate_question = match.group(1).strip().split('\n')[0].strip()
            if len(candidate_question) > 5 and not re.match(r'^\d+$', candidate_question): # Avoid just numbers or very short strings
                question_text = candidate_question
        if not question_text: # If still no question, try looking for text right above variable name
            match = re.search(rf"(?:^|\n)([^\n]+?)\s*\n\s*{re.escape(var_name)}[.:]?", markdown_content, re.IGNORECASE | re.DOTALL)
            if match:
                candidate_question = match.group(1).strip()
                if len(candidate_question) > 5 and not re.match(r'^\d+$', candidate_question):
                    question_text = candidate_question


    # 2. Value labels
    if sav_value_labels:
        values = sav_value_labels
        variables_with_sav_labels += 1
        var_type = "categorical" if len(values) <= 25 else "continuous" # Re-evaluate type based on labels
    else:
        # If no SAV labels, try to extract from markdown
        md_labels = {}

        search_start_index = -1
        # Prioritize searching by var_name, then question_text
        match_var_name = re.search(rf"(?:^|\n)\s*{re.escape(var_name)}[.:]?", markdown_content, re.IGNORECASE)
        if match_var_name:
            search_start_index = match_var_name.start()
        elif question_text:
            match_question_text = re.search(rf"(?:^|\n){re.escape(question_text)}", markdown_content, re.IGNORECASE)
            if match_question_text:
                search_start_index = match_question_text.start()

        if search_start_index != -1:
            search_block = markdown_content[search_start_index:search_start_index + 1000] # Search next 1000 chars

            # Pattern for "Label Text  Code" or "Code  Label Text"
            label_code_pattern_1 = re.compile(r"([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9\s,'’\-]+?)\s+(\d{1,3})(?:\s*=>.*)?", re.IGNORECASE)
            code_label_pattern_2 = re.compile(r"(\d{1,3})\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9\s,'’\-]+?)", re.IGNORECASE)

            # Look for labels near the variable name
            for match in label_code_pattern_1.finditer(search_block):
                label, code = match.groups()
                md_labels[code.strip()] = label.strip()
            
            if not md_labels:
                for match in code_label_pattern_2.finditer(search_block):
                    code, label = match.groups()
                    md_labels[code.strip()] = label.strip()

        if md_labels:
            values = md_labels
            variables_enriched_from_md += 1
            var_type = "categorical" if len(values) <= 25 else "continuous"
        else:
            # If no labels found in SAV or markdown, use unique values from data as null labels
            if var_name in df.columns:
                unique_values = df[var_name].unique()
                # Filter out NaN and common missing values, convert to string keys
                unique_codes = sorted([str(int(v)) for v in unique_values if isinstance(v, (int, float)) and not (v == -99 or v == 999 or v == 99 or v == -999 or v == 9999)]) # Added 9999
                
                if 0 < len(unique_codes) <= 25:
                    values = {code: None for code in unique_codes}
                    var_type = "categorical"
                elif df[var_name].dtype == 'object':
                    var_type = "text"
                    values = {}
                elif len(unique_codes) > 25:
                    var_type = "continuous"
                    values = {}
                else:
                    values = {}
                    var_type = "continuous"

            if not values and var_type != "text":
                variables_still_null += 1


    # 3. Type: Adjusted based on value labels, now also consider number of unique values
    if var_name in df.columns:
        if df[var_name].dtype == 'object':
            var_type = "text"
            values = {} # Text variables do not have value labels
        elif var_type == "continuous" and len(values) > 0: # If we have many labels, it's actually continuous
            var_type = "continuous"
            values = {}
        elif var_type == "continuous" and len(df[var_name].unique()) <= 25 and len(values) == 0: # If it's continuous by default but has few unique values and no labels, treat as categorical with null labels
             unique_values = df[var_name].unique()
             unique_codes = sorted([str(int(v)) for v in unique_values if isinstance(v, (int, float)) and not (v == -99 or v == 999 or v == 99 or v == -999 or v == 9999)]) # Added 9999
             if unique_codes:
                values = {code: None for code in unique_codes}
                var_type = "categorical"


    # 4. Missing codes
    missing = []
    if search_block: # Only search in search_block if it's not empty
        missing_search_area = search_block
    else:
        missing_search_area = markdown_content

    missing_code_pattern = re.compile(r"(?:Missing|Non applicable|Ne s'applique pas|Refused|Préfère ne pas répondre|I prefer not answering)\s*[:-]?\s*(\d{1,4})", re.IGNORECASE)
    for match in missing_code_pattern.finditer(missing_search_area):
        code = match.group(1).strip()
        if code not in missing:
            missing.append(code)


    # Notes (skip patterns or special instructions)
    notes = None
    skip_pattern_match = re.search(rf"{re.escape(var_name)}[.:]?.*?(\n\s*=>\s*[^\n]+)", markdown_content, re.IGNORECASE | re.DOTALL)
    if skip_pattern_match:
        notes = skip_pattern_match.group(1).strip()


    if question_text or values: # Only include if we have at least a question or some values
        codebook["variables"][var_name] = {
            "question": question_text if question_text else "",
            "type": var_type,
            "values": values,
            "missing": missing if missing else [],
        }
        if notes:
            codebook["variables"][var_name]["notes"] = notes

# Calculate actual counts of variables_still_null after all processing
final_variables_still_null = 0
for var_name, var_data in codebook["variables"].items():
    if not var_data["values"] and var_data["type"] != "text": # If values is empty and not a text variable
        final_variables_still_null += 1

variables_still_null = final_variables_still_null

output_file = f"{surveys_dir}/codebook.json"
with open(output_file, "w", encoding='utf-8') as f:
    json.dump(codebook, f, indent=2, ensure_ascii=False)

print(f"Script: {surveys_dir}/generate_codebook.py")
print(f"codebook.json written: {output_file}")
print(f"Variables: {len(codebook['variables'])}")
print(f"Labels from SAV only: {variables_with_sav_labels}")
print(f"Labels enriched from PDF/DOC: {variables_enriched_from_md}")
print(f"Labels still null (not found anywhere): {variables_still_null}")
print(f"Sources used: {', '.join(markdown_files)}, {sav_file}")
