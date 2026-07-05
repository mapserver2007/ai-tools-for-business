---
name: agent-article-to-markdown
description: >-
  WebページのURLを受け取り、記事内容をLLM最適化Markdownに変換し、git commitまで自動実行する。
  git push はユーザー確認後のみ実行。
  「記事を保存して」「この記事をmarkdownにして」「URLをmarkdown化して」等で起動する。
  認証なしサイトと x.com（認証あり）に対応。
---

# agent-article-to-markdown

URL を受け取り、記事を Markdown 化し、git commit まで自動実行する。**git push はユーザー確認後のみ。**

## 実行手順

1. URL からサイトを判定
2. 適切なスクリプトを実行
3. 出力ファイルを確認（公開してよい内容か確認）
4. git add → commit（自動）
5. **ユーザーに push 可否を確認してから push**

取得〜commit までは自動でよい。push だけは必ずユーザー承認を取ること。

## 保存対象の制限

以下は保存・commit しない。該当する場合はユーザーに報告して停止する:

- 非公開・限定公開の x.com 投稿（フォロワー限定、鍵アカウント等）
- 認証が必要な社内 URL・イントラネット URL
- 取得内容にローカルパス（`file://`, `file+.vscode-resource` 等）が含まれる場合は除去してから保存

## フロー判定

| URL パターン | スクリプト |
|---|---|
| `x.com/*` または `twitter.com/*` | `extract_xcom.py` |
| 上記以外 | `extract_article.py` |

## フローA: 認証なしサイト

```bash
python3 .cursor/skills/agent-article-to-markdown/extract_article.py "<URL>"
```

スクリプトは以下を stdout に JSON で出力する:

```json
{"file_path": "agent-articles/タイトル.md", "title": "記事タイトル"}
```

## フローB: x.com（認証あり）

```bash
python3 .cursor/skills/agent-article-to-markdown/extract_xcom.py "<URL>"
```

- デフォルトブラウザ: **Brave**（固定、引数不要）
- 前提: ユーザーが Brave で x.com にログイン済み
- stdout 出力形式はフローA と同一

## Git 操作

スクリプト実行後、以下を**自動**実行する:

```bash
git add agent-articles/{filename}.md
git commit -m "docs(articles): add {タイトル要約}"
```

push は**ユーザー確認後のみ**:

```bash
git push
```

push 前にユーザーへ「公開リポジトリへ push してよいか」を確認すること。明示的な承認なしに push しない。

### コミットメッセージ規則

- 形式: `docs(articles): add {タイトルを50文字以内に要約}`
- 記事タイトルから、何の記事か分かる簡潔なメッセージを生成
- 日本語記事は日本語で、英語記事は英語で要約
- 例: `docs(articles): add React Server Components解説`
- 例: `docs(articles): add @user thread on LLM agents`

## 出力フォーマット仕様

保存先: `agent-articles/{sanitized_title}.md`

ファイル名のサニタイズ: `/\:*?"<>|` を除去、空白を `-` に変換、100文字以内に切り詰め。

### Markdown 構造

```markdown
---
title: "記事タイトル"
source_url: "https://example.com/article"
author: "著者名"
published_at: "YYYY-MM-DD"
retrieved_at: "YYYY-MM-DDTHH:MM:SS+09:00"
site: "example.com"
content_type: "article"
---

# 記事タイトル

{本文}
```

### frontmatter フィールド

| フィールド | 必須 | 説明 |
|---|---|---|
| title | Yes | 記事タイトル |
| source_url | Yes | 元URL |
| author | No | 著者名（取得できない場合は省略） |
| published_at | No | 公開日（取得できない場合は省略） |
| retrieved_at | Yes | 取得日時（ISO 8601） |
| site | Yes | ドメイン名 |
| content_type | Yes | `article` / `tweet` / `thread` |

### 本文変換ルール

- 見出し(h1-h6)、段落、リスト、引用、コードブロックをそのまま Markdown に変換
- **画像OCR**: 画像は `![alt](url)` 形式で保持しつつ、macOS Vision framework で OCR を実行し、読み取った内容を自然言語で説明するブロック引用を直下に付与する（画像自体はダウンロードしない）
- リンクは `[text](url)` 形式で保持（`file://` / `file+.vscode-resource` は除去）
- 広告・ナビゲーション・フッターは除去
- 内容自体は改変しない

### 画像OCR処理

記事内の画像に対して自動的にOCR（文字認識）を実行し、画像内のテキストを読み取って説明を付与する。

**処理フロー:**
1. Markdown 内の `![alt](url)` パターンを検出
2. 画像をダウンロード（一時ファイル）
3. macOS Vision framework (`VNRecognizeTextRequest`) で OCR 実行（日本語・英語対応）
4. 読み取ったテキストをブロック引用形式で画像直下に追記
5. 一時ファイルを削除

**出力フォーマット:**

テキストが読み取れた場合:
```markdown
![alt](url)

> **[図の説明]** OCRで読み取ったテキスト内容
```

テキストが読み取れないが alt テキストがある場合:
```markdown
![alt](url)

> **[図の説明]** alt テキスト
```

テキストもaltも無い場合はそのまま:
```markdown
![alt](url)
```

**フォールバック:** `pyobjc-framework-Vision` が未インストールの場合、OCR をスキップして従来通り `![alt](url)` のみ出力する（stderr に警告を出力）。

## 設定

| 項目 | 値 |
|---|---|
| x.com 用ブラウザ | Brave（固定） |
| 出力先 | `agent-articles/` |
| macOS 依存 | あり（Keychain による Cookie 復号、Vision framework による OCR） |
| OCR 対応言語 | 日本語、英語 |
| OCR エンジン | macOS Vision framework (`VNRecognizeTextRequest`) |

## 制約

- **Cookie 値の直接操作禁止**: AI は Cookie 値を読み取り・ログ出力しない
- **push 無承認禁止**: ユーザー確認なしに git push しない
- **内容改変禁止**: 記事本文は要約・編集せず忠実に変換する（ローカルパスリンクの除去を除く）
- **エラー時のみ停止**: スクリプトが非ゼロ終了した場合のみユーザーに報告する

## エラーハンドリング

| エラー | 対応 |
|---|---|
| ネットワークエラー | エラーメッセージを報告して停止 |
| x.com 認証失敗 | 「Brave で x.com にログインし直してください」と報告 |
| ページ内容取得不可 | エラー内容を報告して停止 |
| git push 失敗 | エラー内容を報告（ファイルは保存済み） |
