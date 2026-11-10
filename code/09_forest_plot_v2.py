#!/usr/bin/env python3
"""Regenerate Figure 6 (v2) from saved tables."""
import os, shutil
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt

T = "outputs/tables_v2"
F = "outputs/figures_v2"
os.makedirs(F, exist_ok=True)

t3 = pd.read_csv(f"{T}/table3v2_cognition_impairment.csv")
t4 = pd.read_csv(f"{T}/table4v2_depression.csv")

EXPO = {
    'ses_poor': 'Childhood SES: Poor (vs well-off)',
    'hlth_poor': 'Childhood health: Fair/Poor/Very poor (vs Good/Very good)',
    'bed_yes': 'Childhood bedridden >=1 month (vs No)'
}

M_PREFIX = {'M0': 'Model 0', 'M1': 'Model A', 'M2': 'Model B', 'M3': 'Model C'}
colors = {'M0': '#999999', 'M1': '#2b8cbe', 'M2': '#d95f0e', 'M3': '#31a354'}

# Forest plot: primary models
fig, axes = plt.subplots(1, 2, figsize=(11, 5), dpi=200, sharey=True)
for ax, tt, ttl in [(axes[0], t3, 'Cognitive impairment (mem+orient)'), (axes[1], t4, 'Depressive symptoms (CES-D >= 4)')]:
    ylabels = []; y = 0
    for e in ['ses_poor', 'hlth_poor', 'bed_yes']:
        for m in ['M0', 'M1', 'M2', 'M3']:
            sub = tt[(tt.Exposure == EXPO[e]) & (tt.Model.str.startswith(M_PREFIX[m]))]
            if len(sub) == 0:
                continue
            r = sub.iloc[0]
            ax.errorbar(r.Estimate, y, xerr=[[r.Estimate - r.CI_lower], [r.CI_upper - r.Estimate]], fmt='o', color=colors[m], capsize=2)
            ylabels.append(f"{EXPO[e].split(' (')[0]} | {m}")
            y += 1
        y += 1
        ylabels.append('')
    ax.axvline(1, color='k', lw=.8, ls='--')
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xticks([0.8, 1, 1.25, 1.5, 2])
    ax.set_title(ttl, fontsize=10, fontweight='bold')
    ax.set_xlabel('Prevalence ratio (log scale), 95% CI')
    ax.set_yticks(range(len(ylabels)))
    ax.set_yticklabels(ylabels, fontsize=7)
    ax.invert_yaxis()

fig.suptitle('Figure 6 (v2): Sequential models on a common sample (M0 unadjusted -> M3 + adult health)', fontsize=10, fontweight='bold')
fig.tight_layout()
fig.savefig(f"{F}/figure6v2_forest_sequential.png")
plt.close(fig)
print("Figure 6 regenerated successfully.")

