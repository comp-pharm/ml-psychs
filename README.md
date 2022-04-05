# [WIP] ml-psychs

This repository is for scripts related to retraining [ChemProp](https://github.com/chemprop/chemprop) on 5-HT2A receptor bioassays, and using the resulting model for drug discovery. 

## Layout

The project is laid out according to the [Cookiecutter Data Science layout](https://drivendata.github.io/cookiecutter-data-science/).
Raw data from PubChem lives in `data/raw/`, script for turning that data into interim data for feeding into the model (`data/interim`) live in `src/data`.
Notebooks for exploratory data analysis live in `notebooks`.

## Data

Originally trained with [PubChem bioassay 1706](https://pubchem.ncbi.nlm.nih.gov/bioassay/1706), which has hundreds of thousands of negative examples but only a few hundred low-quality positive examples.
Now training with [PubChem bioassay 624381](https://pubchem.ncbi.nlm.nih.gov/bioassay/624381), which is a much higher quality (confirmation) assay that more closely matches the antibiotic discovery search which was the first application for chemprop.

## Training

Training with the original, large dataset only achieves ~63% accuracy, with all efforts put into intelligent data splitting, feature engineering, ensembling, etc. all _worsening_ performance. 
Training with the new dataset naively gets 94.8% accuracy with the default ChemProp hyperparemeters, and can achieve >96% accuracy with RDKit generated features, hyperparameter tuning, and ensembling enabled. 

| Description                                                   | Results        |
|---------------------------------------------------------------|----------------|
| Old data, default hyperparameters, no added features          | auc = 0.630919 |
| New data, default hyperparameters, no added features          | auc = 0.948752 |
| New data, default hyperparameters, rdkit features             | auc = 0.954657 |
| New data, default hyperparameters, rdkit features, 5-ensemble | auc = 0.955548 |
| New data, tuned hyperparameters, no added features            | auc = 0.955770 |
| New data, tuned hyperparameters, rdkit features, 5-ensemble   | auc = 0.963235 |
