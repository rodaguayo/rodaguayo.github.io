"""Generate publications.md and cv-publications.md from data/publications.yml."""

import yaml
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_FILE = os.path.join(ROOT, "data", "publications.yml")
OUTPUT_DIR = os.path.join(ROOT, "_includes")

with open(DATA_FILE) as f:
    all_pubs = yaml.safe_load(f)

published = [p for p in all_pubs if "in review" not in p.get("journal", "").lower()]
in_review = [p for p in all_pubs if "in review" in p.get("journal", "").lower()]

published.sort(key=lambda p: (-p["year"], p["id"]))


def format_authors(authors, for_cv=False):
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


def render_entry(pub, with_extras=True):
    author_str = format_authors(pub["authors"])

    doi = pub.get("doi", "")
    title = pub["title"]
    if doi:
        title = f"[{title}](https://doi.org/{doi})"

    year = pub["year"]
    journal = pub["journal"]

    line = f"- {author_str} ({year}). {title}. *{journal}*."
    lines = [line]

    if with_extras:
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


# === Publications page (with tags, extras) ===
output = []
for pub in published:
    output.append(render_entry(pub, with_extras=True))

if in_review:
    output.append("---")
    output.append("")
    output.append("## In Review")
    output.append("")
    for pub in in_review:
        output.append(render_entry(pub, with_extras=True))

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(os.path.join(OUTPUT_DIR, "publications.md"), "w") as f:
    f.write("\n".join(output) + "\n")
print(f"Generated {OUTPUT_DIR}/publications.md ({len(all_pubs)} total)")


# === CV publications page (clean, no HTML, grouped by year) ===
cv_output = []

by_year = {}
for pub in published:
    by_year.setdefault(pub["year"], []).append(pub)

for year in sorted(by_year.keys(), reverse=True):
    cv_output.append(f"### {year}")
    cv_output.append("")
    for pub in by_year[year]:
        cv_output.append(render_entry(pub, with_extras=False))
    cv_output.append("")

if in_review:
    cv_output.append("### In Review")
    cv_output.append("")
    for pub in in_review:
        cv_output.append(render_entry(pub, with_extras=False))

with open(os.path.join(OUTPUT_DIR, "cv-publications.md"), "w") as f:
    f.write("\n".join(cv_output) + "\n")
print(f"Generated {OUTPUT_DIR}/cv-publications.md ({len(all_pubs)} total)")


# === Featured publications (for homepage, bold first author) ===
featured = [p for p in published if p.get("featured")]
featured.sort(key=lambda p: (-p["year"], p["id"]))

feat_out = []
for pub in featured:
    author_str = format_authors(pub["authors"])
    doi = pub.get("doi", "")
    title = pub["title"]
    if doi:
        title = f"[{title}](https://doi.org/{doi})"
    year = pub["year"]
    journal = pub["journal"]
    feat_out.append(f"- {author_str} ({year}). {title}. *{journal}*.")
    feat_out.append("")

with open(os.path.join(OUTPUT_DIR, "featured.md"), "w") as f:
    f.write("\n".join(feat_out) + "\n")
print(f"Generated {OUTPUT_DIR}/featured.md ({len(featured)} total)")
