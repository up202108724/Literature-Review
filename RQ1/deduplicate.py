import pandas as pd
import re
from pathlib import Path

# ---------- Helper Functions ----------

def normalize_title(title):
    """Lowercase, remove punctuation, collapse spaces."""
    if pd.isna(title):
        return ""
    title = title.lower()
    title = re.sub(r'[^a-z0-9 ]+', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def normalize_doi(doi):
    if pd.isna(doi):
        return ""
    doi = doi.strip().lower()
    doi = doi.replace("https://doi.org/", "")
    return doi

# ---------- Load Files ----------

files = [
    r"C:\Users\Andre Silva\Desktop\Literature Review\RQ1\acm.csv",
    r"C:\Users\Andre Silva\Desktop\Literature Review\RQ1\IEEEexport2025.12.11-16.55.31.csv",
    r"C:\Users\Andre Silva\Desktop\Literature Review\RQ1\scopus_export_Dec 11-2025_daae2a1c-ddb4-43f4-93f5-6ff62a5fbc23.csv"
]

dfs = []
for f in files:
    print(f"Loading {f}")
    df = pd.read_csv(f, dtype=str)
    df["source_file"] = Path(f).name
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

# ---------- Normalize fields ----------
if "doi" not in data.columns:
    data["doi"] = ""

data["norm_doi"] = data["doi"].apply(normalize_doi)

title_col = "title" if "title" in data.columns else "Document Title"  # IEEE/Scopus
data["norm_title"] = data[title_col].apply(normalize_title)

# ---------- Deduplication Logic ----------
# Rule 1: Deduplicate by DOI when present
no_duplicate = data.sort_values("norm_doi").drop_duplicates(subset=["norm_doi"], keep="first")

# Rule 2: Deduplicate remaining by normalized title
no_duplicate = no_duplicate.sort_values("norm_title").drop_duplicates(subset=["norm_title"], keep="first")

# ---------- Save Output ----------
output_path =  r"C:\Users\Andre Silva\Desktop\Literature Review\RQ1\deduplicated_publications.csv"
no_duplicate.to_csv(output_path, index=False)

print(f"\nDeduplicated file saved to: {output_path}")
print(f"Original records: {len(data)}")
print(f"Deduplicated records: {len(no_duplicate)}")