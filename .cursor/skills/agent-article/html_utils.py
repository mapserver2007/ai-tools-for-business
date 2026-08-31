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


CONTENT_TYPE_LABELS = {
    "article": "ARTICLE",
    "tweet": "TWEET",
    "thread": "THREAD",
    "slides": "SLIDES",
}


def _render_toc_items(tokens: list[dict]) -> tuple[str, int]:
    """Render heading tokens as nested ordered-list items."""
    items = []
    count = 0
    for token in tokens:
        children_html, children_count = _render_toc_items(
            token.get("children", [])
        )
        level = int(token.get("level", 0))
        if level < 2:
            items.append(children_html)
            count += children_count
            continue

        token_id = escape(str(token.get("id", "")), quote=True)
        label = escape(str(token.get("name", "")))
        nested = f"<ol>{children_html}</ol>" if children_html else ""
        items.append(
            f'<li><a href="#{token_id}">{label}</a>{nested}</li>'
        )
        count += 1 + children_count
    return "".join(items), count


def _build_toc(tokens: list[dict]) -> str:
    """Build a styled table of contents from Markdown headings."""
    items, count = _render_toc_items(tokens)
    if not count:
        return ""
    return f"""<nav class="toc" aria-label="目次">
  <div class="toc-heading">
    <span class="toc-title">目次</span>
    <span class="toc-count">{count} セクション</span>
  </div>
  <ol>{items}</ol>
</nav>"""


def _split_leading_h1(body_html: str, title: str) -> tuple[str, str]:
    """Move the first Markdown h1 into the article hero."""
    match = re.match(
        r"\s*(<h1\b[^>]*>.*?</h1>)(?P<rest>.*)\Z",
        body_html,
        flags=re.DOTALL,
    )
    if match:
        return match.group(1), match.group("rest")
    return f'<h1 id="article-title">{escape(title)}</h1>', body_html


_INTERACTION_SCRIPT = """<script>
(() => {
  const progress = document.querySelector(".reading-progress > span");
  const updateProgress = () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = scrollable > 0 ? window.scrollY / scrollable : 0;
    if (progress) progress.style.width = `${Math.min(1, ratio) * 100}%`;
  };
  window.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();

  document.querySelectorAll("pre").forEach((block) => {
    const button = document.createElement("button");
    button.className = "copy-button";
    button.type = "button";
    button.textContent = "コピー";
    button.addEventListener("click", async () => {
      const text = block.querySelector("code")?.innerText || block.innerText;
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(text);
        } else {
          const textarea = document.createElement("textarea");
          textarea.value = text;
          textarea.style.position = "fixed";
          textarea.style.opacity = "0";
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand("copy");
          textarea.remove();
        }
        button.textContent = "コピー済み";
        window.setTimeout(() => { button.textContent = "コピー"; }, 1600);
      } catch (error) {
        button.textContent = "失敗";
        window.setTimeout(() => { button.textContent = "コピー"; }, 1600);
      }
    });
    block.appendChild(button);
  });

  const links = new Map(
    [...document.querySelectorAll(".toc a")].map((link) => [link.hash, link])
  );
  const headings = [...document.querySelectorAll(
    ".article-body h2[id], .article-body h3[id], .article-body h4[id]"
  )];
  if ("IntersectionObserver" in window && headings.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => link.classList.remove("is-active"));
        links.get(`#${entry.target.id}`)?.classList.add("is-active");
      });
    }, { rootMargin: "-12% 0px -72% 0px" });
    headings.forEach((heading) => observer.observe(heading));
  }
})();
</script>"""


