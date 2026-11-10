#!/usr/bin/env bash
# ==============================================================================
# LASI Wave 1: Master Replication Pipeline Script
# Executes the end-to-end quantitative empirical analysis pipeline for SOC450
# ==============================================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "========================================================================"
echo "LASI Wave 1: Life-Course Disadvantage & Late-Life Health Replication"
echo "Course: SOC450 - Sociology of Ageing, IIT Kanpur"
echo "========================================================================"

# Determine Python executable (prioritizing local or parent virtual environment)
if [ -d ".venv" ]; then
    PYTHON=".venv/bin/python"
elif [ -d "../.venv" ]; then
    PYTHON="../.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
else
    echo "ERROR: Python 3 executable not found."
    exit 1
fi

echo "Using Python: $PYTHON ($($PYTHON --version))"

# Step 1: Analytic Dataset Verification / Build
if [ -f "dataset/3_LASI_W1_Individual_v4.dta" ]; then
    echo "[Step 1/6] Rebuilding cleaned analytic dataset from raw Stata microdata..."
    $PYTHON code/07_build_dataset_v2.py
elif [ -f "data_analysis/lasi_clean_v2.parquet" ]; then
    echo "[Step 1/6] Raw Stata file not detected; verified pre-processed data_analysis/lasi_clean_v2.parquet."
else
    echo "ERROR: Neither dataset/3_LASI_W1_Individual_v4.dta nor data_analysis/lasi_clean_v2.parquet found."
    echo "Please see dataset/README.md for instructions on downloading the LASI microdata."
    exit 1
fi

# Step 2: Descriptive Statistics and Distribution Figures
if [ -f "data_analysis/lasi_clean_analysis.parquet" ]; then
    echo "[Step 2/6] Generating descriptive characteristics and prevalence plots..."
    $PYTHON code/03_descriptive_analysis.py
else
    echo "[Step 2/6] Skipping descriptive script (data_analysis/lasi_clean_analysis.parquet not found)."
fi

# Step 3: Survey-Weighted Regressions, Interaction Tests & IPW
echo "[Step 3/6] Fitting survey-weighted Poisson models, interaction tests, and IPW..."
$PYTHON code/08_models_v2.py

# Step 4: Forest Plots
echo "[Step 4/6] Generating sequential model forest plots..."
$PYTHON code/09_forest_plot_v2.py

# Step 5: Intergenerational Social Mobility Trajectory Models
echo "[Step 5/6] Estimating intergenerational social mobility models and figures..."
$PYTHON code/12_social_mobility.py

# Step 6: Continuous Cognitive Domain Sensitivity Extension
if [ -f "extension/01_cognitive_sensitivity.py" ]; then
    echo "[Step 6/6] Estimating continuous cognitive domain sensitivity models..."
    $PYTHON extension/01_cognitive_sensitivity.py
fi

echo "========================================================================"
echo "Replication pipeline completed successfully."
echo "Generated outputs are available in:"
echo "  - Descriptive tables: outputs/tables/"
echo "  - Primary model tables: outputs/tables_v2/"
echo "  - Descriptive figures: outputs/figures/"
echo "  - Primary model figures: outputs/figures_v2/"
echo "  - Diagnostic summaries: outputs/diagnostics/"
echo "  - Extension results: extension/continuous_cognitive_sensitivity.csv"
echo "  - Full Research Report: report.pdf"
echo "========================================================================"
