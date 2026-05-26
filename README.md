# rodaguayo.github.io

Personal academic website for **Rodrigo Aguayo** — Scientist & Hydrologist.

Built with [Quarto](https://quarto.org/) and deployed to GitHub Pages via GitHub Actions.

## Contents

| Page | Description |
|------|-------------|
| [Home](index.qmd) | Landing page with research themes, featured publications, and news |
| [About](about.qmd) | Research focus, background, and affiliations |
| [CV](cv.qmd) | Full academic CV |
| [Publications](publications.qmd) | Peer-reviewed articles and preprints |
| [Teaching](teaching.qmd) | Teaching and supervision experience |
| [Talks](talks.qmd) | Presentations and invited talks |
| [Datasets](datasets.qmd) | Published datasets (PatagoniaMet, etc.) |
| [Open Science](open-science.qmd) | Reproducible research and open-source tools |
| [Blog](blog/index.qmd) | Posts and updates |
| [Contact](contact.qmd) | Contact information and links |

## Tech stack

- **[Quarto](https://quarto.org/)** — Scientific publishing system
- **GitHub Actions** — Automated build and deployment
- **GitHub Pages** — Hosting

## Project structure

```
.
├── _quarto.yml              # Website configuration
├── index.qmd                # Home page
├── about.qmd                # About page
├── cv.qmd                   # CV (generated from data/cv.yml)
├── publications.qmd         # Publications (from data/publications.yml)
├── blog/                    # Blog posts
├── data/                    # YAML data files (CV, publications)
├── assets/
│   └── styles.css           # Custom styles
├── _site/                   # Rendered output (gitignored)
└── .github/workflows/
    └── deploy.yml           # CI/CD workflow
```

