"""
Plant counts and emissions-rate distribution by WECC region.

Input:  build/output/eGrid2018_thermal.csv
        (produced by running the original authors' build/code/eGrid.py
        on eGRID2018 data -- see README for how to obtain this)

Output: results/01_plant_counts_and_distribution.csv

Regions: 0 = unmatched, 1 = California, 2 = Northwest,
         3 = Southwest, 4 = Rockies
"""

import pandas as pd

INPUT_PATH = "build/output/eGrid2018_thermal.csv"
OUTPUT_PATH = "results/01_plant_counts_and_distribution.csv"

REGION_NAMES = {
    0: "Unmatched",
    1: "California",
    2: "Northwest",
    3: "Southwest",
    4: "Rockies",
}


def main():
    df = pd.read_csv(INPUT_PATH)

    print("Plant counts by region:")
    print(df["Region"].value_counts())
    print()

    stats = df.groupby("Region")["e_rate_(plant_lb/MWh)"].describe()
    print("Emissions-rate distribution by region (lb/MWh):")
    print(stats)

    out = stats[["count", "mean", "std", "50%", "75%", "max"]].reset_index()
    out.columns = [
        "region", "n_plants", "mean_rate_lb_per_mwh", "std_rate_lb_per_mwh",
        "median_rate_lb_per_mwh", "p75_rate_lb_per_mwh", "max_rate_lb_per_mwh",
    ]
    out["region_name"] = out["region"].map(REGION_NAMES)
    out = out[[
        "region", "region_name", "n_plants", "mean_rate_lb_per_mwh",
        "std_rate_lb_per_mwh", "median_rate_lb_per_mwh",
        "p75_rate_lb_per_mwh", "max_rate_lb_per_mwh",
    ]]
    out.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
