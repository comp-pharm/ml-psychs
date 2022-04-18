# [WIP] ml-psychs

This repository is for scripts related to retraining [ChemProp](https://github.com/chemprop/chemprop) on 5-HT2A receptor bioassays, and using the resulting model for drug discovery. 

## Layout

The project is laid out according to the [Cookiecutter Data Science layout](https://drivendata.github.io/cookiecutter-data-science/).
Raw data from PubChem lives in `data/raw/`, script for turning that data into interim data for feeding into the model (`data/interim`) live in `src/data`.
Notebooks for exploratory data analysis live in `notebooks/`.

## Data

Originally trained with [PubChem bioassay 1706](https://pubchem.ncbi.nlm.nih.gov/bioassay/1706), which has hundreds of thousands of negative examples but only a few hundred low-quality positive examples.
Now training with [PubChem bioassay 624381](https://pubchem.ncbi.nlm.nih.gov/bioassay/624381), which is a much higher quality (confirmation) assay that more closely matches the [antibiotic discovery search which was the first application for chemprop](https://www.cell.com/cell/fulltext/S0092-8674(20)30102-1).

## Training

Training with the original, large dataset only achieves ~63% accuracy, with all efforts put into intelligent data splitting, feature engineering, ensembling, etc. all _worsening_ performance. 
Training with the smaller dataset naively gets 94.8% accuracy with the default ChemProp hyperparemeters, and can achieve >96% accuracy with RDKit generated features, hyperparameter tuning, and ensembling enabled. 

| Description                                                       | Results        |
|-------------------------------------------------------------------|----------------|
| Old data, default hyperparameters, no added features              | auc = 0.630919 |
| Smaller data, default hyperparameters, no added features          | auc = 0.948752 |
| Smaller data, default hyperparameters, rdkit features             | auc = 0.954657 |
| Smaller data, default hyperparameters, rdkit features, 5-ensemble | auc = 0.955548 |
| Smaller data, tuned hyperparameters, no added features            | auc = 0.955770 |
| Smaller data, tuned hyperparameters, rdkit features, 5-ensemble   | auc = 0.963235 |
| Augmented data, default hyperparameters, no added features        | auc = 0.942714 |
| Augmented data, default hyperparameters, rdkit features           | auc = 0.947792 |

<details>
    <summary>Full results from old data</summary>

| Data Split           | Hyperparameters         | Results                                                                                                                                                                                 |
|----------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Default random split | Default hyperparameters | Model 0 test auc = 0.630919 Ensemble test auc = 0.630919 1-fold cross validation         Seed 0 ==> test auc = 0.630919 Overall test auc = 0.630919 +/- 0.000000 Elapsed time = 3:07:13 |
| Manual split         | Default hyperparameters | Model 0 test auc = 0.596546 Ensemble test auc = 0.596546 1-fold cross validation         Seed 0 ==> test auc = 0.596546 Overall test auc = 0.596546 +/- 0.000000 Elapsed time = 2:39:13 |
| scaffold_balanced    | Default hyperparameters | Model 0 test auc = 0.627393 Ensemble test auc = 0.627393 1-fold cross validation         Seed 0 ==> test auc = 0.627393 Overall test auc = 0.627393 +/- 0.000000 Elapsed time = 2:42:57 |
| Random split with 98/1/1 split size | Default hyperparameters | Model 0 test auc = 0.704176 Ensemble test auc = 0.704176 1-fold cross validation 	Seed 0 ==> test auc = 0.704176 Overall test auc = 0.704176 +/- 0.000000 Elapsed time = 2:00:14 | 
| Default random split | Default with rdkit features | Model 0 test auc = 0.616364 Ensemble test auc = 0.616364 1-fold cross validation         Seed 0 ==> test auc = 0.616364 Overall test auc = 0.616364 +/- 0.000000 Elapsed time = 6:53:38 |
| Random split with 98/1/1 split size | Default hyperparameters with rdkit | Model 0 test auc = 0.555728 Ensemble test auc = 0.555728 1-fold cross validation 	Seed 0 ==> test auc = 0.555728 Overall test auc = 0.555728 +/- 0.000000 Elapsed time = 7:00:45 |
| Default random split | Default with class balance | Model 0 test auc = 0.614006 Ensemble test auc = 0.614006 1-fold cross validation 	Seed 0 ==> test auc = 0.614006 Overall test auc = 0.614006 +/- 0.000000 Elapsed time = 0:11:56 | 
| Default random split | Default with 100 epochs | Model 0 test auc = 0.620170 Ensemble test auc = 0.620170 1-fold cross validation 	Seed 0 ==> test auc = 0.620170 Overall test auc = 0.620170 +/- 0.000000 Elapsed time = 5:24:05 | 
| Default random split | Default with 3 ensemble | Model 2 test auc = 0.620461 Ensemble test auc = 0.629669 1-fold cross validation 	Seed 0 ==> test auc = 0.629669 Overall test auc = 0.629669 +/- 0.000000 Elapsed time = 4:52:46 | 
| Default random split | {'depth': 2, 'dropout': 0.0, 'ffn_num_layers': 3, 'hidden_size': 2400} | Model 0 test auc = 0.617250 Ensemble test auc = 0.617250 1-fold cross validation 	Seed 0 ==> test auc = 0.617250 Overall test auc = 0.617250 +/- 0.000000 Elapsed time = 4:52:37 |
| Default random split | Above, with rdkit features | Model 0 test auc = 0.601644 Ensemble test auc = 0.601644 1-fold cross validation 	Seed 0 ==> test auc = 0.601644 Overall test auc = 0.601644 +/- 0.000000 Elapsed time = 9:52:27 |
| Default random split | Default with 5 ensemble | Ensemble test auc = 0.622447 1-fold cross validation 	Seed 0 ==> test auc = 0.622447 Overall test auc = 0.622447 +/- 0.000000 Elapsed time = 8:09:57 |
| Default random split | Default with 5 ensemble and rdkit freatures | Model 4 test auc = 0.606309 Ensemble test auc = 0.616090 1-fold cross validation 	Seed 0 ==> test auc = 0.616090 Overall test auc = 0.616090 +/- 0.000000 Elapsed time = 15:13:30 |
| scaffold_balanced with 98/1/1 split size | Default hyperparameters | Model 0 test auc = 0.751387 Ensemble test auc = 0.751387 1-fold cross validation 	Seed 0 ==> test auc = 0.751387 Overall test auc = 0.751387 +/- 0.000000 Elapsed time = 1:30:36 |
</details>

## Prediction

Running predictions on the Broad Institute Drug Repurposing Hub dataset reveals mediocre results. 
The old data had extremely reasonable output from the DRH dataset, top predictions were Dihydroergotamine and Pergolide.
The new data outputs some reasonable values, but includes several long-chain alcohols as extremely likely candidates. 

TODO: Supplement the new dataset with negatives from the old dataset unlike compounds that are in the new dataset.