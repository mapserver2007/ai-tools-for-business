#!/usr/bin/env python3
"""Render an existing article Markdown file as HTML."""

import json
import sys
from pathlib import Path

from html_utils import REPO_ROOT, write_html


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: render_html.py <Markdown file>", file=sys.stderr)
        sys.exit(1)

    markdown_path = Path(sys.argv[1])
    if not markdown_path.is_absolute():
        markdown_path = Path.cwd() / markdown_path
    markdown_path = markdown_path.resolve()
    if markdown_path.suffix.lower() != ".md":
        print("ERROR: Markdown ファイル（.md）を指定してください", file=sys.stderr)
        sys.exit(1)
    if not markdown_path.is_file():
        print(f"ERROR: ファイルが見つかりません: {markdown_path}", file=sys.stderr)
        sys.exit(1)

    html_path = write_html(
        markdown_path.read_text(encoding="utf-8"),
        markdown_path.name,
    )
    print(
        json.dumps(
            {
                "file_path": str(markdown_path.relative_to(REPO_ROOT)),
                "html_file_path": str(html_path.relative_to(REPO_ROOT)),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
