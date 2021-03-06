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

## Training
`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --save_dir models/default_run/` 

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --split_sizes 0.98 0.01 0.01 --save_dir models/default_run_98_data_split/`

`chemprop_train --data_path data/interim/train_SMILES_to_Activity.csv --separate_val_path data/interim/val_SMILES_to_Activity.csv --separate_test_path data/interim/test_SMILES_to_Activity.csv  --dataset_type classification --save_dir models/stratified_data_default_hp`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --features_generator rdkit_2d_normalized --no_features_scaling --save_dir models/default_augmented_rdkit/`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --split_sizes 0.98 0.01 0.01 --features_generator rdkit_2d_normalized --no_features_scaling --save_dir models/rdkit_98_data_split/`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --save_dir models/class_balance/ --class_balance` 

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --save_dir models/100_epochs/ --epochs 100`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --save_dir models/3_ensemble/ --ensemble_size 3`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --save_dir models/rkdit_hyper/ --config_path models/20hyper --features_generator rdkit_2d_normalized --no_features_scaling`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --save_dir models/5_ensemble/ --ensemble_size 5`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --save_dir models/rdkit_5_ensemble/ --features_generator rdkit_2d_normalized --no_features_scaling --ensemble_size 5`

`chemprop_train --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --split_sizes 0.98 0.01 0.01 --split_type scaffold_balanced --save_dir models/scaffold_balanced_98_data_split/`


### Results

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

 


## Hyperparameter optimization

`chemprop_hyperopt --data_path data/interim/SMILES_to_Activity.csv --dataset_type classification --num_iters 20 --config_save_path models/20hyper`

100%|██| 20/20 [78:42:25<00:00, 14167.28s/trial, best loss: -0.6172501081853173]
best
{'depth': 2, 'dropout': 0.0, 'ffn_num_layers': 3, 'hidden_size': 2400}
num params: 23,721,601
0.6172501081853173 +/- 0.0 auc
Elapsed time = 3 days, 6:42:26

`chemprop_hyperopt --data_path data/interim/SMILES_to_Activity.csv --split_sizes 0.98 0.01 0.01 --dataset_type classification --num_iters 20 --features_generator rdkit_2d_normalized --no_features_scaling --config_save_path models/rdkit_hyper_98`

100%|██| 20/20 [191:07:01<00:00, 34401.09s/trial, best loss: -0.6363898102082182]
best
{'depth': 6, 'dropout': 0.05, 'ffn_num_layers': 2, 'hidden_size': 1800}
num params: 10,589,401
0.6363898102082182 +/- 0.0 auc
Elapsed time = 7 days, 23:07:02



## Prediction

`chemprop_predict --test_path data/interim/repurposing_SMILES.csv --checkpoint_dir models/default_run/ --preds_path data/output/raw_results.csv`