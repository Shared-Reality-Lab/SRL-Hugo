import os
import yaml
from pybtex.database import parse_file

# Paths
bib_path = "static/publications/auto/pubs-list.bib"
papers_path = "static/publications/papers"
thesis_path = "static/publications/thesis"
output_path = "data/publications.yaml"

# Load BibTeX
bib_data = parse_file(bib_path)

# Gather available PDFs
pdf_lookup = {}
for folder, prefix in [(papers_path, "papers"), (thesis_path, "thesis")]:
    if not os.path.isdir(folder):
        continue
    for f in os.listdir(folder):
        if f.endswith(".pdf"):
            key = f.replace(".pdf", "")
            pdf_lookup[key.lower()] = f"/publications/{prefix}/{f}"

# Collect flattened publication entries
all_pubs = []

for key, entry in bib_data.entries.items():
    fields = entry.fields
    entry_type = entry.type
    year = fields.get("year", "unknown")
    title = fields.get("title", "").replace("{", "").replace("}", "")
    venue = (
        fields.get("booktitle")
        or fields.get("journal")
        or fields.get("school")
        or fields.get("publisher")
        or ""
    )
    authors_raw = [str(p) for p in entry.persons.get("author", [])]
    keywords = [kw.strip() for kw in fields.get("keywords", "").split(",") if kw.strip()]

    # Match PDF if possible
    matched_pdf = None
    for pdf_key, pdf_path in pdf_lookup.items():
        if key.lower() in pdf_key:
            matched_pdf = pdf_path
            break

    pub = {
        "key": key,
        "title": title,
        "authors": ", ".join(authors_raw),
        "author_list": authors_raw,
        "venue": venue,
        "year": year,
        "type": entry_type,
        "keywords": keywords,
        "pdf": matched_pdf,
        "has_pdf": matched_pdf is not None,
        "bibtex": f"/publications/auto/pubs-list.bib"
    }

    all_pubs.append(pub)

# Write YAML
with open(output_path, "w") as f:
    yaml.dump(all_pubs, f, sort_keys=False, allow_unicode=True)

print(f" !!!! Wrote {len(all_pubs)} entries to {output_path}")
