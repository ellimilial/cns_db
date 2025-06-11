# B3DB_KC



###############################
QSAR Modeling of the Blood–Brain Barrier Permeability for Diverse Organic Compounds
Zhang, L. et al 2008
 - evaluated multiple types of descriptors 
 - concept of Applicability Domain - do not evaluate compounds which are further than (mean for all training set compounds(euclidean distance to k nearest neighbours i  + 0.5 std euclidean distance ))
 - (kNN + SVM) * 3 sets of features (MolconnZ, MOE, Dragon)
 - 157 compounds with LogBB, further evaluated on 2 BBB+/- datasets of 99 and 267 compounds

##############################
Moving beyond Rules: The Development of a Central Nervous System Multiparameter Optimization (CNS MPO) Approach To Enable Alignment of Druglike Properties
Wager, T. et al 2010

Uses the following properties:
ClogP, ClogD, MW, TPSA, HBD, pKa
  
##############################
Central Nervous System Multiparameter Optimization Desirability: Application in Drug Discovery
Wager, T. 2016
reviewed 21 new CNS MPO candidates

##############################
Probabilistic Approach to Generating MPOs and Its Application as a Scoring Function for CNS Drugs
Gunaydin, H. 2016

TPSA, HBD, MW, cLogD, basic pKa

##############################
Technically Extended MultiParameter Optimization (TEMPO): An Advanced Robust Scoring Scheme To Calculate Central Nervous System Druggability and Monitor Lead Optimization 
Ghose A. et al. 2016

number of basic amines, 
carbon–heteroatom (non-carbon, non-hydrogen) ratio
number of aromatic rings
number of chains
number of rotatable bonds
number of H-acceptors
computed octanol/water partition coefficient (AlogP)
number of nonconjugated C atoms in nonaromatic rings. 

##############################
CNS Physicochemical Property Space Shaped by a Diverse Set of Molecules with Experimentally Determined Exposure in the Mouse Brain
Rankovic, Z, 2017
(CNS MPO v2)
Two data sets 
BEA-BP - (Brain Penetrant) internal Eli Lilly brain penetrant data set (N=260), partially resetricted BEA-PR (N=308)
CNS (N=324) and non CNS (N=845) drugs 
A total of 1737 Drugs used
Analysed in the context of 
cLogP
cLogD
pKa
MW
HBD
HBA
TPSA
Rotable Bonds (RB)


##############################
The Blood–Brain Barrier (BBB) Score
Gupta, M et al. , 2019

270 CNS drugs and 720 non-CNS drugs taken from various sources (e.g. https://www.selleckchem.com/screening/cns-penetrant-compound-library.html, or blog posts like this http://www.cureffi.org/2013/10/04/list-of-fda-approved-drugs-and-cns-drugs-with-smiles/ - collates DrugBank with a list of drugs offered by the insurers in Central Nervous systems agents)
evaluates their own against MPO and MPOv2

They manually removed molecules that are reported to follow active transport, such as L-DOPA, glucose, gabapentin, and vitamins were removed.

Their own uses polynomial (cubic and linear) piecewise functions with different weights :
AroR (weight 1)
HA (weight 1)
MWHBN (weight 1.5)
TPSA (weight 2)
pKa (weight 0.5)



##############
Balanced Permeability Index: A Multiparameter Index for Improved In Vitro Permeability
Dahlia R. Weiss et al, 2024
https://pubs.acs.org/doi/10.1021/acsmedchemlett.3c00542
Introduces Balanced Permeability Index (BPI) 
BPI = 1000 LogD/PSA*HAC
(LogD at 7.4pH measured by chromatographic high-throughput assay)
PSA - the authors note the limited reliability of TPSA and rely on experimentally - derived EPSA (exposed polar surface area)
Heavy atom count

Any computational approach will be limited.

#################


A curated diverse molecular database of blood-brain barrier permeability with chemical descriptors
 Meng, F. et al, 2021
 https://www.nature.com/articles/s41597-021-01069-5
 
4956 BBB+, 2851 BBB- + 1056 logBB values

Aggregates 50 datasets, 33825 raw records



##############################

Explaining Blood−Brain Barrier Permeability of Small Molecules by Integrated Analysis of Different Transport Mechanisms
Cornelissen Fleur M G, J Med Chem 2023
https://pubs.acs.org/doi/10.1021/acs.jmedchem.2c01824
XGBoost - feature importance
Multiple transport mechanisms :
 - BBB (+1769, -508) Weng et al 2018 (R13)
 - Efflux via ABC transporters, Influx via SLC transporters and PAMPA, measured against CNS Drugs dataset), Metra Base
 - Influx via SLC transporters
 - PAMPA (passive membranes)
 - measured against CNS benchmark (411 CNS drus from Drugbank) 

Feature importance:
BBB    Overall
TPSA      
LogD
MW
LogP
LogS
R.B
HBD
HBA

####################
On regression
BBB defines permeating at > -1. 
Muehlbacher 2011 adapts the average error of 0.3 calculated by Abraham 2006 in defining BBB+ 
as logBB > 0.3 and BBB- at logBB < -0.3, discarding the compounds in the range between these values.    

########################333
Manual negatives check:
Antibiotics:
  - Ribavirin
  - Gentamicin
  - Vancomycin
Markers:
  - Inulin
  - Sucrose
