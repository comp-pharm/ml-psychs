# [WIP] ml-psychs

This repository is for scripts related to retraining [ChemProp](https://github.com/chemprop/chemprop) on [a serotonin receptor bioassay](https://pubchem.ncbi.nlm.nih.gov/bioassay/624169). 

The two files in `data/raw/` are manually downloaded from [the PubChem page for the bioassay](https://pubchem.ncbi.nlm.nih.gov/bioassay/1706).
`AID_6234169_datatable.csv` is from the "Deposited Data Table Only" link, and `SID_to_SMILES.txt` is from the "Tested Compounds Structures" link.

The file `src/data/make_dataset.py` has two functions to take that raw data and turn it into cleaned data ready for ingestion into the model.
The `make_data` function takes the two raw files and creates `data/interim/SMILES_to_Activity.csv`, which is the full data set of SMILES strings to binary activity data for classification. 
The script could easily be modified to save the numerical data for regression instead of classification, ChemProp supports both.
The `split_data` function splits the data set into _stratified_ train/validate/test sets. 
ChemProp can automatically take `SMILES_to_Activity.csv` and split it into the relevant sets, but it does so fully randomly.
This is a problem because only 0.66% of the dataset is positive results (compounds that are 5-HT2A agonists), the rest are negatives. 
To achieve better results we want to stratify the data sets so the appropriate number of active compounds end up in each of the sets, and not all of the positive compounds are in the test set. 

### Training
`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --save_dir models/default_run/` 

`chemprop_train --data_path data/interim/train_SMILES_to_Activity.csv --separate_val_path data/interim/val_SMILES_to_Activity.csv --separate_test_path data/interim/test_SMILES_to_Activity.csv  --dataset_type classification --save_dir models/stratified_data_default_hp`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --features_generator rdkit_2d_normalized --no_features_scaling --save_dir models/default_augmented_rdkit/`
### Results

| Data Split           | Hyperparameters         | Results                                                                                                                                                                                 |
|----------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Default random split | Default hyperparameters | Model 0 test auc = 0.630919 Ensemble test auc = 0.630919 1-fold cross validation         Seed 0 ==> test auc = 0.630919 Overall test auc = 0.630919 +/- 0.000000 Elapsed time = 3:07:13 |
| Manual split         | Default hyperparameters | Model 0 test auc = 0.596546 Ensemble test auc = 0.596546 1-fold cross validation         Seed 0 ==> test auc = 0.596546 Overall test auc = 0.596546 +/- 0.000000 Elapsed time = 2:39:13 |
| scaffold_balanced    | Default hyperparameters | Model 0 test auc = 0.627393 Ensemble test auc = 0.627393 1-fold cross validation         Seed 0 ==> test auc = 0.627393 Overall test auc = 0.627393 +/- 0.000000 Elapsed time = 2:42:57 |
| Default random split | Default with rdkit features | Model 0 test auc = 0.616364 Ensemble test auc = 0.616364 1-fold cross validation         Seed 0 ==> test auc = 0.616364 Overall test auc = 0.616364 +/- 0.000000 Elapsed time = 6:53:38 | 


