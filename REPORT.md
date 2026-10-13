# The Economic Divergence & Inequality Report
### Are India's richer and poorer states converging? Evidence from per-capita NSDP, 2001-02 to 2024-25

**Data:** RBI Handbook of Statistics on Indian States, Table 10, Per Capita Net State Domestic Product, state-wise, at constant prices (₹). Source: National Statistics Office. Original workbook kept unedited in `data/raw/`.
**Code:** `build_data.py` reads the workbook, `analysis.py` produces every number and figure below.

---

## 1. Headline findings

1. **The gap is widening, not closing.** Across the 17 major states, the Gini coefficient rises from 0.194 in 2001-02 to 0.254 in 2024-25. The spread of log income rises from 0.395 to 0.503 and the top-5 to bottom-5 income ratio rises from 2.4 to 3.1. Every measure moves the same way.
2. **There is no sign of catch-up.** States that started poor did not grow faster than states that started rich. The test slope is positive (+0.78) and not statistically different from zero, so the data show no convergence.
3. **The same states stay at the bottom.** Bihar, Jharkhand, Madhya Pradesh and Uttar Pradesh are in the bottom five in both 2001-02 and 2024-25. Haryana, Karnataka and Maharashtra stay in the top five. The Spearman rank correlation between the two years is 0.83.
4. **Bihar is running to stand still.** Its income has stayed at roughly one third of the All-India figure (33% in 2001-02, 32% in 2024-25). It grew 5.1% a year, which is close to the national median of 5.0%, but from so low a base that the rupee gap with Gujarat grew about 6.4 times.
5. **Chhattisgarh is falling behind.** It slipped from 94% to 82% of the All-India figure, and from 85% to 45% of Gujarat.
6. **Gujarat is the clear divergence story.** It grew 7.6% a year (second fastest of 28 states), rising from 110% to 182% of the All-India figure.

## 2. Method

| Step | What was done |
|---|---|
| Inequality measures | Gini, coefficient of variation (CV), standard deviation of ln(income), which is the "sigma" of convergence theory, plus Theil, max/min ratio and top-5 to bottom-5 ratio, computed for every year. States are weighted equally, not by population. |
| Base-year breaks | The table has three separate series (base 1999-2000, 2004-05, 2011-12). RBI notes that data before 2011-12 are NSDP at factor cost, so levels from different bases are **not comparable**. Inequality is first computed *within* each base. |
| Splicing | For one 24-year view, the older series are chained to 2011-12 prices using each state's own growth rates at the overlap years (2004-05 and 2011-12). This is standard practice but approximate (see §6). |
| Samples | **Major 17 states** (main): Andhra Pradesh, Assam, Bihar, Chhattisgarh, Gujarat, Haryana, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Odisha, Punjab, Rajasthan, Tamil Nadu, Uttar Pradesh, West Bengal. **Broad 28:** every state and Jammu & Kashmir with full history (Telangana left out, no data before 2011-12). **Broad 28 excluding Goa and Sikkim**, and the **first 11 states** from the screenshot version, as robustness checks. Union Territories (Delhi, Chandigarh, Puducherry, Andaman & Nicobar) are excluded. |
| Convergence tests | Sigma convergence (does dispersion fall over time?) and beta convergence (does low initial income predict faster growth?). |
| 2025-26 | Only some states report it, so it is excluded from inequality calculations and used as a growth snapshot only. Nagaland has no 2024-25 value, so the Broad 28 results end in 2023-24. |

## 3. Is the gap closing or widening?

**Major 17 states, within each base series**

| Base series | Years | Gini start → end | Slope per year | p-value |
|---|---|---|---|---|
| 1999-2000 | 2001-02 → 2004-05 | 0.197 → 0.205 | +0.0020 | 0.37 (only 4 points) |
| 2004-05 | 2004-05 → 2011-12 | 0.205 → 0.239 | +0.0041 | 0.003 |
| 2011-12 | 2011-12 → 2024-25 | 0.227 → 0.254 | +0.0020 | < 0.001 |

All three series point the same direction, and the two longer ones are statistically clear. This matters because each series stands on its own, so the result does not depend on the splicing.

**Spliced 2001-02 to 2024-25, Major 17**