Anti-cancer
  - Cisplatin


Other:
  - Amyl nitrates

2nd gen antihistamines :
    Cetirizine
Sucrose
Inulin



Detour on Sildenafil:
 https://onlinelibrary.wiley.com/doi/10.1111/jnc.13454 calculates sildenafil's logBB as -0.39 BUT they for some reason 
report K(p, uu) (unbound plasma, basically multiply by 20 , unbound brain - proxied by cerebrospinal fluid), above -1 identified in 10.1002/jps.21745 (Mensch 2009)
The actual value when calculated without the adjustment for unbound plasma concentration is -1.3, consistent with R47 and R23.

The -1.3 value comes from: 
Validation of an LC–ESI-MS/MS method for the quantitation of phosphodiesterase-5 inhibitors and their main metabolites in rat serum and brain tissue samples
https://pdf.sciencedirectassets.com/271442/1-s2.0-S0731708512X00098/1-s2.0-S0731708512002270/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCICKpGL6%2FkcBFuhwEJrCigQT7ba%2Fd%2BjeFBRoKVzaiE%2FTHAiAmFtr%2FZUwOELudlhYcepYPblCopU8cuUwSE4NG3UcBFiq8BQjo%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAUaDDA1OTAwMzU0Njg2NSIMUK6dlSHBrUOUaGA3KpAFHwCO1UqHUSBdmTzsQPSkcBlLEtSY8tLxI4%2FwX3FZNju23ul15KZDTd6xzF4s92IPFn561%2BaQgaSCbfHkCnqj5Q%2FWlF%2FfciDhB6IEdDKJPG5nBk1x1KOaqqcAD6WL33WpzYeTiOVhmB76EjzSsYh28LsSpByJHsVHU1QJIUCCdZQ5RN4eMp1ezGDVz9QqrGNJF6LBuFfQNbmXD5QyViVDfdREXj%2B0Z%2FXFINh2yctR3NUTYZ%2B%2FtoikaN%2F7gejKIJuUyWoqXhVrROswicneWDIa1W8pOKT4tR17WwIMLhhy%2FY91ks5bwXWXacbkCkzC9iAEx4qJn%2BRJvuHUypZqW2%2F0bfrJcWGDfDw8a9KhMGmA1WjOuIfKIK1IJ7wDR7C1o9cCZ1%2BHaTJ6ANiq6dK23vaQv5SBP4x2sXXroxg0zlg1%2FSk0lobM7xo18eOZdO3TedLoLLxUQvQjxaGxQMRYDR%2Btt7MuNpaLRm9PX9WEejbx5pz7j7BjezW8Xc8pzKm6Iw4qoRRk%2Bq787SgJGKCGIj1XYtIMIE3lhfEBzvrlDQZ4nWyz1SLGph9RgXu%2Bgw5uPyN3RcFbtgZdE6ViVmF4nRUBV%2Fip0iryjMkn%2BeQ1Rs7mjrgz6%2F%2BeL2flTMy9zNKXwAWYEX6yxjmipY%2Fa7kpW8JyOOvUGE1yzFlNMcBW38e30aPRGGwvsbSzZaKuzFISwkI801iV9ETAp26mcqBEFJp4VbId82QbV6HRSb4G2C4h1kGEmZoxh3LL0qx24CQpxZqWH0mEDL3ex6vL0CVijc12iWL9SdrM6HnZCR0QtPypmK4O4V9mpxv%2FN%2FBpz%2BmRhu2oueAbwIOjbZTgjhyStDv9I%2BB2EjgK%2B4%2BqsMBLDSufUVlgwkd23sQY6sgH0lnzv5boVJYEi1qNr1IBlp%2FzQgiQrHmPjGIX1YD52VjRyucmrY7xDx5BxnOkSy1fxaGZm3ocFAwHx8za1AmtzIPbNtpI%2Bv4WU97Lds3Pwbp%2BmsSc7234yFamsnKbXGSIMzyYZdt4iyHP2b9Ma2LzAaA1ClJyuKuJN8P5%2FlIlLbUuiGuZIxxSwkShBQAn4UJtke4ky%2BrKSA3EeMaewANyQPKTnlGcPoMQKpAG7PI8MVtD0&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240428T074915Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTY5L5YMOHP%2F20240428%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=0d2ad6e3c9bbcf73069b875134f2b70a05d6d38af172174278a10aa521b9c20a&hash=72a3d0ac51e13680c73c8093391f56055b91255aa254b6cd592f3299320c256f&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S0731708512002270&tid=spdf-3e4e04e6-dc7f-40a2-85eb-b52290346bf0&sid=ba55ca8f7dff524f5f19ff407f3156c7f833gxrqb&type=client&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&ua=05015d560454515a55&rr=87b574663c957698&cc=gb
They measure rat brain concentration at 60 mins
They found tadalafil in similar concentration to 

Is sildenafil just easily P-GP thrown away?


