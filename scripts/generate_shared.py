"""Generate shared includes from data/site.yml."""

import datetime
import yaml
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_FILE = os.path.join(ROOT, "data", "site.yml")
OUTPUT_DIR = os.path.join(ROOT, "_includes")

with open(DATA_FILE, encoding="utf-8") as f:
    site = yaml.safe_load(f)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# === site-heading.md ===
heading = f"**{site['tagline']}**\n"
with open(os.path.join(OUTPUT_DIR, "site-heading.md"), "w", encoding="utf-8") as f:
    f.write(heading)
print("Generated _includes/site-heading.md")

# === site-email.md (inline, no wrapper) ===
email_link = f'<a href="mailto:{site["email"]}">{site["email"]}</a>'
with open(os.path.join(OUTPUT_DIR, "site-email.md"), "w", encoding="utf-8") as f:
    f.write(email_link + "\n")
print("Generated _includes/site-email.md")

# === site-address.md ===
addr = "<br>\n".join(site["address"])
address_block = f"<p>\n{addr}\n</p>\n"
with open(os.path.join(OUTPUT_DIR, "site-address.md"), "w", encoding="utf-8") as f:
    f.write(address_block)
print("Generated _includes/site-address.md")

# === social-links.html ===
SVG_PATHS = {
    "email":    "M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z",
    "bluesky":  "M5.202 2.857C7.954 4.922 10.913 9.11 12 11.358c1.087-2.247 4.046-6.436 6.798-8.501C20.783 1.366 24 .213 24 3.883c0 .732-.42 6.156-.667 7.037-.856 3.061-3.978 3.842-6.755 3.37 4.854.826 6.089 3.562 3.422 6.299-5.065 5.196-7.28-1.304-7.847-2.97-.104-.305-.152-.448-.153-.327 0-.121-.05.022-.153.327-.568 1.666-2.782 8.166-7.847 2.97-2.667-2.737-1.432-5.473 3.422-6.3-2.777.473-5.899-.308-6.755-3.369C.42 10.04 0 4.615 0 3.883c0-3.67 3.217-2.517 5.202-1.026",
    "github":   "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12",
    "scholar":  "M5.242 13.769L0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z",
    "orcid":    "M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.303v7.444h2.297c3.272 0 4.022-2.484 4.022-3.722 0-2.016-1.284-3.722-4.097-3.722h-2.222z",
    "rg":       "M19.586 0c-.818 0-1.508.19-2.073.565-.563.377-.97.936-1.213 1.68a3.193 3.193 0 0 0-.112.437 8.365 8.365 0 0 0-.078.53 9 9 0 0 0-.05.727c-.01.282-.013.621-.013 1.016a31.121 31.123 0 0 0 .014 1.017 9 9 0 0 0 .05.727 7.946 7.946 0 0 0 .077.53h-.005a3.334 3.334 0 0 0 .113.438c.245.743.65 1.303 1.214 1.68.565.376 1.256.564 2.075.564.8 0 1.536-.213 2.105-.603.57-.39.94-.916 1.175-1.65.076-.235.135-.558.177-.93a10.9 10.9 0 0 0 .043-1.207v-.82c0-.095-.047-.142-.14-.142h-3.064c-.094 0-.14.047-.14.141v.956c0 .094.046.14.14.14h1.666c.056 0 .084.03.084.086 0 .36 0 .62-.036.865-.038.244-.1.447-.147.606-.108.385-.348.664-.638.876-.29.212-.738.35-1.227.35-.545 0-.901-.15-1.21-.353-.306-.203-.517-.454-.67-.915a3.136 3.136 0 0 1-.147-.762 17.366 17.367 0 0 1-.034-.656c-.01-.26-.014-.572-.014-.939a26.401 26.403 0 0 1 .014-.938 15.821 15.822 0 0 1 .035-.656 3.19 3.19 0 0 1 .148-.76 1.89 1.89 0 0 1 .742-1.01c.344-.244.593-.352 1.137-.352.508 0 .815.096 1.144.303.33.207.528.492.764.925.047.094.111.118.198.07l1.044-.43c.075-.048.09-.115.042-.199a3.549 3.549 0 0 0-.466-.742 3 3 0 0 0-.679-.607 3.313 3.313 0 0 0-.903-.41A4.068 4.068 0 0 0 19.586 0zM8.217 5.836c-1.69 0-3.036.086-4.297.086-1.146 0-2.291 0-3.007-.029v.831l1.088.2c.744.144 1.174.488 1.174 2.264v11.288c0 1.777-.43 2.12-1.174 2.263l-1.088.2v.832c.773-.029 2.12-.086 3.465-.086 1.29 0 2.951.057 3.667.086v-.831l-1.49-.2c-.773-.115-1.174-.487-1.174-2.264v-4.784c.688.057 1.29.057 2.206.057 1.748 3.123 3.41 5.472 4.355 6.56.86 1.032 2.177 1.691 3.839 1.691.487 0 1.003-.086 1.318-.23v-.744c-1.031 0-2.063-.716-2.808-1.518-1.26-1.376-2.95-3.582-4.355-6.074 2.32-.545 4.04-2.722 4.04-4.9 0-3.208-2.492-4.698-5.758-4.698zm-.515 1.29c2.406 0 3.839 1.26 3.839 3.552 0 2.263-1.547 3.782-4.097 3.782-.974 0-1.404-.03-2.063-.086v-7.19c.66-.059 1.547-.059 2.32-.059z",
}


