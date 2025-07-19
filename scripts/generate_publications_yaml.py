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
            key = os.path.splitext(f)[0].lower()
            pdf_lookup[key] = f"/publications/{prefix}/{f}"

# Collect flattened publication entries
all_pubs = []

for key, entry in bib_data.entries.items():
    fields = entry.fields
    entry_type = entry.type
    year = fields.get("year", "unknown")

    # Clean up title braces
    title = fields.get("title", "").replace("{", "").replace("}", "")

    # Venue selection (in preferred order)
    venue = (
        fields.get("booktitle")
        or fields.get("journal")
        or fields.get("school")
        or fields.get("publisher")
        or ""
    )

    # Clean author names using first/middle/last
    author_list = [
        " ".join(p.first_names + p.middle_names + p.last_names)
        for p in entry.persons.get("author", [])
    ]


    # Keyword parsing
    keywords = [
        kw.strip() for kw in fields.get("keywords", "").split(",")
        if kw.strip()
    ]

    # PDF match by exact key
    matched_pdf = pdf_lookup.get(key.lower(), None)

    # Extract additional URLs like url_paper, url_video, etc.
    extra_urls = {
        k: v for k, v in fields.items()
        if k.startswith("url_")
    }

    pub = {
        "key": key,
        "title": title,
        "authors": ", ".join(author_list),
        "author_list": author_list,
        "venue": venue,
        "year": year,
        "type": entry_type,
        "keywords": keywords,
        "pdf": matched_pdf,
        "has_pdf": matched_pdf is not None,
        "bibtex": f"/publications/auto/pubs-list.bib",
        "url": fields.get("url"),
        "doi": fields.get("doi"),
        "month": fields.get("month"),
        "address": fields.get("address"),
        "pages": fields.get("pages"),
        "volume": fields.get("volume"),
        "number": fields.get("number"),
        "note": fields.get("note"),
        "extra_urls": extra_urls if extra_urls else None
    }

    all_pubs.append(pub)

# Write to YAML
with open(output_path, "w", encoding="utf-8") as f:
    yaml.dump(all_pubs, f, sort_keys=False, allow_unicode=True)

print(f" ✅ Wrote {len(all_pubs)} entries to {output_path}")