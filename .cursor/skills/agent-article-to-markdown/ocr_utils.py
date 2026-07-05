#!/usr/bin/env python3
"""macOS Vision framework OCR utility for extracting text from images."""

import os
import re
import sys
import tempfile

import requests

_VISION_AVAILABLE: bool | None = None


def _check_vision() -> bool:
    """Check if macOS Vision framework is available (once per process)."""
    global _VISION_AVAILABLE
    if _VISION_AVAILABLE is None:
        try:
            import Vision  # noqa: F401

            _VISION_AVAILABLE = True
        except ImportError:
            _VISION_AVAILABLE = False
            print(
                "WARNING: pyobjc-framework-Vision が未インストールのため画像OCRをスキップします",
                file=sys.stderr,
            )
    return _VISION_AVAILABLE


def _ocr_with_vision(image_path: str, languages: list[str] | None = None) -> str:
    """Run OCR on a local image file using macOS Vision framework."""
    if not _check_vision():
        return ""

    from Foundation import NSURL
    import Vision

    if languages is None:
        languages = ["ja", "en"]

    file_url = NSURL.fileURLWithPath_(image_path)
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(
        file_url, None
    )

    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(1)  # VNRequestTextRecognitionLevelAccurate
    request.setRecognitionLanguages_(languages)
    request.setUsesLanguageCorrection_(True)

    success, error = handler.performRequests_error_([request], None)
    if not success:
        return ""

    results = request.results()
    if not results:
        return ""

    lines = []
    for observation in results:
        candidates = observation.topCandidates_(1)
        if candidates:
            lines.append(candidates[0].string())

    return "\n".join(lines)


def download_and_ocr(image_url: str, languages: list[str] | None = None) -> str:
    """Download an image from URL and extract text via OCR.

    Returns extracted text, or empty string on failure.
    """
    if not image_url or image_url.startswith("data:"):
        return ""
    if not _check_vision():
        return ""

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
        return ""

    content_type = resp.headers.get("content-type", "")
    if "png" in content_type:
        ext = ".png"
    elif "webp" in content_type:
        ext = ".webp"
    elif "gif" in content_type:
        ext = ".gif"
    else:
        ext = ".jpg"

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
            f.write(resp.content)
            tmp_path = f.name
        return _ocr_with_vision(tmp_path, languages)
    except Exception:
        return ""
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def enrich_markdown_images(markdown_text: str) -> str:
    """Replace ![alt](url) with OCR-based text descriptions (no image links)."""
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    vision_ok = _check_vision()

    def _replace(match: re.Match) -> str:
        alt = match.group(1)
        url = match.group(2)

        if vision_ok:
            ocr_text = download_and_ocr(url)
            if ocr_text.strip():
                desc_lines = ocr_text.strip().split("\n")
                quoted = "\n> ".join(desc_lines)
                return f"> **[図]** {quoted}"

        if alt and alt not in ("image", ""):
            return f"> **[図]** {alt}"
        return ""

    result = pattern.sub(_replace, markdown_text)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result
