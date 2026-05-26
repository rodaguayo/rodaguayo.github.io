"""Generate publications.md from data/publications.yml for Quarto inclusion."""

import yaml
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_FILE = os.path.join(ROOT, "data", "publications.yml")
OUTPUT_DIR = os.path.join(ROOT, "_includes")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "publications.md")

with open(DATA_FILE) as f:
    all_pubs = yaml.safe_load(f)

published = [p for p in all_pubs if "in review" not in p.get("journal", "").lower()]
in_review = [p for p in all_pubs if "in review" in p.get("journal", "").lower()]

published.sort(key=lambda p: (-p["year"], p["id"]))


def format_authors(authors):
    names = []
    for a in authors:
        name = a["name"]
        if a.get("highlight"):
            name = f"**{name}**"
        names.append(name)

    MAX_BEFORE_TRUNCATE = 8
    if len(names) > MAX_BEFORE_TRUNCATE:
        first = ", ".join(names[:5])
        return first + ", ... and " + names[-1]
    else:
        last = names.pop()
        return ", ".join(names) + " and " + last


def render_entry(pub, include_year=True):
    lines = []
    author_str = format_authors(pub["authors"])

    doi = pub.get("doi", "")
    title = pub["title"]
    if doi:
        title = f"[{title}](https://doi.org/{doi})"

    year = pub["year"]
    journal = pub["journal"]

    if include_year:
        lines.append(f"- {author_str} ({year}). {title}. *{journal}*.")
    else:
        lines.append(f"- {author_str} ({year}). {title}. *{journal}*.")

    tags = pub.get("tags", [])
    if tags:
        pills = " ".join(f'<span class="tag-pill">{t}</span>' for t in tags)
        lines.append(f"  {pills}")

    extras = []
    if pub.get("code_url"):
        extras.append(f"[Code]({pub['code_url']})")
    if pub.get("pdf_url"):
        extras.append(f"[PDF]({pub['pdf_url']})")
    if extras:
        lines.append(f'  <span class="pub-links">{" · ".join(extras)}</span>')

    lines.append("")
    return "\n".join(lines)


output = []
for pub in published:
    output.append(render_entry(pub, include_year=True))

if in_review:
    output.append("---")
    output.append("")
    output.append("## In Review")
    output.append("")
    for pub in in_review:
        output.append(render_entry(pub, include_year=True))

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(output) + "\n")

count = len(all_pubs)
print(f"Generated {OUTPUT_FILE} ({count} publications, {len(in_review)} in review)")
