---
title: "第2部 pstackとは何か"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a5fb04"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:26+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 8
---

# 第2部 pstackとは何か

第2部では、「**pstackは、[第1部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/86acbc)の条件をどういう部品で実現しているか**」を、pstackの設計を通して解説します。

結論から言うと、pstackは、**入口を一つにし、中身を必要なときに必要な分だけ読む設計**で、この条件を実現しています。

利用者が覚える入口は、基本的に [`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) だけです。

`/poteto-mode` が依頼の種類を見てPlaybookを1冊選び、Playbookが作業の順番を決め、各手順で必要なSkillを呼びます。その間、Principleが「この一手を採るか」「まだ終わりではないか」の判断基準として働きます。

すべてを最初に読み込むわけではなく、Playbookは依頼に合う1冊だけを開き、Principleは最初に一覧だけを読んで、条件に該当したときに本文を読みます。この設計が、**手順の厳密さとトークン効率の両立**を支えています。

## 第2部で分かること

第2部を読むと、次のことが分かります。

- pstackが解こうとしている問題と、何を目指して作られたか
- `/poteto-mode` に依頼を渡すと何が起きるか。良い依頼の書き方
- Playbook、Skill、Principleがそれぞれ何を担当し、どう異なるのか
- 手順と判断基準を「必要なときに呼び出す」仕組みと、その利点

[第3部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/72f8ee)から[第5部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2a4af5)は、pstackの全項目を扱う詳細編です。第2部は、その詳細を読むための地図にあたります。部品の役割分担をつかんでおくと、各項目が「どの部品の、どの役割を担っているか」を迷わずに読めます。

## この部の章

| 章 | 役割 |
| --- | --- |
| [第6章 pstackは何を解決するのか](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/33f073) | pstackの全体像と目的。何を問題とし、何を目指しているか |
| [第7章 /poteto-mode ― 依頼を適切な進め方につなぐ入口](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d) | 入口の使い方。依頼がPlaybookに振り分けられる流れと、依頼の書き方 |
| [第8章 Playbook・Skill・Principleは何を担うのか](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d) | 3つの部品の役割と違い。サブエージェントの位置づけ |
| [第9章 pstackが必要なものだけを読み込む理由](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496) | 読み込みの設計。なぜ全部を常に読ませないのか |

[第6章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/33f073)で「何のために」を、[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)で「どう使うか」を、[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)と[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)で「中はどうなっているか」を扱います。[はじめに](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/d4d843)で紹介した重複行の依頼は、[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)で、『[**Bug fix**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)』Playbookに振り分けられ、SkillとPrincipleが働く場所をたどる例として登場します。各章を順に読むことを推奨します。