Mensch 2009 
https://pdf.sciencedirectassets.com/313843/1-s2.0-S0022354909X82006/1-s2.0-S0022354916332099/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIHzv4UzK6syyDVwMC4jYdoECLnhHFgDFuCiRWfFVLrVpAiEA5nfNq6JhvvV85Y1XjQKKiIasRgyoQM%2F%2FX3fDLZ%2BiYPQqvAUI6P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAFGgwwNTkwMDM1NDY4NjUiDFprzKQQrZtv2CvFnyqQBXHfTkOh4vZESkR4sgJxHK4Q9dLy5GvLldEb7F72xfC53%2FQQuvpVpFm2p5LXJz7fk0RrAG39g6VuskJF4kZE8TAM0L0fFCGVf0SU9SKHPKJBP65sgN0q8lL6%2FdJrLO5HTGKb3BDgEzsM5%2FQx%2FlFI%2B28Gy%2BqEvCKRaVVNUNjHPphslN8NDgqJSfDUKBQd2giZp2zyM%2BtxJq8reDwiGLynfqmdj0jgaNSJdYZHvIN%2FaMCvAQxIsta8MZVPOD9s9bN%2FE9DDNPcJxGixXke%2FmHJN6fgJVQJ5x%2FEofdw6%2FhgfcNARDb648jDlgwaBobY5F6fq%2FE%2FPmGSuMrd6wBVMYYOSOwdZBfu%2FdpOb73GuxuvbvBVhZqfN%2BEl%2Fg5AdwAcxEtyF06jni%2F2Iv6riz57CSmW32Yi8ImIQppUwCJR6BQYSCIRW0fUmEEqkb6n7MfyNtCyXJk7nf8cyxNzbe0a9Y26mWS1nMa637LiW4gnhGOfBQMV%2B6nn9aIntWMIEgfSM3hHYkQtmUhVEG68R1J4eRK%2FuoRR2egt5jrqBuaN1Zk5xMc1olkAhKeXtxhMk5dgoxYBZNKXRJOiyGwYN9ozVjWkZNE740Rw3IJ8GHbHjQOEVHwrksyb2UU3QvBMFrNGiVawXJs1kqYdZOPaf7hOT4KfGxtnnLQ7Y%2BwI1sNZWhnoP9PVsb2V15CrFf82wC1sT%2FSzTx%2FfqFR%2FvvxU%2FwMJCJyEpR3SGmJuh2QmWwhg5W1j9VdEJ%2BFbCjLojFa333Vx14R%2FaphldNLzTvMBdDqVSz6rVVZHy7otwrKPHdSP6T%2F4afsfAiX3P%2FjmynxXALlkzSjjJjHxPQBa1AqCncgc1onVnesPE9uHQoYsDEXZBVXRIVdmXMPnat7EGOrEBKXX9Ys0ERFAxAwT4hB8oF6ZbD%2BEOfg1xTplgnwaopLK%2FUD%2FZX%2BXJ5WJWr44HLjFQi%2B6F3vyNK2uUFgXz96K0lrC02c%2Bx6M93DnGyoxpIo7W4NpE2DUXAroEBGPEOg5rvAFGGPOrIXH8wOanGV2nHIp6%2FRP3YUxuOCvx8V2odcudFPLP3STIZStAoZJ5%2B5rsVbO51exHpOXmnpxNjZEkM7%2B2WXtHriqJZHK7kg6WciEuB&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240428T072818Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYWL3XPX7I%2F20240428%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=2f0ed34906ad171ebe0b1ec4bbaf61bc882bd43a4ce74062b3ee735833b933d0&hash=2c5efa9960b251e8dadf7b51fc58217209b7d6c659928c0138a60ade2af931d6&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S0022354916332099&tid=spdf-c187322e-6e95-4df0-8c3f-653532d1d5c2&sid=ba55ca8f7dff524f5f19ff407f3156c7f833gxrqb&type=client&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&ua=05015d560454535b01&rr=87b555b59c9377a0&cc=gb
 - The table summarising the logBB used to determine the descriminant classes. This ranges from -1   
##############################
b3db_prop.txt file was generated using MOE descriptor calculator from ChEMBL-pipeline-normalised SMILES


Source aggregation

R1 (Martins 2012)
 - Zhang 2008 (R36)
 - Zhao 2007 (R19)
 - Li 2005 (R28)
 - ! Doninger 2002 (quoted as 2000, titles match)
 
R2 (Singh 2020)
 - Wang 2015 (R8)
 - Brito-Sanchez 2015 (R25)
! This dataset could therefore be removed

R3 (Abraham 2006)
 - Describes and distinguishes between in vitro and in-vivo methods for determining the coefficients
 - They measure the differences (whold dataset ~45 compounds) between blood- , serum- and plasma- to brain identifying they do not differ meaningfully and could be combined
 - They measure the difference between human and rat in-vitro models indicating they could be combined 
 - A compiled database
Keep
 
R4 (Mente 2005)
 - 3 classes - in house mouse data, in-house rat data, compiled literature data from rats (~15 articles) 

R5 (Guerra 2008)
 - 108 compounds compiled from 4 rat studies 
Need to verify against R4 literature rat studies to perhaps remove 
Verified overlap against R4, no natively, after smiles sanitisation - 21 / ~20%, keep

R6 (Adenot 2004)
 - 1696 Obtained from WDI database using ATC classification system (therepeutic usage)
Keep (a good example of limited usefulness)

R7 (Andres 2006)
 - 224 compounds were selected randomly from various therapeutic categories and small organic substances, for which either experimental logBB or the observed CNS activity arewell established
 - looks like the compilation might have been manual
Keep

R8 (Wang 2015) 
 - Muehlbacher 2011 (R21)
 - Vilar 2010 (R40)
 - Hou 2003 (R48)
 - Abraham 2006 (R3)
