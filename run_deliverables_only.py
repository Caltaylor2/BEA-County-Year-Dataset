#!/usr/bin/env python3
r"""
run_deliverables_only.py

Self-contained runner for your Deliverables folder.
Inputs (must be in this same folder):
  - county_panel_full.csv
  - bea_variable_map.csv   (columns: old_col, variable)
Outputs (written here):
  - county_panel_full_renamed.csv
  - rename_report.txt
Usage:
  python -u run_deliverables_only.py
"""

from __future__ import annotations
import argparse, re
from pathlib import Path
from typing import Dict, List
import pandas as pd
import numpy as np

NA_TOKENS = ["(NA)", "NA", "NaN", "D", "*", "...", "", " "]
AGGREGATE_FIPS_BADLIST = {"00000", "00998", "00999", "99999"}

def normalize_fips(val: str) -> str | float:
    if pd.isna(val): return np.nan
    d = re.sub(r"[^\d]", "", str(val))
    return d.zfill(5) if d else np.nan

def is_real_county_fips(f: str) -> bool:
    if not isinstance(f, str) or len(f) != 5 or not f.isdigit(): return False
    if f in AGGREGATE_FIPS_BADLIST: return False
    if f.endswith("000"): return False
    return True

def read_panel_here(here: Path) -> pd.DataFrame:
    # try common names; prefer the expected one
    for p in [here/"county_panel_full.csv", here/"county_panel.csv", here/"county_panel_unrenamed.csv"]:
        if p.exists():
            return pd.read_csv(p, dtype=str, na_values=NA_TOKENS, low_memory=False)
    raise SystemExit("[ERROR] No unrenamed panel found (expected county_panel_full.csv).")

def load_mapping(here: Path) -> Dict[str,str]:
    mpath = here/"bea_variable_map.csv"
    if not mpath.exists():
        print("[INFO] bea_variable_map.csv not found; skipping rename.")
        return {}
    m = pd.read_csv(mpath, dtype=str)
    old_key = next((c for c in ["old_col","old","column","source"] if c in m.columns), None)
    new_key = next((c for c in ["variable","new","pretty_name","label"] if c in m.columns), None)
    if not (old_key and new_key):
        print(f"[WARN] Mapping headers missing; expected (old_col, variable). Got {list(m.columns)}.")
        return {}
    return (m[[old_key,new_key]].dropna().astype(str).drop_duplicates()
              .set_index(old_key)[new_key].to_dict())

def drop_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    fcol = next((c for c in ["county_fips","fips","geofips","GeoFIPS","GEOFIPS","GEOID"] if c in df.columns), None)
    if not fcol: raise SystemExit("[ERROR] No FIPS column (e.g., county_fips).")
    if "year" not in df.columns: raise SystemExit("[ERROR] No 'year' column.")
    out = df.copy()
    out["county_fips"] = out[fcol].astype(str).map(normalize_fips)
    out = out.dropna(subset=["county_fips","year"])
    out["county_fips"] = out["county_fips"].astype(str)
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    out = out.dropna(subset=["year"])
    out["year"] = out["year"].astype(int)
    out = out[out["county_fips"].map(is_real_county_fips)]
    return out

def write_report(path: Path, subset_map: Dict[str,str], before: List[str], after: List[str]):
    lines = [
        "=== Rename Report ===",
        f"Columns before: {len(before)}",
        f"Columns after : {len(after)}",
        f"Columns renamed (exact): {len(subset_map)}",
    ]
    if subset_map:
        lines.append("Examples:")
        for k,v in list(subset_map.items())[:15]:
            lines.append(f"  {k} -> {v}")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[INFO] Report written: {path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Overwrite outputs if present")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    out_csv = here/"county_panel_full_renamed.csv"
    out_report = here/"rename_report.txt"
    if out_csv.exists() and not args.force:
        raise SystemExit(f"[ABORT] {out_csv} exists; use --force to overwrite.")

    print("[STEP 1] Load unrenamed panel…")
    panel = read_panel_here(here)

    print("[STEP 2] Drop aggregates/fake counties…")
    panel_clean = drop_aggregates(panel)

    print("[STEP 3] Apply rename map…")
    mapping = load_mapping(here)
    before = list(panel_clean.columns)
    if mapping:
        subset = {k:v for k,v in mapping.items() if k in panel_clean.columns}
        renamed = panel_clean.rename(columns=subset)
    else:
        subset, renamed = {}, panel_clean

    renamed.to_csv(out_csv, index=False)
    write_report(out_report, subset, before, list(renamed.columns))
    print("\n[DONE]")
    print(f"  Renamed: {out_csv}")
    print(f"  Report : {out_report}")

if __name__ == "__main__":
    pd.set_option("future.no_silent_downcasting", True)
    main()
