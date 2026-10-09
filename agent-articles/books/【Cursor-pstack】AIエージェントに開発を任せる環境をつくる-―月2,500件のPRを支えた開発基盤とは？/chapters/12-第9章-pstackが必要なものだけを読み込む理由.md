---
title: "第9章 pstackが必要なものだけを読み込む理由"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:27+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 12
---

# 第9章 pstackが必要なものだけを読み込む理由

**pstackは、Playbook、Principle、Skillのすべてを最初に読み込むわけではありません。先に読むのは、`/poteto-mode` の本体とPrincipleの索引だけ**です。

Playbookは依頼に合う1冊だけを、Principleの本文は条件に該当したときにそのPrincipleを、SkillはPlaybookの手順がその場面に来たときに読み込みます。

部品の呼ばれ方は[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)と[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)で見ました。この章では、読み込むものを4つのレイヤーに分ける設計と、その元にある考え方、設計の利点と弱点を解説します。

## この章の構成

この章の構成は次のとおりです。

- pstackは、読むものを4つのレイヤーに分けている
- この設計は、原則『Guard the Context Window』と同じ線引きをしている
- この設計には3つの利点があり、弱点は途中の点検で補う
- まとめ

## pstackは、読むものを4つのレイヤーに分けている

pstackが読むものは、**入口、手順、判断、能力の4つのレイヤー**に分かれており、常に読むのは入口だけです。

| レイヤー | 読むもの | 読むタイミング |
| --- | --- | --- |
| 第1レイヤー：入口 | [`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) の`SKILL.md`全体 | `/poteto-mode` を呼んだとき |
| 第2レイヤー：手順 | 依頼に合うPlaybookのファイル1冊 | 依頼をPlaybookに照らし合わせたとき |
| 第3レイヤー：判断 | 条件に該当したPrincipleの`SKILL.md` | 今の作業が索引の条件に該当したとき |
| 第4レイヤー：能力 | Playbookの手順や `Non-negotiables` が求めるSkillの`SKILL.md` | Playbookの手順がその場面に来たとき |

第1レイヤーの`SKILL.md`には、Playbookの本文もPrincipleの本文も入っていません。あるのは、`Non-negotiables` や返答の書き方のような、どの作業にも共通する決まりと、Playbookの1行の説明とファイルの場所、Principleの一覧（索引）と適用条件です。**第1レイヤーは、「何があり、いつ使うか」を知らせる目次と、共通の決まりでできています**。

4つのレイヤーとは別に、常に適用される小さなファイルが1つあります。`/setup-pstack` が書き出すモデル設定のルール `~/.cursor/rules/pstack-models.mdc` です。1行に1つの役割を書く短いファイルなので、常に適用されても、コンテキストに占める量は小さく済みます。詳しくは[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)で扱います。

## この設計は、原則『Guard the Context Window』と同じ線引きをしている

pstackの読み込みの設計は、原則『[**Guard the Context Window**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-guard-the-context-window/SKILL.md)』が**エージェントに求めるのと同じ線引き**をしています。

### 毎回使うものは中に、条件付きのものは外に置く

この原則では、**コンテキストウィンドウは有限で、すべてのトークンがコストに見合うべき**、と定めています。コンテキストウィンドウが占有されると推論の質が落ちるからです。

同原則には、毎回使う参照はSkillのファイルの中に置く、という項目があります。pstackでも、毎回使うPrincipleの索引と `Non-negotiables` は`SKILL.md`の中に、条件に該当したときだけ使う本文は別ファイルにしてあります。**毎回使うものは中に、ときどき使うものは外に**、という線引きがされています。

### サブエージェントへの渡し方も、コンテキストを節約する

`SKILL.md`の節『Subagents』は、サブエージェントには**コンテキストを書き写さず、ファイルの場所を渡すことを既定にしています**（[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)）。サブエージェントは必要なファイルを自分で開くので、主エージェントが長いコンテキストを積み上げて渡さずに済みます。

## この設計には3つの利点があり、弱点は途中の点検で補う

この設計の利点は、次の3つです。

1. **トークンとコストの節約**・・・ 使わない手順や判断基準がコンテキストを占めず、コンテキストウィンドウがあふれるまでの余裕が残ります。poteto氏も『The Complete Guide to pstack』[Part 2](https://x.com/poteto/status/2097732320606507506)で、Playbookを1冊ずつ読み込む理由をトークン効率だと説明しています。
2. **作業の一貫性**・・・ どの部品も、必要になった時点で完全な本文を読むので、エージェントの記憶や言い換えに頼らずに済みます。
3. **覚えることの少なさ**・・・ 利用者は70件の名前と使いどころを覚えず、`/poteto-mode` を覚えるだけで済みます。

### 弱点：条件の判定がエージェント任せになる

この設計の弱点は、どのPrincipleやPlaybookに該当するかの判定が、**エージェントに任されていること**です。判定を誤れば、読むべき本文が読まれないこともありえます。

本書では、pstackの次の仕組みが、これを途中の点検で補うものだと読みます。

| 仕組み | 利用者が点検できること |
| --- | --- |
| 飛ばした手順が `skip: <理由>` でTODOリストに残る | どの手順を、なぜやらなかったか |
| 判断を変えたPrincipleを返答で名前で挙げる（挙げてよいのは本文を読んだPrincipleだけ） | どの基準を読み、どの選択に効かせたか |
| Principleの名前を一言返すだけで方向を変えられる | ずれた判定を、その場で直せる |

!

**TODOリスト**・・・ エージェントが作業の始めに作る、その作業でやることの一覧（計画）です。Cursorでは、チャットの画面に表示されます。利用者は、この一覧を見て、エージェントがどの手順を進め、どの手順を飛ばしたか（`skip: <理由>`）を確かめられます（同梱ガイド [`01-setup.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md)）。

## まとめ

- **4つのレイヤー**・・・ pstackは、入口、手順、判断、能力の4つのレイヤーを、必要な時点で読み込みます。常に読むのは入口の `SKILL.md`（目次と索引、共通の決まり）だけです。
- **設計の元にある考え方**・・・ 原則『**Guard the Context Window**』と同じく、毎回使う索引は中に、条件付きで使う本文は外に置いています。
- **利点と弱点**・・・ 利点はトークン効率、一貫性、覚えやすさです。判定がエージェント任せになる弱点は、TODOリストと返答で点検します。

[第2部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a5fb04)では、pstackが何を解決し、入口の `/poteto-mode` がどう依頼を振り分け、3つの部品がどう分担し、それらがどう読み込まれるかを見てきました。次の[第3部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/72f8ee)からは、23件のPlaybookを一つずつ見ていきます。最初の[第10章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ea525d)では、コードを変えずに問題を調べ、診断するためのPlaybookを扱います。
