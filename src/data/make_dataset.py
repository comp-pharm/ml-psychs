import pandas as pd


def make_data():
    # Load the SID to Activity data
    datatable = pd.read_csv("../../data/raw/AID_624169_datatable.csv", skiprows=[1, 2, 3, 4])
    sid_to_outcome = datatable[["PUBCHEM_SID", "PUBCHEM_ACTIVITY_OUTCOME"]]
    sid_to_outcome = sid_to_outcome.replace(
        {"PUBCHEM_ACTIVITY_OUTCOME": {"Inactive": 0, "Active": 1}}
    )

    # Load the SID to SMILES data
    smiles = pd.read_csv("../../data/raw/SID_to_SMILES.txt", sep='\t', names=["PUBCHEM_SID", "SMILES"])

    # Create the SMILES to SID data
    data = pd.merge(sid_to_outcome, smiles, how="inner", on="PUBCHEM_SID")
    data.dropna(inplace=True)  # One SID has no SMILES string, drop it
    data.drop("PUBCHEM_SID", axis=1, inplace=True)  # Drop the SID column as we are done with it
    data = data[["SMILES", "PUBCHEM_ACTIVITY_OUTCOME"]]  # Reorder

    data.to_csv("../../data/interim/SMILES_to_Activity.csv", index=False)


if __name__ == "__main__":
    make_data()
