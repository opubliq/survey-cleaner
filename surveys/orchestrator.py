#!/usr/bin/env python3
"""
Survey Cleaning Orchestrator

Exécute le workflow complet de WORKFLOW.md via appels API Anthropic directs.
Chaque agent = 1 call API avec contexte frais → pas de limite de contexte.

Usage:
    python surveys/orchestrator.py <survey_id>
    python surveys/orchestrator.py <survey_id> --limit 10
    python surveys/orchestrator.py <survey_id> --only-var <var_name>
"""

import os
import sys
import json
import re
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env
load_dotenv(override=True)


# ========================================================================
# Custom tools for Claude Agent SDK
# ========================================================================

def bash_tool(command: str) -> str:
    """Execute a bash command and return output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout if result.returncode == 0 else result.stderr
        return output or f"Command executed (exit code: {result.returncode})"
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out after 30 seconds"
    except Exception as e:
        return f"ERROR: {str(e)}"


def read_file_tool(file_path: str) -> str:
    """Read a file and return its contents."""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"ERROR: File not found: {file_path}"

        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: Failed to read file: {str(e)}"


def write_file_tool(file_path: str, content: str) -> str:
    """Write content to a file."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as f:
            f.write(content)

        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"ERROR: Failed to write file: {str(e)}"


def edit_file_tool(file_path: str, old_string: str, new_string: str) -> str:
    """Edit a file by replacing old_string with new_string."""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"ERROR: File not found: {file_path}"

        with open(path, 'r') as f:
            content = f.read()

        if old_string not in content:
            return f"ERROR: String not found in file: {old_string[:100]}..."

        new_content = content.replace(old_string, new_string)

        with open(path, 'w') as f:
            f.write(new_content)

        return f"Successfully edited {file_path}"
    except Exception as e:
        return f"ERROR: Failed to edit file: {str(e)}"


