"""Generate cv-content-before-pubs.md and cv-content-after-pubs.md from data/cv.yml."""

import html
import yaml
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_FILE = os.path.join(ROOT, "data", "cv.yml")
OUTPUT_DIR = os.path.join(ROOT, "_includes")

with open(DATA_FILE, encoding="utf-8") as f:
    cv = yaml.safe_load(f)


def start_year(value):
    """First year of a period given as 2024 or '2018-2021', for sorting."""
    return int(str(value).split("-")[0])


def fmt_period(value):
    """Render a period with an en dash, matching the other CV sections."""
    return str(value).replace("-", "–")


out = []
out_before_pubs = []

# === Positions ===
out_before_pubs.append("## Positions")
out_before_pubs.append("")
for p in cv.get("positions", []):
    start = p["start"]
    end = p.get("end", "present")
    out_before_pubs.append(f"- **{start}–{end}**: {p['role']}, {p['institution']} — {p['description']}")
out_before_pubs.append("")

# === Education ===
out_before_pubs.append("## Education")
out_before_pubs.append("")
for e in cv.get("education", []):
    out_before_pubs.append(f"- **{e['start']}–{e['end']}**: {e['degree']}, {e['institution']}, {e.get('location', '')}. {e['description']}")
out_before_pubs.append("")

# === Mobility ===
out.append("## Mobility")
out.append("")
for m in cv.get("mobility", []):
    dur = f" ({m['duration']})" if m.get("duration") else ""
    out.append(f"- **{m['year']}**: {m['role']}, {m['institution']}, {m.get('location', '')}{dur}. {m['description']}")
out.append("")

# === Grants & Funding ===
out.append("## Grants & Funding")
out.append("")
for g in cv.get("grants", []):
    if "start" in g and "end" in g:
        out.append(f"- **{g['start']}–{g['end']}**: {g['title']} — {g.get('description', '')}")
    elif "year" in g:
        out.append(f"- **{g['year']}**: {g['title']} — {g.get('description', '')}")
    else:
        out.append(f"- {g['title']}")
out.append("")

# === Awards ===
out.append("## Awards")
out.append("")
for a in cv.get("awards", []):
    parts = [f"- **{a['year']}**: {a['title']}"]
    if a.get("organization"):
        parts[0] += f", *{a['organization']}*"
    if a.get("description"):
        parts.append(f"  — {a['description']}")
    out.extend(parts)
out.append("")

# === Supervision ===
out.append("## Supervision")
out.append("")
for s in cv.get("supervision", []):
    cosup = f"\n  Co-supervised with {s.get('cosupervisor', '')}" if s.get("cosupervisor") else ""
    out.append(f"- **{s['student']}** ({s['role']}, {s['institution']}, {s['period']}) — {s['project']}.{cosup}")
out.append("")

# === Teaching ===
out.append("## Teaching")
out.append("")
by_inst = {}
for t in cv.get("teaching", []):
    by_inst.setdefault(t["institution"], []).append(t)
for inst, courses in by_inst.items():
    out.append(f"### {inst}")
    out.append("")
    for c in courses:
        period = c.get("period") or str(c.get("year", ""))
        dur = f" ({c['duration']})" if c.get("duration") else ""
        out.append(f"- **{c['course']}** ({period}){dur}")
    out.append("")

# === Datasets ===
out.append("## Datasets")
out.append("")
for d in sorted(cv.get("datasets", []), key=lambda x: -x["year"]):
    out.append(f"- **{d['name']}** ({d['year']}) — {d['description']}. DOI: [{d['doi']}](https://doi.org/{d['doi']})")
out.append("")

# === Outreach & Media ===
out.append("## Outreach & Media")
out.append("")
for o in cv.get("outreach", []):
    url = o.get("url")
    title = o["title"]
    if url:
        title = f"[{title}]({url})"
    out.append(f"- **{o['year']}**: {title} — *{o['publisher']}*")
