#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex is not installed."
    echo "Please install it with: sudo dnf install texlive-scheme-medium"
    echo "Alternatively, upload SOC450_Final_Report_Overleaf.zip directly to Overleaf."
    exit 1
fi

TARGET="${1:-new}"

if [ "$TARGET" = "legacy" ]; then
    cd "$DIR/report"
    echo "Compiling legacy final_research_report.tex..."
    pdflatex -interaction=nonstopmode final_research_report.tex
    pdflatex -interaction=nonstopmode final_research_report.tex
    echo "Success! Output generated at: $DIR/report/final_research_report.pdf"
else
    cd "$DIR/report/new_report"
    echo "Compiling master modular report (new_report/main.tex)..."
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex
    echo "Success! Output generated at: $DIR/report/new_report/main.pdf"
fi
