#!/usr/bin/env python3
"""
Step 06: Generate Self-Contained, Publication-Ready HTML Report
- Converts report/final_research_report.md into a fully self-contained HTML document
- Encodes Figures 1-5 directly into base64 data URIs (fully portable, no external links)
- Applies professional journal-grade CSS styling with print support
"""

import os
import re
import base64
import markdown

MD_PATH = "report/final_research_report.md"
HTML_PATH = "report/final_research_report.html"
FIGS_DIR = "outputs/figures"

print("Reading Markdown report from:", MD_PATH)
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# Encode figures as base64 data URIs
fig_files = {
    "figure1": os.path.join(FIGS_DIR, "figure1_age_distribution.png"),
    "figure2": os.path.join(FIGS_DIR, "figure2_childhood_disadvantage_prevalence.png"),
    "figure3": os.path.join(FIGS_DIR, "figure3_outcome_prevalence_by_age.png"),
    "figure4": os.path.join(FIGS_DIR, "figure4_cognitive_interaction.png"),
    "figure5": os.path.join(FIGS_DIR, "figure5_depression_interaction.png"),
}

fig_b64 = {}
for key, path in fig_files.items():
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            b64_str = base64.b64encode(img_file.read()).decode("utf-8")
            fig_b64[key] = f"data:image/png;base64,{b64_str}"

# Insert images into markdown before conversion
# In the markdown, we have sections where figures belong
img_insert_map = {
    "Figure 1 illustrates": f'<div class="figure-container"><img src="{fig_b64.get("figure1", "")}" alt="Figure 1: Age Distribution" /><p class="figure-caption"><strong>Figure 1:</strong> Survey-weighted population age distribution of Indian adults aged 45 and above in LASI Wave 1 (N = 66,606).</p></div>\n\nFigure 1 illustrates',
    "Figure 2 summarizes": f'<div class="figure-container"><img src="{fig_b64.get("figure2", "")}" alt="Figure 2: Childhood Disadvantage Prevalence" /><p class="figure-caption"><strong>Figure 2:</strong> Survey-weighted prevalence of early-life disadvantage exposures among adults aged 45 and above.</p></div>\n\nFigure 2 summarizes',
    "Table 2 and Figure 3 depict": f'<div class="figure-container"><img src="{fig_b64.get("figure3", "")}" alt="Figure 3: Outcome Prevalence across Age Groups" /><p class="figure-caption"><strong>Figure 3:</strong> Survey-weighted prevalence of cognitive impairment and depressive symptoms across age strata (45–59, 60–74, 75+).</p></div>\n\nTable 2 and Figure 3 depict',
    "ADJUSTED PREDICTED COGNITIVE IMPAIRMENT ACROSS AGE STRATA (FIGURE 4)": f'ADJUSTED PREDICTED COGNITIVE IMPAIRMENT ACROSS AGE STRATA (FIGURE 4)\n```\n<div class="figure-container"><img src="{fig_b64.get("figure4", "")}" alt="Figure 4: Cognitive Interaction" /><p class="figure-caption"><strong>Figure 4:</strong> Adjusted predicted prevalence of cognitive impairment by childhood SES across age groups with 95% confidence intervals.</p></div>\n```',
    "ADJUSTED PREDICTED DEPRESSIVE SYMPTOMS ACROSS AGE STRATA (FIGURE 5)": f'ADJUSTED PREDICTED DEPRESSIVE SYMPTOMS ACROSS AGE STRATA (FIGURE 5)\n```\n<div class="figure-container"><img src="{fig_b64.get("figure5", "")}" alt="Figure 5: Depression Interaction" /><p class="figure-caption"><strong>Figure 5:</strong> Adjusted predicted prevalence of depressive symptoms by childhood SES across age groups with 95% confidence intervals.</p></div>\n```'
}

for target, replacement in img_insert_map.items():
    if target in md_content:
        md_content = md_content.replace(target, replacement, 1)

# Convert Markdown to HTML with table and fenced code extensions
html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])

# Build complete publication HTML with elegant styling
full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LASI Wave 1 Ageing Study: Research Report</title>
<style>
  :root {{
    --primary: #1a365d;
    --primary-light: #2b6cb0;
    --accent: #2c5282;
    --text: #2d3748;
    --text-muted: #718096;
    --bg: #ffffff;
    --bg-alt: #f7fafc;
    --border: #e2e8f0;
    --callout-bg: #ebf8ff;
    --callout-border: #3182ce;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: var(--text);
    background-color: var(--bg);
    line-height: 1.68;
    margin: 0;
    padding: 0;
    font-size: 15px;
  }}

  .container {{
    max-width: 960px;
    margin: 40px auto;
    padding: 0 32px 80px 32px;
    background: #ffffff;
  }}

  h1 {{
    color: var(--primary);
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1.25;
    margin-bottom: 12px;
    border-bottom: 3px solid var(--primary);
    padding-bottom: 16px;
  }}

  h2 {{
    color: var(--primary);
    font-size: 1.5rem;
    font-weight: 700;
    margin-top: 40px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }}

  h3 {{
    color: var(--accent);
    font-size: 1.2rem;
    font-weight: 600;
    margin-top: 24px;
    margin-bottom: 12px;
  }}

  h4 {{
    font-size: 1.05rem;
    font-weight: 600;
    margin-top: 18px;
  }}

  p, li {{
    color: var(--text);
  }}

  blockquote {{
    margin: 20px 0;
    padding: 16px 20px;
    background: var(--callout-bg);
    border-left: 4px solid var(--callout-border);
    border-radius: 4px;
  }}

  blockquote p {{
    margin: 0;
    font-size: 0.95rem;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    font-size: 0.9rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}

  table th, table td {{
    padding: 10px 14px;
    text-align: left;
    border: 1px solid var(--border);
  }}

  table th {{
    background-color: #f1f5f9;
    color: var(--primary);
    font-weight: 600;
  }}

  table tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  table tr:hover {{
    background-color: #f1f5f9;
  }}

  .figure-container {{
    margin: 32px 0;
    padding: 16px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    text-align: center;
  }}

  .figure-container img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
  }}

  .figure-caption {{
    margin-top: 12px;
    font-size: 0.88rem;
    color: var(--text-muted);
    line-height: 1.4;
    text-align: left;
    padding: 0 8px;
  }}

  code {{
    font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.88em;
    background: #edf2f7;
    padding: 2px 6px;
    border-radius: 3px;
  }}

  pre {{
    background: #1a202c;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 0.85rem;
    line-height: 1.5;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  hr {{
    border: 0;
    height: 1px;
    background: var(--border);
    margin: 36px 0;
  }}

  .meta-box {{
    background: #f7fafc;
    padding: 16px 20px;
    border-radius: 6px;
    border: 1px solid var(--border);
    margin-bottom: 24px;
    font-size: 0.92rem;
  }}

  @media print {{
    body {{
      font-size: 11pt;
      line-height: 1.4;
    }}
    .container {{
      max-width: 100%;
      margin: 0;
      padding: 0;
    }}
    .figure-container {{
      page-break-inside: avoid;
      box-shadow: none;
      border: none;
    }}
    table {{
      page-break-inside: avoid;
    }}
  }}
</style>
</head>
<body>
<div class="container">
{html_body}
</div>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Successfully generated self-contained HTML report ({len(full_html):,} bytes) at:")
print(f"  - {HTML_PATH}")
