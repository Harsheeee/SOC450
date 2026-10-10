#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR/report"

if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex is not installed."
    echo "Please install it with: sudo dnf install texlive-scheme-medium"
    exit 1
fi

echo "Compiling final_research_report.tex (Pass 1)..."
pdflatex -interaction=nonstopmode final_research_report.tex

echo "Compiling final_research_report.tex (Pass 2 for cross-references)..."
pdflatex -interaction=nonstopmode final_research_report.tex

echo "Success! Output generated at: $DIR/report/final_research_report.pdf"
