"""Split the preserved full analysis notebook into smaller phase notebooks."""

from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_NOTEBOOK = ROOT / "notebooks" / "customer_segmentation_analysis.ipynb"
OUTPUT_DIR = ROOT / "notebooks" / "sections"

SPLITS = [
    {
        "filename": "00_project_overview_and_imports.ipynb",
        "title": "Project overview and imports",
        "start": 0,
        "end": 21,
    },
    {
        "filename": "01_data_analysis_cleaning_feature_engineering.ipynb",
        "title": "Data analysis, cleaning, and feature engineering",
        "start": 21,
        "end": 85,
    },
    {
        "filename": "02_visualisation_and_scaling.ipynb",
        "title": "Data visualisation and feature scaling",
        "start": 85,
        "end": 129,
    },
    {
        "filename": "03_clustering_and_model_selection.ipynb",
        "title": "Clustering and model selection",
        "start": 129,
        "end": 203,
    },
    {
        "filename": "04_cluster_interpretation_and_insights.ipynb",
        "title": "Cluster interpretation and business insights",
        "start": 203,
        "end": None,
    },
]


def load_notebook(path: Path) -> dict:
    """Load a notebook as JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_notebook(path: Path, notebook: dict) -> None:
    """Write a notebook with deterministic JSON formatting."""
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def split_notebook() -> list[Path]:
    """Create smaller notebooks while preserving original cells exactly."""
    source = load_notebook(SOURCE_NOTEBOOK)
    cells = source["cells"]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    written_paths = []
    for split in SPLITS:
        section = copy.deepcopy(source)
        section["cells"] = copy.deepcopy(cells[split["start"] : split["end"]])
        section.setdefault("metadata", {})["split_from"] = {
            "source": str(SOURCE_NOTEBOOK.relative_to(ROOT)).replace("\\", "/"),
            "title": split["title"],
            "cell_start": split["start"],
            "cell_end": split["end"] if split["end"] is not None else len(cells),
        }

        output_path = OUTPUT_DIR / split["filename"]
        write_notebook(output_path, section)
        written_paths.append(output_path)

    return written_paths


if __name__ == "__main__":
    for path in split_notebook():
        print(path.relative_to(ROOT))
