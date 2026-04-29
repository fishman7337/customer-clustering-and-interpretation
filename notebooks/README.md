# Notebooks

The full original analysis notebook is preserved here:

```text
notebooks/customer_segmentation_analysis.ipynb
```

For easier review, the same notebook content is also split into smaller phase notebooks
under `notebooks/sections/`. The split notebooks are derived artifacts; concatenating their
cells in filename order reproduces the full notebook content exactly.

## Split Notebooks

| File | Coverage |
| --- | --- |
| `sections/00_project_overview_and_imports.ipynb` | Project overview and import setup. |
| `sections/01_data_analysis_cleaning_feature_engineering.ipynb` | Data loading, analysis, cleaning, and feature engineering. |
| `sections/02_visualisation_and_scaling.ipynb` | Exploratory visualisations and feature scaling. |
| `sections/03_clustering_and_model_selection.ipynb` | K-Means, agglomerative clustering, DBSCAN, and model comparison. |
| `sections/04_cluster_interpretation_and_insights.ipynb` | Cluster interpretation and business insights. |

Regenerate the split notebooks with:

```powershell
python scripts/split_notebook.py
```
