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
3. **画像説明の生成**: スクリプト出力の `images` 配列を処理し、各画像を読み取って説明文を書く（後述）
4. 出力ファイルを確認（公開してよい内容か確認）
5. git add → commit（自動）
6. **ユーザーに push 可否を確認してから push**

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
{
  "file_path": "agent-articles/タイトル.md",
  "title": "記事タイトル",
  "images": [
    {"index": 0, "alt": "alt text", "original_url": "https://...", "local_path": "/tmp/article-images/abc123.jpg"}
  ]
}
```

`images` が空でない場合、エージェントは「画像説明の生成」ステップを実行する（後述）。

## フローB: x.com（認証あり）

```bash
python3 .cursor/skills/agent-article-to-markdown/extract_xcom.py "<URL>"
```

- デフォルトブラウザ: **Brave**（固定、引数不要）
- 前提: ユーザーが Brave で x.com にログイン済み
- stdout 出力形式はフローA と同一（`images` 配列を含む）

## Git 操作

スクリプト実行 → 画像説明の生成後、以下を**自動**実行する:

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
- **画像**: 画像リンク (`![alt](url)`) は出力しない。代わりにエージェントが画像を読み取り、内容を自然言語で説明するテキストに置換する（後述の「画像説明の生成」を参照）
- リンクは `[text](url)` 形式で保持（`file://` / `file+.vscode-resource` は除去）
- 広告・ナビゲーション・フッターは除去
- 内容自体は改変しない

### 画像説明の生成（エージェント処理）

スクリプトは画像を `<!-- DESCRIBE_IMAGE_N -->` プレースホルダーに置換し、画像ファイルをローカルにダウンロードする。エージェントが画像を直接読み取り、内容を自然言語で説明する。

**スクリプト出力の `images` 配列が空でない場合、以下を実行する:**

1. `images` 配列の各要素について:
   a. `local_path` のファイルを **Read ツールで読み取る**（画像として認識される）
   b. 画像の内容を見て、**何が描かれているか・何を伝えているかを自然言語で簡潔に説明する**文を書く
   c. Markdown ファイル内の `<!-- DESCRIBE_IMAGE_N -->` を `> **[図]** {説明文}` に置換する
2. `local_path` が `null`（ダウンロード失敗）の場合:
   - `alt` テキストがあれば `> **[図]** {alt}` に置換
   - なければプレースホルダーを除去
3. 全画像の処理後、一時ファイルを削除する: `rm -rf /tmp/article-images/`

**説明文の書き方:**
- 画像の内容を客観的に、1〜3文で説明する
- グラフ・図表の場合は、軸・ラベル・主要な数値・傾向を含める
- スクリーンショットの場合は、表示されているUI要素・テキストの要点を記述する
- 写真の場合は、被写体・構図・文脈を記述する
- コードの画像の場合は、コード内容をそのままテキストとして書き起こす

**出力フォーマット:**

```markdown
> **[図]** 2024年1月〜12月の月次売上推移を示す折れ線グラフ。1月の100万円から右肩上がりで推移し、12月に400万円に達している。
```

## 設定

| 項目 | 値 |
|---|---|
| x.com 用ブラウザ | Brave（固定） |
| 出力先 | `agent-articles/` |
| 画像一時保存先 | `/tmp/article-images/` |
| macOS 依存 | あり（Keychain による Cookie 復号） |

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
