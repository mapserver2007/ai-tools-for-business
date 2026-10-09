#!/usr/bin/env python3
"""Fetch all chapters of a public Zenn book and save Markdown (+ optional HTML)."""

import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from markdownify import markdownify as md

sys.path.insert(0, str(Path(__file__).resolve().parent))
from html_utils import REPO_ROOT, write_html

JST = timezone(timedelta(hours=9))
BOOK_API = "https://zenn.dev/api/books/{slug}"
CHAPTER_API = "https://zenn.dev/api/chapters/{chapter_id}"
ZENN_BASE = "https://zenn.dev"
BOOKS_ROOT = REPO_ROOT / "agent-articles" / "books"


def sanitize_filename(title: str) -> str:
    sanitized = re.sub(r'[/\\:*?"<>|]', "", title)
    sanitized = re.sub(r"\s+", "-", sanitized.strip())
    sanitized = re.sub(r"-+", "-", sanitized)
    return sanitized[:100]


def html_to_markdown(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()
    converted = md(
        str(soup),
        heading_style="ATX",
        bullets="-",
    )
    lines = converted.split("\n")
    cleaned = []
    blank_count = 0
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                cleaned.append("")
        else:
            blank_count = 0
            cleaned.append(line)
    return "\n".join(cleaned).strip()


def get_json(url: str) -> dict:
    with urlopen(
        Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60
    ) as resp:
        return json.load(resp)


def build_frontmatter(
    title: str,
    book_title: str,
    source_url: str,
    author: str | None,
    published_at: str | None,
    position: int,
) -> str:
    now = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f'book_title: "{book_title}"')
    lines.append(f'source_url: "{source_url}"')
    if author:
        lines.append(f'author: "{author}"')
    if published_at:
        lines.append(f'published_at: "{published_at}"')
    lines.append(f'retrieved_at: "{now}"')
    lines.append('site: "zenn.dev"')
    lines.append('content_type: "article"')
    lines.append(f"chapter_position: {position}")
    lines.append("---")
    return "\n".join(lines)


def extract_zenn_book(book_url: str, render_html: bool = True) -> dict:
    m = re.search(
        r"zenn\.dev/([^/]+)/books/([a-f0-9]+)",
        book_url,
    )
    if not m:
        raise ValueError(f"Not a Zenn book URL: {book_url}")
    username, book_slug = m.group(1), m.group(2)

    book = get_json(BOOK_API.format(slug=book_slug))["book"]
    book_title = book["title"]
    author = book.get("user", {}).get("name")
    published_at = (book.get("published_at") or "")[:10] or None

    safe_book = sanitize_filename(book_title)
    book_dir = BOOKS_ROOT / safe_book
    chapters_dir = book_dir / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    chapter_paths: list[dict] = []
    combined_parts: list[str] = []

    book_front = build_frontmatter(
        book_title,
        book_title,
        f"https://zenn.dev/{username}/books/{book_slug}",
        author,
        published_at,
        0,
    )
    combined_parts.append(book_front)
    combined_parts.append(f"\n# {book_title}\n")

    for ch_meta in sorted(book["chapters"], key=lambda c: c["position"]):
        ch = get_json(CHAPTER_API.format(chapter_id=ch_meta["id"]))["chapter"]
        title = ch["title"]
        position = ch["position"]
        source_url = urljoin(ZENN_BASE, ch["path"])
        body_md = html_to_markdown(ch.get("body_html") or "")

        front = build_frontmatter(
            title, book_title, source_url, author, published_at, position
        )
        chapter_md = f"{front}\n\n# {title}\n\n{body_md}\n"
        fname = f"{position:02d}-{sanitize_filename(title)}.md"
        out_path = chapters_dir / fname
        out_path.write_text(chapter_md, encoding="utf-8")

        html_path = None
        if render_html:
            html_path = write_html(
                chapter_md,
                fname,
                output_dir=chapters_dir,
            )

        chapter_paths.append(
            {
                "position": position,
                "title": title,
                "file_path": str(out_path.relative_to(REPO_ROOT)),
                "html_file_path": (
                    str(html_path.relative_to(REPO_ROOT)) if html_path else None
                ),
                "source_url": source_url,
            }
        )

        combined_parts.append(f"\n\n---\n\n# {position:02d}. {title}\n\n")
        combined_parts.append(body_md)

    combined_path = book_dir / "全文.md"
    combined_path.write_text("".join(combined_parts), encoding="utf-8")

    combined_html_path = None
    if render_html:
        combined_html_path = write_html(
            combined_path.read_text(encoding="utf-8"),
            "全文.md",
            output_dir=book_dir,
        )

    return {
        "book_title": book_title,
        "book_dir": str(book_dir.relative_to(REPO_ROOT)),
        "chapter_count": len(chapter_paths),
        "chapters_dir": str(chapters_dir.relative_to(REPO_ROOT)),
        "combined_md": str(combined_path.relative_to(REPO_ROOT)),
        "combined_html": (
            str(combined_html_path.relative_to(REPO_ROOT))
            if combined_html_path
            else None
        ),
        "chapters": chapter_paths,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_zenn_book.py <Zenn book URL>", file=sys.stderr)
        sys.exit(1)
    result = extract_zenn_book(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
