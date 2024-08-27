from pathlib import Path
import pandas as pd

# Arachne.ai (https://arachne.ai) is a proprietary biomedical data operations package.
import arachne

CHEMBL_VERSION = "chembl_33"
CHEMBL_MOL_PROPERTIES_FILE = Path(__file__).parent / "chembl_mol_properties.csv.gz"


def main():
    def _generate():
        for m in arachne.get_dataset("ChEMBL/Molecules", CHEMBL_VERSION, return_format="dict"):
            d = {
                "chembl_id": m["chembl_id"],
                "pref_name": m["pref_name"],
                # The fields below are for model analysis.
                "molecule_type": m["molecule_type"],
                "therapeutic_flag": m["therapeutic_flag"],
                "max_phase": m["max_phase"],
                "indication_class": m["indication_class"],
                "oral": m["oral"],
                "topical": m["topical"],
                "prodrug": m["prodrug"],
                "withdrawn_flag": m["withdrawn_flag"],
            }
            if len(m["compound_structures"]) > 0:
                for cs in ["canonical_smiles", "standard_inchi", "standard_inchi_key"]:
                    d[cs] = m["compound_structures"][0][cs]
            if len(m["compound_properties"]) > 0:
                for cp in ["cx_logd", "cx_logp", "cx_most_apka", "cx_most_bpka"]:
                    d[cp] = m["compound_properties"][0][cp]
            yield d

    df_chembl_molecule_properties = pd.DataFrame(_generate())
    assert len(df_chembl_molecule_properties) > 2_000_000
    df_chembl_molecule_properties.to_csv(CHEMBL_MOL_PROPERTIES_FILE, index=False)


def get_chembl_properties():
    pass


if __name__ == "__main__":
    main()
