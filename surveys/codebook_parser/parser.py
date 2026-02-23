"""Codebook Parser — entrée principale.

Détecte le format du fichier codebook et délègue à la stratégie appropriée.

Stratégies disponibles:
  - XLSX: parsing direct openpyxl (SPSS 2-feuilles, liste simple, index sheet)
  - PDF:  extraction texte → regex pour SPSS-export, ou LLM pour les autres
  - DOCX: parsing direct python-docx (table govcan POR003 ou prose)
  - MD:   lecture directe du markdown structuré

Usage:
    from surveys.codebook_parser.parser import CodebookParser

    parser = CodebookParser(survey_id="eeq_2022", data_dir=Path("_SharedFolder_data_produit"))
    codebook = parser.parse()           # CodebookSchema
    codebook_json = codebook.model_dump_json(indent=2)
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path
from typing import Optional

from .schemas import CodebookSchema, SurveyMetadata, VariableSchema

# Extensions reconnues comme codebooks (pas de données brutes)
_CODEBOOK_EXTENSIONS = {".pdf", ".xlsx", ".md", ".txt", ".docx", ".doc"}

# Noms de fichiers courants à exclure (données, pas codebooks)
_DATA_EXTENSIONS = {".csv", ".sav", ".dta", ".sav", ".xlsx"}
_DATA_NAME_HINTS = {"base de données", "data", "données", "dataset", "spss"}


class CodebookNotFoundError(FileNotFoundError):
    pass


class UnsupportedFormatError(ValueError):
    pass


class CodebookParser:
    """Point d'entrée unique pour parser un codebook quelle que soit sa forme.

    Args:
        survey_id: Identifiant du sondage (= nom du dossier dans data_dir).
        data_dir:  Chemin vers _SharedFolder_data_produit/.
        codebook_path: Chemin explicite vers le fichier codebook (optionnel).
                       Si non fourni, auto-détection dans data_dir/survey_id/.
        llm_model: Modèle LiteLLM à utiliser pour les cas complexes (PDF non-SPSS, .doc).
                   Ex: "openrouter/mistralai/mistral-7b-instruct:free"
        verbose: Affiche les étapes de parsing sur stdout.
    """

    DEFAULT_LLM_MODEL = "openrouter/mistralai/mistral-7b-instruct:free"

    def __init__(
        self,
        survey_id: str,
        data_dir: Path | str,
        codebook_path: Optional[Path | str] = None,
        llm_model: Optional[str] = None,
        verbose: bool = False,
    ):
        self.survey_id = survey_id
        self.data_dir = Path(data_dir)
        self.verbose = verbose
        self.llm_model = llm_model or os.getenv("CODEBOOK_LLM_MODEL", self.DEFAULT_LLM_MODEL)

        if codebook_path:
            self.codebook_path = Path(codebook_path)
        else:
            self.codebook_path = self._auto_detect_codebook()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self) -> CodebookSchema:
        """Parse le codebook et retourne un CodebookSchema validé."""
        ext = self.codebook_path.suffix.lower()
        self._log(f"Parsing {self.codebook_path.name} (format: {ext})")

        if ext == ".xlsx":
            from .strategies.xlsx_parser import parse_xlsx
            variables, notes = parse_xlsx(self.codebook_path, verbose=self.verbose)
        elif ext == ".pdf":
            from .strategies.pdf_parser import parse_pdf
            variables, notes = parse_pdf(
                self.codebook_path, llm_model=self.llm_model, verbose=self.verbose
            )
        elif ext in (".docx", ".doc"):
            from .strategies.docx_parser import parse_docx
            variables, notes = parse_docx(
                self.codebook_path, llm_model=self.llm_model, verbose=self.verbose
            )
        elif ext in (".md", ".txt"):
            from .strategies.md_parser import parse_md
            variables, notes = parse_md(self.codebook_path, verbose=self.verbose)
        else:
            raise UnsupportedFormatError(
                f"Format non supporté: {ext}. "
                f"Formats acceptés: {', '.join(sorted(_CODEBOOK_EXTENSIONS))}"
            )

        metadata = SurveyMetadata(
            survey_id=self.survey_id,
            source_file=self.codebook_path.name,
            source_format=ext.lstrip("."),
            parsed_date=date.today().isoformat(),
            parser_model=self.llm_model if ext in (".pdf", ".doc") else None,
            notes=notes or None,
        )

        codebook = CodebookSchema(metadata=metadata, variables=variables)
        self._log(
            f"Done: {codebook.n_variables} variables parsed "
            f"({len(codebook.low_confidence_variables())} low-confidence)"
        )
        return codebook

    # ------------------------------------------------------------------
    # Auto-detection
    # ------------------------------------------------------------------

    def _auto_detect_codebook(self) -> Path:
        """Cherche le fichier codebook dans data_dir/survey_id/.

        Priorité:
          1. Fichiers dont le nom contient 'codebook', 'livre de codes', 'livredescode',
             'variable information', 'data dictionary', 'data-dictionary'
          2. Fichiers .md existants (déjà générés)
          3. Fichiers PDF (souvent le codebook dans les vieux sondages)
          4. Fichiers .docx / .doc
          5. Fichiers .xlsx qui ne sont PAS clairement des données brutes

        Raises:
            CodebookNotFoundError: si aucun fichier candidat trouvé.
        """
        survey_dir = self.data_dir / self.survey_id
        if not survey_dir.exists():
            raise CodebookNotFoundError(
                f"Survey directory not found: {survey_dir}"
            )

        # Collecte tous les fichiers avec une extension reconnue
        candidates: list[Path] = []
        for p in survey_dir.iterdir():
            if p.is_file() and p.suffix.lower() in _CODEBOOK_EXTENSIONS:
                candidates.append(p)

        if not candidates:
            raise CodebookNotFoundError(
                f"No codebook file found in {survey_dir}. "
                f"Supported: {', '.join(sorted(_CODEBOOK_EXTENSIONS))}"
            )

        # Score de priorité pour chaque candidat
        def _priority(p: Path) -> int:
            name = p.name.lower()
            ext = p.suffix.lower()
            score = 0

            # Mots-clés de codebook dans le nom
            codebook_hints = [
                "codebook", "livre de codes", "livredescode",
                "variable information", "data dictionary", "data-dictionary",
                "variable-information", "données",
            ]
            if any(h in name for h in codebook_hints):
                score += 100

            # Format: .md déjà structuré = idéal
            if ext == ".md":
                score += 50
            elif ext == ".docx":
                score += 30
            elif ext == ".pdf":
                score += 20
            elif ext == ".xlsx":
                # Pénaliser si le nom suggère des données brutes
                if any(h in name for h in _DATA_NAME_HINTS):
                    score -= 50
                else:
                    score += 10

            return score

        best = max(candidates, key=_priority)
        self._log(f"Auto-detected codebook: {best.name}")

        # Si le meilleur candidat a un score négatif, aucun codebook fiable
        if _priority(best) < 0:
            raise CodebookNotFoundError(
                f"Could not reliably identify a codebook in {survey_dir}. "
                f"Files found: {[p.name for p in candidates]}. "
                f"Provide codebook_path explicitly."
            )

        return best

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(f"[codebook_parser] {msg}")