class SurveyOrchestrator:
    """Orchestrateur principal qui exécute les 5 agents du workflow"""

    def __init__(self, survey_id, limit=None, only_var=None):
        self.survey_id = survey_id
        self.limit = limit
        self.only_var = only_var
        self.base_path = Path(__file__).parent
        self.survey_path = self.base_path / survey_id
        self.status_file = self.base_path / "status.json"

        # API client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = Anthropic(api_key=api_key)

        # Load status
        self.status = self.load_status()

    def load_status(self):
        """Charge status.json"""
        with open(self.status_file) as f:
            return json.load(f)

    def save_status(self):
        """Sauvegarde status.json"""
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2, ensure_ascii=False)

    def get_survey_status(self):
        """Retourne le status du sondage"""
        return self.status["surveys"][self.survey_id]

    def update_survey_field(self, field, value):
        """Met à jour un champ du sondage"""
        self.status["surveys"][self.survey_id][field] = value
        self.status["surveys"][self.survey_id]["last_updated"] = datetime.now().isoformat()
        self.save_status()

    def increment_cleaned_count(self):
        """Incrémente le compteur de variables nettoyées"""
        survey = self.status["surveys"][self.survey_id]
        survey["variables"]["cleaned"] += 1
        survey["variables"]["pending"] -= 1

        # Passe en in_progress si c'était not_started
        if survey["status"] == "not_started":
            survey["status"] = "in_progress"

        survey["last_updated"] = datetime.now().isoformat()
        self.save_status()

    def get_pending_variables(self):
        """
        Retourne la liste des variables à nettoyer.
        TODO: implémenter tracking granulaire des variables dans status.json
        Pour l'instant, retourne toutes les variables du dataset.
        """
        # Lit le fichier data pour avoir la liste des variables
        data_file = self.find_data_file()
        if not data_file:
            raise ValueError(f"No data file found for {self.survey_id}")

        # Load avec pandas pour avoir les colonnes
        import pandas as pd
        if data_file.suffix == '.csv':
            df = pd.read_csv(data_file, nrows=1)
        elif data_file.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(data_file, nrows=1)
        elif data_file.suffix == '.sav':
            import pyreadstat
            df, _ = pyreadstat.read_sav(data_file, row_limit=1)
        elif data_file.suffix == '.dta':
            df = pd.read_stata(data_file, chunksize=1).__next__()
        else:
            raise ValueError(f"Unsupported file type: {data_file.suffix}")

        all_vars = df.columns.tolist()

        # Si only_var spécifié
        if self.only_var:
            if self.only_var not in all_vars:
                raise ValueError(f"Variable {self.only_var} not found in dataset")
            return [self.only_var]

        # Appliquer limit
        if self.limit:
            return all_vars[:self.limit]

        return all_vars

    def validate_variable(self, variable_name, transformation_code, standard_name):
        """
        Valide une variable en comparant raw vs cleaned frequencies.
        Exécute SEULEMENT le code de transformation fourni (pas tout clean.py).

        Args:
            variable_name: Nom de la variable originale dans les données raw
            transformation_code: Code Python de transformation (une seule ligne)
            standard_name: Nom standardisé de la variable cleaned

        Returns:
            bool: True si validation OK, False sinon
        """
        import pandas as pd
        import numpy as np

        print(f"\n{'='*60}")
        print(f"Validation: {variable_name} → {standard_name}")
        print(f"{'='*60}\n")

        # 1. Load raw data
        data_file = self.find_data_file()
        if not data_file:
            print("WARNING: No data file found, skipping validation")
            return True

        try:
            if data_file.suffix == '.csv':
                df_raw = pd.read_csv(data_file)
            elif data_file.suffix in ['.xlsx', '.xls']:
                df_raw = pd.read_excel(data_file)
            elif data_file.suffix == '.sav':
                import pyreadstat
                df_raw, _ = pyreadstat.read_sav(data_file)
            elif data_file.suffix == '.dta':
                df_raw = pd.read_stata(data_file)
            else:
                print(f"WARNING: Unsupported file type: {data_file.suffix}")
                return True
        except Exception as e:
            print(f"WARNING: Failed to load data: {e}")
            return True

        # 2. Execute ONLY the transformation code for this variable
        try:
            # Prepare execution context with necessary variables
            exec_globals = {
                "pd": pd,
                "np": np
            }
            exec_locals = {
                "df": df_raw,
                "df_clean": pd.DataFrame(index=df_raw.index)
            }

            # Execute the transformation code with proper context
            exec(transformation_code, exec_globals, exec_locals)

            # Retrieve the modified df_clean
            df_clean = exec_locals["df_clean"]

        except Exception as e:
            print(f"WARNING: Failed to execute transformation code: {e}")
            print(f"   Code: {transformation_code}")
            return False

        # 3. Compare frequencies
        print(f"RAW frequencies ({variable_name}):")
        if variable_name in df_raw.columns:
            print(df_raw[variable_name].value_counts().sort_index())
        else:
            print(f"  (variable not found in raw data)")

        print(f"\nCLEANED frequencies ({standard_name}):")
        if standard_name in df_clean.columns:
            print(df_clean[standard_name].value_counts().sort_index())
        else:
            print(f"  (variable not found in cleaned data)")

        # 4. Validation checks
        if standard_name not in df_clean.columns:
            print(f"\nFAILED: Variable {standard_name} not created")
            return False

        has_values = df_clean[standard_name].notna().sum() > 0

        print(f"\n{'='*60}")
        print(f"{'PASSED' if has_values else 'FAILED'}")
        print(f"{'='*60}\n")

        return has_values

    def initialize_survey(self):
        """
        Initialise un nouveau survey (déterministe - pas besoin de LLM).

        Returns:
            bool: True si succès, False sinon
        """
        import pandas as pd
        import shutil

        # 1. Vérifier que le survey existe dans _SharedFolder_data_produit
        shared_folder = self.base_path.parent / "_SharedFolder_data_produit" / self.survey_id
        if not shared_folder.exists():
            print(f"ERROR: Survey directory not found: {shared_folder}")
            return False

        # 2. Trouver le fichier data
        data_file = self.find_data_file()
        if not data_file:
            print(f"ERROR: No data file found in {shared_folder}")
            return False

        print(f"Found data file: {data_file.name}")

        # 3. Compter les variables et observations
        try:
            if data_file.suffix == '.csv':
                df = pd.read_csv(data_file)
            elif data_file.suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(data_file)
            elif data_file.suffix == '.sav':
                import pyreadstat
                df, _ = pyreadstat.read_sav(data_file)
            elif data_file.suffix == '.dta':
                df = pd.read_stata(data_file)
            else:
                print(f"ERROR: Unsupported file type: {data_file.suffix}")
                return False

            n_vars = len(df.columns)
            n_obs = len(df)
            print(f"Dataset: {n_obs} observations, {n_vars} variables")

        except Exception as e:
            print(f"ERROR: Failed to read data file: {e}")
            return False

        # 4. Créer le répertoire du survey
        self.survey_path.mkdir(parents=True, exist_ok=True)

        # 5. Copier le template clean.py
        template_file = self.base_path / "_template" / "clean.py"
        target_file = self.survey_path / "clean.py"

        if template_file.exists():
            shutil.copy(template_file, target_file)
            print(f"Copied template clean.py to {target_file}")
        else:
            print(f"WARNING: Template clean.py not found at {template_file}")

        # 6. Créer l'entrée dans status.json
        self.status["surveys"][self.survey_id] = {
            "status": "not_started",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "data_file": data_file.name,
            "n_observations": n_obs,
            "n_variables": n_vars,
            "variables": {
                "total": n_vars,
                "cleaned": 0,
                "pending": n_vars
            },
            "pipeline": {
                "uploaded": False
            }
        }
        self.save_status()

        print(f"Created status.json entry for {self.survey_id}")

        return True

    def find_data_file(self):
        """Trouve le fichier data.csv/xlsx/sav/dta dans _SharedFolder_data_produit"""
        shared_folder = self.base_path.parent / "_SharedFolder_data_produit" / self.survey_id

        for ext in ['.csv', '.xlsx', '.xls', '.sav', '.dta']:
            files = list(shared_folder.glob(f"*{ext}"))
            if files:
                return files[0]
        return None

    def call_agent(self, agent_name, context):
        """
        Fait un appel API à un agent spécialisé avec tool use.

        Args:
            agent_name: Nom de l'agent (clean-variable, transform-codebook, etc.)
            context: Dict avec le contexte spécifique à passer à l'agent

        Returns:
            Dict avec le résultat de l'agent
        """
        # Load instructions de l'agent
        agent_file = self.base_path.parent / ".claude" / "agents" / f"{agent_name}.md"
        if not agent_file.exists():
            raise ValueError(f"Agent file not found: {agent_file}")

        with open(agent_file) as f:
            agent_instructions = f.read()

        # Prépare le prompt pour l'agent
        user_prompt = json.dumps(context, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"Calling agent: {agent_name}")
        print(f"Context: {list(context.keys())}")
        print(f"{'='*60}\n")

        # Définir les tools disponibles
        tools = [
            {
                "name": "bash",
                "description": "Execute a bash command and return output",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "The bash command to execute"}
                    },
                    "required": ["command"]
                }
            },
            {
                "name": "read_file",
                "description": "Read a file and return its contents",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the file to read"}
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write content to a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the file to write"},
                        "content": {"type": "string", "description": "Content to write to the file"}
                    },
                    "required": ["file_path", "content"]
                }
            },
            {
                "name": "edit_file",
                "description": "Edit a file by replacing old_string with new_string",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the file to edit"},
                        "old_string": {"type": "string", "description": "String to find and replace"},
                        "new_string": {"type": "string", "description": "String to replace with"}
                    },
                    "required": ["file_path", "old_string", "new_string"]
                }
            }
        ]

        # Tool execution mapping
        tool_map = {
            "bash": bash_tool,
            "read_file": read_file_tool,
            "write_file": write_file_tool,
            "edit_file": edit_file_tool
        }

        # Conversation messages
        messages = [{
            "role": "user",
            "content": user_prompt
        }]

        # Loop until agent finishes
        max_turns = 50
        for turn in range(max_turns):
            # Appel API avec tool use et prompt caching
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,
                system=[{
                    "type": "text",
                    "text": agent_instructions,
                    "cache_control": {"type": "ephemeral"}
                }],
                tools=tools,
                messages=messages
            )

            # Check stop reason
            if response.stop_reason == "end_turn":
                # Agent finished
                result_text = ""
                for block in response.content:
                    if block.type == "text":
                        result_text += block.text

                print(f"\nAgent {agent_name} completed after {turn + 1} turns")
                print(f"Response preview: {result_text[:200]}...")

                return {
                    "success": True,
                    "response": result_text,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                        "cache_read_tokens": getattr(response.usage, 'cache_read_input_tokens', 0),
                        "cache_creation_tokens": getattr(response.usage, 'cache_creation_input_tokens', 0)
                    }
                }

            elif response.stop_reason == "tool_use":
                # Agent wants to use tools
                messages.append({"role": "assistant", "content": response.content})

                # Execute all tool calls
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input

                        print(f"  Tool: {tool_name}({list(tool_input.keys())})")

                        # Execute tool
                        if tool_name in tool_map:
                            result = tool_map[tool_name](**tool_input)
                        else:
                            result = f"ERROR: Unknown tool {tool_name}"

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })

                # Add tool results to conversation
                messages.append({"role": "user", "content": tool_results})

            elif response.stop_reason == "max_tokens":
                # Agent hit token limit mid-response — ask it to continue
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": "Continue where you left off."})
                print(f"  (max_tokens hit, continuing...)")

            else:
                # Unexpected stop reason
                print(f"WARNING: Unexpected stop_reason: {response.stop_reason}")
                return {"success": False, "response": f"Unexpected stop: {response.stop_reason}"}

        # Max turns reached
        print(f"WARNING: Agent {agent_name} reached max turns ({max_turns})")
        return {"success": False, "response": "Max turns reached"}

    def run_workflow(self):
        """Exécute le workflow complet"""

        print(f"\n{'='*60}")
        print(f"Starting survey cleaning workflow")
        print(f"Survey: {self.survey_id}")
        print(f"{'='*60}\n")

        # 0. Init survey si pas dans status.json (déterministe - fait en Python)
        if self.survey_id not in self.status["surveys"]:
            print("Step 0: Initializing survey structure...")

            if not self.initialize_survey():
                print("ERROR: Survey initialization failed")
                return

            print("Survey initialized successfully\n")

        survey = self.get_survey_status()
        total_vars = survey["variables"]["total"]

        # 1. Transform codebook (si pas déjà fait)
        shared_folder = self.base_path.parent / "_SharedFolder_data_produit" / self.survey_id
        codebook_md = shared_folder / "codebook.md"
        if not codebook_md.exists():
            print("Step 1: Transforming codebook...")

            # Chercher un codebook source automatiquement
            codebook_extensions = ['.pdf', '.pptx', '.txt', '.md', '.docx']
            codebook_files = []
            for ext in codebook_extensions:
                codebook_files.extend(shared_folder.glob(f"*codebook*{ext}"))
                codebook_files.extend(shared_folder.glob(f"*Codebook*{ext}"))
                codebook_files.extend(shared_folder.glob(f"*questionnaire*{ext}"))

            if codebook_files:
                # Codebook trouvé, transformer directement
                result = self.call_agent("transform-codebook", {
                    "survey_id": self.survey_id,
                    "shared_folder": str(shared_folder),
                    "codebook_source": str(codebook_files[0]),
                    "task": "transform_codebook"
                })
            else:
                # Pas de codebook trouvé — demander à l'utilisateur
                print(f"\nNo codebook file found in {shared_folder}")
                print(f"Files available:")
                for f in sorted(shared_folder.iterdir()):
                    print(f"  - {f.name}")

                print(f"\nOptions:")
                print(f"  - Enter a sheet name/number (e.g. 'sheet:2', 'sheet:Codebook')")
                print(f"  - Enter a file path")
                print(f"  - Type 'skip' to continue without codebook")

                hint = input("\nWhere is the codebook? > ").strip()

                if hint.lower() == 'skip':
                    print("Skipping codebook transformation, continuing without...")
                else:
                    result = self.call_agent("transform-codebook", {
                        "survey_id": self.survey_id,
                        "shared_folder": str(shared_folder),
                        "codebook_hint": hint,
                        "task": "transform_codebook"
                    })

                    # Vérifier si le codebook a été créé
                    if not codebook_md.exists():
                        print("WARNING: Codebook was not created. Continuing without...")
        else:
            print("Step 1: Codebook already exists, skipping...")

        # 2. Clean variables (loop avec contexte frais à chaque fois)
        print(f"\nStep 2: Cleaning variables...")
        pending_vars = self.get_pending_variables()

        print(f"Variables to clean: {len(pending_vars)}/{total_vars}")

        # Trouver le fichier data UNE FOIS pour toutes les variables
        data_file = self.find_data_file()
        if not data_file:
            print(f"ERROR: No data file found for survey {self.survey_id}")
            return

        for i, var_name in enumerate(pending_vars, 1):
            print(f"\n--- Variable {i}/{len(pending_vars)}: {var_name} ---")

            # 1. Appel API avec contexte frais + data_file_path + codebook
            codebook_path = self.base_path.parent / "_SharedFolder_data_produit" / self.survey_id / "codebook.md"
            context = {
                "survey_id": self.survey_id,
                "variable": var_name,
                "data_file": str(data_file),
                "task": "clean_variable"
            }
            if codebook_path.exists():
                context["codebook_file"] = str(codebook_path)

            result = self.call_agent("clean-variable", context)

            # 2. Parse la réponse JSON de l'agent
            try:
                # Extract JSON from response (peut être entouré de ```json ... ```)
                response_text = result.get("response", "")
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)

                if json_match:
                    agent_data = json.loads(json_match.group(1))
                else:
                    # Try direct parsing
                    agent_data = json.loads(response_text)

                transformation_code = agent_data.get("transformation_code")
                standard_name = agent_data.get("standard_name", var_name)

            except (json.JSONDecodeError, AttributeError) as e:
                print(f"WARNING: Failed to parse agent response as JSON: {e}")
                print(f"   Skipping validation for {var_name}")
                transformation_code = None
                standard_name = var_name

            # 3. Valide immédiatement avec le code généré
            if result["success"] and transformation_code:
                validation_ok = self.validate_variable(var_name, transformation_code, standard_name)

                if validation_ok:
                    self.increment_cleaned_count()
                    print(f"Variable {var_name} cleaned and validated")
                else:
                    print(f"WARNING: Variable {var_name} validation failed (check output above)")
                    # Ne pas incrementer cleaned_count
            else:
                print(f"ERROR: Failed to clean variable {var_name}")

        # 3. Finalize (si toutes les variables sont nettoyées)
        survey = self.get_survey_status()
        if survey["variables"]["pending"] == 0:
            print(f"\nStep 3: Finalizing survey...")
            self.call_agent("finalize-survey", {
                "survey_id": self.survey_id,
                "task": "finalize"
            })
            self.update_survey_field("status", "completed")
            print(f"\nSurvey {self.survey_id} completed!")
        else:
            print(f"\nSurvey not complete yet: {survey['variables']['pending']} variables pending")

        print(f"\n{'='*60}")
        print(f"Workflow completed")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Survey cleaning orchestrator")
    parser.add_argument("survey_id", help="Survey ID to clean")
    parser.add_argument("--limit", type=int, help="Limit number of variables to clean")
    parser.add_argument("--only-var", help="Clean only this specific variable")

    args = parser.parse_args()

    # Activate venv check
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("WARNING: Virtual environment not activated. Run 'source venv/bin/activate' first.")
        sys.exit(1)

    orchestrator = SurveyOrchestrator(args.survey_id, limit=args.limit, only_var=args.only_var)
    orchestrator.run_workflow()


if __name__ == "__main__":
    main()
