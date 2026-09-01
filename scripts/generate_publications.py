"""Generate publications.md, cv-publications.md, and featured.md from data/publications.yml."""

import html
import yaml
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_FILE = os.path.join(ROOT, "data", "publications.yml")
OUTPUT_DIR = os.path.join(ROOT, "_includes")

with open(DATA_FILE, encoding="utf-8") as f:
    all_pubs = yaml.safe_load(f)

published = [p for p in all_pubs if "in review" not in p.get("journal", "").lower()]
in_review = [p for p in all_pubs if "in review" in p.get("journal", "").lower()]

published.sort(key=lambda p: (-p["year"], p["id"]))

os.makedirs(OUTPUT_DIR, exist_ok=True)


def format_authors(authors, for_cv=False, as_html=False, truncate=True):
    names = []
    for a in authors:
        name = html.escape(a["name"], quote=False) if as_html else a["name"]
        if a.get("highlight"):
            name = f"<strong>{name}</strong>" if as_html else f"**{name}**"
        names.append(name)

    MAX_BEFORE_TRUNCATE = 15
    if truncate and len(names) > MAX_BEFORE_TRUNCATE:
        first = ", ".join(names[:5])
        return first + ", ... and " + names[-1]
    else:
        last = names.pop()
        return ", ".join(names) + " and " + last


def render_entry(pub):
    """Plain list entry used for the CV publications list."""
    author_str = format_authors(pub["authors"])
    doi = pub.get("doi", "")
    title = pub["title"]
    if doi:
        title = f"[{title}](https://doi.org/{doi})"

    year = pub["year"]
    journal = pub["journal"]
    return f"- {author_str} ({year}). {title}. *{journal}*.\n"


def render_timeline_entry(pub):
    """Timeline-style entry (matches the homepage) used for the full publications listing.

    Tags aren't shown on the card — they ride along as a `data-tags` attribute
    so the tag-filter bar (assets/filters.js) can still filter by them.
    """
    author_str = format_authors(pub["authors"], as_html=True)
    doi = pub.get("doi", "")
    title = html.escape(pub["title"], quote=False)
    if doi:
        title = f'<a href="https://doi.org/{doi}">{title}</a>'

    year = pub["year"]
    journal = html.escape(pub["journal"], quote=False)
    tags = pub.get("tags", [])
    tags_attr = f' data-tags="{html.escape("|".join(tags), quote=True)}"' if tags else ""

    # Flush left and no blank lines: pandoc must read this as one raw HTML block
    # (indented lines, or a blank line mid-entry, would break out of it).
    lines = [f'<div class="pub-tl-item"{tags_attr}>']
    lines.append(f'<div class="pub-tl-year">{year}</div>')
    lines.append('<div class="pub-tl-body">')
    lines.append(f'<div class="pub-tl-title">{title}</div>')
    lines.append(f'<div class="pub-tl-authors">{author_str} ({year}).</div>')
    lines.append(f'<div class="pub-tl-journal">{journal}</div>')
    lines.append("</div>")
    lines.append("</div>")
    return "\n".join(lines)


# === Publications page (timeline style, matching the homepage) ===
output = ['<div class="pub-timeline">']
for pub in published:
    output.append(render_timeline_entry(pub))
output.append("</div>")

if in_review:
    output.append("")
    output.append("---")
    output.append("")
    output.append("## In Review")
    output.append("")
    output.append('<div class="pub-timeline">')
    for pub in in_review:
        output.append(render_timeline_entry(pub))
    output.append("</div>")

with open(os.path.join(OUTPUT_DIR, "publications.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(output) + "\n")
print(f"Generated {OUTPUT_DIR}/publications.md ({len(all_pubs)} total)")


# === CV publications page (clean, no HTML, flat list newest first) ===
cv_output = []

for pub in published:
    cv_output.append(render_entry(pub))

if in_review:
    cv_output.append("")
    cv_output.append("### In Review")
    cv_output.append("")
    for pub in in_review:
        cv_output.append(render_entry(pub))

with open(os.path.join(OUTPUT_DIR, "cv-publications.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(cv_output) + "\n")
print(f"Generated {OUTPUT_DIR}/cv-publications.md ({len(all_pubs)} total)")


# === Featured publications (for homepage, rendered as a year timeline) ===
featured = [p for p in published if p.get("featured")]
featured.sort(key=lambda p: (-p["year"], p["id"]))

feat_out = ['<div class="pub-timeline">']
for pub in featured:
    # Featured entries list every author — no "... and" elision.
    author_str = format_authors(pub["authors"], as_html=True, truncate=False)
    doi = pub.get("doi", "")
    title = html.escape(pub["title"], quote=False)
    if doi:
        title = f'<a href="https://doi.org/{doi}">{title}</a>'
    year = pub["year"]
    journal = html.escape(pub["journal"], quote=False)
    # Flush left and no blank lines: pandoc must read this as one raw HTML block
    # (indented lines would be parsed as a markdown code block instead).
    feat_out.append('<div class="pub-tl-item">')
    feat_out.append(f'<div class="pub-tl-year">{year}</div>')
    feat_out.append('<div class="pub-tl-body">')
    feat_out.append(f'<div class="pub-tl-title">{title}</div>')
    feat_out.append(f'<div class="pub-tl-authors">{author_str} ({year}).</div>')
    feat_out.append(f'<div class="pub-tl-journal">{journal}</div>')
    feat_out.append("</div>")
    feat_out.append("</div>")
feat_out.append("</div>")

with open(os.path.join(OUTPUT_DIR, "featured.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(feat_out) + "\n")
print(f"Generated {OUTPUT_DIR}/featured.md ({len(featured)} total)")
