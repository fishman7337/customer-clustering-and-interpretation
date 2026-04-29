from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL_NOTEBOOK = ROOT / "notebooks" / "customer_segmentation_analysis.ipynb"
SECTION_NOTEBOOKS = [
    ROOT / "notebooks" / "sections" / "00_project_overview_and_imports.ipynb",
    ROOT / "notebooks" / "sections" / "01_data_analysis_cleaning_feature_engineering.ipynb",
    ROOT / "notebooks" / "sections" / "02_visualisation_and_scaling.ipynb",
    ROOT / "notebooks" / "sections" / "03_clustering_and_model_selection.ipynb",
    ROOT / "notebooks" / "sections" / "04_cluster_interpretation_and_insights.ipynb",
]


def load_cells(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["cells"]


def test_split_notebooks_preserve_original_notebook_cells_in_order() -> None:
    original_cells = load_cells(FULL_NOTEBOOK)
    split_cells = []
    for path in SECTION_NOTEBOOKS:
        split_cells.extend(load_cells(path))

    assert split_cells == original_cells
