import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re

RAW_DIR = Path("../data/raw")
CLEAN_DIR = Path("../data/cleaned")



SOURCES = {
    "plato": {
        "wikipedia": "https://en.wikipedia.org/wiki/Plato",
        "sep": "https://plato.stanford.edu/entries/plato/",
        "iep": "https://iep.utm.edu/plato/"
    }
}

def fetch_html(url: str) -> str:
    print(f"Fetching: {url}")
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.text

def clean_html(html: str, source: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if "wikipedia" in source:
        content = soup.select_one("#bodyContent")  # Wikipedia
    elif "stanford" in source:
        content = soup.select_one("#main-text") or soup  # SEP
    elif "iep.utm.edu" in source:
        content = soup.select_one("article") or soup     # IEP
    else:
        content = soup
    return content.get_text(separator="\n", strip=True)

def postprocess_text(text: str) -> str:
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip blank lines
        if re.match(r"^\[\d+\]$", line):  # skip reference tags like [1]
            continue
        if any(x in line.lower() for x in [
            "navigation", "citation", "edit", "last modified", "cookie policy", "privacy policy"
        ]):
            continue  # skip junk

        # Remove inline references like "Plato was a philosopher [1]"
        line = re.sub(r"\[\d+\]", "", line)

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def save(text: str, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def process_author(author_id: str, links: dict):
    for label, url in links.items():
        raw_path = RAW_DIR / f"{author_id}_{label}.html"
        txt_path = CLEAN_DIR / f"{author_id}_{label}.txt"

        html = fetch_html(url)
        save(html, raw_path)

        cleaned = postprocess_text(clean_html(html, url))
        save(cleaned, txt_path)

        print(f"[✓] Saved cleaned text to {txt_path}")

if __name__ == "__main__":
    for author, links in SOURCES.items():
        process_author(author, links)
