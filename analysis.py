"""Economic Divergence & Inequality Report - analysis.
Data: RBI Handbook of Statistics on Indian States, Table 10 (per capita NSDP, constant prices, Rs).
Run build_data.py first. Run from the project folder.
"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("data/per_capita_nsdp_table10.csv")
BASES = ["1999-00", "2004-05", "2011-12"]
ALL_INDIA = "All-India per capita NNI"
UTS = ["Andaman & Nicobar Islands", "Chandigarh", "Delhi", "Puducherry"]

def wide(b, states=None):
    w = df[df.base == b].pivot(index="year", columns="state", values="pc_nsdp")
    return w if states is None else w[states]

india = {b: wide(b)[ALL_INDIA] for b in BASES}
STATES = [s for s in df.state.unique() if s != ALL_INDIA and s not in UTS]       # 28 states + J&K = 29
FIRST11 = ["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana",
           "Himachal Pradesh","Jammu & Kashmir","Jharkhand"]
MAJOR17 = ["Andhra Pradesh","Assam","Bihar","Chhattisgarh","Gujarat","Haryana","Jharkhand","Karnataka","Kerala",
           "Madhya Pradesh","Maharashtra","Odisha","Punjab","Rajasthan","Tamil Nadu","Uttar Pradesh","West Bengal"]
BROAD = [s for s in STATES if s != "Telangana"]        # Telangana has no data before 2011-12 (formed 2014)
SAMPLES = {
    "Major 17 states (main)": MAJOR17,
    "Broad 28 (all with full history)": BROAD,
    "Broad 28 excl. Goa & Sikkim": [s for s in BROAD if s not in ("Goa", "Sikkim")],
    "First 11 (screenshot set)": FIRST11,
    "First 11 excl. Goa": [s for s in FIRST11 if s != "Goa"],
}

# ---------- inequality measures (unweighted across states) ----------
def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    return (2*np.sum(np.arange(1, n+1)*x) / (n*x.sum())) - (n+1)/n
def cv(x):    x = np.asarray(x, float); return x.std(ddof=0)/x.mean()
def sdlog(x): return np.log(np.asarray(x, float)).std(ddof=0)          # "sigma" in convergence literature
def theil(x): x = np.asarray(x, float); r = x/x.mean(); return np.mean(r*np.log(r))
def top_bottom(x, k=5): x = np.sort(np.asarray(x, float)); return x[-k:].mean()/x[:k].mean()

def metrics(w):
    out = pd.DataFrame(index=w.index)
    out["Gini"] = w.apply(gini, axis=1);  out["CV"] = w.apply(cv, axis=1)
    out["SD_log"] = w.apply(sdlog, axis=1); out["Theil"] = w.apply(theil, axis=1)
    out["Max/Min"] = w.max(axis=1)/w.min(axis=1); out["Top5/Bottom5"] = w.apply(top_bottom, axis=1)
    return out

# ---------- splice the three base series into one (2011-12 prices) ----------
def splice(w1, w2, w3):
    sp = pd.DataFrame(index=list(w1.index[:-1]) + list(w2.index[:-1]) + list(w3.index), columns=w3.columns, dtype=float)
    sp.loc[w3.index] = w3
    f2 = w3.loc["2011-12"]/w2.loc["2011-12"]
    for y in w2.index[:-1]: sp.loc[y] = w2.loc[y]*f2
    f1 = sp.loc["2004-05"]/w1.loc["2004-05"]
    for y in w1.index[:-1]: sp.loc[y] = w1.loc[y]*f1
    return sp.sort_index()

def spliced_for(cols):
    return splice(*[wide(b, cols) for b in BASES])

def trend(m, k):
    r = stats.linregress(np.arange(len(m)), m[k]); return r.slope, r.pvalue

def run_sample(name, cols):
    print(f"\n{'='*92}\nSAMPLE: {name}  (n={len(cols)})\n{'='*92}")
    res = {"cols": cols}
    seg = {}
    for b in BASES:
        w = wide(b, cols).dropna()                                 # complete cross-sections only
        seg[b] = metrics(w)
        m = seg[b]
        print(f"Base {b}: years {m.index[0]}..{m.index[-1]} | Gini {m.Gini.iloc[0]:.3f}->{m.Gini.iloc[-1]:.3f} "
              f"(slope {trend(m,'Gini')[0]:+.4f}, p={trend(m,'Gini')[1]:.3f}) | "
              f"SD_log {m.SD_log.iloc[0]:.3f}->{m.SD_log.iloc[-1]:.3f} (slope {trend(m,'SD_log')[0]:+.4f}, p={trend(m,'SD_log')[1]:.3f})"
              f" | CV {m.CV.iloc[0]:.3f}->{m.CV.iloc[-1]:.3f} (slope {trend(m,'CV')[0]:+.4f}, p={trend(m,'CV')[1]:.3f})")
    res["seg"] = seg
    sp = spliced_for(cols); res["sp_all"] = sp
    sp = sp.dropna(); res["sp"] = sp
    m = metrics(sp); res["sp_m"] = m
    print(f"Spliced {sp.index[0]}..{sp.index[-1]} ({len(sp)} yrs):")
    for k in ["Gini", "CV", "SD_log", "Theil", "Top5/Bottom5", "Max/Min"]:
        s, p = trend(m, k)
        print(f"   {k:13s} {m[k].iloc[0]:7.3f} -> {m[k].iloc[-1]:7.3f}   slope/yr {s:+.5f}  p={p:.4f}")
    # beta convergence on spliced full period
    n = len(sp) - 1
    g = ((sp.iloc[-1]/sp.iloc[0])**(1/n) - 1)*100
    r = stats.linregress(np.log(sp.iloc[0]), g)
    print(f"   BETA (spliced growth vs ln initial): slope {r.slope:+.3f}  p={r.pvalue:.3f}  R2={r.rvalue**2:.2f}")
    res["beta"] = r; res["g"] = g
    # rank persistence
    rho, prho = stats.spearmanr(sp.iloc[0], sp.iloc[-1])
    top0 = set(sp.iloc[0].nlargest(5).index); top1 = set(sp.iloc[-1].nlargest(5).index)
    bot0 = set(sp.iloc[0].nsmallest(5).index); bot1 = set(sp.iloc[-1].nsmallest(5).index)
    print(f"   Rank persistence: Spearman {rho:.2f}; top-5 in both years {sorted(top0 & top1)}; bottom-5 in both {sorted(bot0 & bot1)}")
    res["rank"] = (rho, top0, top1, bot0, bot1)
    # per-base beta
    for b in BASES:
        w = wide(b, cols).dropna(); nn = len(w) - 1
        gg = ((w.iloc[-1]/w.iloc[0])**(1/nn) - 1)*100
        rr = stats.linregress(np.log(w.iloc[0]), gg)
        print(f"   beta base {b} ({nn} yrs): {rr.slope:+.3f} (p={rr.pvalue:.3f})")
    return res

R = {k: run_sample(k, v) for k, v in SAMPLES.items()}

# ---------- all-India benchmark, spliced ----------
ind_sp = splice(*[india[b].to_frame("India") for b in BASES])["India"].dropna()
sp_all = spliced_for(BROAD)                                         # every state with full history, all years
sp_all_full = sp_all.dropna(how="all")

# ---------- growth velocity (common end year 2024-25; Nagaland only reports to 2023-24) ----------
END = "2024-25"
rows = []
for st in BROAD:
    r = dict(state=st)
    for b in BASES:
        s = wide(b)[st].dropna(); r[f"CAGR {b}"] = ((s.iloc[-1]/s.iloc[0])**(1/(len(s)-1)) - 1)*100
    s = sp_all[st].dropna(); s = s.loc[:END]
    r["Spliced start"] = s.iloc[0]; r["Spliced end"] = s.iloc[-1]; r["End year"] = s.index[-1]
    r["CAGR spliced"] = ((s.iloc[-1]/s.iloc[0])**(1/(len(s)-1)) - 1)*100; r["Multiple"] = s.iloc[-1]/s.iloc[0]
    rows.append(r)
gv = pd.DataFrame(rows).set_index("state").sort_values("CAGR spliced", ascending=False)
print("\n=== Growth velocity, % p.a. (spliced 2001-02 to 2024-25; Nagaland to 2023-24) ===\n", gv.round(2).to_string())
gv.round(3).to_csv("data/growth_velocity.csv")
print("Rank of Bihar / Chhattisgarh / Gujarat / Haryana / Goa by spliced CAGR (of 28):",
      {k: int(gv["CAGR spliced"].rank(ascending=False)[k]) for k in ["Bihar","Chhattisgarh","Gujarat","Haryana","Goa"]}, "| median CAGR", round(gv["CAGR spliced"].median(),2))

# ---------- relative position vs All-India ----------
sp_c = sp_all[["Goa","Gujarat","Haryana","Bihar","Chhattisgarh","Uttar Pradesh","Maharashtra","Tamil Nadu","Karnataka","Kerala"]].dropna()
rel = sp_c.div(ind_sp.reindex(sp_c.index), axis=0)*100
print("\n=== State as % of All-India per capita NNI (spliced) ===\n", rel.iloc[[0,5,10,15,-1]].round(1).T.to_string())
sp17 = R["Major 17 states (main)"]["sp"]
rel17 = pd.DataFrame({"Bihar % of 17-state mean": sp17["Bihar"]/sp17.mean(axis=1)*100,
                      "Chhattisgarh % of 17-state mean": sp17["Chhattisgarh"]/sp17.mean(axis=1)*100,
                      "Bihar % of Gujarat": sp17["Bihar"]/sp17["Gujarat"]*100,
                      "Bihar % of Haryana": sp17["Bihar"]/sp17["Haryana"]*100,
                      "Chhattisgarh % of Gujarat": sp17["Chhattisgarh"]/sp17["Gujarat"]*100,
                      "Chhattisgarh % of Haryana": sp17["Chhattisgarh"]/sp17["Haryana"]*100})
print("\n=== Relative position within Major 17 ===\n", rel17.iloc[[0,5,10,15,-1]].round(1).to_string())
rel.round(2).to_csv("data/relative_to_all_india.csv"); rel17.round(2).to_csv("data/relative_position_major17.csv")
gap = pd.DataFrame({"Gujarat-Bihar": sp17["Gujarat"]-sp17["Bihar"], "Haryana-Bihar": sp17["Haryana"]-sp17["Bihar"]})
print("\nAbsolute gaps Rs (2011-12 prices), first/last:\n", gap.iloc[[0,-1]].round(0).to_string())
goa_bihar = (sp_all["Goa"]/sp_all["Bihar"]).loc[:END]; print("Goa/Bihar ratio first/last:", round(goa_bihar.iloc[0],1), round(goa_bihar.iloc[-1],1))

# 2025-26 snapshot
w3 = wide("2011-12"); g2526 = ((w3.loc["2025-26"]/w3.loc["2024-25"] - 1)*100).dropna().round(1)
print("\n2025-26 growth over 2024-25 (states reporting):\n", g2526.to_string())
print("Goa 2011-12..2015-16:", w3["Goa"].iloc[:5].tolist(), "| 2020-21 vs 2019-20 % chg (Bihar, Haryana, Goa):",
      ((w3.loc["2020-21"]/w3.loc["2019-20"] - 1)*100).round(1)[["Bihar","Haryana","Goa"]].to_dict())

# ---------- save tables ----------
out = pd.concat({k: v["sp_m"] for k, v in R.items()}, axis=1); out.round(4).to_csv("data/spliced_inequality_by_sample.csv")
seg_rows = []
for k, v in R.items():
    for b in BASES:
        m = v["seg"][b].copy(); m.insert(0, "base", b); m.insert(0, "sample", k); seg_rows.append(m.reset_index(names="year"))
pd.concat(seg_rows).round(4).to_csv("data/inequality_within_base.csv", index=False)
sp_all_full.round(0).to_csv("data/spliced_per_capita_nsdp_28_states.csv")

# ---------- figures ----------
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9})
C = {"Goa":"#b8860b","Gujarat":"#c0392b","Haryana":"#e67e22","Bihar":"#1f4e79","Chhattisgarh":"#2e86c1"}
main = R["Major 17 states (main)"]; broad = R["Broad 28 (all with full history)"]; first11 = R["First 11 (screenshot set)"]

fig, ax = plt.subplots(1, 3, figsize=(12, 3.6))
for a_, k, t in zip(ax, ["Gini", "CV", "SD_log"], ["Gini coefficient", "Coefficient of variation", "Std. dev. of ln(per-capita NSDP)"]):
    for b, c in zip(BASES, ["#7f8c8d", "#2c3e50", "#c0392b"]):
        m = main["seg"][b]; a_.plot(m.index, m[k], marker="o", ms=3, color=c, label=f"base {b}")
    a_.set_title(t); a_.tick_params(axis="x", rotation=90, labelsize=6)
ax[0].legend(frameon=False, fontsize=7)
fig.suptitle("Major 17 states: inequality within each base series (levels are NOT comparable across bases)", fontsize=9)
fig.tight_layout(); fig.savefig("figures/01_inequality_by_base.png"); plt.close()

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
for key, col, lab in [("Major 17 states (main)", "#c0392b", "Major 17"), ("Broad 28 (all with full history)", "#2c3e50", "Broad 28"),
                      ("Broad 28 excl. Goa & Sikkim", "#16a085", "Broad 28 excl. Goa & Sikkim")]:
    m = R[key]["sp_m"]
    ax[0].plot(m.index, m.Gini, marker="o", ms=3, color=col, label=lab); ax[1].plot(m.index, m.SD_log, marker="o", ms=3, color=col, label=lab)
for a_, t in zip(ax, ["Gini", "Std. dev. of ln(per-capita NSDP)  (sigma)"]):
    a_.set_title(t + ", spliced to 2011-12 prices"); a_.tick_params(axis="x", rotation=90, labelsize=7)
    for c in ["2004-05", "2011-12"]: a_.axvline(c, ls=":", color="grey")
ax[0].legend(frameon=False, fontsize=8); fig.tight_layout(); fig.savefig("figures/02_spliced_inequality.png"); plt.close()

fig, ax = plt.subplots(figsize=(8, 4.2))
for st in ["Goa", "Gujarat", "Haryana", "Chhattisgarh", "Bihar"]:
    s = sp_all[st].dropna(); ax.plot(s.index, s/1000, color=C[st], label=st, lw=1.8)
ax.plot(ind_sp.index, ind_sp/1000, color="black", ls="--", lw=1.2, label="All-India")
ax.set_yscale("log"); ax.set_ylabel("Rs '000 (log scale), 2011-12 prices"); ax.legend(frameon=False, ncol=6, fontsize=7, loc="upper left")
ax.tick_params(axis="x", rotation=90, labelsize=7); ax.set_title("Per-capita NSDP: high-income vs low-income states (spliced)")
fig.tight_layout(); fig.savefig("figures/03_levels_log.png"); plt.close()

sp, g, r = main["sp"], main["g"], main["beta"]
fig, ax = plt.subplots(figsize=(6.8, 4.6)); x0 = np.log(sp.iloc[0])
ax.scatter(x0, g, s=40, color="#2c3e50")
for st in sp.columns: ax.annotate(st, (x0[st], g[st]), fontsize=7, xytext=(3, 3), textcoords="offset points")
xs = np.linspace(x0.min(), x0.max(), 50); ax.plot(xs, r.intercept + r.slope*xs, "--", color="#c0392b", label=f"slope {r.slope:.2f} (p={r.pvalue:.2f})")
ax.set_xlabel("ln(per-capita NSDP in 2001-02, 2011-12 prices)"); ax.set_ylabel("CAGR 2001-02 to 2024-25 (%)"); ax.legend(frameon=False, fontsize=8)
ax.set_title("Beta-convergence test, major 17 states"); fig.tight_layout(); fig.savefig("figures/04_beta_convergence.png"); plt.close()

fig, ax = plt.subplots(figsize=(8, 3.8))
for st in ["Bihar", "Chhattisgarh", "Uttar Pradesh"]:
    ax.plot(rel.index if st in rel else sp_c.index, (sp_all[st].dropna().reindex(rel.index)/ind_sp.reindex(rel.index)*100), marker="o", ms=3, label=st,
            color=C.get(st, "#7f8c8d"))
ax.axhline(100, color="black", lw=0.8, ls="--"); ax.set_ylabel("% of All-India per-capita NNI"); ax.legend(frameon=False)
ax.tick_params(axis="x", rotation=90, labelsize=7); ax.set_title("Catching up with the national average?")
fig.tight_layout(); fig.savefig("figures/05_relative_position.png"); plt.close()

fig, ax = plt.subplots(figsize=(7.5, 7))
gs = gv["CAGR spliced"].sort_values()
cols = ["#1f4e79" if s in ("Bihar", "Chhattisgarh") else "#b8860b" if s in ("Goa", "Gujarat", "Haryana") else "#95a5a6" for s in gs.index]
ax.barh(gs.index, gs.values, color=cols); ax.set_xlabel("CAGR of real per-capita NSDP, 2001-02 to 2024-25 (%)  [Nagaland to 2023-24]")
ax.set_title("Growth velocity, 28 states (spliced)"); fig.tight_layout(); fig.savefig("figures/06_growth_velocity.png"); plt.close()
print("\nfigures saved")
