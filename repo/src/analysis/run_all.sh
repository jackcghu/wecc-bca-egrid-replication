#!/usr/bin/env bash
# Run all analysis scripts in order.
# Must be run from the project root (the folder containing src/, build/, results/).
set -e

python src/analysis/01_plant_counts_and_distribution.py
echo "---"
python src/analysis/02_outlier_drilldown.py
echo "---"
python src/analysis/03_weighted_vs_simple_average.py
echo "---"
python src/analysis/04_fuel_breakdown_by_region.py
