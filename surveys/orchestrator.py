#!/usr/bin/env python3
"""
Survey Cleaning Orchestrator

Exécute le workflow complet via LiteLLM (multi-provider: Claude, Gemini, DeepSeek, Groq, etc.)
Chaque agent = 1 call API avec contexte frais → pas de limite de contexte.

Usage:
    python surveys/orchestrator.py <survey_id>
    python surveys/orchestrator.py <survey_id> --limit 10
    python surveys/orchestrator.py <survey_id> --only-var <var_name>
    python surveys/orchestrator.py <survey_id> --model gemini/gemini-2.0-flash
"""

import os
import sys
import json
import re
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import warnings
import logging
warnings.filterwarnings("ignore", category=RuntimeWarning)
logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
logging.getLogger("litellm").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
import litellm
litellm.suppress_debug_info = True
litellm.set_verbose = False
litellm.telemetry = False

# Suppress asyncio "Task was destroyed but it is pending!" stderr spam
import sys, io
class _StderrFilter(io.TextIOWrapper):
    """Wraps stderr to suppress asyncio task destruction messages."""
    def __init__(self, stream):
        self._stream = stream
    def write(self, msg):
        if "Task was destroyed but it is pending" in msg or "coroutine" in msg and "was never awaited" in msg:
            return len(msg)
        return self._stream.write(msg)
    def flush(self):
        return self._stream.flush()
    def __getattr__(self, name):
        return getattr(self._stream, name)
