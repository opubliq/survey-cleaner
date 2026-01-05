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
import argparse
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic


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
        if survey_id not in self.status["surveys"]:
            raise ValueError(f"Survey {survey_id} not found in status.json. Run /init-survey first.")

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
        elif data_file.suffix == '.xlsx':
            df = pd.read_excel(data_file, nrows=1)
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

    def find_data_file(self):
        """Trouve le fichier data.csv/xlsx dans _SharedFolder_data_produit"""
        shared_folder = self.base_path.parent / "_SharedFolder_data_produit" / self.survey_id

        for ext in ['.csv', '.xlsx', '.xls']:
            files = list(shared_folder.glob(f"*{ext}"))
            if files:
                return files[0]
        return None

    def call_agent(self, agent_name, context):
        """
        Fait un appel API à un agent spécialisé.

        Args:
            agent_name: Nom de l'agent (survey-init, clean-variable, etc.)
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
        print(f"🤖 Calling agent: {agent_name}")
        print(f"📝 Context: {list(context.keys())}")
        print(f"{'='*60}\n")

        # Appel API avec prompt caching
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
            system=[
                {
                    "type": "text",
                    "text": agent_instructions,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )

        # Extract text response
        result_text = ""
        for block in response.content:
            if block.type == "text":
                result_text += block.text

        print(f"\n✅ Agent {agent_name} completed")
        print(f"📄 Response preview: {result_text[:200]}...")

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

    def run_workflow(self):
        """Exécute le workflow complet"""

        print(f"\n{'='*60}")
        print(f"🚀 Starting survey cleaning workflow")
        print(f"📊 Survey: {self.survey_id}")
        print(f"{'='*60}\n")

        survey = self.get_survey_status()
        total_vars = survey["variables"]["total"]

        # 1. Transform codebook (si pas déjà fait)
        codebook_md = self.base_path.parent / "_SharedFolder_data_produit" / self.survey_id / "codebook.md"
        if not codebook_md.exists():
            print("📖 Step 1: Transforming codebook...")
            self.call_agent("transform-codebook", {
                "survey_id": self.survey_id,
                "task": "transform_codebook"
            })
        else:
            print("✅ Step 1: Codebook already exists, skipping...")

        # 2. Clean variables (loop avec contexte frais à chaque fois)
        print(f"\n🧹 Step 2: Cleaning variables...")
        pending_vars = self.get_pending_variables()

        print(f"📊 Variables to clean: {len(pending_vars)}/{total_vars}")

        for i, var_name in enumerate(pending_vars, 1):
            print(f"\n--- Variable {i}/{len(pending_vars)}: {var_name} ---")

            # Appel API avec contexte frais
            result = self.call_agent("clean-variable", {
                "survey_id": self.survey_id,
                "variable": var_name,
                "task": "clean_variable"
            })

            # Update status
            if result["success"]:
                self.increment_cleaned_count()
                print(f"✅ Variable {var_name} cleaned successfully")
            else:
                print(f"❌ Failed to clean variable {var_name}")

        # 3. Finalize (si toutes les variables sont nettoyées)
        survey = self.get_survey_status()
        if survey["variables"]["pending"] == 0:
            print(f"\n🎉 Step 3: Finalizing survey...")
            self.call_agent("finalize-survey", {
                "survey_id": self.survey_id,
                "task": "finalize"
            })
            self.update_survey_field("status", "completed")
            print(f"\n✅ Survey {self.survey_id} completed!")
        else:
            print(f"\n⏸️  Survey not complete yet: {survey['variables']['pending']} variables pending")

        print(f"\n{'='*60}")
        print(f"✅ Workflow completed")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Survey cleaning orchestrator")
    parser.add_argument("survey_id", help="Survey ID to clean")
    parser.add_argument("--limit", type=int, help="Limit number of variables to clean")
    parser.add_argument("--only-var", help="Clean only this specific variable")

    args = parser.parse_args()

    # Activate venv check
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not activated. Run 'source venv/bin/activate' first.")
        sys.exit(1)

    orchestrator = SurveyOrchestrator(args.survey_id, limit=args.limit, only_var=args.only_var)
    orchestrator.run_workflow()


if __name__ == "__main__":
    main()