| Measure | Start → end | Slope per year |
|---|---|---|
| Gini | 0.194 → 0.254 | +0.0027 |
| CV | 0.341 → 0.449 | +0.0049 |
| Std. dev. of ln(income) | 0.395 → 0.503 | +0.0048 |
| Theil | 0.061 → 0.104 | +0.0020 |
| Top 5 / bottom 5 income ratio | 2.36 → 3.11 | +0.033 |
| Max / min ratio | 4.9 → 5.8 | +0.049 |

**Robustness across samples (spliced)**

| Sample | Gini | Std. dev. of ln(income) |
|---|---|---|
| Major 17 (to 2024-25) | 0.194 → 0.254 | 0.395 → 0.503 |
| Broad 28 (to 2023-24) | 0.227 → 0.280 | 0.418 → 0.512 |
| Broad 28 excluding Goa and Sikkim | 0.171 → 0.237 | 0.343 → 0.451 |
| First 11 (screenshot set) | 0.304 → 0.312 | 0.570 → 0.590 |

In every sample the Gini and the log-spread rise. The one exception is the CV in the Broad 28 sample, which stays flat (0.520 → 0.520), and in the First 11 sample, where it falls. In both cases the cause is Goa. Its per-capita income dropped from ₹259k to ₹188k between 2011-12 and 2013-14 and then grew slowest of any state, which pulls down the CV, a measure that is very sensitive to a single outlier. **Where one extreme state is removed or the sample is larger, the widening shows up clearly.** The first draft of this report used only the first 11 columns, where Goa's weight hid part of the widening.

*Figures: `figures/01_inequality_by_base.png`, `figures/02_spliced_inequality.png`.*

## 4. Why do Goa, Gujarat and Haryana stay on top?

The table gives levels and growth, not causes. The points below are **hypotheses consistent with the data, backed by general development knowledge, not tested here**.

- **Goa: a small, narrow economy.** At ₹342k in 2024-25 it is more than 9 times Bihar's level. A very small population with tourism, mining and high-value services produces a high per-capita figure. It is high but *not pulling away*: it grew only 4.2% a year (23rd of 28), and fell from 383% to 299% of the All-India figure. Its swings (₹259k → ₹188k → ₹279k between 2011-12 and 2015-16) are typical of a small, narrowly based economy, and the dip coincides with the period of mining disruption, which is worth checking against state sources. The Goa to Bihar ratio actually *narrowed* (11.5 → 9.4).
- **Gujarat: sustained fast growth.** It had the fastest growth of the first 11 states in every series (8.7%, 8.5%, 7.0%), and 7.6% overall. It started mid-pack at ₹38.6k, below Haryana and Himachal Pradesh, and its income rose 5.4 times. The data are consistent with an industrial and trade-led growth model.
- **Haryana: high base, steady growth.** It started at ₹54.5k, grew 5.7% a year (9th of 28) and stayed between roughly 155% and 180% of the All-India figure. Proximity to the Delhi region and a manufacturing and services mix are the usual explanations.
- **Other leaders pulled ahead too.** Tamil Nadu (121% → 172% of All-India) and Karnataka (147% → 182%) both gained, so divergence is not just a Gujarat story.
- **Common thread:** a **high starting level** combined with **at least moderate growth**. Convergence requires poor states to grow *faster*, and the leaders did not slow down enough for anyone to catch them.

## 5. Are Bihar and Chhattisgarh catching up?

| | CAGR 99-00 base | CAGR 04-05 base | CAGR 11-12 base | Spliced 2001-02 → 2024-25 | Rank of 28 | Level, ₹ 2011-12 prices |
|---|---|---|---|---|---|---|
| Bihar | 4.15% | **7.52%** | 4.24% | 5.09% | 14 | 11.6k → 36.3k |
| Chhattisgarh | 4.86% | 5.59% | 4.36% | 4.70% | 17 | 32.7k → 94.0k |
| Gujarat | 8.65% | 8.49% | 6.97% | **7.62%** | 2 | 38.6k → 208.9k |
| Haryana | 6.18% | 7.18% | 4.76% | 5.68% | 9 | 54.5k → 194.3k |
| Goa | 4.89% | 7.70% | 2.16% | 4.17% | 23 | 133.7k → 342.4k |

