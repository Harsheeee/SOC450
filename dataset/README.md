# LASI Wave 1 Dataset Access Guide

This repository contains the replication pipeline for analyzing the **Longitudinal Ageing Study in India (LASI) Wave 1 (2017–2018)**.

## How to Obtain the Raw Data

Due to data-use agreements and file size constraints (>1.4 GB), the raw Stata microdata files are **not distributed directly** in this GitHub repository. 

Researchers can request and download the official LASI Wave 1 microdata free of charge for academic research purposes from:

1. **International Institute for Population Sciences (IIPS), Mumbai:**
   - Website: [https://www.iipsindia.ac.in/lasi/](https://www.iipsindia.ac.in/lasi/)
   - Form: Submit the official LASI Data Request Form specifying your academic institution and research topic.

2. **Gateway to Global Aging Data (USC / NIA):**
   - Website: [https://g2aging.org/](https://g2aging.org/)
   - Register for an academic account to access harmonized files and cross-national aging survey codebooks.

## Expected Directory Layout

Once downloaded, place the unzipped Stata (`.dta`) files directly into this `dataset/` directory:

```
dataset/
├── 1_LASI_W1_HH_roster.dta
├── 2_LASI_W1_Household_v4.dta
├── 3_LASI_W1_Individual_v4.dta          # Primary microdata file analyzed (N = 72,250)
├── 4_LASI_W1_Biomarker.dta
├── 5_LASI_W1_CV_memberfile.dta
├── 6_LASI_W1_CV_deathmemberfile.dta
├── LASI_W1_Community_data_AllstatesUTs_v4.dta
└── Data user guide_IIPS-LASI_All_states&UTs.pdf
```

## Running the Extraction Script

Once the raw files are in place, execute the data extraction and cleaning script:
```bash
python code/07_build_dataset_v2.py
```
This generates `data_analysis/lasi_clean_v2.parquet`, which forms the foundation of all downstream regression models and sensitivity checks.