def social_link(href, label, svg_key):
    # Inline SVG (rather than an <img> data URI) so the icon inherits the pill's
    # colour via currentColor and tracks the light/dark theme.
    path_d = SVG_PATHS[svg_key]
    return (
        f'  <a class="social-link" href="{href}">\n'
        f'    <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="{path_d}" fill="currentColor"/></svg>\n'
        f'    {label}\n'
        f'  </a>'
    )


# (href, label, icon key) — shared by the homepage pills and the site footer
SOCIALS = [
    (f'mailto:{site["email"]}', "Email", "email"),
    (f'https://bsky.app/profile/{site["bluesky"]}', "Bluesky", "bluesky"),
    (f'https://github.com/{site["github"]}', "GitHub", "github"),
    (f'https://scholar.google.com/citations?user={site["scholar_id"]}&hl=en', "Google Scholar", "scholar"),
    (f'https://orcid.org/{site["orcid"]}', "ORCID", "orcid"),
    (f'https://www.researchgate.net/profile/{site["researchgate"]}', "ResearchGate", "rg"),
]

links = [social_link(*s) for s in SOCIALS]

social_block = '<div class="social-links">\n' + "\n".join(links) + "\n</div>\n"
with open(os.path.join(OUTPUT_DIR, "social-links.html"), "w", encoding="utf-8") as f:
    f.write(social_block)
print("Generated _includes/social-links.html")

# === site-group.md ===
group_block = f'<p><a href="{site["group_url"]}">{site["group"]}</a></p>\n'
with open(os.path.join(OUTPUT_DIR, "site-group.md"), "w", encoding="utf-8") as f:
    f.write(group_block)
print("Generated _includes/site-group.md")

# === footer.yml ===
# Loaded by _quarto.yml via `metadata-files`, so the footer icons come from the
# same SOCIALS list as the homepage and the copyright year stays current.
footer_icons = "".join(
    f'<a href="{href}" title="{label}"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">'
    f'<path d="{SVG_PATHS[key]}" fill="currentColor"/></svg></a>'
    for href, label, key in SOCIALS
)
footer = {"website": {"page-footer": {
    "left": f"© {datetime.date.today().year} {site['name']}",
    "right": f'<span class="footer-social">{footer_icons}</span>',
}}}
with open(os.path.join(OUTPUT_DIR, "footer.yml"), "w", encoding="utf-8") as f:
    f.write("# Generated by scripts/generate_shared.py from data/site.yml — do not edit.\n")
    yaml.safe_dump(footer, f, allow_unicode=True, width=10**6)
print("Generated _includes/footer.yml")
