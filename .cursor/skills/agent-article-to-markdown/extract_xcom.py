#!/usr/bin/env python3
"""Extract tweet/thread content from x.com using browser cookies and Playwright."""

import asyncio
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse

JST = timezone(timedelta(hours=9))
OUTPUT_DIR = Path(__file__).resolve().parents[3] / "agent-articles"
DEFAULT_BROWSER = "brave"


def sanitize_filename(title: str) -> str:
    sanitized = re.sub(r'[/\\:*?"<>|]', '', title)
    sanitized = re.sub(r'\s+', '-', sanitized.strip())
    sanitized = re.sub(r'-+', '-', sanitized)
    return sanitized[:100]


def _get_cookies(browser: str) -> list[dict]:
    """Get x.com cookies from local browser via browser-cookie3."""
    try:
        import browser_cookie3
    except ImportError:
        print("ERROR: browser-cookie3 が未インストールです。pip install browser-cookie3 を実行してください。", file=sys.stderr)
        sys.exit(1)

    def _find_brave_profile() -> str | None:
        base = os.path.expanduser(
            "~/Library/Application Support/BraveSoftware/Brave-Browser"
        )
        for profile in ["Default", "Profile 1", "Profile 2", "Profile 3"]:
            db = os.path.join(base, profile, "Cookies")
            if not os.path.exists(db):
                continue
            tmp = shutil.copy2(db, tempfile.mktemp(suffix=".db"))
            try:
                conn = sqlite3.connect(tmp)
                cur = conn.execute(
                    "SELECT COUNT(*) FROM cookies WHERE host_key LIKE '%.x.com' OR host_key LIKE '%.twitter.com'"
                )
                count = cur.fetchone()[0]
                conn.close()
            finally:
                os.unlink(tmp)
            if count > 0:
                return os.path.join(base, profile)
        return None

    try:
        if browser == "brave":
            profile_dir = _find_brave_profile()
            if profile_dir:
                b = browser_cookie3.Brave(cookie_file=os.path.join(profile_dir, "Cookies"))
                all_cookies = list(b.load())
                xcom_cookies = [
                    c for c in all_cookies
                    if any(d in (c.domain or "") for d in ["x.com", "twitter.com"])
                ]
                return [
                    {
                        "name": c.name,
                        "value": c.value,
                        "domain": c.domain if c.domain else ".x.com",
                        "path": c.path if c.path else "/",
                    }
                    for c in xcom_cookies
                    if c.value
                ]
            jar = browser_cookie3.brave(domain_name=".x.com")
        elif browser == "chrome":
            jar = browser_cookie3.chrome(domain_name=".x.com")
        else:
            print(f"ERROR: 不明なブラウザ: {browser}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: Cookie の取得に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

    return [
        {
            "name": c.name,
            "value": c.value,
            "domain": c.domain if c.domain else ".x.com",
            "path": c.path if c.path else "/",
        }
        for c in jar
        if c.value
    ]


def _extract_tweet_id(url: str) -> str:
    """Extract tweet/post ID from URL."""
    match = re.search(r'/status/(\d+)', url)
    if match:
        return match.group(1)
    raise ValueError(f"URL からツイートIDを抽出できません: {url}")


_EXTRACT_JS = """() => {
    function articleNodeToMd(node) {
        if (!node) return '';
        if (node.nodeType === Node.TEXT_NODE) return node.textContent;

        const tag = node.tagName ? node.tagName.toLowerCase() : '';
        const testid = node.getAttribute ? node.getAttribute('data-testid') : null;

        if (testid === 'markdown-code-block') {
            const text = node.innerText || '';
            const lines = text.split('\\n');
            const lang = lines[0] || '';
            const code = lines.slice(1).join('\\n');
            return '\\n```' + lang + '\\n' + code + '\\n```\\n';
        }

        if (tag === 'br') return '\\n';
        if (tag === 'a') {
            const href = node.getAttribute('href') || '';
            const text = [...node.childNodes].map(articleNodeToMd).join('');
            return `[${text}](${href})`;
        }
        if (tag === 'img') {
            const src = node.getAttribute('src') || '';
            const alt = node.getAttribute('alt') || 'image';
            return `![${alt}](${src})`;
        }
        if (tag === 'h1') return '\\n# ' + node.innerText.trim() + '\\n\\n';
        if (tag === 'h2') return '\\n## ' + node.innerText.trim() + '\\n\\n';
        if (tag === 'h3') return '\\n### ' + node.innerText.trim() + '\\n\\n';
        if (tag === 'h4') return '\\n#### ' + node.innerText.trim() + '\\n\\n';
        if (tag === 'li') return '- ' + node.innerText.trim() + '\\n';
        if (tag === 'blockquote') return '> ' + node.innerText.trim() + '\\n\\n';
        if (tag === 'strong' || tag === 'b') return '**' + node.innerText + '**';
        if (tag === 'em' || tag === 'i') return '*' + node.innerText + '*';
        if (tag === 'code' && node.parentElement
            && node.parentElement.getAttribute('data-testid') !== 'markdown-code-block') {
            return '`' + node.innerText + '`';
        }

        let result = '';
        for (const child of node.childNodes) {
            result += articleNodeToMd(child);
        }

        if (tag === 'p' || tag === 'div') {
            const trimmed = result.trim();
            if (trimmed) return trimmed + '\\n\\n';
        }
        return result;
    }

    function extractUserMeta(article) {
        const userEl = article.querySelector('[data-testid="User-Name"]');
        let author = '';
        let handle = '';
        if (userEl) {
            for (const span of userEl.querySelectorAll('span')) {
                if (span.textContent.startsWith('@')) {
                    handle = span.textContent;
                    break;
                }
            }
            const nameLink = userEl.querySelector('a span');
            if (nameLink) author = nameLink.textContent;
        }
        const timeEl = article.querySelector('time');
        const datetime = timeEl ? timeEl.getAttribute('datetime') : '';
        return { author, handle, datetime };
    }

    const tweetArticle = document.querySelector('article[data-testid="tweet"]');
    const articleTitleEl = document.querySelector('[data-testid="twitter-article-title"]');
    const articleBodyEl = document.querySelector('[data-testid="longformRichTextComponent"]');

    if (articleTitleEl && articleBodyEl) {
        const meta = tweetArticle ? extractUserMeta(tweetArticle) : { author: '', handle: '', datetime: '' };
        const body = articleNodeToMd(articleBodyEl).trim();
        return {
            content_type: 'article',
            title: articleTitleEl.innerText.trim(),
            body,
            author: meta.author,
            handle: meta.handle,
            datetime: meta.datetime,
        };
    }

    const tweets = [];
    for (const article of document.querySelectorAll('article[data-testid="tweet"]')) {
        const textEl = article.querySelector('[data-testid="tweetText"]');
        const text = textEl ? textEl.innerText : '';
        const meta = extractUserMeta(article);

        const images = [];
        for (const img of article.querySelectorAll('[data-testid="tweetPhoto"] img')) {
            if (img.src && !img.src.includes('profile_images')) {
                images.push({ alt: img.alt || '', src: img.src });
            }
        }

        if (text || images.length) {
            tweets.push({ text, author: meta.author, handle: meta.handle, datetime: meta.datetime, images });
        }
    }

    return {
        content_type: tweets.length > 1 ? 'thread' : 'tweet',
        tweets,
    };
}"""


def _format_published_at(datetime_str: str) -> str:
    if not datetime_str:
        return ""
    try:
        dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return ""


def _build_frontmatter(
    title: str,
    url: str,
    content_type: str,
    author: str = "",
    handle: str = "",
    published_at: str = "",
) -> list[str]:
    now = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    site = urlparse(url).netloc
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f'source_url: "{url}"')
    if author:
        lines.append(f'author: "{author} ({handle})"' if handle else f'author: "{author}"')
    if published_at:
        lines.append(f'published_at: "{published_at}"')
    lines.append(f'retrieved_at: "{now}"')
    lines.append(f'site: "{site}"')
    lines.append(f'content_type: "{content_type}"')
    lines.append("---")
    return lines


