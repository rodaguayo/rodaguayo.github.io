"""Generate cv-content-before-pubs.md and cv-content-after-pubs.md from data/cv.yml."""

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


# === talks-content.md ===
talks_out = []
talks_out.append("*⭐ indicates invited talk, 🧑‍💼 indicates conference convener role.*")
talks_out.append("")
talks_out.append("---")
talks_out.append("")

for t in sorted(cv.get("talks", []), key=lambda x: (-x["year"], not x.get("invited", False))):
    convener_tag = "🧑‍💼 " if t.get("convener") else ""
    invited_tag = "⭐ " if t.get("invited") else ""
    loc_val = t.get("location") or t.get("country") or ""
    loc = f" ({loc_val})" if loc_val else ""
    talks_out.append(f"- **{t['year']}**: {invited_tag}{convener_tag}*{t['event']}*{loc} — {t['title']}")
talks_out.append("")

with open(os.path.join(OUTPUT_DIR, "talks-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(talks_out) + "\n")
print("Generated _includes/talks-content.md")


# === teaching-content.md ===
teaching_out = []
# NOTE: card markup below keeps indentation under 4 spaces — Pandoc turns
# 4-space-indented lines into a code block and would render the HTML literally.
teaching_out.append("## Courses Taught")
teaching_out.append("")
teaching_out.append('<div class="themes-grid">')
teaching_out.append("")
for c in sorted(cv.get("teaching", []), key=lambda x: -start_year(x.get("period") or x["year"])):
    period = fmt_period(c.get("period") or c["year"])
    meta = f"{period} &middot; {c['duration']}" if c.get("duration") else period
    teaching_out.append('<div class="card">')
    teaching_out.append(f'  <h3>{c["course"]}</h3>')
    teaching_out.append(f'  <p>{c["institution"]}</p>')
    teaching_out.append(f'  <p class="card-meta">{meta}</p>')
    teaching_out.append("</div>")
    teaching_out.append("")
teaching_out.append("</div>")
teaching_out.append("")

teaching_out.append("## Student Supervision")
teaching_out.append("")
teaching_out.append('<div class="themes-grid">')
teaching_out.append("")
for s in sorted(cv.get("supervision", []), key=lambda x: -start_year(x["period"])):
    teaching_out.append('<div class="card">')
    teaching_out.append(f'  <h3>{s["student"]}</h3>')
    teaching_out.append(f'  <p><span class="tag-pill">{s["role"]}</span></p>')
    teaching_out.append(f'  <p>{s["project"]}</p>')
    meta = f"{s['institution']} &middot; {fmt_period(s['period'])}"
    if s.get("cosupervisor"):
        meta += f"<br>Co-supervised with {s['cosupervisor']}"
    teaching_out.append(f'  <p class="card-meta">{meta}</p>')
    teaching_out.append("</div>")
    teaching_out.append("")
teaching_out.append("</div>")
teaching_out.append("")

teaching_out.append("## Short Courses & Workshops")
teaching_out.append("")
teaching_out.append('<div class="themes-grid">')
teaching_out.append("")
for sc in sorted(cv.get("short_courses", []), key=lambda x: -x["year"]):
    meta = f"{sc['year']} &middot; {sc['hours']} hr" if sc.get("hours") else str(sc["year"])
    teaching_out.append('<div class="card">')
    teaching_out.append(f'  <h3>{sc["name"]}</h3>')
    teaching_out.append(f'  <p>{sc["provider"]}</p>')
    teaching_out.append(f'  <p class="card-meta">{meta}</p>')
    teaching_out.append("</div>")
    teaching_out.append("")
teaching_out.append("</div>")
teaching_out.append("")

with open(os.path.join(OUTPUT_DIR, "teaching-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(teaching_out) + "\n")
print("Generated _includes/teaching-content.md")


# === datasets-content.md ===
datasets_out = []
for d in sorted(cv.get("datasets", []), key=lambda x: -x["year"]):
    extra_str = f" &middot; {d['extra']}" if d.get("extra") else ""
    datasets_out.append('<div class="card">')
    datasets_out.append(f'  <h3>{d["name"]}</h3>')
    datasets_out.append(f'  <p>{d["description"]}</p>')
    datasets_out.append(f'  <p class="card-meta">{d["year"]}{extra_str}</p>')
    # NOTE: keep indentation below 4 spaces — Pandoc turns 4-space-indented
    # lines into a code block, which would render these anchors as literal text.
    datasets_out.append('  <div class="card-links">')
    datasets_out.append(f'  <a href="https://doi.org/{d["doi"]}" class="btn">Data</a>')
    if d.get("code"):
        datasets_out.append(f'  <a href="{d["code"]}" class="btn">Code</a>')
    datasets_out.append("  </div>")
    datasets_out.append("</div>")
    datasets_out.append("")

with open(os.path.join(OUTPUT_DIR, "datasets-content.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(datasets_out) + "\n")
print("Generated _includes/datasets-content.md")
