#!/usr/bin/env python3
"""
pipeline.py — Orchestrateur v3 du pipeline de nettoyage de sondages.

Usage:
    python surveys/pipeline.py <survey_id>
    python surveys/pipeline.py eeq_2007
    python surveys/pipeline.py eeq_2007 --vars q2 q3 nomx   # subset de variables
    python surveys/pipeline.py eeq_2007 --skip-validate      # skip étape validation
"""

import argparse
import json
import subprocess
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

SURVEYS_DIR = Path(__file__).parent
REPO_ROOT = SURVEYS_DIR.parent
SHARED_FOLDER = REPO_ROOT / "_SharedFolder_data_produit"


# ============================================================================
# Helpers
# ============================================================================

def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def run_agent(agent: str, prompt: str, survey_id: str, tag: str) -> str:
    """
    Appelle `opencode run --agent <agent> --format json <prompt>`.
    Capture le sessionID depuis le premier event JSON.
    Exporte la session dans surveys/{survey_id}/logs/{tag}_{session_id}.json.
    Retourne le sessionID.
    """
    logs_dir = SURVEYS_DIR / survey_id / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["opencode", "run", "--agent", agent, "--format", "json", prompt]
    log(f"  → agent={agent} tag={tag}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Extraire le sessionID du premier event JSON valide
    session_id = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
            session_id = event.get("sessionID")
            if session_id:
                break
        except json.JSONDecodeError:
            continue

    if result.returncode != 0:
        log(f"  [ERREUR] agent={agent} tag={tag} rc={result.returncode}")
        if result.stderr:
            print(result.stderr[:500], file=sys.stderr)

    # Exporter la session pour debug
    if session_id:
        export_session(session_id, logs_dir, tag)
    else:
        log(f"  [WARN] Pas de sessionID pour {tag} — export impossible")

    return session_id or ""


def export_session(session_id: str, logs_dir: Path, tag: str) -> None:
    """Exporte la session opencode en JSON dans logs/."""
    out_path = logs_dir / f"{tag}_{session_id}.json"
    export = subprocess.run(
        ["opencode", "export", session_id],
        capture_output=True, text=True,
    )
    if export.returncode == 0:
        out_path.write_text(export.stdout, encoding="utf-8")
        log(f"  [log] {out_path.relative_to(REPO_ROOT)}")
    else:
        log(f"  [WARN] Export session {session_id} échoué")


# ============================================================================
# Étapes du pipeline
# ============================================================================

def parse_codebook(survey_id: str) -> None:
    """Étape 1 — Appelle l'agent transform-codebook → codebook.json."""
    log(f"[1/5] parse_codebook({survey_id})")
    prompt = json.dumps({
        "survey_id": survey_id,
        "shared_folder": str(SHARED_FOLDER),
        "surveys_dir": str(SURVEYS_DIR),
    })
    run_agent("transform-codebook", prompt, survey_id, "transform-codebook")


def clean_variable(survey_id: str, variable_name: str) -> str:
    """Étape 2 — Appelle l'agent clean-variable pour UNE variable."""
    ctx_path = SURVEYS_DIR / survey_id / "vars" / f"ctx_{variable_name}.json"
    if not ctx_path.exists():
        log(f"  [WARN] Pas de ctx_{variable_name}.json — clean-variable utilisera codebook.json")
        prompt = json.dumps({
            "survey_id": survey_id,
            "variable_name": variable_name,
            "surveys_dir": str(SURVEYS_DIR),
        })
    else:
        prompt = ctx_path.read_text(encoding="utf-8")

    tag = f"clean-variable_{variable_name}"
    return run_agent("clean-variable", prompt, survey_id, tag)


def clean_all_variables(survey_id: str, variables: list[str], max_workers: int = 4) -> None:
    """Étape 2 — Nettoie toutes les variables en parallèle."""
    log(f"[2/5] clean_variable x{len(variables)} (max_workers={max_workers})")
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(clean_variable, survey_id, var): var
            for var in variables
        }
        for fut in as_completed(futures):
            var = futures[fut]
            try:
                fut.result()
                log(f"  [ok] {var}")
            except Exception as exc:
                log(f"  [ERREUR] {var}: {exc}")


