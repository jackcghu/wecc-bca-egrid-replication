"""
Drill down on the most extreme plant-level emissions rates in California.

A naive plant-level average is easily distorted by peaker plants that
ran for only a handful of hours all year -- dividing near-zero annual
emissions by an even smaller annual generation figure produces an
inflated "rate" that says little about real-world impact. This script
surfaces the top outliers so they can be inspected directly.

Input:  build/output/eGrid2018_thermal.csv
Output: results/02_outlier_drilldown.csv
"""

import pandas as pd

INPUT_PATH = "build/output/eGrid2018_thermal.csv"
OUTPUT_PATH = "results/02_outlier_drilldown.csv"
REGION = 1  # California
TOP_N = 3


def main():
    df = pd.read_csv(INPUT_PATH)
    ca = df[df["Region"] == REGION]

    cols = [
        "plant_county", "fuel_type", "NC_(generator_MW)",
        "Net_Generation_(generator_MWh)", "e_rate_(plant_lb/MWh)",
    ]
    top = ca.nlargest(TOP_N, "e_rate_(plant_lb/MWh)")[cols]

    print(f"Top {TOP_N} plant-level emissions rates in region {REGION}:")
    print(top.to_string(index=False))

    top = top.rename(columns={
        "NC_(generator_MW)": "nameplate_capacity_mw",
        "Net_Generation_(generator_MWh)": "net_generation_mwh",
        "e_rate_(plant_lb/MWh)": "e_rate_lb_per_mwh",
    })
    top.insert(0, "region", REGION)
    top.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
