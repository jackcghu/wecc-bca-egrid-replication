"""
Generation-weighted vs. simple regional average emissions intensity.

A simple mean treats every plant equally regardless of how much it
actually generated -- so a single idle peaker plant with an absurd
"rate" can swing the average. Weighting each plant's rate by its
actual annual generation gives the economically meaningful number:
what's really being emitted per MWh actually produced.

Input:  build/output/eGrid2018_thermal.csv
Output: results/03_weighted_vs_simple_average.csv
"""

import numpy as np
import pandas as pd

INPUT_PATH = "build/output/eGrid2018_thermal.csv"
OUTPUT_PATH = "results/03_weighted_vs_simple_average.csv"
LB_PER_MWH_TO_TONNES_PER_MWH = 0.00045359237

REGION_NAMES = {1: "California", 2: "Northwest", 3: "Southwest", 4: "Rockies"}


def weighted_avg(group):
    return np.average(
        group["e_rate_(plant_lb/MWh)"],
        weights=group["Net_Generation_(generator_MWh)"],
    )


def main():
    df = pd.read_csv(INPUT_PATH)
    df = df[df["Region"] != 0]  # drop the small unmatched bucket

    weighted = df.groupby("Region").apply(weighted_avg)
    simple_mean = df.groupby("Region")["e_rate_(plant_lb/MWh)"].mean()
    simple_median = df.groupby("Region")["e_rate_(plant_lb/MWh)"].median()

    out = pd.DataFrame({
        "simple_mean_lb_per_mwh": simple_mean.round(1),
        "simple_median_lb_per_mwh": simple_median.round(1),
        "generation_weighted_lb_per_mwh": weighted.round(1),
    }).reset_index().rename(columns={"Region": "region"})

    out["generation_weighted_tonnes_per_mwh"] = (
        out["generation_weighted_lb_per_mwh"] * LB_PER_MWH_TO_TONNES_PER_MWH
    ).round(3)
    out["region_name"] = out["region"].map(REGION_NAMES)
    out = out[[
        "region", "region_name", "simple_mean_lb_per_mwh",
        "simple_median_lb_per_mwh", "generation_weighted_lb_per_mwh",
        "generation_weighted_tonnes_per_mwh",
    ]]

    print(out.to_string(index=False))
    out.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
