"""Read the official RBI Handbook Table 10 workbook (3 sheets) into one tidy CSV.

Input : data/raw/RBI_Handbook_Table10_per_capita_NSDP.xlsx   (downloaded from RBI, never edited)
Output: data/per_capita_nsdp_table10.csv  (columns: base, year, state, pc_nsdp)
RBI notes: pre-2011-12 data are NSDP at factor cost; J&K from 2019-20 is the UT of J&K only;
           Assam, Haryana, Nagaland were taken from a release as on 1 Aug 2025.
"""
import openpyxl, pandas as pd

SRC = "data/raw/RBI_Handbook_Table10_per_capita_NSDP.xlsx"
BASE_LABEL = {"1999-2000": "1999-00", "2004-05": "2004-05", "2011-12": "2011-12"}

wb = openpyxl.load_workbook(SRC, data_only=True)
rows = []
for ws in wb:                                   # sheets T_10(i), (ii), (iii) hold different state columns
    header, base = None, None
    for r in ws.iter_rows(values_only=True):
        r = r[1:]                               # column A is empty
        first = r[0]
        if first == "State / Union Territory":
            header = list(r[1:]); continue
        if isinstance(first, str) and first.startswith("(Base"):
            base = BASE_LABEL[first.split(":")[1].strip(" )")]; continue
        if header and isinstance(first, str) and len(first) == 7 and first[4] == "-":
            for state, v in zip(header, r[1:]):
                if state is not None:
                    rows.append(dict(base=base, year=first, state=state,
                                     pc_nsdp=pd.to_numeric(v, errors="coerce")))   # "." becomes NaN

df = pd.DataFrame(rows)
df.to_csv("data/per_capita_nsdp_table10.csv", index=False)
print(df.groupby("base").year.nunique().to_dict(), "| states:", df.state.nunique(), "| missing cells:", int(df.pc_nsdp.isna().sum()))
