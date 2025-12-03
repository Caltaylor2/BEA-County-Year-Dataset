#!/usr/bin/env python3
"""
run_panel_summary_json.py

Creates a quick metadata summary for the final renamed county–year panel.
Reads:   county_panel_full_renamed.csv
Writes:  panel_summary.json
"""

import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT = BASE_DIR / "county_panel_full_renamed.csv"
OUTPUT = BASE_DIR / "panel_summary.json"

print(f"[START] Loading panel: {INPUT}")

df = pd.read_csv(INPUT, low_memory=False)

summary = {
    "n_rows": int(df.shape[0]),
    "n_columns": int(df.shape[1]),
    "columns": list(df.columns),
    "column_types": {c: str(df[c].dtype) for c in df.columns},
    "missing_by_column": {c: int(df[c].isna().sum()) for c in df.columns},
    "nonmissing_by_column": {c: int(df[c].notna().sum()) for c in df.columns},
}

# Also add a few quick stats for numeric columns
num_df = df.select_dtypes(include=["number", "float64", "int64"])
if not num_df.empty:
    numeric_summary = {
        "means": num_df.mean(skipna=True).round(3).to_dict(),
        "stds": num_df.std(skipna=True).round(3).to_dict(),
        "mins": num_df.min(skipna=True).to_dict(),
        "maxs": num_df.max(skipna=True).to_dict(),
    }
    summary["numeric_summary"] = numeric_summary

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(f"[DONE] Summary JSON saved → {OUTPUT}")
print(f"[INFO] Total rows: {summary['n_rows']}, columns: {summary['n_columns']}")
