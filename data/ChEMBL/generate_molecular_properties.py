from pathlib import Path

import chembl_downloader
import pandas as pd

CHEMBL_VERSION = "34"
CSV_PATH = Path(__file__).resolve().parent / "chembl_molecule_properties.csv.gz"


def generate_chembl_molecule_properties():
    chembl_path = chembl_downloader.download_extract_sqlite(version=CHEMBL_VERSION)
    print(f"ChEMBL SQLite file available at {chembl_path}")

    sql = """
    SELECT
        md.chembl_id,
        md.pref_name,
        md.molecule_type,
        md.therapeutic_flag,
        md.max_phase,
        md.indication_class,
        md.indication_class,
        md.oral,
        md.topical,
        md.prodrug,
        md.withdrawn_flag,
        
        cs.canonical_smiles,
        cs.standard_inchi,
        cs.standard_inchi_key,
        
        cp.cx_logd,
        cp.cx_logp,
        cp.cx_most_apka,
        cp.cx_most_bpka
        
    FROM molecule_dictionary AS md
    LEFT JOIN compound_structures AS cs ON md.molregno == cs.molregno
    LEFT JOIN compound_properties AS cp ON md.molregno == cp.molregno
    """

    df = chembl_downloader.query(sql, version=CHEMBL_VERSION)
    print(len(df.chembl_id), len(set(df.chembl_id)))
    print(f"Saving {len(df)} molecules to {CSV_PATH}")
    df.to_csv(CSV_PATH, index=False)


def get_molecular_properties() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH)


if __name__ == '__main__':
    generate_chembl_molecule_properties()
    df = get_molecular_properties()
    print(f"{len(df)} molecule properties available from ChEMBL (v.{CHEMBL_VERSION})")
