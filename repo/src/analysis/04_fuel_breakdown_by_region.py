"""
Fuel-type breakdown (GAS / COAL / OIL) by WECC region.

Explains *why* the generation-weighted regional averages diverge from
the simple averages (see 03_weighted_vs_simple_average.py): coal
generates a larger share of real output in the Northwest and Rockies
than its plant count alone would suggest, and coal's per-MWh rate is
consistently far higher than gas's in every region.

Input:  build/output/eGrid2018_thermal.csv
Output: results/04_fuel_breakdown_by_region.csv
"""

import pandas as pd

INPUT_PATH = "build/output/eGrid2018_thermal.csv"
OUTPUT_PATH = "results/04_fuel_breakdown_by_region.csv"
REGION_NAMES = {1: "California", 2: "Northwest", 3: "Southwest", 4: "Rockies"}


def main():
    df = pd.read_csv(INPUT_PATH)
    df = df[df["Region"] != 0]

    out = df.groupby(["Region", "fuel_type"]).agg(
        n_plants=("e_rate_(plant_lb/MWh)", "count"),
        total_generation_mwh=("Net_Generation_(generator_MWh)", "sum"),
        mean_rate_lb_per_mwh=("e_rate_(plant_lb/MWh)", "mean"),
    ).round(1).reset_index()

    out = out.rename(columns={"Region": "region"})
    out["region_name"] = out["region"].map(REGION_NAMES)
    out = out[[
        "region", "region_name", "fuel_type", "n_plants",
        "total_generation_mwh", "mean_rate_lb_per_mwh",
    ]]

    print(out.to_string(index=False))
    out.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
