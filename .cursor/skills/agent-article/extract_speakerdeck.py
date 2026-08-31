#!/usr/bin/env python3
"""Extract Speaker Deck presentations and save LLM-optimized Markdown and HTML."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_article import OUTPUT_DIR, REPO_ROOT, build_frontmatter, sanitize_filename
from image_utils import download_image
from html_utils import write_html

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
MAX_SLIDES = 250


def yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def normalize_talk_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme or "https", parsed.netloc, path, "", "", ""))


def parse_json_ld(soup: BeautifulSoup) -> dict | None:
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        candidates = data if isinstance(data, list) else [data]
        for item in candidates:
            if isinstance(item, dict) and item.get("@type") == "PresentationDigitalDocument":
                return item
    return None


def author_name(ld: dict | None, soup: BeautifulSoup) -> str:
    if ld:
        author = ld.get("author")
        if isinstance(author, dict) and author.get("name"):
            return str(author["name"]).strip()
        if isinstance(author, str) and author.strip():
            return author.strip()
    og = soup.find("meta", attrs={"property": "og:author"})
    if og and og.get("content"):
        return og["content"].strip()
    return ""


def published_date(ld: dict | None) -> str:
    if not ld:
        return ""
    value = str(ld.get("datePublished") or "")
    match = re.match(r"\d{4}-\d{2}-\d{2}", value)
    return match.group(0) if match else ""


def presentation_id(soup: BeautifulSoup, ld: dict | None) -> str:
    embed = soup.find("div", class_="speakerdeck-embed", attrs={"data-id": True})
    if embed and embed.get("data-id"):
        return embed["data-id"]
    if ld:
        for key in ("thumbnailUrl",):
            match = re.search(
                r"/presentations/([0-9a-f]{32})/",
                str(ld.get(key) or ""),
            )
            if match:
                return match.group(1)
        media = ld.get("associatedMedia") or {}
        if isinstance(media, dict):
            match = re.search(
                r"/presentations/([0-9a-f]{32})/",
                str(media.get("contentUrl") or ""),
            )
            if match:
                return match.group(1)
    match = re.search(r"/presentations/([0-9a-f]{32})/", str(soup))
    return match.group(1) if match else ""


def slide_image_url(presentation_id: str, index0: int) -> str:
    return (
        f"https://files.speakerdeck.com/presentations/"
        f"{presentation_id}/slide_{index0}.jpg"
    )


def clean_slide_text(text: str) -> str:
    text = text.replace("\f", "").replace("\u000c", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def slides_from_json_ld(ld: dict) -> list[dict]:
    parts = ld.get("hasPart") or []
    slides = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        position = part.get("position")
        try:
            position = int(position)
        except (TypeError, ValueError):
            continue
        slides.append({
            "position": position,
            "text": clean_slide_text(str(part.get("text") or "")),
        })
    slides.sort(key=lambda s: s["position"])
    return slides


def slides_from_html(soup: BeautifulSoup) -> list[dict]:
    container = soup.select_one("#transcript") or soup.select_one(".transcript")
    if not container:
        return []
    slides = []
    for index, div in enumerate(container.select(".slide-transcript"), start=1):
        text = clean_slide_text(div.get_text("\n", strip=True))
        href = ""
        link = div.find("a", href=True)
        if link:
            href = link["href"]
        match = re.search(r"/slide_(\d+)\.(?:jpg|png|webp)", href)
        position = int(match.group(1)) + 1 if match else index
        slides.append({"position": position, "text": text})
    slides.sort(key=lambda s: s["position"])
    return slides


def probe_slide_count(pres_id: str, known_count: int) -> int:
    if known_count > 0:
        return known_count
    count = 0
    for index in range(MAX_SLIDES):
        url = slide_image_url(pres_id, index)
        try:
            resp = requests.head(url, headers=HEADERS, timeout=15, allow_redirects=True)
        except requests.RequestException:
            break
        if resp.status_code != 200:
            break
        count += 1
    return count


def build_body(
    description: str,
    slides: list[dict],
    pres_id: str,
    total: int,
) -> tuple[str, list[dict]]:
    sections = []
    images = []
    if description:
        sections.append(description.strip())
    for slide in slides:
        pos = slide["position"]
        index = pos - 1
        image_url = slide_image_url(pres_id, index)
        images.append({
            "index": index,
            "slide_number": pos,
            "alt": f"スライド {pos}",
            "original_url": image_url,
            "local_path": download_image(image_url),
            "transcript": slide["text"],
        })
        sections.append(
            f"## スライド {pos} / {total}\n\n"
            f"<!-- INTERPRET_SLIDE_{index} -->"
        )
    if not sections:
        raise ValueError("スライド本文も画像も取得できませんでした")
    return "\n\n".join(sections) + "\n", images


def extract_speakerdeck(url: str) -> dict:
    url = normalize_talk_url(url)
    parsed = urlparse(url)
    if "speakerdeck.com" not in parsed.netloc:
        raise ValueError("speakerdeck.com の URL ではありません")
    path_parts = [p for p in parsed.path.split("/") if p]
    if len(path_parts) < 2:
        raise ValueError("トーク URL（https://speakerdeck.com/{user}/{slug}）を指定してください")

    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")

    ld = parse_json_ld(soup)
    title = ""
    if ld and ld.get("name"):
        title = str(ld["name"]).strip()
    if not title:
        og = soup.find("meta", attrs={"property": "og:title"})
        title = (og.get("content") or "").strip() if og else ""
    if not title:
        h1 = soup.find("h1")
        title = h1.get_text(" ", strip=True) if h1 else "Untitled"

    description = ""
    if ld and ld.get("description"):
        description = str(ld["description"]).strip()
    if not description:
        desc_el = soup.select_one(".deck-description")
        if desc_el:
            description = desc_el.get_text(" ", strip=True)

    pres_id = presentation_id(soup, ld)
    if not pres_id:
        raise ValueError("プレゼンテーション ID を取得できませんでした")

    slides = slides_from_json_ld(ld) if ld else []
    if not slides:
        slides = slides_from_html(soup)

    total = probe_slide_count(pres_id, len(slides))
    if total == 0:
        raise ValueError("スライド画像を取得できませんでした（非公開の可能性があります）")

    if slides and len(slides) < total:
        have = {s["position"] for s in slides}
        for pos in range(1, total + 1):
            if pos not in have:
                slides.append({"position": pos, "text": ""})
        slides.sort(key=lambda s: s["position"])
    elif not slides:
        slides = [{"position": i + 1, "text": ""} for i in range(total)]

    meta = {
        "source_url": url,
        "site": parsed.netloc,
    }
    author = author_name(ld, soup)
    if author:
        meta["author"] = yaml_escape(author)
    pub = published_date(ld)
    if pub:
        meta["published_at"] = pub

    body_md, images = build_body(description, slides, pres_id, total)

    safe_title = yaml_escape(title)
    frontmatter = build_frontmatter(safe_title, meta, content_type="slides")
    full_md = f"{frontmatter}\n\n# {title}\n\n{body_md.strip()}\n"

    filename = sanitize_filename(title) + ".md"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    output_path.write_text(full_md, encoding="utf-8")
    html_path = write_html(full_md, filename)

    return {
        "file_path": str(output_path.relative_to(REPO_ROOT)),
        "html_file_path": str(html_path.relative_to(REPO_ROOT)),
        "title": title,
        "images": images,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_speakerdeck.py <URL>", file=sys.stderr)
        sys.exit(1)
    try:
        result = extract_speakerdeck(sys.argv[1])
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
