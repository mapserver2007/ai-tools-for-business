#!/usr/bin/env python3
"""Render an article Markdown file as a standalone HTML document."""

import re
from html import escape
from pathlib import Path

import markdown


REPO_ROOT = Path(__file__).resolve().parents[3]
HTML_OUTPUT_DIR = REPO_ROOT / "agent-articles" / "html"


def _split_frontmatter(markdown_text: str) -> tuple[dict[str, str], str]:
    """Split simple YAML frontmatter from the Markdown body."""
    match = re.match(
        r"\A---\r?\n(?P<frontmatter>.*?)\r?\n---(?:\r?\n|\Z)",
        markdown_text,
        flags=re.DOTALL,
    )
    if not match:
        return {}, markdown_text

    metadata: dict[str, str] = {}
    for line in match.group("frontmatter").splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        metadata[key.strip()] = value
    return metadata, markdown_text[match.end():]


def markdown_to_html(markdown_text: str) -> str:
    """Convert article Markdown into a self-contained, readable HTML page."""
    metadata, body = _split_frontmatter(markdown_text)
    body_html = markdown.markdown(
        body,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )

    title = metadata.get("title", "記事")
    source_url = metadata.get("source_url", "")
    metadata_items = []
    if metadata.get("author"):
        metadata_items.append(f"<span>著者: {escape(metadata['author'])}</span>")
    if metadata.get("published_at"):
        metadata_items.append(
            f"<span>公開日: {escape(metadata['published_at'])}</span>"
        )
    if source_url:
        metadata_items.append(
            '<a href="'
            + escape(source_url, quote=True)
            + '">原文</a>'
        )
    metadata_html = (
        '<p class="metadata">' + " · ".join(metadata_items) + "</p>"
        if metadata_items
        else ""
    )

    meta_tags = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<meta name="title" content="{escape(title, quote=True)}">',
    ]
    for key, value in metadata.items():
        if key == "title":
            continue
        if value:
            meta_tags.append(
                f'<meta name="{escape(key, quote=True)}" '
                f'content="{escape(value, quote=True)}">'
            )

    return f"""<!doctype html>
<html lang="ja">
<head>
{chr(10).join(meta_tags)}
<title>{escape(title)}</title>
<style>
:root {{
  color-scheme: light;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.8;
}}
body {{
  margin: 0;
  background: #f6f7f9;
  color: #202124;
}}
.article {{
  box-sizing: border-box;
  max-width: 860px;
  margin: 0 auto;
  padding: 3rem 1.5rem 5rem;
  background: #fff;
  min-height: 100vh;
}}
.metadata {{
  margin: -0.5rem 0 2rem;
  color: #5f6368;
  font-size: 0.9rem;
}}
a {{
  color: #1967d2;
}}
img {{
  max-width: 100%;
  height: auto;
}}
pre {{
  overflow-x: auto;
  padding: 1rem;
  border-radius: 6px;
  background: #f1f3f4;
}}
code {{
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}}
blockquote {{
  margin: 1rem 0;
  padding: 0.25rem 1rem;
  border-left: 4px solid #dadce0;
  color: #5f6368;
}}
table {{
  display: block;
  max-width: 100%;
  overflow-x: auto;
  border-collapse: collapse;
}}
th, td {{
  padding: 0.5rem 0.75rem;
  border: 1px solid #dadce0;
  text-align: left;
}}
@media (max-width: 600px) {{
  .article {{
    padding: 2rem 1rem 4rem;
  }}
}}
</style>
</head>
<body>
<main class="article">
{metadata_html}
{body_html}
</main>
</body>
</html>
"""


def write_html(markdown_text: str, markdown_filename: str) -> Path:
    """Write the HTML counterpart and return its path."""
    html_filename = Path(markdown_filename).with_suffix(".html").name
    HTML_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = HTML_OUTPUT_DIR / html_filename
    output_path.write_text(markdown_to_html(markdown_text), encoding="utf-8")
    return output_path