- **Bihar** had one real growth spurt in 2004-12 (7.5% a year, faster than Haryana but below Gujarat), then growth fell back to 4.2%. Its share of the 17-state average moved from 31.8% to 28.8%, and against Gujarat from 30% to 17%. In 2024-25 it still sits at 32% of the All-India figure.
- **Chhattisgarh** grew below the median and lost relative ground (90% → 75% of the 17-state average).
- **The poor states in general are not catching up.** Madhya Pradesh (4.7%), Jharkhand (4.6%) and Uttar Pradesh (4.3%) all grew below the median of 5.0%. Uttar Pradesh fell from 62% to 50% of the All-India figure.
- **Who did grow fast from a modest base?** Sikkim, Mizoram, Tripura, Uttarakhand and Tamil Nadu were among the fastest. Several are small economies or had unusual spurts (Sikkim grew 15.6% a year in the 2004-05 series), so they do not form a clean "poor catch up" pattern.
- **Convergence arithmetic:** a state at about 30% of the national level would need to grow roughly 5 percentage points faster than the average every year for 25 years just to reach it. No state in the poor group came close to that.
- **2025-26 snapshot** (partial): Bihar +7.2%, Chhattisgarh +6.7% and Gujarat +7.5%, with All-India NNI +6.3%. Encouraging for Bihar, but it is one year of partial data.

*Figures: `figures/03_levels_log.png`, `figures/04_beta_convergence.png`, `figures/05_relative_position.png`, `figures/06_growth_velocity.png`.*

## 6. Limitations (read before citing any number)

1. **Splicing is an approximation.** Re-basing changes sector weights and data sources, and pre-2011-12 numbers are NSDP at factor cost while the 2011-12 series is different in concept. The within-base results in §3 do not depend on splicing and agree with the spliced view.
2. **Short first series.** The 1999-2000 base has only 4 data points, so no trend there is meaningful.
3. **Andhra Pradesh and Telangana.** Older series cover undivided Andhra Pradesh and the 2011-12 series covers the residual state, so Andhra Pradesh's spliced growth is the least reliable. Telangana is left out of spliced results because it has no data before 2011-12.
4. **Other data notes from RBI.** Jammu & Kashmir from 2019-20 is the Union Territory only. Assam, Haryana and Nagaland values come from a release as on 1 August 2025. Uttar Pradesh revised its data from 2011-12. Nagaland has no 2024-25 value.
5. **Unweighted inequality.** A Gini across states treats Goa, with about 1.5 million people, the same as Uttar Pradesh. Population-weighting would be a worthwhile next step (this table has no population data).
6. **Outlier sensitivity.** Goa and Sikkim flip the sign of some CV trends. Results are therefore reported with and without them.
7. **Overstated p-values.** Yearly observations are strongly autocorrelated, so p-values for time trends look more impressive than they are. Rely on the size and consistency of the moves across measures and samples rather than on the p-values themselves.
8. **NSDP per capita is not household welfare.** It measures output within the state, not income or consumption. Remittances matter a lot for states like Bihar and are not captured.
9. **Low power for beta tests.** With 17 to 28 states, "not significant" means "no evidence of convergence", not proof that none exists.
10. **2025-26 is incomplete** and is excluded from inequality calculations.

## 7. Conclusion

Over about two decades the data do **not** support a story of poorer states catching up. Inequality across the 17 major states has risen on every measure and in every base series, the bottom and top of the ranking are largely unchanged, and the absolute rupee gap between rich and poor states has widened several-fold. Gujarat, Tamil Nadu and Karnataka pulled further ahead, while Bihar kept pace with the national median but could not close the gap and Chhattisgarh, Uttar Pradesh, Madhya Pradesh and Jharkhand lost ground. Goa remains the richest state but its relative lead has narrowed.

## 8. Suggested extensions

- Weight states by population (add Census or projection data) for a welfare-relevant Gini.
- Add sector composition (GSVA by agriculture, industry and services) to test the hypotheses in §4.
- Try conditional convergence: regress growth on initial income plus investment, urbanisation or schooling.
- Check sensitivity to the splicing method, for example by using only the 2011-12 series (2011-12 to 2024-25), where the sample is largest.
