---
title: "第5部 Skillで仕事の能力を広げる"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2a4af5"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:31+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 27
---

# 第5部 Skillで仕事の能力を広げる

第5部では、pstackの全Skill（27件）を網羅的に取り扱います。

!

この部は読み飛ばしても構いません。関心のある章だけを読む使い方を推奨します。

各Skillの原文は、[pstack](https://github.com/cursor/plugins/tree/main/pstack)のリポジトリでいつでも読めます。必要になったときに、該当する章とファイルを参照してください。

## 第5部で分かること

- 各Skillが何をし、どんなときに使うか（例：`/how` は、コードを変える前に、今のコードの挙動を説明する）
- どんな形の出力を返すか（例：`/why` は、見つけた理由の一つ一つに、記録で裏づけられたものか推測かを示す段階を付ける）
- 直接呼ぶときの依頼例と、似ているSkillとの使い分け（例：差分の中の弱点を探すなら `/interrogate`、差分の外で壊れるものを探すなら `/blast-radius`）

Skillは、調べる（例：`/why`）、設計する（例：`/architect`）、確かめる（例：`/blast-radius`）、整える（例：`/unslop`）といった作業の手順を、名前で呼べば何度でも、同じ手順で動くようにまとめたものです。

多くは、`/poteto-mode` がPlaybookの手順の中で自動で呼びます。

利用者は、Skillを名前で直接呼ぶこともできます。直接呼ぶのは、Playbookが決めたSkillの選び方を変えたいときや、既定より念入りな確認が欲しいときです。

たとえば、`/poteto-mode` の手順が `/blast-radius` を呼ばない小さな差分でも、利用者が信用しきれなければ、`/blast-radius` を直接呼んで、その差分が何を壊しうるかを確かめられます。

**直接呼ぶには、各Skillが何をするかを利用者が知っている必要があります**。第5部の各章は、そのための説明です。

## この部の章

| 章 | 役割 | 扱うSkill |
| --- | --- | --- |
| [第22章 コードベースと過去の作業を理解する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746) | 今のコードの挙動と、コードが今の形になった理由を調べ、前回の作業の続きから再開する | [`/how`](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md)、[`/why`](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md)、[`/teach`](https://github.com/cursor/plugins/blob/main/pstack/skills/teach/SKILL.md)、[`/recall`](https://github.com/cursor/plugins/blob/main/pstack/skills/recall/SKILL.md) |
| [第23章 依頼に合うPlaybookが存在しない作業のPlaybookを設計する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/3ce2b2) | 合うPlaybookがない作業のために、終了条件と検証の仕組みを先に決めた手順を設計する | [`/figure-it-out`](https://github.com/cursor/plugins/blob/main/pstack/skills/figure-it-out/SKILL.md) |
| [第24章 複数のエージェントを並列に動かし、設計と成果物を比べる](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346) | 実装の前に型とモジュールの境界を決め、複数のエージェントに同じ課題を解かせて案を比べ、仕事を複数のエージェントに分担させる | [`/architect`](https://github.com/cursor/plugins/blob/main/pstack/skills/architect/SKILL.md)、[`/arena`](https://github.com/cursor/plugins/blob/main/pstack/skills/arena/SKILL.md)、[`/swarm`](https://github.com/cursor/plugins/blob/main/pstack/skills/swarm/SKILL.md) |
| [第25章 pstackを自分の流儀とGrok Botに広げる](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f) | 利用者のチャットの履歴から利用者専用の mode のSkillを作り、Grok Bot をボタンで起動するページを作る | [`/automate-me`](https://github.com/cursor/plugins/blob/main/pstack/skills/automate-me/SKILL.md)、[`/make-bot-ui`](https://github.com/cursor/plugins/blob/main/pstack/skills/make-bot-ui/SKILL.md) |
| [第26章 検証の仕組みを作り、アプリに合わせ続ける](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca) | アプリをユーザーと同じ経路で動かして確かめるプロジェクト専用のSkill（検証スキル）を作り、アプリの変化に合わせて直す | [`/create-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md)、[`/maintain-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md) |
| [第27章 測った性能の数値を、報告する前に点検する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/167c91) | 測った性能の数値が、測りたかった作業を測ったものかを、報告や判断の前に7つの質問で点検する | [`/benchmark-checklist`](https://github.com/cursor/plugins/blob/main/pstack/skills/benchmark-checklist/SKILL.md) |
| [第28章 変更が壊しうるものと、差分の弱点を確かめる](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880) | 変更したファイルの外で壊れうるものを探し、差分の弱点を複数のモデルに探させる | [`/blast-radius`](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md)、[`/interrogate`](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md) |
| [第29章 判断を記録し、エージェントの長時間作業を証拠でたどれるようにする](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/724887) | 判断とその根拠を記録に残し、別系統のモデルに点検させる | [`/show-me-your-work`](https://github.com/cursor/plugins/blob/main/pstack/skills/show-me-your-work/SKILL.md) |
| [第30章 TypeScriptの16の規則で、コードの品質を保つ](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f9a46) | 不正な状態を型で書けなくし、外から受け取るデータを入ってくる場所で一度だけ検証する | [`/typescript-best-practices`](https://github.com/cursor/plugins/blob/main/pstack/skills/typescript-best-practices/SKILL.md) |
| [第31章 【TDD】修正前に失敗するテストで確かめる](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ad5727) | 不具合を直す前に、修正前に失敗するテストを書く | [`/tdd`](https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md) |
| [第32章 コメントを消し、コードベースを整備する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8960d3) | 差分の不要なコメントを、書いていないエージェントに審査させて消す | [`/no-comments`](https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md) |
| [第33章 文章の品質を保つ](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b) | 文章からAIらしい癖を取り除き、分かりにくい返答を専門用語なしで言い直し、文書の種類を決めてから書く | [`/unslop`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md)、[`/bro`](https://github.com/cursor/plugins/blob/main/pstack/skills/bro/SKILL.md)、[`/technical-writing`](https://github.com/cursor/plugins/blob/main/pstack/skills/technical-writing/SKILL.md) |
| [第34章 作業の学びを振り返り、反映する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f70847) | 長い作業で学んだことを、既存のSkillに追記するなどして残す | [`/reflect`](https://github.com/cursor/plugins/blob/main/pstack/skills/reflect/SKILL.md) |
| [第35章 繰り返す間違いを、リポジトリの仕組みで起こせなくする](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/fe17ab) | エージェントが繰り返す間違いを履歴から見つけ、アーキテクチャ、型、lint、テストで起こせなくする | [`/correct`](https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md) |
| [第36章 pstackを導入し、役割ごとのモデルを決める](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0) | pstackをインストールし、pstackが役割ごとに使うモデルを設定する | [`/setup-pstack`](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md) |
| [第37章 /poteto-help ― pstackの使い方を尋ね、依頼文を受け取る](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/77207a) | pstackの使い方に関する質問に対して、次の3つを返す。質問への回答、送れる依頼文、出典のリンク | [`/poteto-help`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md) |
| [第38章 /poteto-mode ― pstackのRouter](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911) | 依頼に合うPlaybookを選び、必要なSkillとPrincipleを読み込ませる規則を整理する | [`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) |

本書では、章を仕事の流れに沿って並べています。流れは次のとおりです。

- 今のコードを理解する（[第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746)）
- 複数のエージェントを並列に動かし、設計と成果物を比べる（[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)）
- 実装して、動くことを確かめる（[第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca)）
- 測った性能の数値を確かめる（[第27章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/167c91)）
- 変更が壊しうるものを確かめる（[第28章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880)）
- 判断を記録する（[第29章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/724887)）
- コードを整える（第30〜32章）
- 文章を整える（[第33章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b)）
- 学んだことを残す（[第34章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f70847)）
- 繰り返す間違いを、仕組みで起こせなくする（[第35章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/fe17ab)）

[第23章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/3ce2b2)は、合うPlaybookがない作業のために、進め方そのものを設計するSkillの章です。流れの中の特定の工程ではなく、作業全体の進め方を扱うので、流れとは別に扱います。

[第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f)は、pstackを利用者の流儀や Grok Bot に合わせて広げる2つのSkillをまとめた章です。流れの中の特定の工程で使うものではないので、流れとは別に扱います。

[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)はモデルを設定する `/setup-pstack` の章、[第37章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/77207a)は使い方に迷ったときに質問する `/poteto-help` の章、[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)は依頼を最初に受け取る `/poteto-mode` の章です。

pstackの [README](https://github.com/cursor/plugins/blob/main/pstack/README.md) は、使い始める手順を「`/setup-pstack` でモデルを選び、厳密さが必要な作業では `/poteto-mode` を使う。それだけ」とまとめ、ほかのSkillは `/poteto-mode` が必要に応じて使う、と書いています。

`/setup-pstack` は使い始めるときに、`/poteto-mode` は作業を始めるたびに、最初に使うSkillです。`/poteto-help` は、使い方に迷ったときに使うSkillです。3つとも、流れの中の特定の工程で使うものではないので、本書では流れとは別の章で扱います。

## 全Skillの早見表

| Skill | 概要 | 使う場面 | 使い方（誰が呼ぶか） | 解説 |
| --- | --- | --- | --- | --- |
| [`/how`](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md) | 今のコードの挙動（処理のきっかけ、通る関数、データの流れ）を説明する | 利用者やエージェントが、コードを変える前にサブシステムの挙動を知りたいとき、またはコードをどこに置くべきかを問うとき | `/poteto-mode`（『Non-negotiables』の規則と、『[**Investigation**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/investigation.md)』『[**Bug fix**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)』『[**Feature**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md)』『[**Refactoring**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/refactoring.md)』などのPlaybookの手順）、`/teach`、`/architect`、`/no-comments`、利用者 | [第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746) |
| [`/why`](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md) | コードが今の形になった理由を、コミット、PR、チケットなどの記録から調べ、記録で裏づけられる理由と推測を分けて答える | 利用者やエージェントが、設計の理由、リグレッションの経緯、しきい値の由来を問うとき | `/poteto-mode`（『Investigation』『Bug fix』のPlaybookの手順）、`/teach`、`/recall`、`/architect`、`/no-comments`、利用者 | [第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746) |
| [`/teach`](https://github.com/cursor/plugins/blob/main/pstack/skills/teach/SKILL.md) | `/how` と `/why` を呼び、コードや変更が何で、どう動き、なぜそう作られているかを一つの平易な説明にまとめる | 利用者が、要約では足りず、変更やサブシステムを本当に理解したいとき | 利用者が名前で呼んだときだけ | [第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746) |
| [`/recall`](https://github.com/cursor/plugins/blob/main/pstack/skills/recall/SKILL.md) | 自分のチャット履歴と共有の記録から最近の作業の経緯を集め、作業がどこまで進み、次に何をすべきかを短く返す | 利用者が、作業を始める前や再開する前に、前回どこまで進めたかを知りたいとき | 利用者が名前で呼んだときだけ | [第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746) |
| [`/blast-radius`](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md) | 変更したファイルの外で壊れうるものを探し、変更が安全だと言える根拠を、コードを実行して確かめる | 利用者が、小さく見えるのに信用しきれない差分について、ほかに何を壊しうるかを知りたいとき | 利用者が名前で呼んだときだけ | [第28章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880) |
| [`/interrogate`](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md) | 別々のモデルのレビュアーに同じ差分の弱点を探させ、主エージェントがその指摘を4つに仕分ける | 利用者やエージェントが、厳しいコード品質の観点も含めて、差分がどこで壊れるかを複数のモデルに探させたいとき | `/poteto-mode`（意見の分かれる設計をマージする前に使う『Non-negotiables』の規則と、『Feature』『[**Opening a PR**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md)』のPlaybookの手順）、`/architect`、利用者 | [第28章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880) |
| [`/figure-it-out`](https://github.com/cursor/plugins/blob/main/pstack/skills/figure-it-out/SKILL.md) | 依頼に合うPlaybookがない作業のために、終了条件と検証の仕組みを先に決め、判断の記録を残しながら進める手順を設計する | 利用者が、多くの呼び出し元にまたがる移行や、席を外している間に進めてもらう作業を任せるとき、または依頼に合うPlaybookがないとき | `/poteto-mode`（節『Playbooks』の規則。大きな作業、席を外す作業、合うPlaybookがない作業をこのSkillに回す）、利用者 | [第23章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/3ce2b2) |
| [`/architect`](https://github.com/cursor/plugins/blob/main/pstack/skills/architect/SKILL.md) | 関数の境界をまたぐコードを書く前に、型、関数のシグネチャ、モジュールの境界を、関数の中身を書かない骨組みで決める | エージェントが、関数の境界をまたぐコードを書こうとするとき | `/poteto-mode`（『Non-negotiables』の規則と、『Feature』『Bug fix』『Refactoring』『[**Perf issue**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/perf-issue.md)』のPlaybookの手順）、`/figure-it-out`、`/no-comments`、利用者 | [第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346) |
| [`/arena`](https://github.com/cursor/plugins/blob/main/pstack/skills/arena/SKILL.md) | 同じ課題をN個の候補に並列に解かせ、最も良い候補を土台に選び、ほかの候補の良い考えを移植する | 利用者やエージェントが、後から変えると高くつく成果物（例：キャッシュキーの形式）を作るとき | `/poteto-mode`（『Non-negotiables』の規則と、『Feature』『[**Eval**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md)』『[**Orchestrate**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md)』のPlaybookの手順）、`/architect`、`/blast-radius`、利用者 | [第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346) |
| [`/swarm`](https://github.com/cursor/plugins/blob/main/pstack/skills/swarm/SKILL.md) | N体のWorkersを分担か競争で並列に動かし、その結果を一つの報告にまとめる | エージェントが、網羅、競争、関門、探索の分割のために仕事を並列に分けるとき | `/poteto-mode`（『Non-negotiables』の規則と、『[**Multi-phase or multi-PR plan**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md)』『[**Autopilot-full**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-full.md)』のPlaybookの手順）、利用者 | [第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346) |
| [`/automate-me`](https://github.com/cursor/plugins/blob/main/pstack/skills/automate-me/SKILL.md) | 利用者のチャットの履歴と質問への答えから、その利用者専用の `-mode` Skillを作る | 利用者が、自分の好みや働き方に合う mode のSkillをエージェントに従わせたいとき | 利用者が名前で呼んだときだけ | [第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f) |
| [`/make-bot-ui`](https://github.com/cursor/plugins/blob/main/pstack/skills/make-bot-ui/SKILL.md) | ボタンを押すと webhook で Grok Bot を起動するページを、送信キーをエージェントに見せずに作る | 利用者が、Grok Bot を webhook で起動するページを作り、送信キーを渡し、そのページを Tailscale で公開したいとき | 利用者が名前で呼んだときだけ | [第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f) |
| [`/create-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) | アプリを起動・操作して証拠を残すプロジェクト専用の検証スキルを、`.cursor/skills/verify-<app>/` に生成する | 利用者のプロジェクトに、アプリの挙動をスクリプトで繰り返し証明する手段がないとき | 利用者、`/setup-pstack`（最後の手順で生成を提案し、利用者が受け入れたときに呼ぶ） | [第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca) |
| [`/maintain-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md) | 検証スキルと Feature Map が今のアプリと食い違っていないかを点検し、そのずれを直す | 利用者が、アプリを変えた後に、Feature Map の記述と今のアプリのずれを直したいとき | 利用者が名前で呼んだときだけ | [第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca) |
| [`/benchmark-checklist`](https://github.com/cursor/plugins/blob/main/pstack/skills/benchmark-checklist/SKILL.md) | 測った性能の数値を、頭打ちの原因、設定、限界、エラー、再現性、全体の中での意味、作業が行われたかを問う7つの質問で点検し、結論を先に報告する | エージェントがベンチマークを実行したり、自分で性能を測ったり、測った高速化や性能の低下を報告したりするとき | `/poteto-mode`（性能を測るときの規則と、『Perf issue』『Hillclimb』のPlaybookの手順）、利用者 | [第27章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/167c91) |
| [`/show-me-your-work`](https://github.com/cursor/plugins/blob/main/pstack/skills/show-me-your-work/SKILL.md) | 長い作業の判断と根拠を `decisions.tsv` に記録し、その記録を別系統のモデルに点検させる | エージェントが、長い作業、自律的な作業、利用者が席を外して後で確かめる作業を進めるとき | `/poteto-mode`（『Non-negotiables』の規則と、『[**Autonomous run**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autonomous-run.md)』『Orchestrate』『[**Hillclimb**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md)』『Autopilot-full』などのPlaybookの手順）、`/figure-it-out`、利用者 | [第29章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/724887) |
| [`/typescript-best-practices`](https://github.com/cursor/plugins/blob/main/pstack/skills/typescript-best-practices/SKILL.md) | 不正な状態を型で書けなくする方法を、TypeScript の16の規則で示す | エージェントが `.ts` か `.tsx` のファイルを読んだり編集したりするとき | 自動では読み込まれない。TypeScriptのファイルを扱う作業で、利用者が名前を出して呼ぶ | [第30章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f9a46) |
| [`/tdd`](https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md) | 不具合を直す前に回帰テストを一つ書き、そのテストが修正前に失敗し、修正後に通ることを確かめる | 利用者がTDDや失敗するテストを頼んだとき、または不具合を手元ですぐ実行できるテストで確かめられるとき | `/poteto-mode`（『Bug fix』Playbookの手順5）、利用者 | [第31章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ad5727) |
| [`/no-comments`](https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md) | 差分のコメントを、コメントを書いていないサブエージェント Comment Sicko に審査させ、受け入れた指摘を直す | エージェントが、レビューの前に差分のコメントを取り除くとき | `/poteto-mode`（『Non-negotiables』の規則と、『Opening a PR』『Autopilot-full』『[**Autopilot-stack**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-stack.md)』『Multi-phase or multi-PR plan』のPlaybookの手順）、利用者 | [第32章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8960d3) |
| [`/unslop`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) | どんな文章からも、AIが書いたと分かる癖を、番号付きの規則で取り除く | エージェントが、返答を含むあらゆる文章を書くとき | `/poteto-mode`（『Non-negotiables』の規則と、『Investigation』『Opening a PR』『Multi-phase or multi-PR plan』のPlaybookの手順）、`/technical-writing`、`/show-me-your-work`、`/recall`、`/teach`、`/blast-radius`、`/automate-me`、利用者 | [第33章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b) |
| [`/bro`](https://github.com/cursor/plugins/blob/main/pstack/skills/bro/SKILL.md) | エージェントの直前の返答を、専門用語なしで言い直す | 利用者が、エージェントの返答は詳しいのに、何を言っているのか分からないとき | 利用者が名前で呼んだときだけ | [第33章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b) |
| [`/technical-writing`](https://github.com/cursor/plugins/blob/main/pstack/skills/technical-writing/SKILL.md) | 技術文書を書くときに従う規範を、文書の種類から一文の書き方までの4つの層で示す | エージェントが、ドキュメント、RFC、README、PR説明、コミットメッセージを書くときやレビューするとき | `/poteto-mode`（『Non-negotiables』の規則と、『Opening a PR』『Multi-phase or multi-PR plan』のPlaybookの手順）、利用者 | [第33章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b) |
| [`/reflect`](https://github.com/cursor/plugins/blob/main/pstack/skills/reflect/SKILL.md) | 作業の会話から次の作業でも使える学びを取り出し、利用者が承認したものだけを、既存のSkillに追記するなどして残す | 学びのあった作業の直後に、利用者が `/reflect` を呼んだとき | 利用者が名前で呼んだときだけ | [第34章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f70847) |
| [`/correct`](https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md) | エージェントが繰り返す間違いを、コミットやレビューの履歴から種類ごとにまとめ、アーキテクチャ、型と lint、テスト、文書の順に、止められる段のうち、最も上の段で起こせなくする | 利用者が、同じ間違いについてエージェントを訂正し続けているとき | 利用者が名前で呼んだときだけ | [第35章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/fe17ab) |
| [`/setup-pstack`](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md) | 推論の予算と役割ごとのモデルを尋ね、その答えを常に適用されるルール `~/.cursor/rules/pstack-models.mdc` に書き出す | 利用者が、pstack を使い始めるとき、または pstack が役割ごとに使うモデルを変えたいとき | 利用者。`SKILL.md` に `disable-model-invocation: true` がないので、エージェントが依頼の内容（例：「configure pstack models」）から選んで動かすこともできる | [第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0) |
| [`/poteto-help`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md) | pstackの使い方に関する質問に対して、次の3つを返す。質問への回答、送れる依頼文、出典のリンク | 利用者が、pstackを使い始めたとき、またはどのSkill、Playbook、Principleを使えばよいか迷ったとき | 利用者。`disable-model-invocation: true` を持つので、利用者が `/poteto-help` と入力したときだけ動く | [第37章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/77207a) |
| [`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) | 依頼に合うPlaybookを選び、必要なSkillとPrincipleをエージェントに読み込ませる規則をまとめる | 利用者が、厳密さが必要な作業（例：不具合を再現してから直し、直ったことを確かめる作業）を依頼するとき | 利用者が名前で呼んだときだけ。一度呼ぶと、利用者がやめると言うまで、同じ会話の後のターンでも有効なまま | [第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911) |