def assemble(survey_id: str) -> None:
    """
    Étape 3 — Assemble tous les vars/*.py en un clean.py complet.
    Concatène les fichiers vars/*.py dans le corps de clean_data().
    """
    log(f"[3/5] assemble({survey_id})")
    survey_dir = SURVEYS_DIR / survey_id
    vars_dir = survey_dir / "vars"
    var_files = sorted(vars_dir.glob("*.py")) if vars_dir.exists() else []

    if not var_files:
        log("  [WARN] Aucun fichier vars/*.py trouvé — clean.py non généré")
        return

    template_path = SURVEYS_DIR / "_template" / "clean.py"
    template = template_path.read_text(encoding="utf-8")

    # Construire le bloc de nettoyage à partir des vars/*.py
    var_blocks = []
    for vf in var_files:
        var_blocks.append(f"    # --- {vf.stem} ---")
        for line in vf.read_text(encoding="utf-8").splitlines():
            var_blocks.append("    " + line if line.strip() else "")
        var_blocks.append("")

    injected = "\n".join(var_blocks)

    # Remplacer le placeholder TODO dans le template
    placeholder = (
        "    # ========================================================================\n"
        "    # TODO: Ajouter le code de nettoyage pour chaque variable ci-dessous\n"
        "    # Pattern: nettoyage variable → entrée CODEBOOK_VARIABLES → prochaine variable\n"
        "    # ========================================================================\n"
    )
    if placeholder in template:
        clean_py = template.replace(placeholder, injected + "\n")
    else:
        # Fallback: insérer avant le return df_clean
        clean_py = template.replace("    return df_clean", injected + "\n    return df_clean")

    # Remplacer les placeholders du template
    clean_py = clean_py.replace("[SURVEY_ID]", survey_id).replace("[NOM_SONDAGE]", survey_id)

    out_path = survey_dir / "clean.py"
    out_path.write_text(clean_py, encoding="utf-8")
    log(f"  [ok] {out_path.relative_to(REPO_ROOT)} ({len(var_files)} variables)")


def validate_all_variables(survey_id: str, variables: list[str], max_workers: int = 4) -> None:
    """Étape 4 (optionnelle) — Valide chaque vars/*.py via l'agent validate-cleaning."""
    log(f"[4/5] validate x{len(variables)} (max_workers={max_workers})")

    def _validate_one(var: str) -> str:
        ctx_path = SURVEYS_DIR / survey_id / "vars" / f"ctx_{var}.json"
        prompt = str(ctx_path) if ctx_path.exists() else json.dumps({
            "survey_id": survey_id, "variable_name": var,
        })
        tag = f"validate_{var}"
        return run_agent("validate-cleaning", prompt, survey_id, tag)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_validate_one, var): var for var in variables}
        for fut in as_completed(futures):
            var = futures[fut]
            try:
                fut.result()
                log(f"  [ok] {var}")
            except Exception as exc:
                log(f"  [ERREUR] {var}: {exc}")


def finalize(survey_id: str) -> None:
    """Étape 5 — Appelle l'agent finalize-survey → met status.json à 'completed'."""
    log(f"[5/5] finalize({survey_id})")
    prompt = json.dumps({"survey_id": survey_id, "surveys_dir": str(SURVEYS_DIR)})
    run_agent("finalize-survey", prompt, survey_id, "finalize-survey")


# ============================================================================
# CLI
# ============================================================================

def get_variables_from_codebook(survey_id: str) -> list[str]:
    """Lit codebook.json et retourne la liste des noms de variables brutes."""
    cb_path = SURVEYS_DIR / survey_id / "codebook.json"
    if not cb_path.exists():
        log(f"  [WARN] codebook.json introuvable dans {survey_id}/")
        return []
    data = json.loads(cb_path.read_text(encoding="utf-8"))
    return list(data.get("variables", {}).keys())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline v3 — nettoyage complet d'un sondage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Exemples:
              python surveys/pipeline.py eeq_2007
              python surveys/pipeline.py eeq_2007 --vars q2 q3 nomx
              python surveys/pipeline.py eeq_2007 --skip-codebook --skip-validate
        """),
    )
    parser.add_argument("survey_id", help="ID du sondage (ex: eeq_2007)")
    parser.add_argument("--vars", nargs="+", metavar="VAR",
                        help="Subset de variables à nettoyer (défaut: toutes depuis codebook.json)")
    parser.add_argument("--skip-codebook", action="store_true",
                        help="Sauter l'étape transform-codebook (codebook.json déjà présent)")
    parser.add_argument("--skip-validate", action="store_true",
                        help="Sauter l'étape validate-cleaning")
    parser.add_argument("--skip-finalize", action="store_true",
                        help="Sauter l'étape finalize-survey")
    parser.add_argument("--workers", type=int, default=4,
                        help="Nombre de threads parallèles (défaut: 4)")
    args = parser.parse_args()

    survey_id = args.survey_id
    log(f"=== Pipeline v3 : {survey_id} ===")

    # 1. Codebook
    if not args.skip_codebook:
        parse_codebook(survey_id)
    else:
        log("[1/5] parse_codebook — skipped")

    # 2. Variables à nettoyer
    variables = args.vars or get_variables_from_codebook(survey_id)
    if not variables:
        log("[ERREUR] Aucune variable à nettoyer. Fournir --vars ou générer codebook.json d'abord.")
        sys.exit(1)
    log(f"  Variables: {variables}")
    clean_all_variables(survey_id, variables, max_workers=args.workers)

    # 3. Assemble
    assemble(survey_id)

    # 4. Validate
    if not args.skip_validate:
        validate_all_variables(survey_id, variables, max_workers=args.workers)
    else:
        log("[4/5] validate — skipped")

    # 5. Finalize
    if not args.skip_finalize:
        finalize(survey_id)
    else:
        log("[5/5] finalize — skipped")

    log(f"=== Done : {survey_id} ===")


if __name__ == "__main__":
    main()
