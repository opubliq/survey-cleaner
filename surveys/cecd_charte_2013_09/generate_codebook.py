#!/usr/bin/env python3
"""
Generate codebook.json from PDF-extracted codebook text file.
Survey: cecd_charte_2013_09
Source: Livre de codes - Charte_CROP_2013-09.pdf (converted to .txt)
"""

import json
import re
from pathlib import Path

# Paths
SHARED_FOLDER = Path("/home/hubcad25/opubliq/repos/survey-cleaner/_SharedFolder_data_produit/cecd_charte_2013_09")
CODEBOOK_TXT = SHARED_FOLDER / "codebook.txt"
OUTPUT_JSON = SHARED_FOLDER / "codebook.json"

# RIGHT SINGLE QUOTATION MARK (U+2019)
APOS = '\u2019'


def parse_codebook(content: str) -> dict:
    """Parse the codebook text and extract variables."""
    variables = {}
    
    # Split by section separators (80 or more equal signs)
    sections = re.split(r"={80,}", content)
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        lines = section.split("\n")
        
        # Find variable name first
        first_line = lines[0].strip()
        
        # Match: varname 'question text' - with curly apostrophe U+2019
        var_pattern = rf"^(\w+)\s+{APOS}(.+)"
        match = re.match(var_pattern, first_line)
        if not match:
            continue
        
        var_name = match.group(1)
        question_start = match.group(2)
        
        # Collect full question text - collect until we hit a metadata line
        # or until we find a line that ends with apostrophe (end of question)
        question_parts = [question_start]
        
        i = 1
        found_end = question_start.rstrip().endswith(APOS)
        while i < len(lines) and not found_end:
            line = lines[i].strip()
            # Stop at storage mode or other metadata
            if line.startswith("Storage mode") or line.startswith("Measurement") or line.startswith("Values and labels"):
                break
            # Continuation lines - might be empty or contain more question text
            if line:
                # Check if this line starts with apostrophe (continuation)
                if line.startswith(APOS):
                    question_parts.append(line.lstrip(APOS))
                    if line.rstrip().endswith(APOS):
                        found_end = True
                else:
                    # Plain continuation line
                    question_parts.append(line)
                    if line.rstrip().endswith(APOS):
                        found_end = True
            i += 1
        
        question_text = " ".join(question_parts)
        # Clean up trailing apostrophe/whitespace
        question_text = re.sub(rf"{APOS}\s*$", "", question_text)
        question_text = re.sub(r"\s+", " ", question_text).strip()
        
        # Now extract values and labels
        # Find the values section start
        values_start = None
        for j, line in enumerate(lines):
            if line.strip() == "Values and labels":
                values_start = j + 1
                break
        
        values = {}
        if values_start:
            j = values_start
            pending_value = None
            
            # Skip the "N Percent" / "N Valid Total" header and blank lines
            while j < len(lines):
                line = lines[j].strip()
                if line == "N Percent" or line == "N Valid Total" or line.startswith("N ") or not line:
                    j += 1
                else:
                    break
            
            # Now parse values
            while j < len(lines):
                line = lines[j].strip()
                
                # Stop at next section marker or NA
                if line.startswith("=" * 10) or line.startswith("NA M"):
                    break
                
                # Check for pattern: "1 'Label'" - value and label on same line
                val_pattern_full = rf"^(\d+)\s+{APOS}(.+){APOS}$"
                val_match = re.match(val_pattern_full, line)
                if val_match:
                    values[val_match.group(1)] = val_match.group(2)
                    pending_value = None
                    j += 1
                    continue
                
                # Check for pattern: "1" alone - value on its own line, label follows
                val_pattern_num = re.match(r"^(\d+)$", line)
                if val_pattern_num:
                    pending_value = val_pattern_num.group(1)
                    j += 1
                    continue
                
                # Check for pattern: "'Label'" alone - continuation of previous value
                if line.startswith(APOS) and pending_value:
                    label = line.lstrip(APOS)
                    if label.endswith(APOS):
                        label = label[:-1]
                    values[pending_value] = label.strip()
                    pending_value = None
                    j += 1
                    continue
                
                # Skip (unlab.val.) marker
                if line.startswith("(unlab"):
                    if pending_value:
                        values[pending_value] = None
                        pending_value = None
                    j += 1
                    continue
                
                # Skip frequency/percentage lines (decimal numbers like "33.3", "17.5", etc.)
                # But NOT integers - those could be value codes
                if re.match(r"^\d+\.\d+$", line) and pending_value is None:
                    j += 1
                    continue
                
                # Empty line or unknown - skip
                j += 1
        
        # Determine type
        # Check for continuous variables (have Min/Max/Mean)
        has_stats = any("Min:" in l or "Mean:" in l for l in lines)
        
        if values:
            var_type = "categorical"
        elif has_stats:
            var_type = "continuous"
        else:
            var_type = "categorical"
        
        # Create entry
        var_entry = {
            "question": question_text,
            "type": var_type,
            "values": values
        }
        
        variables[var_name] = var_entry
    
    return variables


def main():
    # Read codebook text
    with open(CODEBOOK_TXT, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Parse variables
    variables = parse_codebook(content)
    
    # Build output
    output = {
        "survey_id": "cecd_charte_2013_09",
        "variables": variables
    }
    
    # Write JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Written {OUTPUT_JSON}")
    print(f"Variables: {len(variables)}")


if __name__ == "__main__":
    main()