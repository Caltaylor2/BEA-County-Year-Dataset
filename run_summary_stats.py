#!/usr/bin/env python3
"""
run_summary_stats.py

Generates summary statistics for your final renamed BEA county–year panel.
Reads:   county_panel_full_renamed.csv
Writes:  summary_statistics.csv
Stats:   N, Missing, Mean, Std_Dev, Min, Max
"""

import pandas as pd
from pathlib import Path
import numpy as np

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
INPUT = BASE_DIR / "county_panel_full_renamed.csv"
OUTPUT = BASE_DIR / "summary_statistics.csv"

print(f"[START] Reading panel from {INPUT}")

# --- Load ---
df = pd.read_csv(INPUT, low_memory=False)

# --- Convert to numeric where possible ---
df_num = df.apply(pd.to_numeric, errors="coerce")

print(f"[INFO] Computing stats for {df_num.shape[1]} columns.")

# --- Build summary table ---
summary = pd.DataFrame({
    "N": df_num.count(),
    "Missing": df_num.isna().sum(),
    "Mean": df_num.mean(),
    "Std_Dev": df_num.std(),
    "Min": df_num.min(),
    "Max": df_num.max()
})

# --- Round numeric results ---
summary = summary.round(3)

# --- Save ---
summary.index.name = "Variable"
summary.to_csv(OUTPUT)

print(f"[DONE] Summary stats saved → {OUTPUT}")
print(f"[INFO] Variables summarized: {len(summary)}")
