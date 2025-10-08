#!/usr/bin/env python3
import pyreadstat

# Load SAV file
df, meta = pyreadstat.read_sav('surveys/ces19/raw/ces_2019.sav', encoding='latin1')

# Variables already completed (from git history)
completed = {
    'cps19_ResponseId': 'id_respondent',
    'cps19_consent': 'tech_consent',
    'cps19_citizenship': 'ses_citizenship'
}

# Create todo markdown
todo_lines = ["# Variables Processing Todo - CES 2019\n"]
todo_lines.append(f"**Total variables**: {len(df.columns)}\n")
todo_lines.append(f"**Completed**: {len(completed)}\n")
todo_lines.append(f"**Remaining**: {len(df.columns) - len(completed)}\n\n")

todo_lines.append("## Completed\n")
for raw_var, clean_var in completed.items():
    todo_lines.append(f"- [x] {raw_var} → {clean_var}\n")

todo_lines.append("\n## Pending\n")
for col in df.columns:
    if col not in completed:
        todo_lines.append(f"- [ ] {col}\n")

# Write to file
with open('surveys/ces19/variables_todo.md', 'w') as f:
    f.writelines(todo_lines)

print("Created variables_todo.md with:")
print(f"  - {len(completed)} completed variables")
print(f"  - {len(df.columns) - len(completed)} pending variables")