! This dataset could therefore be removed

R9 (Mahumdar 2019)
Relies on Li 2005 (R28)
! This dataset could therefore be removed

R10 (Miao 2019)
Sources from Gao 2017 (R16)
! Introduces additional duplication - should be removed

R11 (Shen 2008)
151 compunds from 6 publications:
  - Young 1988 (R. C. Young, R. C. Mitchell, T. H. Brown, C. R. Ganellin,R. Griffiths, M. Jones, K. K. Rana, D. Saunders, I. R. Smith,N. E. Sore, T. J. Wilks,J. Med. Chem.1988,31, 656 – 671)
  - Hou 2003 (R48) 
  - Narayanan 2005 (R. Narayanan, S. B. Gunturi,Bioorg. Med. Chem.2005,13,301 7– 3028.)
  - Katritzky 2006 ( A. R. Katritzky, M. Kuanar, S. Slavov, D. A. Dobchev, D. C.Fara, M. Karelson, W. E. Acree, Jr., V. P. Solovev, A. Var-nek,Bioorg. Med. Chem.2006,14, 4888 – 4917.)
  - Subramanian 2003 (R29)
A mixed case - potential for removal if 3 datasets taken care of

R12 (Garg 2006)
  - Platts 2001 (Platts, J. A.; Abraham, M. H.; Zhao, Y. H.; Hersey, A.; Ijaz, L.; Butina,D. Correlation and prediction of a large blood-brain distribution datasetsan LFER study.Eur. J. Med. Chem.2001,36, 719-30.)
  - Rose 2002 (Rose,  K.;  Hall,  L.  H.;  Kier,  L.  B.  Modeling  blood-brain  barrierpartitioning using the electrotopological state.J. Chem. Inf. Comput.Sci.2002,42, 651-666.)
  - ChemSilico Training - company website no longer present 
  - ChemSilico CSBBB  External  Validation  Set  Compound - company website no longer present
Keep

R13 (Wang 2018):
Filtered by MW <= 1000 Da
Used logBB -1 to split.
Used MacroModel 11.1 to neutralize all compounds and generate the most populated neutral tautomer for each compound at pH 7.0 by using Epik 3.5.29 Then, we used Open Babel to standardize dative bonds and generate canonical SMILES for each chemical structure.
All compounds were merged and represented by the canonical SMILES as the unique identifier for each chemical structure. 
Furthermore, some molecules with ambiguous values or contradicting data were eliminated.
Uses:
 - Martins 2012 (R1)
 - Muehlbacher 2011 (R21)
 - Wang 2015 (R8)
- Shen 2010 - J. Shen, F. Cheng, Y. Xu, W. Li, Y. Tang, J. Chem. Inf. Model. 2010, 50, 1034–1041.
     Shen 2010 dataset uses:
        - 1593 compounds from Adenot 2004
! This dataset could therefore be removed. 

R14 (Ghose 2012)
 Compiled 317 CNS and 626 non-CNS (943 total) only approved oral drugs from multiple databases, curated the results against DrugBank and Wikipedia
 2:1 ratio of non-CNS to CNS oral drugs
keep

R15 (Kortagere 2008)
 - Garg 2006 (R12)
 - Hou 2003 (R48)
 - Konovalov 2007 (R38)
 - Li 2005 (R28)
 - Liu 2001 (Development of quantitative structure—property relationship models for early ADME evaluation in drug discovery. 2. blood—brain barrier penetration. J. Chem. Inf. Comput. Sci. 2001;41:1623–1632.) , ~57 compounds 
    - Liu 2001 uses Abraham 1995 (Abraham, M. H.; Chadha, H. S.; Mitchell, R. C. Hydrogen bonding.36.  Determination  of  blood  brain  distribution  using  octanol-waterpartition coefficients.Drug Des. DiscoV.1995,13, 123-131.)
 - Subramanian 2003 (R29)
Potential removal after adding Liu 2001

R16 (Gao 2017)
Augments the predictions with SIDER
  - Abraham 2006 (R3)
  - Li 2005 (R28)
  - Subramanian 2003 (R29)
  - Wang 2015 (R8)
  - Winkler 2004 (Winkler D.A., Burden F.R. (2004) Modelling blood–brain barrier partitioning using Bayesian neural nets. J. Mol. Graph. Model., 22, 499–505.)
    - Winkler 2004 uses Rose 2002 ((Rose K, Hall LH, Kier LB. Modeling blood-brain barrier partitioning using the electrotopological state. J Chem Inf Comput Sci. 2002;42(3):651–666. doi: 10.1021/ci010127n.))
  - Doninger 2002 used as a test set
Potential removal after adding Winkler 2004

R17 (Fu 2008)
111 compounds with logBB taken from:
    [2], [6], [7], [8], [21], [22], [23], [24], [25], [26] 
COULD NOT BE EVALUATED DUE TO ACCESS

R18 (Plisson 2019)
Marine-derived kinases evaluation, only a single database used for training set
 - Chico 2009 (R26)
!Remove

R19 (Zhao 2007)
 - Adenot 2004 (R6)
 - Li 2005 (R25)
!Remove

