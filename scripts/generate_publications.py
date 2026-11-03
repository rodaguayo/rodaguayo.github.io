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

    if len(names) == 1:
        return names[0]

    MAX_BEFORE_TRUNCATE = 15
    if not (truncate and len(names) > MAX_BEFORE_TRUNCATE):
        return ", ".join(names[:-1]) + " and " + names[-1]

    # Truncate long lists, but never elide a highlighted author: keep the first
    # five, every highlighted author, and the last, with "..." over each gap.
    last_i = len(names) - 1
    keep = set(range(5)) | {i for i, a in enumerate(authors) if a.get("highlight")}
    keep.discard(last_i)
    parts, prev = [], -1
    for i in sorted(keep):
        if i != prev + 1:
            parts.append("...")
        parts.append(names[i])
        prev = i
    sep = ", ... and " if last_i != prev + 1 else " and "
    return ", ".join(parts) + sep + names[last_i]


def render_entry(pub):
    """Plain list entry used for the CV publications list."""
    author_str = format_authors(pub["authors"])
    doi = pub.get("doi", "")
    title = pub["title"]
    if doi:
        title = f"[{title}](https://doi.org/{doi})"

    year = pub["year"]
    journal = pub["journal"]
    note = f" ⭐ {pub['badge']}." if pub.get("badge") else ""
    return f"- {author_str} ({year}). {title}. *{journal}*.{note}\n"


def render_title(pub):
    """Linked title plus an optional `badge` pill (e.g. dataset downloads)."""
    doi = pub.get("doi", "")
    title = html.escape(pub["title"], quote=False)
    if doi:
        title = f'<a href="https://doi.org/{doi}">{title}</a>'
    if pub.get("badge"):
        title += f'<span class="tl-badge">{html.escape(pub["badge"], quote=False)}</span>'
    return title


def render_timeline_entry(pub, same_year=False):
    """Timeline-style entry used for the full publications listing.

    Years are grouped like the talks page: only the first entry of a year shows
    the label; later ones get `same-year` (smaller dot, empty label). The year
    rides along as `data-year` so assets/filters.js can regroup after filtering.
    Tags aren't shown on the card — they ride along as a `data-tags` attribute
    so the tag-filter bar can still filter by them.
    """
    author_str = format_authors(pub["authors"], as_html=True)
    title = render_title(pub)

    year = pub["year"]
    journal = html.escape(pub["journal"], quote=False)
    tags = pub.get("tags", [])
    tags_attr = f' data-tags="{html.escape("|".join(tags), quote=True)}"' if tags else ""
    cls = "pub-tl-item same-year" if same_year else "pub-tl-item"

    # Flush left and no blank lines: pandoc must read this as one raw HTML block
    # (indented lines, or a blank line mid-entry, would break out of it).
    lines = [f'<div class="{cls}" data-year="{year}"{tags_attr}>']
    lines.append(f'<div class="pub-tl-year">{"" if same_year else year}</div>')
    lines.append('<div class="pub-tl-body">')
    lines.append(f'<div class="pub-tl-title">{title}</div>')
    lines.append(f'<div class="pub-tl-authors">{author_str} ({year}).</div>')
    lines.append(f'<div class="pub-tl-journal">{journal}</div>')
    lines.append("</div>")
    lines.append("</div>")
    return "\n".join(lines)


def render_grouped_timeline(pubs):
    lines = ['<div class="pub-timeline tl-grouped">']
    prev = None
    for pub in pubs:
        lines.append(render_timeline_entry(pub, same_year=pub["year"] == prev))
        prev = pub["year"]
    lines.append("</div>")
    return lines


# === Publications page (timeline grouped by year, like the talks page) ===
output = render_grouped_timeline(published)

if in_review:
    output.append("")
    output.append("---")
    output.append("")
    output.append("## In Review")
    output.append("")
    output += render_grouped_timeline(in_review)

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
    title = render_title(pub)
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
