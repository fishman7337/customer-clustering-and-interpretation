# Model Card

## Model Summary

The reusable training pipeline fits a K-Means clustering model to customer demographic and
spending features. The default configuration uses six clusters to align with the original
notebook analysis.

## Intended Use

- Segment customers into interpretable groups.
- Support exploratory business recommendations.
- Demonstrate unsupervised learning, preprocessing, and model evaluation practices.

## Not Intended For

- Automated decisions that materially affect people.
- Production personalization without further validation.
- Sensitive demographic inference.
- High-stakes financial, employment, insurance, or eligibility decisions.

## Features

The trained package model uses:

- `Age`
- `Income (k$)`
- `How Much They Spend`

`Gender` is validated and preserved for analysis, but it is not used by the default K-Means
training pipeline.

## Evaluation Metrics

The CLI exports:

- Silhouette score
- Davies-Bouldin score
- Calinski-Harabasz score
- K-Means inertia
- Number of samples
- Number of clusters

## Limitations

- Clustering is sensitive to scaling, outlier handling, and the selected number of clusters.
- Clusters describe patterns in the provided dataset, not universal customer behavior.
- The model does not establish causality.
- Evaluation metrics for unsupervised learning are only proxies for business usefulness.

## Ethical Notes

Segmentation should be used to improve service quality and customer understanding. It
should not be used to discriminate, exclude, or unfairly target customers.