R20 (Lanevskij 2011) 
 - In-depth analysis of logBB consideration (e.g. high protein binding in plasma would push logBB down despite good BBB permeability)  
 - Quantitative logBB values were collected from origi-nal experimental articles and earlier modeling works,the latter being rechecked in the original source wherever possible
 - Several algorithms sources listed 
    - Abraham 2006 (R3)
    - Van Damme 2008 (Van Damme S, Langenaeker W, Bultinck P. 2008. Predictionof blood–brain partitioning: A model based on ab initio cal-culated quantum chemical descriptors. J Mol Graph Model26:1223–1236)
    - Fu 2008 (R17)
    - Zhang 2008 (R36)
    - Kortagere 2008 (R15)
    - Chen 2009 (R35) 
    - Fan 2010 (Fan Y, Unwalla R, Denny RA, Di L, Kerns EH, Diller DJ, Hum-blet C. 2010. Insights for predicting blood–brain barrier pene-tration of CNS targeted molecules using QSPR approaches. JChem Inf Model 50:1123–1133)
More analysis required if removal considered, potentially more data than from the modelling articles (article does not provide a sensible reference)
Compare against R25

R21 (Muehlbacher 2011)
 logBB compounds from:
 - Vilar 2010 (R40) - 195
 - Mente 2005 (R4) - 94
 - Zhang 2008 (R36) - 147
 - Abraham 2006 (R3) - 197
 - Garg 2006 (R12) - 168
 - Guerra 2008 - 106
 - Konovalov 2007 (R38) - 165
 - Platts 2001 (Platts JA, Abraham MH, Zhao YH, Hersey A, Ijaz L, Butina D. Correlation and prediction of a large blood-brain distribution data set—an LFER study. Eur J Med Chem. 2001;36(9):719–730. doi: 10.1016/S0223-5234(01)01269-7) - 64
 - Narayanan 2005 (Narayanan R, Gunturi SB. In silico ADME modelling: prediction models for blood-brain barrier permeation using a systematic variable selection method. Bioorgan Med Chem. 2005;13(8):3017–3028. doi: 10.1016/j.bmc.2005.01.061.) - 43
 - Rose 2002 (Rose K, Hall LH, Kier LB. Modeling blood-brain barrier partitioning using the electrotopological state. J Chem Inf Comput Sci. 2002;42(3):651–666. doi: 10.1021/ci010127n.) - 95 
 - Kelder 1999 (Kelder J, Grootenhuis PDJ, Bayada DM, Delbressine LPC, Ploemen J-P. Polar molecular surface as a dominating determinant for oral absorption and brain penetration of drugs. Pharm Res. 1999;16(10):1514–1519. doi: 10.1023/A:1015040217741) 36
 - Zerara 2009 (Zerara M, Brickmann J, Kretschmer R, Exner TE. Parameterization of an empirical model for the prediction of n-octanol, alkane and cyclohexane/water as well as brain/blood partition coefficients. J Comput Aided Mol Des. 2009;23(2):105–111. doi: 10.1007/s10822-008-9243-2.)
A large aggregator, 5 sources would need to be added to remove.

R22 (Clark 1999)
 - a tiny dataset
problems accessing, keeping as is

R23 (Gupta 2019)
 - Manually curated list of CNS and non-CNS drugs compiled from various sources, including queries to DrugBank, non-existing company datasets (plural) 
 - Wager 2010 (original CNS MPO paper)
 - Rankovic 2017
Keep

R24 (Roy 2019)
- contains 1864 molecules from
 - Adenot 2004 (R6)
 - Li 2005 (R28)  
! - Doniger 2002 - Doniger, S.; Hofmann, T.; Yeh, J. Predicting CNS Permeability of Drug Molecules: Comparison of Neural Network and Support Vector Machine Algorithms. J. Comput. Biol. 2002, 9, 849−864.


R25 (Brito‐Sánchez 2015)
 LogBB data compiled from a large number of studies. 
 Contains Lanevskij 2011 (R20) and Konovalov 2007 (R38), Shen 2008 (R11)

R26 (Chico 2009)
 This review focuses on CNS/kinase discrepencies. It compiles a CNS list + non-CNS kinases   
keep

R27 (Shaker 2020)
 - Adenot 2004 (R6)
 - Gao 2017 (R15)
 - Martins 2012 (R1)
 - Plisson & Piggott 2019 (R18)
 - Singh 2020 (R2)
 - Wang 2018 (R13)
 - Wu 2018 (Molecule Net) - MoleculeNet BBBP should be Martins 2012 (R1)
 - Yuan 2018 Yuan Y.  et al.  (2018) Improved prediction of blood–brain barrier permeability through machine learning with combined use of molecular property-based descriptors and fingerprints. AAPS J., 20, 54.
    - 2 datasets based on Zhao 2007 (R19) (cited as 2009)
    - dataset A : 1593 compounds from Adenot 2004  which uses Kennard-Stone for train-test splitting
    - dataset B: dataset A + Li 2005
    
! This dataset could therefore be removed

