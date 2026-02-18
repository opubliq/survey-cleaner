#!/usr/bin/env python3
"""Generate pattern_library.json from all pattern classes.

This script:
1. Instantiates all pattern classes
2. Calls to_pattern() on each to get Pydantic Pattern
3. Assembles into PatternLibrary
4. Writes to pattern_library.json

Run this after modifying patterns to keep JSON in sync.
"""

import json
from pathlib import Path

from surveys.pattern_engine.patterns import get_all_patterns
from surveys.pattern_engine.schemas.pattern_schema import PatternLibrary


def generate_pattern_library(output_path: Path) -> None:
    patterns = get_all_patterns()
    library = PatternLibrary(patterns=[p.to_pattern() for p in patterns])

    output_path.write_text(
        json.dumps(library.model_dump(mode="json"), indent=2, ensure_ascii=False)
    )
    print(f"Generated {len(library.patterns)} patterns to {output_path}")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_path = project_root / "surveys" / "pattern_engine" / "pattern_library.json"
    generate_pattern_library(output_path)
