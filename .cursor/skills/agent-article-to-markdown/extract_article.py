#!/usr/bin/env python3
"""Extract article content from unauthenticated web pages and save as LLM-optimized Markdown."""

import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from readability import Document
from markdownify import markdownify as md
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from image_utils import replace_images_with_placeholders

JST = timezone(timedelta(hours=9))
OUTPUT_DIR = Path(__file__).resolve().parents[3] / "agent-articles"


def sanitize_filename(title: str) -> str:
    sanitized = re.sub(r'[/\\:*?"<>|]', '', title)
    sanitized = re.sub(r'\s+', '-', sanitized.strip())
    sanitized = re.sub(r'-+', '-', sanitized)
    return sanitized[:100]


def extract_metadata(soup: BeautifulSoup, url: str) -> dict:
    meta = {"source_url": url, "site": urlparse(url).netloc}

    author_tag = (
        soup.find("meta", attrs={"name": "author"})
        or soup.find("meta", attrs={"property": "article:author"})
    )
    if author_tag and author_tag.get("content"):
        meta["author"] = author_tag["content"]

    date_tag = (
        soup.find("meta", attrs={"property": "article:published_time"})
        or soup.find("meta", attrs={"name": "date"})
        or soup.find("time", attrs={"datetime": True})
    )
    if date_tag:
        date_val = date_tag.get("content") or date_tag.get("datetime", "")
        date_match = re.match(r'\d{4}-\d{2}-\d{2}', date_val)
        if date_match:
            meta["published_at"] = date_match.group(0)

    return meta


def html_to_markdown(html_content: str) -> str:
    converted = md(
        html_content,
        heading_style="ATX",
        bullets="-",
        strip=["script", "style", "nav", "footer", "header", "aside"],
    )
    lines = converted.split('\n')
    cleaned = []
    blank_count = 0
    for line in lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                cleaned.append('')
        else:
            blank_count = 0
            cleaned.append(line)
    return '\n'.join(cleaned).strip()


def build_frontmatter(title: str, meta: dict, content_type: str = "article") -> str:
    now = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f'source_url: "{meta["source_url"]}"')
    if "author" in meta:
        lines.append(f'author: "{meta["author"]}"')
    if "published_at" in meta:
        lines.append(f'published_at: "{meta["published_at"]}"')
    lines.append(f'retrieved_at: "{now}"')
    lines.append(f'site: "{meta["site"]}"')
    lines.append(f'content_type: "{content_type}"')
    lines.append("---")
    return '\n'.join(lines)


def extract_article(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    doc = Document(response.text)
    title = doc.title()
    content_html = doc.summary()

    soup_full = BeautifulSoup(response.text, "html.parser")
    meta = extract_metadata(soup_full, url)

    body_md = html_to_markdown(content_html)
    body_md, images = replace_images_with_placeholders(body_md)

    frontmatter = build_frontmatter(title, meta)
    full_md = f"{frontmatter}\n\n# {title}\n\n{body_md}\n"

    filename = sanitize_filename(title) + ".md"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    output_path.write_text(full_md, encoding="utf-8")

    return {
        "file_path": str(output_path.relative_to(OUTPUT_DIR.parent)),
        "title": title,
        "images": images,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_article.py <URL>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    result = extract_article(url)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