R28 (Li 2005)
 415 agents with known BB ratios
 - Micromedex
 - American Hospital Formulary Service
 - Platts 2001 (Platts, J. A.; Abraham, M. H.; Zhao, Y. H.; Hersey, A.; Ijaz, L.; Butina,D. Correlation and prediction of a large blood-brain distribution dataset-an LFER study.Eur. J. Med. Chem.2001,36(9), 719-730.)
 - Luco 1999 (Luco, J. M. Prediction of the brain-blood distribution of a large setof drugs from structurally derived descriptors using partial least-squares(PLS) modeling.J. Chem. Inf. Comput. Sci.1999,39(2), 396-404.)
 - Feher 2000 (Feher,  M.;  Sourial,  E.;  Schmidt,  J.  M.  A  simple  model  for  theprediction of blood-brain partitioning.Int. J. Pharm.2000,201(2),239-247)
 - Crivori 2000 ( Crivori, P.; Cruciani, G.; Carrupt, P. A.; Testa, B. Predicting blood-brain barrier permeation from three-dimensional molecular structure.J. Med. Chem.2000,43(11), 2204-2216.)
 - Ooms 2002 (Ooms,  F.;  Weber,  P.;  Carrupt,  P.  A.;  Testa,  B.  A  simple  model  topredict  blood-brain  barrier  permeation  from  3D  molecular  fields.Biochim. Biophys. Acta2002,1587(2-3), 118-125)
 - Lobell 2003 (Lobell,  M.;  Molna ́r,  L.;  Keseru ̈ ,  G.  M.  Recent  advances  in  theprediction  of  blood-brain  partitioning  from  molecular  structure.J.Pharm. Sci.2003,92(2), 360-370)
 - Iyer 2002 (Iyer,  M.;  Mishru,  R.;  Han,  Y.;  Hopfinger,  A.  J.  Predicting  blood-brain  barrier  partitioning  of  organic  molecules  using  membrane-interaction QSAR analysis.Pharm. Res.2002,19(11), 1611-1621.)
Keep as is

R29 (Subramanian 2003)
 - 281 molecules, split into qualitative training (60), testing (40) and qualitative test (181 - reliable CNS +/- sourced from literature)
keep

R30 (Harvard dataverse - Therapeutic Data Commons)
    1,975 drugs
    Should be from Martins 2012 (R1)
!Check coverage against Martins 2012 (R1), if covered, remove
 
R31 (Carpenter 2014)
 A tiny dataset (12?)
keep

R32 (Lombardo 1996)
55 compounds
 - Abraham 1994 (Abraham, M. H.; Chadha H. S.; Mitchell R. C. HydrogenBonding. 33. Factors that Influence the Distribution of Solutesbetween Blood and Brain.J. Pharm. Sci.1994,83, 1257-1268)
 - Lin 1994 (Lin, J. H.; Chen, I.-W.; Lin, T.-H. Blood-brain barrier perme-ability andin vivoactivity of partial agonists of benzodiazepinereceptor: A study of L-663,581 and its metabolites in rats.J.Pharmacol. Exp. Ther.1994,271, 1197-1202)
 - Van Belle 1995 (VanBelle, K.; Sarre, S.; Ebinger, G.; Michotte, Y. Brain, Liverand Blood Distribution Kinetics of Carbamazepine and itsMetabolic Interaction with Clomipramine in Rats: A Quantita-tive Microdialysis Study.J. Pharmacol. Exp. Ther.1995,272,1217-1222)
 - Ohshima 1995 (Ohshima, N.; Kotaki, H.; Sawada, Y.; Iga, T. The relationshipbetween the pharmacological effect of amitriptyline based on animproved forced-swimming test and plasma concentration inrats.Biol. Pharm. Bull.1995,18,70-74)
 - Shah 1989 (Shah, M. V.; Audus, K. L.; Borchardt, R. T. The Application ofBovine Brain Microvessel Endothelial-Cell Monolayers Grownonto Polycarbonate MembranesIn Vitroto Estimate the Poten-tial Permeability of Solutes Through the Blood-Brain Barrier.Pharm. Res.1989,6, 624-627)
keep

R33 (Norinder 1998)
 63 compounds / 26 in the list?
!problems accessing, covered by Norinder 2002 (R49), remove

R34 (Broccatelli 2012)
 153 oral drugs
 Compiles a plethora (>70) articles for validation of permeability
keep

R35 (Chen 2009)
 145 compounds with logBB, removed 4 outliers
  - Garg 2006 (R12)
  - Norinder 2002 (R49) (cited as 2004 in error)
!remove

R36 (Zhang 2008)
 Norinder, Brewster, Kelder, Feher, Luco, Clark, Subramanian, Lombardo, Abraham are (reverse chronologic order) based on Young 1988
 159 compounds that should cover Young, Salminen and Kelder dataset + 7 other compounds derived from:
  - Hemmateenejad 2006 (R45)
  - Norinder 2002 (R49)
  - Platts 2001 (J. A. Platts, M. H. Abraham, Y. H. Zhao, A. Hersey, L. Ijaz, and D. Butina. Correlation and prediction of a large blood–brain distribution data set—an LFER study. Eur. J. Med. Chem. 36:719–730 (2001).)
! It looks like it may be removed as we cannot exclude other datasets with Platts 2001

R37 (Chen 2011)
246
 - 41 Friden 2009 (M. Fridén, S. Winiwarter, G. Jerndal, O. Bengtsson, H. Wan, U. Bredberg, M. Hammarlund-Udenaes, M. Antonsson Structure–brain exposure relationship in rat and human using a novel data set of unbound drug concentrations in brain interstitial and cerebrospinal fluids)
  These are not exactly logBB but influx / efflux rat data 
 - 111 CNS Marketed drugs from Wager 2010 (CNS-MPO paper)
 - Includes internal compounds as well
