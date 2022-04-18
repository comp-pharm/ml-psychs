import pandas as pd


def make_drh_data():
    """
    Take the raw Drug Repurposing Hub sample data and turn into list of CSV's to run model against.
    """

    drh_data = pd.read_csv("../../data/raw/repurposing_samples_20200324.txt", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8],
                           sep='\t')
    drh_data.drop(drh_data.columns.difference(["smiles", "broad_id"]), 1, inplace=True)
    drh_data.drop_duplicates(subset=["smiles"], inplace=True, ignore_index=True)

    drh_data.to_csv("../../data/interim/repurposing_SMILES_to_broad.csv", index=False)
    drh_data[["smiles"]].to_csv("../../data/interim/repurposing_SMILES.csv", index=False)


def stitch_results():
    """
    Take the results CSV and stitch back together with Broad ID's.
    """
    results = pd.read_csv("../../data/output/drh/raw_results.csv")
    broad_ids = pd.read_csv("../../data/interim/repurposing_SMILES_to_broad.csv")
    joined_results = results.set_index("smiles").join(broad_ids.set_index("smiles"))
    joined_results.sort_values(by=["PUBCHEM_ACTIVITY_OUTCOME"], inplace=True, ascending=False)
    joined_results.to_csv("../../data/output/drh/results.csv")


if __name__ == "__main__":
    stitch_results()