out.append("")

# === Projects & Collaborations ===
out.append("## Projects & Collaborations")
out.append("")
proj_collab = cv.get("projects collaborations", [])
for item in proj_collab:
    if "folder" in item:
        out.append(f"### {item['folder']}")
        out.append("")
        entries = sorted(
            item.get("entries", []),
            key=lambda e: -(start_year(e["year"]) if e.get("year") else 0),
        )
        for entry in entries:
            pi = f" (PI: {entry['pi']})" if entry.get("pi") else ""
            sup = f" (Supervisor: {entry['supervisor']})" if entry.get("supervisor") else ""
            org = f", {entry['organization']}" if entry.get("organization") else ""
            year = f"**{fmt_period(entry['year'])}**: " if entry.get("year") else ""
            inst = f", {entry['institution']}" if entry.get("institution") else ""
            out.append(f"- {year}{entry['title']} — {entry['role']}{pi}{sup}{inst}{org}")
        out.append("")
    elif "peer review" in item:
        out.append("### Peer Review")
        out.append("")
        for j in item["peer review"].get("journals", []):
            out.append(f"- *{j}*")
        out.append("")
out.append("")

# === Fieldwork ===
out.append("## Fieldwork")
out.append("")
for fw in sorted(cv.get("fieldwork", []), key=lambda x: -start_year(x["period"])):
    out.append(f"- **{fmt_period(fw['period'])}**: {fw['location']} — {fw['description']} (PI: {fw['pi']})")
out.append("")

# === Talks & Presentations ===
out.append("## Talks & Presentations")
out.append("")
for t in sorted(cv.get("talks", []), key=lambda x: (-x["year"], not x.get("invited", False))):
    loc_val = t.get("location") or t.get("country") or ""
    loc = f" ({loc_val})" if loc_val else ""
    invited_tag = "⭐ " if t.get("invited") else ""
    out.append(f"- **{t['year']}**: {invited_tag}*{t['event']}*{loc} — {t['title']}")
