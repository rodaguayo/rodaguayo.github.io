"""Generate shared includes from data/site.yml."""

import yaml
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_FILE = os.path.join(ROOT, "data", "site.yml")
OUTPUT_DIR = os.path.join(ROOT, "_includes")

with open(DATA_FILE) as f:
    site = yaml.safe_load(f)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# === site-heading.md ===
heading = f"# {site['name']}\n\n**{site['tagline']}**\n"
with open(os.path.join(OUTPUT_DIR, "site-heading.md"), "w") as f:
    f.write(heading)
print("Generated _includes/site-heading.md")

# === site-email.md (inline, no wrapper) ===
email_link = f'<a href="mailto:{site["email"]}">{site["email"]}</a>'
with open(os.path.join(OUTPUT_DIR, "site-email.md"), "w") as f:
    f.write(email_link + "\n")
print("Generated _includes/site-email.md")

# === site-address.md ===
addr = "<br>\n".join(site["address"])
address_block = f"<p>\n{addr}\n</p>\n"
with open(os.path.join(OUTPUT_DIR, "site-address.md"), "w") as f:
    f.write(address_block)
print("Generated _includes/site-address.md")

# === social-links.md ===
SVG = {
    "email":    '<path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>',
    "bluesky":  '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>',
    "github":   '<path d="M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z"/>',
    "scholar":  '<path d="M12 2L2 7v1l10 5 10-5V7l-10-5zM2 10v5l10 5 10-5v-5L12 15 2 10z"/>',
    "orcid":    '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM7.5 7.5h2v9h-2v-9zm4.5 0h2c1.5 0 2.5.5 3 1.5s.5 2 .5 3.5c0 1.5-.5 2.5-1.5 3.5s-2 1.5-3.5 1.5h-2v-9zm2 7.5c.5 0 .83-.17 1-.5s.33-.83.33-1.5c0-.67-.11-1.17-.33-1.5s-.5-.5-1-.5h-.5v4h.5z"/>',
    "rg":       '<path d="M8 3v18h8V3H8zm6 15h-4v-2h4v2zm0-4h-4v-2h4v2zm0-4h-4V8h4v2zm1-6H9V2h6v2z"/>',
    "vub":      '<path d="M12 2L2 9v2h1v6h8v-6h2v6h8V9h-1V9l-8-6zm0 2.27l6 4.23V15h-2v-5H8v5H6V9.5l6-4.23zM4 19h16v2H4z"/>',
}


def social_link(href, label, svg_key):
    return (
        f'  <a class="social-link" href="{href}">\n'
        f'    <svg viewBox="0 0 24 24" role="img" aria-label="{label}"><title>{label}</title>{SVG[svg_key]}</svg>\n'
        f'    {label}\n'
        f'  </a>'
    )


links = [
    social_link(f'mailto:{site["email"]}', "Email", "email"),
    social_link(f'https://bsky.app/profile/{site["bluesky"]}', "Bluesky", "bluesky"),
    social_link(f'https://github.com/{site["github"]}', "GitHub", "github"),
    social_link(f'https://scholar.google.com/citations?user={site["scholar_id"]}&hl=en', "Google Scholar", "scholar"),
    social_link(f'https://orcid.org/{site["orcid"]}', "ORCID", "orcid"),
    social_link(f'https://www.researchgate.net/profile/{site["researchgate"]}', "ResearchGate", "rg"),
    social_link(site["profile_url"], "VUB Profile", "vub"),
]

social_block = '<div class="social-links">\n' + "\n".join(links) + "\n</div>\n"
with open(os.path.join(OUTPUT_DIR, "social-links.md"), "w", encoding="utf-8") as f:
    f.write(social_block)
print("Generated _includes/social-links.md")