def markdown_to_html(markdown_text: str) -> str:
    """Convert article Markdown into a self-contained, readable HTML page."""
    metadata, body = _split_frontmatter(markdown_text)
    converter = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
    )
    body_html = converter.convert(body)
    title = metadata.get("title", "記事")
    title_html, body_html = _split_leading_h1(body_html, title)
    toc_html = _build_toc(converter.toc_tokens)
    content_type = CONTENT_TYPE_LABELS.get(
        metadata.get("content_type", ""),
        "ARTICLE",
    )
    site = metadata.get("site", "WEB")
    source_url = metadata.get("source_url", "")
    metadata_items = []
    if metadata.get("author"):
        metadata_items.append(
            '<span class="metadata-item">'
            '<span class="metadata-label">著者</span>'
            f"{escape(metadata['author'])}</span>"
        )
    if metadata.get("published_at"):
        metadata_items.append(
            '<span class="metadata-item">'
            '<span class="metadata-label">公開日</span>'
            f"{escape(metadata['published_at'])}</span>"
        )
    if source_url:
        metadata_items.append(
            '<a class="metadata-item source-link" href="'
            + escape(source_url, quote=True)
            + '"><span class="metadata-label">原文</span>読む</a>'
        )
    if metadata.get("site"):
        metadata_items.append(
            '<span class="metadata-item">'
            '<span class="metadata-label">サイト</span>'
            f"{escape(metadata['site'])}</span>"
        )
    if metadata.get("content_type"):
        metadata_items.append(
            '<span class="metadata-item">'
            '<span class="metadata-label">形式</span>'
            f"{escape(content_type)}</span>"
        )

    metadata_html = (
        '<div class="metadata" aria-label="記事メタデータ">'
        + "".join(metadata_items)
        + "</div>"
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

    retrieved_at = metadata.get("retrieved_at", "")
    footer_details = (
        f'<span>取得: {escape(retrieved_at)}</span>'
        if retrieved_at
        else "<span>AI Article Archive</span>"
    )

    return f"""<!doctype html>
<html lang="ja">
<head>
{chr(10).join(meta_tags)}
<title>{escape(title)}</title>
<style>
:root {{
  color-scheme: light;
  --ink: #172033;
  --muted: #64748b;
  --line: #dbe4ef;
  --accent: #2563eb;
  --accent-dark: #1d4ed8;
  --accent-soft: #eff6ff;
  font-family: -apple-system, BlinkMacSystemFont, "Avenir Next",
    "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif;
  font-size: 16px;
  line-height: 1.85;
}}
* {{
  box-sizing: border-box;
}}
html {{
  scroll-behavior: smooth;
}}
body {{
  margin: 0;
  background:
    radial-gradient(circle at 8% 0%, #dbeafe 0, transparent 32rem),
    radial-gradient(circle at 100% 12%, #e0e7ff 0, transparent 28rem),
    #f4f7fb;
  color: var(--ink);
}}
body::before {{
  position: fixed;
  inset: 0;
  z-index: -1;
  content: "";
  pointer-events: none;
  background: linear-gradient(120deg, transparent 0 48%, rgba(255, 255, 255, 0.4));
}}
.article {{
  position: relative;
  isolation: isolate;
  box-sizing: border-box;
  max-width: 920px;
  margin: clamp(1rem, 5vw, 4rem) auto;
  padding: clamp(2rem, 6vw, 5rem) clamp(1.25rem, 7vw, 5.5rem);
  overflow: hidden;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid rgba(203, 213, 225, 0.8);
  border-radius: 24px;
  min-height: 100vh;
  box-shadow:
    0 24px 70px rgba(30, 64, 175, 0.1),
    0 4px 16px rgba(15, 23, 42, 0.04);
}}
.article::before {{
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  height: 5px;
  content: "";
  background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
}}
.metadata {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin: 0 0 2.5rem;
  color: var(--muted);
  font-size: 0.84rem;
}}
.metadata-item {{
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.32rem 0.72rem;
  background: #f8fafc;
  border: 1px solid var(--line);
  border-radius: 999px;
}}
.metadata-label {{
  color: var(--accent-dark);
  font-weight: 700;
}}
a {{
  color: var(--accent-dark);
  text-underline-offset: 0.18em;
  transition: color 160ms ease, background-color 160ms ease;
}}
a:hover {{
  color: #7c3aed;
}}
h1, h2, h3, h4, h5, h6 {{
  color: var(--ink);
  line-height: 1.35;
  text-wrap: balance;
}}
h1 {{
  max-width: 18ch;
  margin: 0 0 2.5rem;
  font-size: clamp(2.15rem, 5vw, 3.65rem);
  letter-spacing: -0.045em;
}}
h2 {{
  position: relative;
  margin: 3.8rem 0 1.25rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--line);
  font-size: clamp(1.45rem, 3vw, 2rem);
  letter-spacing: -0.025em;
}}
h2::after {{
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 4.2rem;
  height: 3px;
  content: "";
  background: linear-gradient(90deg, var(--accent), #7c3aed);
  border-radius: 999px;
}}
h3 {{
  margin: 2.6rem 0 0.8rem;
  color: var(--accent-dark);
  font-size: 1.3rem;
}}
h4, h5, h6 {{
  margin-top: 2rem;
}}
p {{
  margin: 1.15rem 0;
}}
ul, ol {{
  padding-left: 1.5rem;
}}
li {{
  margin: 0.35rem 0;
}}
li::marker {{
  color: var(--accent);
  font-weight: 700;
}}
strong {{
  color: #111827;
}}
blockquote {{
  margin: 1.6rem 0;
  padding: 0.8rem 1.25rem;
  color: #475569;
  background: linear-gradient(90deg, var(--accent-soft), #fff);
  border-left: 4px solid var(--accent);
  border-radius: 0 12px 12px 0;
}}
blockquote p:first-child {{
  margin-top: 0;
}}
blockquote p:last-child {{
  margin-bottom: 0;
}}
hr {{
  margin: 3rem 0;
  border: 0;
  border-top: 1px solid var(--line);
}}
img {{
  display: block;
  max-width: 100%;
  margin: 1.75rem auto;
  height: auto;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
}}
pre {{
  overflow-x: auto;
  margin: 1.6rem 0;
  padding: 1.15rem 1.25rem;
  color: #e2e8f0;
  background: #111827;
  border: 1px solid #253047;
  border-radius: 14px;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.12);
}}
code {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.9em;
}}
:not(pre) > code {{
  padding: 0.15rem 0.4rem;
  color: #9f1239;
  background: #fff1f2;
  border-radius: 5px;
}}
table {{
  display: block;
  max-width: 100%;
  overflow-x: auto;
  margin: 1.6rem 0;
  border-collapse: collapse;
  border: 1px solid var(--line);
  border-radius: 12px;
}}
th, td {{
  min-width: 7rem;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--line);
  text-align: left;
}}
th {{
  color: #1e3a8a;
  background: #eff6ff;
  font-weight: 700;
}}
tr:nth-child(even) td {{
  background: #f8fafc;
}}
@media (max-width: 600px) {{
  .article {{
    margin: 0;
    padding: 2rem 1rem 4rem;
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }}
  h1 {{
    max-width: none;
    font-size: clamp(2rem, 10vw, 2.75rem);
  }}
  .metadata {{
    margin-bottom: 2rem;
  }}
}}
@media print {{
  body {{
    background: #fff;
  }}
  .article {{
    max-width: none;
    margin: 0;
    padding: 0;
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }}
  .article::before {{
    display: none;
  }}
  a {{
    color: inherit;
  }}
}}
</style>
<style>
:root {{
  color-scheme: dark;
  --bg: #0f1419;
  --surface: #1a2332;
  --surface-raised: #202c3f;
  --surface-soft: rgba(26, 35, 50, 0.72);
  --border: #2d3a4f;
  --text: #e6edf3;
  --muted: #8b949e;
  --accent: #58a6ff;
  --accent-strong: #79c0ff;
  --green: #3fb950;
  --purple: #bc8cff;
  font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN",
    "Noto Sans JP", -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 16px;
  line-height: 1.75;
}}
* {{
  box-sizing: border-box;
}}
html {{
  scroll-behavior: smooth;
  background: var(--bg);
}}
body {{
  min-width: 320px;
  overflow-x: hidden;
  margin: 0;
  padding: 2rem 1.5rem 5rem;
  color: var(--text);
  background:
    radial-gradient(circle at 8% 0%, rgba(31, 111, 235, 0.18), transparent 32rem),
    radial-gradient(circle at 100% 12%, rgba(137, 87, 229, 0.14), transparent 28rem),
    var(--bg);
}}
body::before {{
  position: fixed;
  inset: 0;
  z-index: -1;
  content: "";
  pointer-events: none;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.018) 1px, transparent 1px);
  background-size: 32px 32px;
  mask-image: linear-gradient(to bottom, black, transparent 75%);
}}
.reading-progress {{
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  z-index: 20;
  height: 3px;
  background: rgba(45, 58, 79, 0.7);
}}
.reading-progress > span {{
  display: block;
  width: 0;
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--purple), #f778ba);
  box-shadow: 0 0 14px rgba(88, 166, 255, 0.8);
  transition: width 80ms linear;
}}
.article {{
  position: relative;
  max-width: 1040px;
  margin: 0 auto;
  padding: clamp(1.5rem, 4vw, 3rem);
  background: rgba(15, 20, 25, 0.76);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow:
    0 28px 80px rgba(0, 0, 0, 0.28),
    0 0 0 1px rgba(88, 166, 255, 0.035) inset;
  backdrop-filter: blur(16px);
}}
.article::before {{
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  height: 2px;
  content: "";
  background: linear-gradient(90deg, var(--accent), var(--purple), #f778ba);
  border-radius: 16px 16px 0 0;
}}
.article-header {{
  padding-bottom: 1.75rem;
  border-bottom: 1px solid var(--border);
}}
.eyebrow {{
  display: flex;
  align-items: center;
  gap: 0.55rem;
  margin-bottom: 1rem;
  color: var(--muted);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}}
.eyebrow-dot {{
  width: 0.5rem;
  height: 0.5rem;
  background: var(--green);
  border-radius: 50%;
  box-shadow: 0 0 12px rgba(63, 185, 80, 0.75);
}}
.eyebrow-separator {{
  color: var(--border);
}}
.metadata {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0 0 1.5rem;
  color: var(--muted);
  font-size: 0.78rem;
}}
.metadata-item {{
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.28rem 0.65rem;
  background: rgba(32, 44, 63, 0.68);
  border: 1px solid var(--border);
  border-radius: 999px;
}}
.metadata-label {{
  color: var(--accent-strong);
  font-weight: 700;
}}
.source-link {{
  color: var(--text);
  text-decoration: none;
}}
.source-link:hover {{
  border-color: var(--accent);
  background: rgba(88, 166, 255, 0.12);
}}
a {{
  color: var(--accent);
  overflow-wrap: anywhere;
  text-decoration: none;
  text-underline-offset: 0.18em;
  transition: color 160ms ease, background-color 160ms ease;
}}
a:hover {{
  color: var(--accent-strong);
  text-decoration: underline;
}}
h1, h2, h3, h4, h5, h6 {{
  color: var(--text);
  line-height: 1.35;
  text-wrap: balance;
}}
h1 {{
  max-width: 24ch;
  margin: 0;
  font-size: clamp(2rem, 5vw, 3.2rem);
  font-weight: 750;
  letter-spacing: -0.045em;
  background: linear-gradient(120deg, #fff 12%, #b9d8ff 58%, #bc8cff);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}
h2 {{
  position: relative;
  margin: 3.2rem 0 1.1rem;
  padding: 0.75rem 0 0.65rem;
  border-bottom: 1px solid var(--border);
  font-size: clamp(1.35rem, 3vw, 1.75rem);
  letter-spacing: -0.025em;
}}
h2::after {{
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 3.8rem;
  height: 2px;
  content: "";
  background: var(--accent);
  box-shadow: 0 0 12px rgba(88, 166, 255, 0.7);
}}
h3 {{
  margin: 2.25rem 0 0.7rem;
  color: var(--accent-strong);
  font-size: 1.2rem;
}}
h4, h5, h6 {{
  margin-top: 1.75rem;
}}
p {{
  margin: 0.9rem 0;
}}
ul, ol {{
  margin: 0.75rem 0;
  padding-left: 1.5rem;
}}
li {{
  margin: 0.3rem 0;
}}
li::marker {{
  color: var(--accent);
}}
strong {{
  color: #fff;
}}
blockquote {{
  margin: 1.4rem 0;
  padding: 0.85rem 1.15rem;
  color: #c9d1d9;
  background: linear-gradient(100deg, rgba(88, 166, 255, 0.1), rgba(26, 35, 50, 0.55));
  border: 1px solid rgba(88, 166, 255, 0.18);
  border-left: 3px solid var(--accent);
  border-radius: 0 8px 8px 0;
}}
blockquote p:first-child {{
  margin-top: 0;
}}
blockquote p:last-child {{
  margin-bottom: 0;
}}
hr {{
  margin: 2.5rem 0;
  border: 0;
  border-top: 1px solid var(--border);
}}
img {{
  display: block;
  max-width: 100%;
  height: auto;
  margin: 1.5rem auto;
  border: 1px solid var(--border);
  border-radius: 10px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
}}
pre {{
  position: relative;
  overflow-x: auto;
  margin: 1.35rem 0;
  padding: 1rem 1.15rem;
  color: #dbeafe;
  background: #0d1117;
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}}
pre code {{
  color: inherit;
  background: transparent;
}}
code {{
  font-family: "SF Mono", "Fira Code", ui-monospace, monospace;
  font-size: 0.86em;
}}
:not(pre) > code {{
  padding: 0.12em 0.38em;
  color: #ffabbc;
  background: rgba(248, 81, 73, 0.11);
  border-radius: 4px;
}}
.copy-button {{
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  padding: 0.25rem 0.55rem;
  color: var(--muted);
  font: inherit;
  font-size: 0.72rem;
  background: rgba(32, 44, 63, 0.9);
  border: 1px solid var(--border);
  border-radius: 4px;
  cursor: pointer;
}}
.copy-button:hover {{
  color: var(--text);
  border-color: var(--accent);
}}
table {{
  display: block;
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  margin: 1.35rem 0;
  border: 1px solid var(--border);
  border-radius: 8px;
  border-spacing: 0;
}}
th, td {{
  min-width: 7rem;
  padding: 0.6rem 0.75rem;
  border-right: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  text-align: left;
  vertical-align: top;
}}
th {{
  color: var(--accent);
  background: var(--surface);
  font-weight: 700;
}}
tr:nth-child(even) td {{
  background: rgba(26, 35, 50, 0.42);
}}
tr:last-child td {{
  border-bottom: 0;
}}
th:last-child, td:last-child {{
  border-right: 0;
}}
.toc {{
  margin: 1.75rem 0 2.5rem;
  padding: 1rem 1.25rem;
  background: var(--surface-soft);
  border: 1px solid var(--border);
  border-radius: 8px;
}}
.toc-heading {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 0.65rem;
  border-bottom: 1px solid var(--border);
}}
.toc-title {{
  color: var(--accent);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.08em;
}}
.toc-count {{
  color: var(--muted);
  font-size: 0.72rem;
}}
.toc ol {{
  margin: 0.7rem 0 0;
  padding-left: 1.25rem;
}}
.toc ol ol {{
  margin: 0.2rem 0;
}}
.toc li {{
  margin: 0.18rem 0;
  font-size: 0.86rem;
}}
.toc li::marker {{
  color: var(--muted);
}}
.toc a {{
  display: inline-block;
  max-width: 100%;
  color: var(--muted);
  transition: color 160ms ease, transform 160ms ease;
}}
.toc a:hover, .toc a.is-active {{
  color: var(--accent-strong);
  text-decoration: none;
  transform: translateX(2px);
}}
.article-body {{
  max-width: 78ch;
  margin: 0 auto;
}}
.article-footer {{
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 3rem;
  padding-top: 1rem;
  color: var(--muted);
  font-size: 0.74rem;
  border-top: 1px solid var(--border);
}}
.article-footer a {{
  color: var(--muted);
}}
@media (max-width: 720px) {{
  body {{
    padding: 0 0 3rem;
  }}
  .article {{
    min-height: 100vh;
    padding: 1.5rem 1rem 3rem;
    border-right: 0;
    border-left: 0;
    border-radius: 0;
  }}
  .article::before {{
    border-radius: 0;
  }}
  h1 {{
    max-width: none;
    font-size: clamp(1.9rem, 9vw, 2.6rem);
  }}
  .article-footer {{
    align-items: flex-start;
    flex-direction: column;
  }}
}}
@media print {{
  :root {{
    color-scheme: light;
  }}
  body {{
    padding: 0;
    color: #111;
    background: #fff;
  }}
  .reading-progress, .toc, .copy-button {{
    display: none;
  }}
  .article {{
    max-width: none;
    padding: 0;
    background: #fff;
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }}
  .article::before {{
    display: none;
  }}
  h1, h2, h3, h4, h5, h6, strong {{
    color: #111;
    -webkit-text-fill-color: initial;
  }}
  a {{
    color: inherit;
    text-decoration: underline;
  }}
  pre {{
    color: #111;
    background: #f4f4f4;
    box-shadow: none;
  }}
}}
</style>
</head>
<body>
<div class="reading-progress" aria-hidden="true"><span></span></div>
<main id="article-top" class="article">
  <header class="article-header">
    <div class="eyebrow">
      <span class="eyebrow-dot"></span>
      <span>{escape(content_type)}</span>
      <span class="eyebrow-separator">/</span>
      <span>{escape(site)}</span>
    </div>
    {metadata_html}
    {title_html}
  </header>
{toc_html}
  <div class="article-body">
{body_html}
  </div>
  <footer class="article-footer">
    {footer_details}
    <a href="#article-top">↑ 先頭へ戻る</a>
  </footer>
</main>
{_INTERACTION_SCRIPT}
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