! B3DB data only includes CNS-MPO resource, ideally we should add 41 drugs from Friden 2009 (article contains a supplementary data)

R38 (Konovalov 2007)
  - Abraham 2006 (R3) - (328 -> 291) deduplicated, averaged and pruned if descriptors not calculable 
!Remove

R39 (Shayanfar 2011)
  - logbb of 122 compounds
  - Platts 2001 (Platts J. A., Abraham M. H., Zhao Y. H., Hersey A., Ijaz L., Butina D.,
Eur. J. Med. Chem., 36, 719—730 (2001).)
  - Chen 2009 (R35)
  - Katritzky 2006 (Katritzky A. R., Kuanar M., Slavov S., Dobchev D. A., Fara D. C., Karelson M., Acree W. E. Jr., Solov’ev V. P., Varnek A., Bioorg. Med.  Chem., 14, 4888—4917 (2006))
  - Guerra 2008 (R5)
! Platts should already be included. Take a look at Katritzky 2006 - should already be included in Shen 2008 (R11), which in turn should be included in Brito‐Sánchez (R25)  

R40 (Vilar 2010)
 - 307 compounds from mostly rat studies
 - Abraham 2006 (R3)
 - Konovalov 2007 (R38)
 - Luco 1999 (Prediction of the brain–blood distribution of a large set of drugs from structurally derived descriptors using partial least-squares (PLS) modeling)
 - Clark 1999 (R22)
 - Abraham 1997 (M.H. Abraham, K. TakacsNovak, R.C. Mitchell On the partition of ampholytes: application to blood–brain distribution J. Pharm. Sci., 86 (1997), pp. 310-315)
 - Garg 2006 (R12) 
 - Mente 2005 (R4)
 - Ooms 2002 (F. Ooms, P. Weber, P.A. Carrupt, B. Testa A simple model to predict blood–brain barrier permeation from 3D molecular fields BBA-Mol. Basis Dis., 1587 (2002), pp. 118-125) 
 - Escuder-Gilabert 2004 (L. Escuder-Gilabert, A. Molero-Monfort, R.M. Villanueva-Camanas, S. Sagrado, M.J. Medina-Hernandez Potential of biopartitioning micellar chromatography as an in vitro technique for predicting drug penetration across the blood–brain barrier J. Chromatogr. B, 807 (2004), pp. 193-201)
 - Rose 2002 (K. Rose, L.H. Hall, L.B. Kier  Modeling blood–brain barrier partitioning using the electrotopological state J. Chem. Inf. Comput. Sci., 42 (2002), pp. 651-666)
 - Usansky 2003 (H.H. Usansky, P.J. Sinko Computation of log BB values for compounds transported through carrier-mediated mechanisms using in vitro permeability data from brain microvessel endothelial cell (BMEC) monolayers Pharm. Res., 20 (2003), pp. 390-396)

