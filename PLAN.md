# Implementation Plan — Academic Research Website

## Overview
Build a complete academic research website for Rodrigo Aguayo (climate scientist, hydrologist, glaciologist) using **Quarto** static site generator, deployed to **GitHub Pages** via **GitHub Actions**.

## Phases

### Phase 1a — Repository Cleanup
- Delete `docs/` directory (old Notion redirect)
- Update `.gitignore` (remove Hugo paths, add Quarto paths)
- Create `PLAN.md` (this file)

### Phase 1b — Quarto Project Scaffolding
- `_quarto.yml` — site config, navbar, theme settings
- `assets/styles.css` — full custom CSS design system (dark/light mode, typography, layout)
- `assets/cv-pdf.tex` — minimal LaTeX template for PDF CV
- `data/cv.yml` — empty scaffold (populated in Phase 2)
- `data/publications.yml` — empty scaffold (populated in Phase 2)

All 11 page `.qmd` files created:
1. `index.qmd` — Home
2. `about.qmd` — About
3. `cv.qmd` — CV (renders from YAML)
4. `publications.qmd` — Publications (renders from YAML)
5. `projects/index.qmd` — Projects listing
6. `teaching.qmd` — Teaching
7. `talks.qmd` — Talks
8. `datasets.qmd` — Datasets
9. `open-science.qmd` — Open Science
10. `blog/index.qmd` — Blog (minimal placeholder)
11. `contact.qmd` — Contact

Plus individual project `.qmd` files in `projects/`.

### Phase 2 — Data Migration
- `data/publications.yml`: Extract all 20+ publications from existing CV markdown
- `data/cv.yml`: Convert all CSV exports + markdown sections to structured YAML
  - Sections: positions, education, grants, awards, supervision, teaching, service, skills, fieldwork, collaborations, talks, datasets, outreach

### Phase 3 — Page Content
Populate all 11 pages with real content extracted from CV:
- Home: short bio, research themes, featured pubs, social links
- About: extended bio, affiliations
- CV: programmatic render from YAML, TOC, PDF download button
- Publications: grouped by year, authors (own name bold), DOI/PDF/Code, BibTeX copy button
- Projects: real content (ICE³, ICE-BUFFER, PhD thesis, PatagoniaMet)
- Teaching: courses + supervision
- Talks: invited vs conference
- Datasets: open data with DOIs
- Open Science: repos, software, workflows
- Blog: "No posts yet" placeholder
- Contact: email, address, social links

### Phase 4 — CV PDF Export
- Quarto HTML → PDF via Pandoc pipeline
- A4, clean academic style, no colors/icons
- Author name header, page numbers
- Button on CV page linking to `/cv/cv.pdf`

### Phase 5 — GitHub Actions Pipeline
- `.github/workflows/deploy.yml`
- Trigger: push to main
- Steps: checkout → install Quarto → install TinyTeX → render → copy PDF → deploy-pages

### Phase 6 — Final Cleanup & Verification
- Delete old `Rodrigo Aguayo CV.md` and `Rodrigo Aguayo CV/` directory
- Run `quarto preview` and verify all pages
- Check mobile layout, dark/light toggle, TOC behavior

---

## Design Decisions (Confirmed)
| Decision | Choice |
|---|---|
| CV PDF method | Quarto HTML → PDF via Pandoc |
| Blog | Minimal placeholder only |
| Old docs/ | Delete |
| Project content | Real scientific summaries from CV |
| Old CV files | Delete after migration |
| Dark/light toggle | Pure CSS + inline JS, localStorage |
| .gitignore | Remove Hugo paths, add Quarto paths |
| Deployment | GitHub Actions → GitHub Pages |
