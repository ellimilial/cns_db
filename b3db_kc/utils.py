import logging
from functools import cache
from pathlib import Path

import chembl_structure_pipeline
import datamol
import pandas as pd
import rdkit
from molfeat.trans import FPVecTransformer
from rdkit.Chem import rdFingerprintGenerator, Descriptors

LOGGER = logging.getLogger(__file__)

@cache
def smiles_to_mol(smiles, verbose=False):
    with datamol.without_rdkit_log():
        mol = rdkit.Chem.MolFromSmiles(smiles)
        if mol is None:
            mol_sanitisation = datamol.to_mol(smiles, sanitize=False)
            if not mol_sanitisation:
                if verbose:
                    print(f"Could not parse SMILES {smiles}")
                return None

            mol_sanitisation = datamol.fix_valence(mol_sanitisation)
            if mol_sanitisation is None:
                if verbose:
                    print(f"Failed to fix valence of SMILES: {smiles}")
                return None

            mol_sanitisation = datamol.sanitize_mol(mol_sanitisation)
            if mol_sanitisation is None:
                if verbose:
                    print(f"Failed to sanitise SMILES: {smiles} ")
                return None

            return mol_sanitisation
        return mol


# TODO Since ECFP4 fingerprints represent 2D fragments, they are not ideal of normalisation due
#  to ignoring stereochemistry information.
@cache
def get_ecfp4_count_fingerprint(smiles):
    mol = smiles_to_mol(smiles)
    mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    return mfpgen.GetCountFingerprint(mol) if mol else None


def get_tanimoto_distance(smiles1, smiles2):
    f1 = get_ecfp4_count_fingerprint(smiles1)
    f2 = get_ecfp4_count_fingerprint(smiles2)
    if not (f1 and f2):
        return 0
    return rdkit.DataStructs.TanimotoSimilarity(f1, f2)


@cache
def chembl_parent_from_smiles(smi):
    if pd.isna(smi):
        return None, None
    mol = smiles_to_mol(smi)
    if not mol:
        return None, None
    with datamol.without_rdkit_log():
        smi_parent, exclude = chembl_structure_pipeline.get_parent_mol(mol)
    return rdkit.Chem.MolToSmiles(smi_parent), exclude


def smiles_to_fingerprint_tuple(smi):
    if pd.isna(smi):
        return None
    return tuple(get_ecfp4_count_fingerprint(smi).ToList())


def calculate_cns_mpo_score_wager_2010(c_log_p, c_log_d, mw, tpsa, hbd, pka):
    def _monotonic_decreasing(val, lower, upper):
        return 1 if val <= lower else 0 if val > upper else 1 - (val - lower) / (upper - lower)

    def _hump(val, lower, lower_peak, upper_peak, upper):
        if val <= lower:
            return 0
        elif val <= lower_peak:
            return (val - lower) / (lower_peak - lower)
        elif val <= upper_peak:
            return 1
        elif val <= upper:
            return 1 - (val - upper_peak) / (upper - upper_peak)
        else:
            return 0

    return sum([
        _monotonic_decreasing(c_log_p, 3, 5),
        _monotonic_decreasing(c_log_d, 2, 4),
        _monotonic_decreasing(mw, 360, 500),
        _hump(tpsa, 20, 40, 90, 120),
        _monotonic_decreasing(hbd, 0.5, 3.5),
        _monotonic_decreasing(pka, 8, 10),
    ])


def calculate_balanced_permeability_index_weiss_2024(c_log_d, psa, hac):
    """
    c_log_d is the logD at 7.4. Authors use experimentally - derived value.
    psa - polar surface area. Authors use experimentally - derived value (Exposed Polar Surface Area).
    hac - heavy atom count.
    """
    return 1000 * c_log_d / (psa * hac)


def normalise_chembl_indication_class(ic):
    rv = []
    for _i in str(ic).split(";"):
        if "(" in _i:
            _i = _i[0:_i.index("(")]
        if "," in _i:  # E.g. "Bronchodilator,Diuretic" or "Antitussive,Antitussive,Antitussive"
            for _j in dict.fromkeys(_i.split(",")):
                rv.append(_j.strip())
        else:
            rv.append(_i.strip())
    return rv


def get_chembl_drugs():
    """
    In our analyses, drugs set consists of small molecules with weight <= 1kD that reached at least clinical trial phase 3 and have not been withdrawn, for which SMILES is available.
    """
    _df_chembl_molecule_properties = pd.read_csv(Path(__file__).resolve().parent.parent / "data" / "ChEMBL" / "chembl_molecule_properties.csv.gz", low_memory=False)
    _df = _df_chembl_molecule_properties[
        (_df_chembl_molecule_properties.molecule_type == "Small molecule") &
        #(_df_chembl_molecule_properties.therapeutic_flag == 1) &
        (_df_chembl_molecule_properties.max_phase >= 3) &
        (_df_chembl_molecule_properties.withdrawn_flag == 0) &
        (pd.notna(_df_chembl_molecule_properties.canonical_smiles))
    ].copy()
    _df["mol"] = _df.canonical_smiles.apply(lambda x: smiles_to_mol(x))
    _n_pre_removal = len(_df)
    _df = _df[_df.mol.apply(Descriptors.ExactMolWt) >= 50]
    _df = _df[_df.mol.apply(Descriptors.ExactMolWt) <= 1000]
    _df["indication_class_normalised"] = _df.indication_class.apply(normalise_chembl_indication_class)
    return _df


def get_chembl_drugs_with_descriptors(descriptors=["desc2D", "ecfp-count", "maccs"]):
    df = get_chembl_drugs().reset_index(drop=True)
    df = df.rename(columns={
        "cx_logd": "chemaxon_logd",
        "cx_logp": "chemaxon_logp",
        "cx_most_bpka": "chemaxon_pka_b",
    })
    with datamol.without_rdkit_log():
        for dt in descriptors:
            tr = FPVecTransformer(kind=dt, dtype=float, n_jobs=16, verbose=False)
            _d = pd.DataFrame(tr(df["mol"]), columns=[f"{dt}_{c}" for c in tr.columns])
            df = df.join(_d)
    #df = df.drop(columns=["mol"])
    _pre_removal = len(df)
    df = df[pd.notna(df["chemaxon_logd"])]
    LOGGER.warning(f"Discarded {_pre_removal - len(df)} drugs without logD or logP specified. {len(df)} remaining.")
    LOGGER.warning(f"Imputing {sum(pd.isna(df.chemaxon_pka_b))} missing most basic group pKa with 0. Used here to allow data exploration as some of the algorithms cannot work on missing values.")
    #_pre_drop = list(df)
    #df = df.dropna(axis=1)
    df = df.fillna(0)
    #LOGGER.warning(f"Dropped {len(_pre_drop) - len(list(df))} nan-containing descriptors from ChEMBL drugs")

    return df


def get_drugbank_small_molecule_drugs():
    _df = pd.read_csv(str(Path(__file__).parent.parent / "data" / "DrugBank" / "drugbank_data.csv"))
    _df["groups"] = _df.groups.apply(eval)
    return _df[
        _df.groups.apply(lambda x: ("approved" in x or "investigational" in x) and "withdrawn" not in x)
    ]

if __name__ == '__main__':
    d = get_chembl_drugs()
    print(len(d))
    breakpoint()