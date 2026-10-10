#!/usr/bin/env python3
"""
Survey utilities (Protocol Amendment 1, A5): design-based stratified-cluster (Taylor linearization)
variance for GLMs fitted with normalized sampling weights. df = n_clusters - n_strata.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

FAMS = {'poisson': sm.families.Poisson, 'gaussian': sm.families.Gaussian, 'binomial': sm.families.Binomial}


class SvyFit:
    pass


def svy_glm(formula, data, family='poisson', wcol='survey_weight', cluster='cluster_psu', stratum='stratum'):
    d = data.reset_index(drop=True)
    w = d[wcol].values.astype(float)
    w = w / w.mean()
    model = smf.glm(formula, d, family=FAMS[family](), freq_weights=w)
    res = model.fit()
    assert int(res.nobs) == len(d) or len(res.model.endog) == len(d), "rows dropped silently; pass complete data"
    y, X, mu = model.endog, model.exog, res.mu
    resid = w * (y - mu)
    if family == 'poisson':
        ww = w * mu
    elif family == 'binomial':
        ww = w * mu * (1 - mu)
    else:
        ww = w
    bread = np.linalg.inv(X.T @ (X * ww[:, None]))
    u = pd.DataFrame(X * resid[:, None])
    key = pd.DataFrame({'s': d[stratum].values, 'c': d[cluster].values})
    cs = u.groupby([key['s'], key['c']]).sum()
    s_idx = cs.index.get_level_values(0)
    nh = pd.Series(1, index=cs.index).groupby(level=0).transform('sum').values
    cs_c = cs - cs.groupby(level=0).transform('mean')
    fac = np.where(nh > 1, nh / np.maximum(nh - 1, 1), 0.0)
    M = cs_c.values * np.sqrt(fac)[:, None]
    S = M.T @ M
    V = bread @ S @ bread
    f = SvyFit()
    f.names = list(res.params.index)
    f.params = res.params
    f.V = pd.DataFrame(V, index=f.names, columns=f.names)
    f.se = pd.Series(np.sqrt(np.diag(V)), index=f.names)
    f.df = cs.shape[0] - s_idx.nunique()
    f.nobs = len(d)
    f.nclust = cs.shape[0]
    f.res = res
    f.model = model
    f.family = family
    return f


def term_row(f, term, exp=True):
    b, se = f.params[term], f.se[term]
    t = stats.t.ppf(0.975, f.df)
    p = 2 * stats.t.sf(abs(b / se), f.df)
    if exp:
        return dict(est=np.exp(b), lo=np.exp(b - t * se), hi=np.exp(b + t * se), p=p)
    return dict(est=b, lo=b - t * se, hi=b + t * se, p=p)


def wald_F(f, terms):
    idx = [f.names.index(t) for t in terms]
    b = f.params.values[idx]
    Vs = f.V.values[np.ix_(idx, idx)]
    W = float(b @ np.linalg.solve(Vs, b))
    q = len(idx)
    F = W / q
    return F, stats.f.sf(F, q, f.df - q + 1)


def wmean_ci(data, ycol, wcol='survey_weight'):
    sub = data.dropna(subset=[ycol])
    f = svy_glm(f"{ycol} ~ 1", sub, 'gaussian', wcol)
    r = term_row(f, 'Intercept', exp=False)
    return r['est'], r['lo'], r['hi'], f.nobs