async def _extract_content(url: str, browser: str) -> dict:
    """Navigate to x.com and extract tweet/article content via Playwright."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("ERROR: playwright が未インストールです。pip install playwright && playwright install chromium を実行してください。", file=sys.stderr)
        sys.exit(1)

    cookies = _get_cookies(browser)
    if not cookies:
        print("ERROR: x.com の Cookie が見つかりません。Brave で x.com にログインしてください。", file=sys.stderr)
        sys.exit(1)

    async with async_playwright() as pw:
        browser_instance = await pw.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser_instance.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            await page.wait_for_selector(
                '[data-testid="tweetText"], [data-testid="twitter-article-title"]',
                timeout=15000,
            )
        except Exception:
            await page.wait_for_timeout(5000)

        if "/login" in page.url or "accounts.x.com" in page.url:
            print("ERROR: 認証が必要です。Brave で x.com にログインし直してください。", file=sys.stderr)
            await context.close()
            await browser_instance.close()
            sys.exit(1)

        # Article のコードブロック等は遅延読み込みされるため、末尾までスクロールして待機
        article_body = page.locator('[data-testid="longformRichTextComponent"]')
        if await article_body.count() > 0:
            await page.evaluate("""() => {
                const el = document.querySelector('[data-testid="longformRichTextComponent"]');
                if (el) el.scrollIntoView({ block: 'end' });
            }""")
            await page.wait_for_timeout(2000)
            try:
                await page.wait_for_selector('[data-testid="markdown-code-block"]', timeout=10000)
            except Exception:
                pass
            await page.wait_for_timeout(1000)

        result = await page.evaluate(_EXTRACT_JS)

        await context.close()
        await browser_instance.close()

    return result


def _build_markdown(data: dict, url: str) -> tuple[str, str]:
    """Build Markdown content from extracted data. Returns (markdown, title)."""
    content_type = data.get("content_type", "tweet")

    if content_type == "article":
        title = data.get("title", "").strip()
        body = data.get("body", "").strip()
        if not title or not body:
            raise ValueError("Article の内容を取得できませんでした")
        author = data.get("author", "")
        handle = data.get("handle", "")
        published_at = _format_published_at(data.get("datetime", ""))

        lines = _build_frontmatter(title, url, "article", author, handle, published_at)
        lines.extend(["", f"# {title}", "", body])
        return "\n".join(lines), title

    tweets = data.get("tweets", [])
    if not tweets:
        raise ValueError("ツイートの内容を取得できませんでした")

    first = tweets[0]
    author = first.get("author", "unknown")
    handle = first.get("handle", "")

    if content_type == "thread":
        title = f"{handle} thread"
    else:
        text_preview = first.get("text", "")[:60].replace("\n", " ")
        title = f"{handle} - {text_preview}"

    published_at = _format_published_at(first.get("datetime", ""))
    lines = _build_frontmatter(title, url, content_type, author, handle, published_at)
    lines.extend(["", f"# {title}", ""])

    for i, tweet in enumerate(tweets):
        if content_type == "thread" and i > 0:
            lines.extend(["---", ""])

        text = tweet.get("text", "")
        if text:
            lines.extend([text, ""])

        for img in tweet.get("images", []):
            alt = img.get("alt", "image")
            src = img.get("src", "")
            lines.extend([f"![{alt}]({src})", ""])

    return "\n".join(lines), title


def extract_xcom(url: str, browser: str = DEFAULT_BROWSER) -> dict:
    data = asyncio.run(_extract_content(url, browser))
    markdown, title = _build_markdown(data, url)

    filename = sanitize_filename(title) + ".md"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    output_path.write_text(markdown, encoding="utf-8")

    return {"file_path": str(output_path.relative_to(OUTPUT_DIR.parent)), "title": title}


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_xcom.py <URL> [browser]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    browser = sys.argv[2].lower() if len(sys.argv) >= 3 else DEFAULT_BROWSER

    result = extract_xcom(url, browser)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