out.append("")

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(os.path.join(OUTPUT_DIR, "cv-content-before-pubs.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out_before_pubs))
with open(os.path.join(OUTPUT_DIR, "cv-content-after-pubs.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Generated _includes/cv-content-before-pubs.md and _includes/cv-content-after-pubs.md")


# === Timeline pages (talks, teaching) ===
# Same timeline markup as the publications page. The date label is shown only on
# the first entry of a run with the same label; later ones get a smaller dot.
# Flush left, no blank lines: pandoc must read this as one raw HTML block.
def esc(text):
    return html.escape(str(text), quote=False)


def badge(text, kind=""):
    return f'<span class="tl-badge {kind}">{esc(text)}</span>'


def render_timeline(entries):
    """entries: dicts with 'label', 'title', 'meta' (list of HTML lines) and
    optionally 'after' (raw HTML lines appended to the entry body)."""
    lines = ['<div class="pub-timeline tl-grouped">']
    prev = None
    for e in entries:
        label = str(e["label"])
        same = label == prev
        prev = label
        # Let long periods ("2016–2018") wrap after the dash in the narrow column
        shown = "" if same else esc(label).replace("–", "–<wbr>")
        lines.append(f'<div class="pub-tl-item{" same-year" if same else ""}">')
        lines.append(f'<div class="pub-tl-year">{shown}</div>')
        lines.append('<div class="pub-tl-body">')
        lines.append(f'<div class="pub-tl-title">{e["title"]}</div>')
        for m in e["meta"]:
            lines.append(f'<div class="tl-meta">{m}</div>')
        lines.extend(e.get("after", []))
        lines.append("</div>")
        lines.append("</div>")
    lines.append("</div>")
    return lines


def summary(parts):
    body = " · ".join(f"<strong>{n}</strong> {what}" for n, what in parts)
    return f'<p class="tl-summary">{body}</p>'


# === talks-content.md ===
talks = sorted(cv.get("talks", []), key=lambda x: (-x["year"], not x.get("invited", False)))
n_invited = sum(1 for t in talks if t.get("invited"))
countries = {t.get("country") for t in talks if t.get("country") and t.get("country") != "Online"}

talk_entries = []
for t in talks:
    loc_val = t.get("location") or t.get("country") or ""
    meta = f'<em>{esc(t["event"])}</em>' + (f" · {esc(loc_val)}" if loc_val else "")
    if t.get("invited"):
        meta += badge("Invited")
    if t.get("convener"):
        meta += badge("Convener", "alt")
    talk_entries.append({"label": t["year"], "title": esc(t["title"]), "meta": [meta]})

talks_out = [summary([(len(talks), "talks"), (n_invited, "invited"), (len(countries), "countries")]), ""]
talks_out += render_timeline(talk_entries)
talks_out.append("")

with open(os.path.join(OUTPUT_DIR, "talks-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(talks_out) + "\n")
print("Generated _includes/talks-content.md")


# === teaching-content.md ===
courses = sorted(cv.get("teaching", []), key=lambda x: -start_year(x.get("period") or x["year"]))
supervision = sorted(cv.get("supervision", []), key=lambda x: -start_year(x["period"]))
short_courses = sorted(cv.get("short_courses", []), key=lambda x: -x["year"])

teaching_out = [summary([
    (len(courses), "courses taught"),
    (len(supervision), "students supervised"),
    (len(short_courses), "short courses taken"),
]), ""]

teaching_out.append("## Courses Taught")
teaching_out.append("")
entries = []
for c in courses:
    meta = esc(c["institution"])
    if c.get("duration"):
        meta += f" · {esc(c['duration'])}"
    entries.append({"label": fmt_period(c.get("period") or c["year"]), "title": esc(c["course"]), "meta": [meta]})
teaching_out += render_timeline(entries)
teaching_out.append("")

teaching_out.append("## Student Supervision")
teaching_out.append("")
entries = []
for s in supervision:
    meta = [f'<strong>{esc(s["student"])}</strong> · {esc(s["institution"])}{badge(s["role"])}']
    if s.get("cosupervisor"):
        meta.append(f"Co-supervised with {esc(s['cosupervisor'])}")
    entries.append({"label": fmt_period(s["period"]), "title": esc(s["project"]), "meta": meta})
teaching_out += render_timeline(entries)
teaching_out.append("")

teaching_out.append("## Short Courses & Workshops")
teaching_out.append("")
entries = []
for sc in short_courses:
    meta = esc(sc["provider"])
    if sc.get("hours"):
        meta += f" · {sc['hours']} h"
    entries.append({"label": sc["year"], "title": esc(sc["name"]), "meta": [meta]})
teaching_out += render_timeline(entries)
teaching_out.append("")

with open(os.path.join(OUTPUT_DIR, "teaching-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(teaching_out) + "\n")
print("Generated _includes/teaching-content.md")


# === datasets-content.md ===
datasets = sorted(cv.get("datasets", []), key=lambda x: -x["year"])

entries = []
for d in datasets:
    doi_url = f"https://doi.org/{d['doi']}"
    title = f'<a href="{doi_url}">{esc(d["name"])}</a>'
    if d.get("extra"):
        title += badge(d["extra"])
    links = f'<a href="{doi_url}">Data</a>'
    if d.get("code"):
        links += f'<a href="{d["code"]}">Code</a>'
    entries.append({
        "label": d["year"],
        "title": title,
        "meta": [esc(d["description"])],
        "after": [f'<div class="pub-links">{links}</div>'],
    })

datasets_out = render_timeline(entries)
datasets_out.append("")

with open(os.path.join(OUTPUT_DIR, "datasets-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(datasets_out) + "\n")
print("Generated _includes/datasets-content.md")
