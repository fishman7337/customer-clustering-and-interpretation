# Section Notebooks

This folder contains smaller notebooks derived from the full original notebook at:

```text
notebooks/customer_segmentation_analysis.ipynb
```

The section notebooks preserve the original cells in order. The pytest suite includes a
check that concatenating these notebooks reproduces the full notebook cells exactly.

Regenerate these files with:

```powershell
python scripts/split_notebook.py
```
