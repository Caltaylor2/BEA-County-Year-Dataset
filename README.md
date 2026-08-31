# BEA County-Year Dataset Builder

This repository contains Python scripts and documentation developed as part of *The Gauntlet* research apprenticeship under Dr. Alan Seals at Auburn University.  
The goal of this project is to construct a reproducible panel dataset of U.S. counties (1969–2023) using data from the **U.S. Bureau of Economic Analysis (BEA)**.

---

## Overview

The scripts in this repository automate the process of:
1. Downloading and cleaning BEA Regional Economic Accounts data  
2. Renaming variables using a structured mapping file (`bea_variable_map.csv`)  
3. Merging multiple series into a unified **county-year panel**  
4. Producing summary tables and documentation for further analysis  

Because BEA data are publicly available but very large, **raw and processed data files are not stored in this repository**.  
All datasets can be reconstructed by running the provided scripts and following the data-access instructions below.

---

## Repository Structure
deliverables/
│
├── bea_variable_map.csv # Variable name mapping
├── build_log.txt # Log of dataset build process
├── panel_summary.json # Summary of merged dataset
├── summary_statistics.xlsx # Basic summary stats
├── run_deliverables_only.py # Script to run only deliverable builds
├── run_panel_summary_json.py # Script to generate summary JSON
├── run_summary_stats.py # Script to generate summary statistics
└── README.md # Documentation

---

## Reproducibility

To rebuild the dataset yourself:

1. **Install dependencies**

2. **Obtain BEA data**
- Go to [https://apps.bea.gov/](https://apps.bea.gov/)
- Download the “Regional Economic Accounts” county-level data for 1969–2023
- Save the raw files into a `data/raw/` directory (not tracked on GitHub)

3. **Run the build scripts**

4. **Check the deliverables**
- Cleaned dataset and summary files appear in `/deliverables/`
- The pipeline logs are stored in `build_log.txt`

---

## Notes

- Large `.csv` and `.xlsx` files are excluded from version control for size and reproducibility reasons.
- Only code, metadata, and documentation are shared here to allow others to replicate the process.
- Please cite the BEA as the original data provider when using derived results.

---

## Contributors

**Callie Taylor**  
Research Apprentice, Department of Economics, Auburn University  
Email: **ctayl102@msudenver.edu**