R41 (Toropov 2017)
 The article claims data for 291 substances comes from
  - Hou 2002 (Not 2003) (Hou, T., Xu, X. ADME evaluation in drug discovery. J Mol Model 8, 337–349 (2002). https://doi.org/10.1007/s00894-002-0101-1)
  While the mentioned article only has ~140 , so do other Hou articles.
Further investigation required to remove

R42 (Ciura 2020)
 45 compounds with logbb handpicked from 13 publications, including author's previous experimental papers 
keep

R43 (Dichiara 2019)
 328 compounds - only pruned in vitro studies (discarded in vitro, predicted etc), discards substrates of P-glycoprotein - an efflux mechanism pumping the substances out - pruned from 559 unique compounds from:
 - Li 2005 (R28) - 415 
 - Muehlbacher 2011 (R21) - 380
 - Abraham 2006 (R3) - 207 
 - !Liu 2001 (Liu, R., Sun, H., and So, S. S. (2001) Development of quantitative structure-property relationship models for early ADME evaluation in drug discovery. 2. Blood-brain barrier penetration. J. Chem. Inf. Model. 41, 1623– 32,  DOI: 10.1021/ci010290i) 57
!This dataset aims at being valuable - but may be too strict for our approach, remove after adding Liu 2001

R44 (Bujak 2015)
 79 compounds, logbb from:
 - Kaliszan 1996 (R. Kaliszan, M. Markuszewski Brain/blood distribution described by a combination of partition coefficient and molecular mass Int. J. Pharm., 145 (1996), pp. 9-16)
 - Molero-Monfort 2002 (M. Molero-Monfort, R.M. Villanueva-Camañas, M.J. Medina-Hernández  Potential of biopartitioning micellar chromatography as an in vitro technique for predicting drug penetration across the blood–brain barrier J. Chromatogr. B, 807 (2002), pp. 193-201)
Keep

R45 (Hemmateenejad 2006)
 123 compounds
 - 115 from: 
   - Hou 2003 (R48)
   - Norinder 2002 (R49)
 - 8 compounds used for the first time
!Validate those 8 with a view of keeping - validated, B3DB only delivers those 8, which are not in R48/R49

R46 (Mendoza Valencia 2017)
 Compilation of resources used for building a logBB model for street - pushed drugs
!Remove, perhaps validate 

R47 (Radchenko 2020)
 LogBB of 529 compounds
 (They provide references to articles describing why curation of QSAR for BBB is important)
 They use Brito‐Sánchez (R25) as a "stress test", 1/3 non overlapping compounds
Keep, perhaps validate

R48 (Hou 2003)
 115 logBB values from rat studies 
 - Based on previous work 20
 - 20 new compounds from: 
   - Yazdanian 1998 (Yazdanian, M.; Glynn, S. L. In vitro blood-brain barrier permeabilityof nevirapine compared to other HIV antiretroviral agents.J. Pharm.Sci.1998,87, 306-310.)
   - Lin 1994 (Lin, J. H.; Chen, I.; Lin, T. Blood-brain barrier permeability and invivo activity of partial agonists of benzodiazepine receptor:  a studyof  L-663,581  and  its  metabolites  in  rats.J.  Pharmacol.  Exp.  Ther.1994,271, 1197-1202.)
   - Van Belle 1995 (Van   Belle,   K.   Brain,   Liver,   and   blood   distribution   kinetics   ofcarbamazepine  and  its  metabolic  interaction  with  clomipramine  inrats:  a quantitative microdialysis study.J. Pharmacol. Exp. Ther.1995,272, 1217-1222)
   - Calder 1994  (Calder,  J.  A.  D.;  Ganelline,  R.  Predicting  the  brain-penetratingcapability of histaminergic compounds.Drug Des. DiscoV.1994,11,259-268)

R49 (Norinder 2002)
 A compilation of multiple studies
  - Young 1988 (R.C. Young, R.C. Mitchell, T.H. Brown, C.R. Ganellin, R. Griffiths, M. Jones, K.K. Rana, D. Saunders, I.R. Smith, N.E. Sore, T.J. Wilks Development of a new physicochemical model for brain penetration and its application to the design of centrally acting H2 receptor histamine antagonists J. Med. Chem., 31 (1988), pp. 656-671)
  - Calder 1994 (J.A.D. Calder, C.R. Ganellin Predicting the brain-penetrating capability of histaminergic compounds Drug Des. Discov., 11 (1994), pp. 259-268)
  - Abraham 1993 (M.H. Abraham Scales of solute hydrogen-bonding: their construction and application to physicochemical and biochemical processes Chem. Soc. Rev., 22 (1993), pp. 73-83)
  - Lombardo 1996 (R32)
  - Molnár 2001 (L. Molnár ,G.M. Keserü High-throughput prediction of blood–brain partitioning: a thermodynamic approach J. Chem. Inf. Comput. Sci., 41 (2001), pp. 120-128)

It tracks the history of papers using those (especially Young) 
Very long, a review, keep.

R50 (Sobańska 2019)
LogBB taken from
 - Vilar 2010 (R40)
 - ACD/LabsTM, Log D Suite 8.0, pKa dB 7.0, Advanced  Chemistry Development Inc., Toronto, Canada, 2004.
!x-refrence potential ACD/LabsTM contribution with a view of source removal 


!!!
R49, R32, R33(not relevant) logBB looks mangled by excel (i.e. uses integer, needs fixing)
!!!

R51 Doninger 2002
 - Fischer 1998
 - Ajay 1999
 - van de Waterbeemd 1998 
 - Lundbeck 2000

Added 
R51 Doninger (2002) Scott Doniger, Thomas Hofmann, and Joanne Yeh. Predicting CNS Permeability of Drug Molecules: Comparison of Neural Network and Support Vector Machine Algorithms.  Journal of Computational Biology.Dec 2002.849-864.http://doi.org/10.1089/10665270260518317
R52 Liu (2001) Liu, Ruifeng, Hongmao Sun, and Sung-Sau So. "Development of quantitative structure− property relationship models for early ADME evaluation in drug discovery. 2. Blood-brain barrier penetration." Journal of chemical information and computer sciences 41.6 (2001): 1623-1632.
R53 Friden (2009) M. Fridén, S. Winiwarter, G. Jerndal, O. Bengtsson, H. Wan, U. Bredberg, M. Hammarlund-Udenaes, M. Antonsson Structure–brain exposure relationship in rat and human using a novel data set of unbound drug concentrations in brain interstitial and cerebrospinal fluids

To check 
R46: YG16(thiazole22aminoethyl)


Tang 2022
	- Martins 2012
	- Liu 2021
	- Shaker 2021
	- Adenot 2004
	- Gao 2017
	- Plisson 2019

Liu 2021
    - Zhao 2007 - pass thwought to Adenot and Lahana
    - Wang 2018
    - Wang 2015
    - Li 2005


EXTENSION - addition of peptides
 - some of the databases will not be useless as they don't include e.g. cysteine bridges 
 -  

Chen 2022 (BBPredict) - blood brain permeating peptides
https://www.frontiersin.org/journals/genetics/articles/10.3389/fgene.2022.845747/full
    - Van Dorpe 2012 - this is actually useful as there are 
    - Kumar 2021a B3Pred
    - Kumar 2021b B3Pdb
    - custom search of pubmed literature (hand curated?)


Additional  

Fu 2005:
Young et al. 1988; + 
Abraham et al. 1994;  +
Salminen et al. 1997;  +
Abraham et al. 1995; + 
Calder and Ganellin 1994; +
Kelder et al. 1999;  + 
Lombardo et al. 1996;  +
Yazdanian and Glynn 1998 +

von Sprecher, et al. 1998;
Greig et al. 1995; 