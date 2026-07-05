#!/usr/bin/env python3
"""Download article images and insert placeholders for agent-based description."""

import hashlib
import re
import shutil
import tempfile
from pathlib import Path

import requests

TEMP_IMAGE_DIR = Path(tempfile.gettempdir()) / "article-images"


def download_image(image_url: str) -> str | None:
    """Download an image and return the local file path, or None on failure."""
    if not image_url or image_url.startswith("data:"):
        return None

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        }
        resp = requests.get(image_url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception:
        return None

    content_type = resp.headers.get("content-type", "")
    if "png" in content_type:
        ext = ".png"
    elif "webp" in content_type:
        ext = ".webp"
    elif "gif" in content_type:
        ext = ".gif"
    else:
        ext = ".jpg"

    TEMP_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    name = hashlib.md5(image_url.encode()).hexdigest()[:12]
    path = TEMP_IMAGE_DIR / f"{name}{ext}"
    path.write_bytes(resp.content)
    return str(path)


def replace_images_with_placeholders(
    markdown_text: str,
    index_offset: int = 0,
) -> tuple[str, list[dict]]:
    """Replace ![alt](url) with <!-- DESCRIBE_IMAGE_N --> placeholders.

    Returns (modified_markdown, image_info_list).
    Each dict: {index, alt, original_url, local_path}.
    """
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    images: list[dict] = []
    counter = [index_offset]

    def _replace(match: re.Match) -> str:
        alt = match.group(1)
        url = match.group(2)
        local_path = download_image(url)
        idx = counter[0]

        images.append({
            "index": idx,
            "alt": alt,
            "original_url": url,
            "local_path": local_path,
        })
        counter[0] += 1
        return f"<!-- DESCRIBE_IMAGE_{idx} -->"

    result = pattern.sub(_replace, markdown_text)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result, images


def cleanup_temp_images() -> None:
    """Remove the temporary image directory."""
    if TEMP_IMAGE_DIR.exists():
        shutil.rmtree(TEMP_IMAGE_DIR)
