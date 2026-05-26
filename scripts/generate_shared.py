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