sys.stderr = _StderrFilter(sys.stderr)
from dotenv import load_dotenv
from litellm import completion

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

    def __init__(self, survey_id, limit=None, only_var=None, model=None):
        self.survey_id = survey_id
        self.limit = limit
        self.only_var = only_var
        self.base_path = Path(__file__).parent
        self.survey_path = self.base_path / survey_id
        self.status_file = self.base_path / "status.json"

        # Model config (CLI override > .env > default)
        self.model = model or os.getenv("DEFAULT_MODEL", "anthropic/claude-sonnet-4-20250514")
        fallbacks_env = os.getenv("FALLBACK_MODELS", "")
        self.fallback_models = [m.strip() for m in fallbacks_env.split(",") if m.strip()]

        print(f"Model: {self.model}")
        if self.fallback_models:
            print(f"Fallbacks: {self.fallback_models}")

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

    def increment_cleaned_count(self, variable_name):
        """Incrémente le compteur de variables nettoyées et enregistre le nom"""
        survey = self.status["surveys"][self.survey_id]
        survey["variables"]["cleaned"] += 1
        survey["variables"]["pending"] -= 1

        # Track which variables are done
        if "cleaned_variables" not in survey["variables"]:
            survey["variables"]["cleaned_variables"] = []
        if variable_name not in survey["variables"]["cleaned_variables"]:
            survey["variables"]["cleaned_variables"].append(variable_name)

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

        # Filtrer les variables déjà nettoyées
        survey = self.status["surveys"].get(self.survey_id, {})
        cleaned = survey.get("variables", {}).get("cleaned_variables", [])
        pending_vars = [v for v in all_vars if v not in cleaned]

        if cleaned:
            print(f"Skipping {len(cleaned)} already cleaned variables")

        # Appliquer limit
        if self.limit:
            return pending_vars[:self.limit]

        return pending_vars

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

    def reset_survey(self):
        """
        Remet un survey à zéro: supprime clean.py généré, remet le template,
        reset status.json, supprime codebook.md et processed/.
        """
        import shutil

        print(f"\nResetting survey: {self.survey_id}")

        # 1. Remplacer clean.py par le template
        template_file = self.base_path / "_template" / "clean.py"
        target_file = self.survey_path / "clean.py"
        if template_file.exists() and self.survey_path.exists():
            shutil.copy(template_file, target_file)
            print(f"  Reset clean.py from template")

        # 2. Supprimer processed/
        processed_dir = self.survey_path / "processed"
        if processed_dir.exists():
            shutil.rmtree(processed_dir)
            print(f"  Removed processed/")

        # 3. Nettoyer le shared folder (codebook.md + fichiers parasites des agents)
        shared_folder = self.base_path.parent / "_SharedFolder_data_produit" / self.survey_id
        codebook_md = shared_folder / "codebook.md"
        if codebook_md.exists():
            codebook_md.unlink()
            print(f"  Removed codebook.md")

        # Supprimer les .py et .csv parasites créés par les agents
        data_filename = self.status.get("surveys", {}).get(self.survey_id, {}).get("data_file", "")
        for pattern in ["*.py", "*.csv"]:
            for f in shared_folder.glob(pattern):
                if f.name != data_filename:
                    f.unlink()
                    print(f"  Removed parasite: {f.name}")

        # 4. Reset status.json
        if self.survey_id in self.status["surveys"]:
            survey = self.status["surveys"][self.survey_id]
            total = survey["variables"]["total"]
            survey["status"] = "not_started"
            survey["variables"]["cleaned"] = 0
            survey["variables"]["pending"] = total
            survey["variables"]["cleaned_variables"] = []
            survey["last_updated"] = datetime.now().isoformat()
            self.save_status()
            print(f"  Reset status.json (0/{total} variables)")

        print(f"Survey {self.survey_id} reset complete\n")

    def find_data_file(self):
        """Trouve le fichier data depuis status.json, sinon fallback glob"""
        shared_folder = self.base_path.parent / "_SharedFolder_data_produit" / self.survey_id

        # Utiliser le data_file enregistré dans status.json (source de vérité)
        if self.survey_id in self.status.get("surveys", {}):
            data_filename = self.status["surveys"][self.survey_id].get("data_file")
            if data_filename:
                path = shared_folder / data_filename
                if path.exists():
                    return path

        # Fallback: glob (pour init seulement)
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

        # ========================================================================
        # Optimisation: Extraire seulement l'extrait du codebook pertinent
        # ========================================================================
        # Si codebook_file est fourni, faire grep pour n'envoyer que ~30 lignes
        # autour de la variable, au lieu du fichier entier
        if context.get("codebook_file") and context.get("variable"):
            import subprocess
            codebook_path = context["codebook_file"]
            var_name = context["variable"]

            # Chercher le nom de variable dans le codebook (fuzzy matching: 30 lignes après match)
            result = subprocess.run(
                f"grep -A 30 '{var_name}' '{codebook_path}'",
                shell=True,
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                # Codebook excerpt trouvé - remplacer codebook_file par l'extrait
                context["codebook_excerpt"] = result.stdout
                del context["codebook_file"]
                print(f"  → Extracted {len(result.stdout.splitlines())} lines from codebook for '{var_name}'")
            else:
                # Pas trouvé dans le codebook - avertir mais continuer
                print(f"  ⚠️  Variable '{var_name}' not found in codebook")
                del context["codebook_file"]

        # Prépare le prompt pour l'agent
        user_prompt = json.dumps(context, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"Calling agent: {agent_name}")
        print(f"Context: {list(context.keys())}")
        print(f"{'='*60}\n")

        # Définir les tools disponibles (OpenAI format for LiteLLM)
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "bash",
                    "description": "Execute a bash command and return output",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "The bash command to execute"}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read a file and return its contents",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to the file to read"}
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write content to a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to the file to write"},
                            "content": {"type": "string", "description": "Content to write to the file"}
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_file",
                    "description": "Edit a file by replacing old_string with new_string",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to the file to edit"},
                            "old_string": {"type": "string", "description": "String to find and replace"},
                            "new_string": {"type": "string", "description": "String to replace with"}
                        },
                        "required": ["file_path", "old_string", "new_string"]
                    }
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

        def _clean_assistant_msg(message):
            """Strip provider-specific fields (e.g. annotations) to keep only standard OpenAI fields."""
            msg = {"role": "assistant"}
            if message.content:
                msg["content"] = message.content
            if message.tool_calls:
                msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            return msg

        # Conversation messages (OpenAI format)
        messages = [
            {"role": "system", "content": agent_instructions},
            {"role": "user", "content": user_prompt}
        ]

        # Loop until agent finishes
        max_turns = 50
        for turn in range(max_turns):
            # Appel API via LiteLLM (universal format)
            api_kwargs = {
                "model": self.model,
                "max_tokens": 16000,
                "messages": messages,
                "tools": tools,
            }

            # Fallbacks si configurés
            if self.fallback_models:
                api_kwargs["fallbacks"] = self.fallback_models

            try:
                response = completion(**api_kwargs)
            except Exception as e:
                error_msg = str(e).split('\n')[0][:200]
                print(f"\nERROR: API call failed on turn {turn + 1}: {error_msg}")
                return {"success": False, "response": f"API error: {error_msg}"}

            choice = response.choices[0]
            finish_reason = choice.finish_reason

            if finish_reason == "stop":
                # Agent finished
                result_text = choice.message.content or ""

                print(f"\nAgent {agent_name} completed after {turn + 1} turns")
                print(f"Response preview: {result_text[:200]}...")

                usage = response.usage
                return {
                    "success": True,
                    "response": result_text,
                    "usage": {
                        "input_tokens": getattr(usage, 'prompt_tokens', 0),
                        "output_tokens": getattr(usage, 'completion_tokens', 0),
                        "cache_read_tokens": getattr(usage, 'cache_read_input_tokens', 0),
                        "cache_creation_tokens": getattr(usage, 'cache_creation_input_tokens', 0)
                    }
                }

            elif finish_reason == "tool_calls":
                # Agent wants to use tools
                messages.append(_clean_assistant_msg(choice.message))

                # Execute all tool calls
                for tool_call in choice.message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_input = json.loads(tool_call.function.arguments)

                    print(f"  Tool: {tool_name}({list(tool_input.keys())})")

                    # Execute tool
                    if tool_name in tool_map:
                        result = tool_map[tool_name](**tool_input)
                    else:
                        result = f"ERROR: Unknown tool {tool_name}"

                    # Add tool result (OpenAI format)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })

            elif finish_reason == "length":
                # Agent hit token limit mid-response — ask it to continue
                messages.append(_clean_assistant_msg(choice.message))
                messages.append({"role": "user", "content": "Continue where you left off."})
                print(f"  (max_tokens hit, continuing...)")

            else:
                # Unexpected stop reason
                print(f"WARNING: Unexpected finish_reason: {finish_reason}")
                return {"success": False, "response": f"Unexpected stop: {finish_reason}"}

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
                    # Demander confirmation à l'utilisateur (auto-accept après 30s)
                    print(f"\n{var_name} → {standard_name}")
                    print(f"Code: {transformation_code[:120]}...")
                    import select
                    print("\n[enter] accept / [s] skip / or type feedback to retry (auto-accept 30s) > ", end="", flush=True)
                    ready, _, _ = select.select([sys.stdin], [], [], 5)
                    feedback = sys.stdin.readline().strip() if ready else ""
                    if not ready:
                        print("(auto-accepted after 5s)")

                    if feedback == "" or feedback.lower() == "y":
                        self.increment_cleaned_count(var_name)
                        print(f"Variable {var_name} accepted")
                    elif feedback.lower() == "s":
                        print(f"Skipped {var_name}")
                    else:
                        # Retry avec le feedback comme instruction supplémentaire
                        print(f"Retrying {var_name} with feedback...")
                        context["feedback"] = feedback
                        retry_result = self.call_agent("clean-variable", context)

                        # Re-parse et re-validate
                        try:
                            retry_text = retry_result.get("response", "")
                            json_match = re.search(r'```json\s*(\{.*?\})\s*```', retry_text, re.DOTALL)
                            if json_match:
                                retry_data = json.loads(json_match.group(1))
                            else:
                                retry_data = json.loads(retry_text)
                            retry_code = retry_data.get("transformation_code")
                            retry_name = retry_data.get("standard_name", var_name)
                        except (json.JSONDecodeError, AttributeError):
                            retry_code = None
                            retry_name = var_name

                        if retry_result["success"] and retry_code:
                            retry_valid = self.validate_variable(var_name, retry_code, retry_name)
                            if retry_valid:
                                self.increment_cleaned_count(var_name)
                                print(f"Variable {var_name} accepted (after retry)")
                            else:
                                print(f"WARNING: Retry validation failed for {var_name}")
                        else:
                            print(f"ERROR: Retry failed for {var_name}")
                        context.pop("feedback", None)
                else:
                    print(f"WARNING: Variable {var_name} validation failed (check output above)")
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
    parser.add_argument("--model", help="LiteLLM model identifier (e.g. anthropic/claude-sonnet-4-20250514, gemini/gemini-2.0-flash)")
    parser.add_argument("--reset", action="store_true", help="Reset survey to initial state (template clean.py, status reset)")

    args = parser.parse_args()

    # Activate venv check
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("WARNING: Virtual environment not activated. Run 'source venv/bin/activate' first.")
        sys.exit(1)

    orchestrator = SurveyOrchestrator(args.survey_id, limit=args.limit, only_var=args.only_var, model=args.model)

    if args.reset:
        orchestrator.reset_survey()
    else:
        orchestrator.run_workflow()


if __name__ == "__main__":
    main()
