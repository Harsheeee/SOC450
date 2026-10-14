#!/usr/bin/env bash
# ==============================================================================
# LASI Wave 1: Master Replication Pipeline Script
# Executes the end-to-end quantitative epidemiological analysis pipeline
# ==============================================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "========================================================================"
echo "LASI Wave 1: Life-Course Disadvantage & Late-Life Health Replication"
echo "========================================================================"

# Determine Python executable
if [ -d ".venv" ]; then
    PYTHON=".venv/bin/python"
else
    PYTHON="python3"
fi

echo "Using Python: $PYTHON ($($PYTHON --version))"

# Step 1: Dataset Build (check if raw data exists)
if [ -f "dataset/3_LASI_W1_Individual_v4.dta" ]; then
    echo "[Step 1/5] Building cleaned analytic dataset from raw Stata files..."
    $PYTHON code/07_build_dataset_v2.py
elif [ -f "data_analysis/lasi_clean_v2.parquet" ]; then
    echo "[Step 1/5] Raw Stata file not found, but pre-processed data_analysis/lasi_clean_v2.parquet exists. Proceeding..."
else
    echo "ERROR: Neither dataset/3_LASI_W1_Individual_v4.dta nor data_analysis/lasi_clean_v2.parquet found."
    echo "Please see dataset/README.md for instructions on downloading the LASI microdata."
    exit 1
fi

# Step 2: Survey-Weighted Regressions and Sensitivity Analyses
echo "[Step 2/5] Fitting sequential survey-weighted models, interactions & IPW..."
$PYTHON code/08_models_v2.py

# Step 3: Visualizations & Forest Plots
echo "[Step 3/6] Generating sequential model forest plots..."
$PYTHON code/09_forest_plot_v2.py

# Step 4: Social Mobility Trajectory Models
echo "[Step 4/6] Estimating life-course social mobility models & figures..."
$PYTHON code/12_social_mobility.py

# Step 5: Continuous Cognitive Sensitivity Extension
if [ -f "extension/01_cognitive_sensitivity.py" ]; then
    echo "[Step 5/6] Running continuous cognitive domain sensitivity extension..."
    $PYTHON extension/01_cognitive_sensitivity.py
fi

# Step 6: Reports
echo "[Step 6/6] Compiling summary research reports..."
$PYTHON code/10_generate_report_v2.py
$PYTHON code/11_generate_latex_report.py

echo "========================================================================"
echo "Replication pipeline completed successfully!"
echo "Outputs available in:"
echo " - Tables:     outputs/tables_v2/"
echo " - Figures:    outputs/figures_v2/ and report/new_report/figures/"
echo " - LaTeX:      report/new_report/main.tex (Master Modular Manuscript)"
echo " - Monolithic: report/final_research_report.tex & report/final_research_report_v2.md"
echo "========================================================================"

