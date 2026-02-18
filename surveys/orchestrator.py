#!/usr/bin/env python3
"""
Survey Cleaning Orchestrator v2

Hybrid architecture: Pattern Engine (Tier 1) + LLM Batch (Tier 2) + LLM Individual (Tier 3)

Routing logic (data-driven):
  1. Classify each variable using pattern_engine.classify()
  2. Tier 1: pattern match >= 0.8 confidence → generate code via pattern
  3. Tier 2: semi-standard variables → batch LLM (10-20 vars per call)
  4. Tier 3: complex cases → individual LLM

State management:
  - status.json tracks each variable: pending/in_progress/done
  - Resume after interruption supported

Usage:
    python surveys/orchestrator.py <survey_id>
    python surveys/orchestrator.py <survey_id> --limit 10
    python surveys/orchestrator.py <survey_id> --only-var <var_name>
    python surveys/orchestrator.py <survey_id> --dry-run
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import warnings
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)
logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
logging.getLogger("litellm").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)

import litellm

litellm.suppress_debug_info = True
litellm.telemetry = False

from dotenv import load_dotenv

load_dotenv(override=True)

from surveys.codebook_parser.parser import CodebookParser
from surveys.codebook_parser.schemas import CodebookSchema, VariableSchema
from surveys.llm_processors import (
    Batch,
    BatchingResult,
    Tier2BatchProcessor,
    VariableCode,
    create_batches,
    get_batch_stats,
    process_tier3_variable,
    process_tier3_batch,
)
from surveys.pattern_engine import (
    BasePattern,
    ClassificationResult,
    MissingCodeInfo,
    classify,
    get_all_patterns,
    get_default_matcher,
)


CONFIG = {
    "tier_1_min_confidence": 0.8,
    "tier_1_max_n_unique": 7,
    "tier_2_max_batch_size": 20,
    "dry_run": False,
    "verbose": True,
}


@dataclass
class VariableState:
    var_name: str
    status: str = "pending"
    tier: Optional[int] = None
    pattern_id: Optional[str] = None
    confidence: float = 0.0
    clean_var_name: Optional[str] = None
    code: Optional[str] = None
    error: Optional[str] = None
    processed_at: Optional[str] = None


@dataclass
class SurveyState:
    survey_id: str
    status: str = "not_started"
    created_date: Optional[str] = None
    data_file: Optional[str] = None
    n_observations: Optional[int] = None
    n_variables: Optional[int] = None
    variables: dict[str, VariableState] = field(default_factory=dict)
    last_updated: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "created_date": self.created_date,
            "data_file": self.data_file,
            "n_observations": self.n_observations,
            "n_variables": self.n_variables,
            "variables": {
                k: {
                    "status": v.status,
                    "tier": v.tier,
                    "pattern_id": v.pattern_id,
                    "confidence": v.confidence,
                    "clean_var_name": v.clean_var_name,
                    "code": v.code,
                    "error": v.error,
                    "processed_at": v.processed_at,
                }
                for k, v in self.variables.items()
            },
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, survey_id: str, data: dict) -> "SurveyState":
        state = cls(survey_id=survey_id)
        state.status = data.get("status", "not_started")
        state.created_date = data.get("created_date")
        state.data_file = data.get("data_file")
        state.n_observations = data.get("n_observations")
        state.n_variables = data.get("n_variables")
        state.last_updated = data.get("last_updated")

        vars_data = data.get("variables", {})
        if isinstance(vars_data, dict):
            if "cleaned_variables" in vars_data:
                total = vars_data.get("total", 0)
                cleaned_list = vars_data.get("cleaned_variables", [])
                state.variables = {
                    v: VariableState(var_name=v, status="done")
                    for v in cleaned_list
                }
            else:
                for var_name, vdata in vars_data.items():
                    if isinstance(vdata, dict):
                        state.variables[var_name] = VariableState(
                            var_name=var_name,
                            status=vdata.get("status", "pending"),
                            tier=vdata.get("tier"),
                            pattern_id=vdata.get("pattern_id"),
                            confidence=vdata.get("confidence", 0.0),
                            clean_var_name=vdata.get("clean_var_name"),
                            code=vdata.get("code"),
                            error=vdata.get("error"),
                            processed_at=vdata.get("processed_at"),
                        )
        return state


class OrchestratorV2:
    def __init__(
        self,
        survey_id: str,
        limit: Optional[int] = None,
        only_var: Optional[str] = None,
        model: Optional[str] = None,
        dry_run: bool = False,
        verbose: bool = True,
    ):
        self.survey_id = survey_id
        self.limit = limit
        self.only_var = only_var
        self.dry_run = dry_run
        self.verbose = verbose

        self.base_path = Path(__file__).parent
        self.survey_path = self.base_path / survey_id
        self.shared_folder = self.base_path.parent / "_SharedFolder_data_produit" / survey_id
        self.status_file = self.base_path / "status.json"

        self.model = model or os.getenv("DEFAULT_MODEL", "anthropic/claude-sonnet-4-20250514")

        self.state = self._load_state()
        self.codebook: Optional[CodebookSchema] = None
        self.patterns = get_all_patterns()
        self._pattern_map = {p.pattern_id: p for p in self.patterns}

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def _load_state(self) -> dict:
        if not self.status_file.exists():
            return {"surveys": {}}
        with open(self.status_file) as f:
            return json.load(f)

    def _save_state(self) -> None:
        with open(self.status_file, "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def _get_survey_state(self) -> SurveyState:
        survey_data = self.state.get("surveys", {}).get(self.survey_id, {})
        return SurveyState.from_dict(self.survey_id, survey_data)

    def _update_survey_state(self, survey_state: SurveyState) -> None:
        self.state.setdefault("surveys", {})[self.survey_id] = survey_state.to_dict()
        self.state["surveys"][self.survey_id]["last_updated"] = datetime.now().isoformat()
        self._save_state()

    def _load_codebook(self) -> Optional[CodebookSchema]:
        codebook_json = self.shared_folder / "codebook.json"
        if codebook_json.exists():
            self._log(f"Loading cached codebook: {codebook_json}")
            with open(codebook_json) as f:
                data = json.load(f)
            return CodebookSchema(**data)

        codebook_md = self.shared_folder / "codebook.md"
        if codebook_md.exists():
            self._log(f"Parsing codebook from markdown: {codebook_md}")
            parser = CodebookParser(
                survey_id=self.survey_id,
                data_dir=self.shared_folder.parent,
                codebook_path=codebook_md,
                verbose=self.verbose,
            )
            codebook = parser.parse()
            with open(codebook_json, "w") as f:
                f.write(codebook.model_dump_json(indent=2))
            return codebook

        codebook_candidates = list(self.shared_folder.glob("codebook*")) + list(
            self.shared_folder.glob("*codebook*")
        )
        for ext in [".xlsx", ".pdf", ".docx"]:
            codebook_candidates.extend(self.shared_folder.glob(f"*{ext}"))

        if codebook_candidates:
            self._log(f"Found codebook source: {codebook_candidates[0]}")
            parser = CodebookParser(
                survey_id=self.survey_id,
                data_dir=self.shared_folder.parent,
                codebook_path=codebook_candidates[0],
                verbose=self.verbose,
            )
            codebook = parser.parse()
            with open(codebook_json, "w") as f:
                f.write(codebook.model_dump_json(indent=2))
            return codebook

        self._log("No codebook found, will rely on data-driven classification")
        return None

    def _find_data_file(self) -> Optional[Path]:
        survey_state = self._get_survey_state()
        if survey_state.data_file:
            path = Path(survey_state.data_file)
            if path.exists():
                return path
            path = self.shared_folder / survey_state.data_file
            if path.exists():
                return path

        for ext in [".csv", ".sav", ".dta", ".xlsx"]:
            files = list(self.shared_folder.glob(f"*{ext}"))
            if files:
                return files[0]
        return None

    def _load_data(self, data_file: Path) -> pd.DataFrame:
        import pandas as pd

        self._log(f"Loading data: {data_file}")
        suffix = data_file.suffix.lower()

        if suffix == ".csv":
            return pd.read_csv(data_file)
        elif suffix == ".sav":
            import pyreadstat

            df, _ = pyreadstat.read_sav(data_file)
            return df
        elif suffix == ".dta":
            df = pd.read_stata(data_file)
            return df if isinstance(df, pd.DataFrame) else df.read()
        elif suffix in [".xlsx", ".xls"]:
            return pd.read_excel(data_file)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    def _initialize_survey(self, data_file: Path, df: pd.DataFrame) -> SurveyState:
        state = SurveyState(
            survey_id=self.survey_id,
            status="initialized",
            created_date=datetime.now().strftime("%Y-%m-%d"),
            data_file=str(data_file),
            n_observations=len(df),
            n_variables=len(df.columns),
            last_updated=datetime.now().isoformat(),
        )

        for col in df.columns:
            state.variables[col] = VariableState(var_name=col, status="pending")

        self._update_survey_state(state)
        self.survey_path.mkdir(parents=True, exist_ok=True)

        template = self.base_path / "_template" / "clean.py"
        target = self.survey_path / "clean.py"
        if template.exists() and not target.exists():
            import shutil

            shutil.copy(template, target)

        return state

    def _classify_variables(
        self, df: pd.DataFrame, survey_state: SurveyState
    ) -> dict[str, tuple[VariableSchema, ClassificationResult]]:
        classified: dict[str, tuple[VariableSchema, ClassificationResult]] = {}

        for var_name in df.columns:
            var_state = survey_state.variables.get(var_name, VariableState(var_name=var_name))

            if var_state.status == "done":
                continue

            var_schema: Optional[VariableSchema] = None
            if self.codebook:
                var_schema = self.codebook.get_variable(var_name)

            series: pd.Series = df[var_name]  # type: ignore[assignment]
            classification = classify(series, var_schema)

            var_state.tier = classification.tier
            var_state.pattern_id = classification.pattern_id
            var_state.confidence = classification.confidence
            survey_state.variables[var_name] = var_state

            if var_schema is None:
                var_schema = VariableSchema(
                    var_name=var_name,
                    var_label=var_name,
                    var_type="unknown",
                )

            classified[var_name] = (var_schema, classification)

        self._update_survey_state(survey_state)
        return classified

    def _process_tier1(
        self,
        var_name: str,
        var_schema: VariableSchema,
        classification: ClassificationResult,
        df: pd.DataFrame,
    ) -> Optional[str]:
        pattern_id = classification.pattern_id
        if not pattern_id or pattern_id not in self._pattern_map:
            return None

        pattern = self._pattern_map[pattern_id]
        clean_var_name = self._generate_clean_var_name(var_name, var_schema, pattern)

        code = pattern.generate_code(var_name, clean_var_name, var_schema)
        return code

    def _generate_clean_var_name(
        self, var_name: str, var_schema: VariableSchema, pattern: Optional[BasePattern] = None
    ) -> str:
        if pattern and pattern.pattern_type == "demographic":
            if "age" in var_name.lower() or "age" in var_schema.var_label.lower():
                return "ses_age_group"
            if "sex" in var_name.lower() or "gender" in var_name.lower():
                return "ses_gender"
            if "province" in var_name.lower():
                return "ses_province"
            if "region" in var_name.lower():
                return "ses_region"
            if "educ" in var_name.lower():
                return "ses_education"
            return f"ses_{var_name.lower()[:20]}"

        if pattern and pattern.pattern_type == "likert":
            return f"op_{var_name.lower()[:20]}"

        if pattern and pattern.pattern_type == "binary":
            return f"op_{var_name.lower()[:20]}"

        return f"op_{var_name.lower()[:20]}"

    def _process_tier2_batch(self, batch: Batch) -> dict[str, VariableCode]:
        processor = Tier2BatchProcessor(model=self.model)
        result = processor.process_batch(batch)
        return result.variables

    def _process_tier3_variable(
        self,
        var_name: str,
        var_schema: VariableSchema,
        classification: ClassificationResult,
        df: pd.DataFrame,
    ) -> str:
        sample_values = df[var_name].dropna().sample(min(20, len(df)), random_state=42).tolist()
        clean_var_name = self._generate_clean_var_name(
            var_name, var_schema,
            self._pattern_map.get(classification.pattern_id) if classification.pattern_id else None
        )

        result = process_tier3_variable(
            var_name=var_name,
            var=var_schema,
            classification=classification,
            sample_values=sample_values,
            clean_var_name=clean_var_name,
        )
        return result.python_code

    def _process_all(
        self,
        classified: dict[str, tuple[VariableSchema, ClassificationResult]],
        survey_state: SurveyState,
        df: pd.DataFrame,
        pending_vars: list[str],
    ) -> None:
        """Passe 2: traitement par tier avec vrai batching Tier 2.

        - Tier 1: traitement immédiat (déterministe)
        - Tier 2: regroupé via create_batches() → lots de 10-20 → un appel LLM par lot
        - Tier 3: traitement individuel (Claude Haiku)

        status.json est sauvegardé après chaque lot (pas après chaque variable).
        """
        # Filtrer les classified selon pending_vars
        pending_classified = {
            k: v for k, v in classified.items() if k in pending_vars
        }

        batching = create_batches(pending_classified)
        stats = get_batch_stats(batching)
        self._log(
            f"Batching: T1={stats['tier_1']['n_variables']} vars, "
            f"T2={stats['tier_2']['n_variables']} vars en {stats['tier_2']['n_batches']} lots, "
            f"T3={stats['tier_3']['n_variables']} vars"
        )

        if self.dry_run:
            for var_name, (_, classification) in pending_classified.items():
                self._log(
                    f"  [DRY RUN] {var_name}: tier={classification.tier}, "
                    f"pattern={classification.pattern_id}, confidence={classification.confidence:.2f}"
                )
            return

        # --- Tier 1: traitement immédiat ---
        tier1_vars_done = 0
        for batch in batching.tier_1_batches:
            for var_name, var_schema, classification in batch.variables:
                var_state = survey_state.variables.get(var_name, VariableState(var_name=var_name))
                var_state.status = "in_progress"
                survey_state.variables[var_name] = var_state

                code: Optional[str] = None
                error: Optional[str] = None
                try:
                    code = self._process_tier1(var_name, var_schema, classification, df)
                except Exception as e:
                    error = str(e)
                    self._log(f"  Tier 1 ERROR {var_name}: {error}")

                var_state.code = code
                var_state.error = error
                var_state.status = "done" if code and not error else "error"
                var_state.processed_at = datetime.now().isoformat()
                survey_state.variables[var_name] = var_state
                tier1_vars_done += 1

            # Sauvegarde après chaque batch Tier 1
            self._update_survey_state(survey_state)
            self._log(f"  Tier 1: {tier1_vars_done} variables traitées")

        # --- Tier 2: batching réel ---
        for batch in batching.tier_2_batches:
            batch_var_names = [v[0] for v in batch.variables]
            self._log(f"\n  Tier 2 lot {batch.batch_index + 1}/{len(batching.tier_2_batches)}: {len(batch_var_names)} variables")

            # Marquer toutes les variables du lot in_progress
            for var_name, var_schema, classification in batch.variables:
                var_state = survey_state.variables.get(var_name, VariableState(var_name=var_name))
                var_state.status = "in_progress"
                survey_state.variables[var_name] = var_state

            try:
                results = self._process_tier2_batch(batch)

                # results est keyé par clean_var_name; construire index inversé par original_var_name
                by_original: dict[str, VariableCode] = {
                    vc.original_var_name: vc
                    for vc in results.values()
                    if vc.original_var_name
                }

                for var_name, var_schema, classification in batch.variables:
                    var_state = survey_state.variables[var_name]
                    vc = by_original.get(var_name) or results.get(var_name)
                    if vc:
                        var_state.code = vc.code
                        var_state.clean_var_name = vc.clean_var_name
                        var_state.status = "done"
                        self._log(f"    ✓ {var_name}")
                    else:
                        var_state.error = "No result from batch processor"
                        var_state.status = "error"
                        self._log(f"    ✗ {var_name}: no result")
                    var_state.processed_at = datetime.now().isoformat()
                    survey_state.variables[var_name] = var_state

            except Exception as e:
                error_msg = str(e)
                self._log(f"  Tier 2 lot ERROR: {error_msg}")
                for var_name, _, _ in batch.variables:
                    var_state = survey_state.variables.get(var_name, VariableState(var_name=var_name))
                    var_state.error = error_msg
                    var_state.status = "error"
                    var_state.processed_at = datetime.now().isoformat()
                    survey_state.variables[var_name] = var_state

            # Sauvegarde après chaque lot Tier 2
            self._update_survey_state(survey_state)

        # --- Tier 3: traitement individuel ---
        for i, batch in enumerate(batching.tier_3_batches, 1):
            var_name, var_schema, classification = batch.variables[0]
            self._log(f"\n  Tier 3 [{i}/{len(batching.tier_3_batches)}] {var_name}")

            var_state = survey_state.variables.get(var_name, VariableState(var_name=var_name))
            var_state.status = "in_progress"
            survey_state.variables[var_name] = var_state

            code = None
            error = None
            try:
                code = self._process_tier3_variable(var_name, var_schema, classification, df)
            except Exception as e:
                error = str(e)
                self._log(f"    ERROR: {error}")

            var_state.code = code
            var_state.error = error
            var_state.status = "done" if code and not error else "error"
            var_state.processed_at = datetime.now().isoformat()
            survey_state.variables[var_name] = var_state

            # Sauvegarde après chaque variable Tier 3
            self._update_survey_state(survey_state)

    def _assemble_clean_py(self, survey_state: SurveyState) -> str:
        lines = [
            '"""Auto-generated cleaning script."""',
            "",
            "import numpy as np",
            "import pandas as pd",
            "",
            "",
            "def clean(df: pd.DataFrame) -> pd.DataFrame:",
            '    """Transform raw survey data to cleaned variables."""',
            "    df_clean = pd.DataFrame(index=df.index)",
            "",
        ]

        sorted_vars = sorted(
            survey_state.variables.items(),
            key=lambda x: (x[1].tier or 99, x[0]),
        )

        for var_name, var_state in sorted_vars:
            if var_state.status != "done" or not var_state.code:
                continue

            lines.append(f"    # {var_name} (Tier {var_state.tier}, confidence: {var_state.confidence:.2f})")
            for line in var_state.code.strip().split("\n"):
                lines.append(f"    {line}")
            lines.append("")

        lines.extend([
            "    return df_clean",
            "",
            "",
            "if __name__ == '__main__':",
            "    import sys",
            "    df = pd.read_csv(sys.argv[1]) if sys.argv[1].endswith('.csv') else pd.read_excel(sys.argv[1])",
            "    df_clean = clean(df)",
            f'    df_clean.to_csv("{self.survey_id}_cleaned.csv", index=False)',
            '    print(f"Saved {len(df_clean.columns)} cleaned variables")',
            "",
        ])

        return "\n".join(lines)

    def run(self) -> None:
        self._log(f"\n{'='*60}")
        self._log(f"OrchestratorV2: {self.survey_id}")
        self._log(f"{'='*60}\n")

        data_file = self._find_data_file()
        if not data_file:
            self._log(f"ERROR: No data file found in {self.shared_folder}")
            return

        df = self._load_data(data_file)
        survey_state = self._get_survey_state()

        if survey_state.status == "not_started" or not survey_state.variables:
            survey_state = self._initialize_survey(data_file, df)

        self.codebook = self._load_codebook()

        self._log(f"Dataset: {len(df)} rows, {len(df.columns)} variables")
        if self.codebook:
            self._log(f"Codebook: {self.codebook.n_variables} variables")

        classified = self._classify_variables(df, survey_state)

        tier_counts = {1: 0, 2: 0, 3: 0}
        for var_name, (_, classification) in classified.items():
            tier_counts[classification.tier] += 1
        self._log(f"Classification: Tier 1={tier_counts[1]}, Tier 2={tier_counts[2]}, Tier 3={tier_counts[3]}")

        pending_vars = [
            v for v in classified.keys()
            if survey_state.variables.get(v, VariableState(var_name=v)).status != "done"
        ]

        if self.only_var:
            if self.only_var not in pending_vars:
                self._log(f"Variable {self.only_var} not found or already done")
                return
            pending_vars = [self.only_var]
        elif self.limit:
            pending_vars = pending_vars[:self.limit]

        self._log(f"Processing {len(pending_vars)} variables (two-pass: classify → batch)...")

        self._process_all(classified, survey_state, df, pending_vars)

        done_count = sum(1 for v in survey_state.variables.values() if v.status == "done")
        total_count = len(survey_state.variables)
        self._log(f"\nProgress: {done_count}/{total_count} variables done")

        if done_count == total_count:
            survey_state.status = "completed"
            clean_py = self._assemble_clean_py(survey_state)
            target = self.survey_path / "clean.py"
            with open(target, "w") as f:
                f.write(clean_py)
            self._log(f"Generated: {target}")
        else:
            survey_state.status = "in_progress"

        self._update_survey_state(survey_state)
        self._log(f"\n{'='*60}")
        self._log(f"Done: {survey_state.status}")
        self._log(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Survey Cleaning Orchestrator v2")
    parser.add_argument("survey_id", help="Survey ID to clean")
    parser.add_argument("--limit", type=int, help="Limit number of variables to process")
    parser.add_argument("--only-var", help="Process only this variable")
    parser.add_argument("--model", help="LLM model for Tier 2/3")
    parser.add_argument("--dry-run", action="store_true", help="Classify only, don't generate code")
    parser.add_argument("--quiet", action="store_true", help="Suppress output")

    args = parser.parse_args()

    if not hasattr(sys, "real_prefix") and not (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("WARNING: Virtual environment not activated. Run 'source venv/bin/activate' first.")
        sys.exit(1)

    orchestrator = OrchestratorV2(
        survey_id=args.survey_id,
        limit=args.limit,
        only_var=args.only_var,
        model=args.model,
        dry_run=args.dry_run,
        verbose=not args.quiet,
    )
    orchestrator.run()


if __name__ == "__main__":
    main()
