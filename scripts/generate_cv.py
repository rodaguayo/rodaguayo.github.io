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
    out.append(f"- **{start}\u2013{end}**: {p['role']}, {p['institution']} \u2014 {p['description']}")
out.append("")

# === Education ===
out.append("## Education")
out.append("")
for e in cv.get("education", []):
    out.append(f"- **{e['start']}\u2013{e['end']}**: {e['degree']}, {e['institution']}, {e.get('location', '')}. {e['description']}")
out.append("")

# === Grants & Funding ===
out.append("## Grants & Funding")
out.append("")
for g in cv.get("grants", []):
    if "start" in g and "end" in g:
        out.append(f"- **{g['start']}\u2013{g['end']}**: {g['title']} \u2014 {g.get('description', '')}")
    elif "year" in g:
        out.append(f"- **{g['year']}**: {g['title']} \u2014 {g.get('description', '')}")
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
        parts.append(f"  \u2014 {a['description']}")
    out.extend(parts)
out.append("")

# === Supervision ===
out.append("## Supervision")
out.append("")
for s in cv.get("supervision", []):
    cosup = f"\n  Co-supervised with {s.get('cosupervisor', '')}" if s.get("cosupervisor") else ""
    out.append(f"- **{s['student']}** ({s['role']}, {s['institution']}, {s['period']}) \u2014 {s['project']}.{cosup}")
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
        out.append(f"- **{t['event']}** ({t['year']}{loc}) \u2014 {t['title']}")
    out.append("")
if conference:
    out.append("### Conference Presentations")
    out.append("")
    for t in conference:
        loc = f", {t['location']}" if t.get("location") else ""
        out.append(f"- **{t['event']}** ({t['year']}{loc}) \u2014 {t['title']}")
    out.append("")

# === Datasets ===
out.append("## Datasets")
out.append("")
for d in cv.get("datasets", []):
    out.append(f"- **{d['name']}** ({d['year']}) \u2014 {d['description']}. DOI: [{d['doi']}](https://doi.org/{d['doi']})")
out.append("")

# === Service ===
out.append("## Service")
out.append("")
for sv in cv.get("service", []):
    if sv.get("venue"):
        out.append(f"- **{sv['role']}** \u2014 *{sv['venue']}* ({sv['year']})")
    elif sv.get("project"):
        out.append(f"- **{sv['role']}** \u2014 {sv['project']}, {sv['institution']} ({sv['year']})")
out.append("")

# === Outreach & Media ===
out.append("## Outreach & Media")
out.append("")
for o in cv.get("outreach", []):
    url = o.get("url")
    title = o["title"]
    if url:
        title = f"[{title}]({url})"
    out.append(f"- **{o['year']}**: {title} \u2014 *{o['publisher']}*")
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
    out.append(f"- **{fw['location']}** ({fw['period']}) \u2014 {fw['description']} (PI: {fw['pi']})")
out.append("")

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(os.path.join(OUTPUT_DIR, "cv-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Generated _includes/cv-content.md")


# === talks-content.md ===
talks_out = []
talks_out.append("*🧑‍💼 indicates conference convener role.*")
talks_out.append("")
talks_out.append("---")
talks_out.append("")

invited = [t for t in cv.get("talks", []) if t.get("type") == "invited"]
conference = [t for t in cv.get("talks", []) if t.get("type") == "conference"]

if invited:
    talks_out.append("## Invited Talks")
    talks_out.append("")
    for t in invited:
        convener = " 🧑‍💼" if t.get("convener") else ""
        loc = f" — {t['location']}" if t.get("location") else ""
        talks_out.append(f"- **{t['event']}**{loc} ({t['year']}){convener}: {t['title']}")
    talks_out.append("")

if conference:
    talks_out.append("## Conference Presentations")
    talks_out.append("")
    for t in conference:
        convener = " 🧑‍💼" if t.get("convener") else ""
        loc = f" — {t['location']}" if t.get("location") else ""
        talks_out.append(f"- **{t['event']}**{loc} ({t['year']}){convener}: {t['title']}")
    talks_out.append("")

with open(os.path.join(OUTPUT_DIR, "talks-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(talks_out) + "\n")
print("Generated _includes/talks-content.md")


# === teaching-content.md ===
teaching_out = []
teaching_out.append("## Courses Taught")
teaching_out.append("")

by_inst: dict = {}
for t in cv.get("teaching", []):
    by_inst.setdefault(t["institution"], []).append(t)
for inst, courses in by_inst.items():
    teaching_out.append(f"### {inst}")
    teaching_out.append("")
    for c in courses:
        period = c.get("period") or str(c.get("year", ""))
        dur = f" — {c['duration']}" if c.get("duration") else ""
        teaching_out.append(f"- **{c['course']}** ({period}){dur}")
    teaching_out.append("")

teaching_out.append("---")
teaching_out.append("")
teaching_out.append("## Student Supervision")
teaching_out.append("")
teaching_out.append("| Student | Role | Project | Institution | Period |")
teaching_out.append("|---------|------|---------|-------------|--------|")
for s in cv.get("supervision", []):
    cosup = f" (co-sup.: {s['cosupervisor']})" if s.get("cosupervisor") else ""
    teaching_out.append(
        f"| {s['student']} | {s['role']}{cosup} | {s['project']} | {s['institution']} | {s['period']} |"
    )
teaching_out.append("")

teaching_out.append("---")
teaching_out.append("")
teaching_out.append("## Short Courses & Workshops")
teaching_out.append("")
for sc in cv.get("short_courses", []):
    hours_str = f" — {sc['hours']} hr" if sc.get("hours") else ""
    teaching_out.append(f"- {sc['name']} ({sc['provider']}, {sc['year']}){hours_str}")
teaching_out.append("")

with open(os.path.join(OUTPUT_DIR, "teaching-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(teaching_out) + "\n")
print("Generated _includes/teaching-content.md")


# === datasets-content.md ===
datasets_out = []
for d in cv.get("datasets", []):
    extra_str = f" | <strong>Downloads:</strong> {d['extra']}" if d.get("extra") else ""
    datasets_out.append('<div class="card">')
    datasets_out.append(f'  <h3>{d["name"]}</h3>')
    datasets_out.append(f'  <p>{d["description"]}</p>')
    datasets_out.append(f'  <p><strong>Year:</strong> {d["year"]}{extra_str}</p>')
    datasets_out.append(f'  <a href="https://doi.org/{d["doi"]}" class="btn">DOI: {d["doi"]}</a>')
    datasets_out.append("</div>")
    datasets_out.append("")

with open(os.path.join(OUTPUT_DIR, "datasets-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(datasets_out) + "\n")
print("Generated _includes/datasets-content.md")
