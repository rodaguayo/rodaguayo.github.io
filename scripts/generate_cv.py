"""Generate cv-content.md from data/cv.yml."""

import yaml
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_FILE = os.path.join(ROOT, "data", "cv.yml")
OUTPUT_DIR = os.path.join(ROOT, "_includes")

with open(DATA_FILE) as f:
    cv = yaml.safe_load(f)

out = []

# === Positions ===
out.append("## Positions")
out.append("")
for p in cv.get("positions", []):
    start = p["start"]
    end = p.get("end", "present")
    out.append(f"- **{start}–{end}**: {p['role']}, {p['institution']} — {p['description']}")
out.append("")

# === Education ===
out.append("## Education")
out.append("")
for e in cv.get("education", []):
    out.append(f"- **{e['start']}–{e['end']}**: {e['degree']}, {e['institution']}, {e.get('location', '')}. {e['description']}")
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

# === Talks & Presentations ===
out.append("## Talks & Presentations")
out.append("")
invited = [t for t in cv.get("talks", []) if t.get("type") == "invited"]
conference = [t for t in cv.get("talks", []) if t.get("type") != "invited"]
if invited:
    out.append("### Invited Talks")
    out.append("")
    for t in invited:
        loc = f", {t['location']}" if t.get("location") else ""
        out.append(f"- **{t['event']}** ({t['year']}{loc}) — {t['title']}")
    out.append("")
if conference:
    out.append("### Conference Presentations")
    out.append("")
    for t in conference:
        loc = f", {t['location']}" if t.get("location") else ""
        out.append(f"- **{t['event']}** ({t['year']}{loc}) — {t['title']}")
    out.append("")

# === Datasets ===
out.append("## Datasets")
out.append("")
for d in cv.get("datasets", []):
    out.append(f"- **{d['name']}** ({d['year']}) — {d['description']}. DOI: [{d['doi']}](https://doi.org/{d['doi']})")
out.append("")

# === Service ===
out.append("## Service")
out.append("")
for sv in cv.get("service", []):
    if sv.get("venue"):
        out.append(f"- **{sv['role']}** — *{sv['venue']}* ({sv['year']})")
    elif sv.get("project"):
        out.append(f"- **{sv['role']}** — {sv['project']}, {sv['institution']} ({sv['year']})")
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

# === Skills ===
out.append("## Skills")
out.append("")
for sk in cv.get("skills", []):
    items = ", ".join(sk["items"])
    out.append(f"- **{sk['category']}**: {items}")
out.append("")

# === Fieldwork ===
out.append("## Fieldwork")
out.append("")
for fw in cv.get("fieldwork", []):
    out.append(f"- **{fw['location']}** ({fw['period']}) — {fw['description']} (PI: {fw['pi']})")
out.append("")

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(os.path.join(OUTPUT_DIR, "cv-content.md"), "w") as f:
    f.write("\n".join(out))
print(f"Generated {OUTPUT_DIR}/cv-content.md")
