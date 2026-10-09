---
title: "第8章 Playbook・Skill・Principleは何を担うのか"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:27+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 11
---

# 第8章 Playbook・Skill・Principleは何を担うのか

pstackの中身は、**Playbook、Skill、Principleの3種類の部品**でできています。

Playbookは作業の順序を決めます。Skillは手順の中で使う能力を提供します。Principleは、特定の状況で作業中の判断を導くルールです。変更を小さくする、根本原因を直す、完了を報告する前に実物を確かめる、といった判断に使います。

この章では、3つの部品の違いと、それぞれの担うものを中心に解説し、部品をつなぐ`Non-negotiables`と2つのサブエージェント、実例の依頼で部品が働く場所を、この順に見ていきます。

## この章の構成

この章の構成は次のとおりです。

- 3つの部品は、「順序」「能力」「判断」を分担している
- Playbookは、作業の種類ごとの手順と順番を決める
- Skillは、手順の中で呼び出す能力
- Principleは、手順や能力ではなく、作業途中の判断の基準
- Non-negotiablesが、3つの部品をつなぐ
- 2つのサブエージェントは、作業を分担する相手
- SkillとPrincipleが働く場所をたどる
- まとめ

## 3つの部品は、「順序」「能力」「判断」を分担している

冒頭で記述したように3つの部品は担当領域が異なります。**Playbookは「何を、どの順でやるか」といった仕事の進め方の型を、Skillは「この手順をどうやるか」といった能力を、Principleは「この一手を採るか。まだ終わりではないか」といった判断を**、それぞれ担当します。

3つの部品は、`/poteto-mode` の中で次のようにつながっています。

1. `/poteto-mode` が依頼の種類を見て、Playbookを1冊選ぶ（[`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) の節『[Playbooks](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#playbooks)』）
2. Playbookには、不具合なら「再現→原因→修正→確認」のように、その作業の手順と順番が書かれている
3. Playbookの各手順には、どこでどのSkillを使うかが書かれている。`/how`（現状把握）や `/arena`（複数案の比較）は、起動時ではなく、その手順に来たときに呼ばれる
4. Principleは、手順とは別の判断ルール。`/poteto-mode` の開始時には一覧（索引）だけを読み、今の作業が条件に該当したときに、そのPrincipleのファイルを全文読む（同ファイルの節『[Principles](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#principles)』）

3つの違いを表にまとめると、次のとおりです。

| 観点 | Playbook | Skill | Principle |
| --- | --- | --- | --- |
| 担うもの | 作業の順序 | 手順の中で使う能力 | 判断の基準 |
| 答える問い | 何を、どの順でやるか | この手順をどうやるか | この一手を採るか。まだ終わりではないか |
| 件数（0.15.15） | 23 | 27 | 24 |
| 置き場所 | `skills/poteto-mode/playbooks/*.md` | `skills/<名前>/SKILL.md` | `skills/principle-<名前>/SKILL.md` |
| 形式 | `/poteto-mode` の中の参照ファイル。Skillではない | 独立したSkill | 1原則1ファイルの短いSkill |
| 呼ばれ方 | `/poteto-mode` が依頼に合う1冊を選んで開く | Playbookの手順やNon-negotiablesの条件に該当したとき。`/how` のように直接も呼べる | 開始時に一覧を読み、条件に該当したら本文を読む |
| コードに触れるか | 手順として指示する | 調べる、書く、確かめるなどの作業をする | 触れない。判断だけをする |
| 例 | 『[**Bug fix**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)』、『[**Feature**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md)』 | `/how`、`/architect`、`/tdd` | 『[**Prove It Works**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md)』、『[**Fix Root Causes**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-fix-root-causes/SKILL.md)』 |

どの部品がいつ読み込まれるかは[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)で扱います。

## Playbookは、作業の種類ごとの手順と順番を決める

Playbookは、**作業の種類ごとに「何を、どの順でやるか」を書いた手順書**です。

`/poteto-mode` が依頼に合う1冊を選んで開くものです。

### 担うもの：手順と順番を、前置き・手順・報告の3部で書く

Playbookのファイルは、おおむね同じ形をしています。

1. **前置き**・・・ Playbook全体で守る基本ルールが書かれています。
2. **番号付きの手順**・・・ TODOリストに一字一句写される部分です。各手順の中に、どこでどのSkillを使うか、どのPrincipleに該当するかが書かれています。
3. **Reply行**・・・ 各Playbookの末尾にあり、作業後の返答に何を書くかを指定します。

!

**TODOリスト**・・・ エージェントが作業の始めに作る、その作業でやることの一覧（計画）です。Cursorでは、チャットの画面に表示されます。利用者は、この一覧を見て、エージェントがどの手順を進め、どの手順を飛ばしたか（`skip: <理由>`）を確かめられます（同梱ガイド [`01-setup.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md)）。

## Skillは、手順の中で呼び出す能力

Skillは、**特定の仕事をするための能力や手順のまとまり**です。

大半は手順を必要とするときに `/poteto-mode` が呼び、残りは利用者が直接呼びます。

### 担うもの：1つのSkillが1種類の仕事を担う

調査なら `/how` と `/why`、設計なら `/architect`、複数案の比較なら `/arena` というように、一つのSkillが一つの種類の仕事を担います。

例外は `/figure-it-out` です。どのPlaybookにも合わない作業のために、その作業専用のPlaybookを即興で作ります。  
個々のSkillの詳細は[第5部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2a4af5)（第22〜38章）で扱います。

### 呼ばれ方：大半は、Playbookが必要とするときに `/poteto-mode` が呼ぶ

**大半のSkillは、Playbookが必要とするときに `/poteto-mode` が代わりに呼びます**。

27件は、呼ばれ方で次のように分かれます。

| 呼ばれ方 | Skill |
| --- | --- |
| 手順や条件に応じて `/poteto-mode` が呼ぶ | `/how`、`/why`、`/architect`、`/arena`、`/swarm`、`/interrogate`、`/unslop`、`/no-comments`、`/technical-writing`、`/tdd`、`/figure-it-out`、`/show-me-your-work`、`/benchmark-checklist` |
| 利用者が呼ぶ | `/setup-pstack`、`/poteto-help`、`/recall`、`/teach`、`/bro`、`/blast-radius`、`/reflect`、`/correct`、`/automate-me`、`/make-bot-ui`、`/create-verification-skill`、`/maintain-verification-skill`、`/typescript-best-practices` |
| 入口 | `/poteto-mode` |

利用者が呼ぶSkillは、導入するとき（`/setup-pstack`）、作業を再開するとき（`/recall`）、長い作業が終わったあと（`/reflect`）のように、作業の節目で使うものが中心です。

### 利用者の使い方：各Skillは明示して呼び出せるし、Playbookから呼ばれない13件は利用者が呼ぶ

Skillは、Playbookと異なり単独で呼び出せます。調べものだけしたいときは、直接呼ぶほうが速いこともあります。

```
/how do we cancel runs? do we have an n+1 when we look up every run to cancel?
// 実行のキャンセルはどうやっている？キャンセルする実行を1件ずつ引くとき、n+1になっていない？
```

**利用者が呼ぶ13件は、Playbookの手順には組み込まれていません**。

## Principleは、手順や能力ではなく、作業途中の判断の基準

Principleは、手順でも能力でもなく、**作業の途中で下す判断の基準**です。

開始時には索引だけが読まれ、適用するときに本文が読まれます。

### 担うもの：作業途中の判断を下す基準

Principleは、**今の一手を採るかと、まだ完了ではないか**といった、**作業途中の判断を下す基準**を提供します。たとえば原則『[**Laziness Protocol**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-laziness-protocol/SKILL.md)』は、抽象やレイヤーを追加したくなったときに、削除と最小の変更を優先させます。原則『**Prove It Works**』は、完了を宣言する前に、本物の成果物で確かめたかを問いかけます。

Principleは1件ずつ独立したファイルになっていて、PlaybookやSkillから名前で参照されます。

Principle24件の詳細は[第4部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4b3166)（第17〜21章）で扱います。

## Non-negotiablesが、3つの部品をつなぐ

Non-negotiablesは、**「この状況なら、このSkill」という条件の一覧で、Playbookをまたいで共通の決まりをかけるつなぎ役**です。

Playbookは作業の種類ごとの流れを決めますが、どの作業にも共通してかかる決まりもあります。それを定めているのが、`/poteto-mode` の節『Non-negotiables』です。主な条件は次のとおりです。

| 条件 | 呼び出すもの |
| --- | --- |
| 自明でない変更、設計の判断 | `/how` |
| 関数の境界をまたぐコード | `/architect` |
| 文章を書くすべての場面（返答も含む） | `/unslop` |
| ドキュメント、PRの説明、コミットメッセージ | `/technical-writing` |
| コミットの前 | `/deslop`（`cursor-team-kit` プラグイン） |
| レビューの前 | `/no-comments` |
| UI、IDE、CLIの変更 | control系Skill（`cursor-team-kit` プラグイン） |
| 長い作業、席を外してあとで見る作業 | `/show-me-your-work` |

Non-negotiablesは、「作業の種類」ではなく「**作業の中で起きる状況**」**に反応します**。

『**Bug fix**』でも『**Feature**』でも、関数の境界をまたぐなら `/architect` が、コミットの前なら `/deslop` がかかります。

## 2つのサブエージェントは、作業を分担する相手

pstackのサブエージェントは、**`/poteto-mode` の流儀で作業する `poteto-agent` と、コメントを審査するComment Sickoの2つ**です。

### `poteto-agent` は、`/poteto-mode` の流儀で働くサブエージェント

`poteto-agent`（[`agents/poteto-agent.md`](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md)）は、`/poteto-mode` のルールを読んでから作業を始めるサブエージェントです。Playbookの手順の中でサブエージェントを起動するときは、原則としてこれを使います。新しい仕事を渡すときは、既存の `poteto-agent` を再開せず、新しい `poteto-agent` を起動するのが既定です（[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)）。

### Comment Sickoは、コメントを消し、直すべきコードを報告する役

Comment Sicko（[`agents/comment-sicko.md`](https://github.com/cursor/plugins/blob/main/pstack/agents/comment-sicko.md)）は、コードのコメントを審査して、残す理由のないコメントを自分で消すサブエージェントです。アプリのコードそのものは書き換えません。その代わりに、コメントがなくても意味が通るように形を直すべきコード（関数や変数など）を、報告の中で `MUST KILL` として挙げます。その報告を受けて、コードを直すのは `/no-comments` です。直接は呼ばず、`/no-comments` を通して使います。詳しくは[第32章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8960d3)で扱います。

### サブエージェントの仕事は、主エージェントが責任を持つ

**サブエージェントに任せても、責任は主エージェントに残ります**。

`/poteto-mode` は、サブエージェントの「終わりました」をそのまま利用者に渡さず、主エージェントが差分を見てから自分の言葉で報告するよう求めています。

[第2章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/27a183)で見た「信頼するのは、エージェントではなく成果物」という考えを、サブエージェントにも当てはめた規則です。

## SkillとPrincipleが働く場所をたどる

**Skillは再現、調査、設計、コミットといった「作業をする」場面に、Principleは再現の仕方、修正の形と大きさ、完了の判定、コミットの並べ方といった判断して何かを「決める」場面に現れます**。

本書の実例は、次の依頼です。

```
/poteto-mode the export writes duplicate rows when a retry lands mid-run. repro first, then fix and verify.
// 再試行が実行の途中に入ると、エクスポートが重複した行を書き出す。まず再現して、それから直して、確かめて。
```

この依頼は『**Bug fix**』Playbookに振り分けられ、TODOリストは、その6つの手順で始まります（手順6は『[**Opening a PR**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md)』を実行してPRを開く手順なので、下の表では省きます）。ここでは、各手順のどこでSkillが呼ばれ、どこでPrincipleが効くかをたどります。

次の表は、`playbooks/bug-fix.md` と、`/poteto-mode` のNon-negotiablesとPrinciple索引に書かれた条件を、この依頼に当てはめたものです。実際の作業でどのPrincipleが選ばれるかは、エージェントがその場で索引の条件を判定して決まります。

### 手順ごとに、呼ばれるSkillと効くPrincipleが決まる

| 『Bug fix』の手順 | 呼ばれるSkill | 条件に該当するPrinciple |
| --- | --- | --- |
| 開始時 | （`/poteto-mode` がPrinciple索引を読む） | 索引全体。この時点では本文は読まない |
| 1. 同じ操作面で自分で再現する | 対応するcontrol系Skill、または検証スキル | 『**Fix Root Causes**』（まず再現する） |
| 2. 原因を二分探索する | `/how`（対象サブシステム）、`/why`（退行の履歴） | 『**Fix Root Causes**』、『[**Guard the Context Window**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-guard-the-context-window/SKILL.md)』 |
| 3. 修正を計画する | 関数の境界をまたぐなら `/architect`。実装はサブエージェントへ | 『[**Model the Domain**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md)』、『[**Make Operations Idempotent**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-make-operations-idempotent/SKILL.md)』、『**Laziness Protocol**』 |
| 4. 同じ操作面で確かめる | 「不具合を再現する手順（手順1）」と同じcontrol系Skill、または検証スキル | 『**Prove It Works**』 |
| 5. 失敗する再現を修正より先にコミットする | 安いローカルテストがあれば `/tdd` | 『[**Sequence Work into Verifiable Units**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-sequence-verifiable-units/SKILL.md)』、『[**Test Behavior, Not Implementation**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-test-behavior-not-implementation/SKILL.md)』 |
| 返答 | `/unslop`（節『Writing the reply』） | 判断を変えたPrincipleを名前で挙げる |

各手順の詳細は[第11章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6fcb42)で、原則が効く場面は[第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b)から[第20章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/c155cc)で扱います。

### 条件に該当しないSkillは呼ばれない

たとえば `/show-me-your-work` は、長い作業や席を外す作業で判断の記録を残すSkillです。今回の依頼は席を外すとは書いていないので、条件に該当しません。長い作業や席を外す作業であれば条件に該当しますが、その場合は、[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)で見た規則により `/figure-it-out` へ回る可能性もあります。

同じ『**Bug fix**』でも、依頼の内容と途中で起きる状況によって、呼ばれるSkillと効くPrincipleは変わります。条件に該当したものだけを読むこの設計が、次の[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)の主題です。

## まとめ

- **3つの部品の違い**・・・ Playbookは作業の順序を、Skillは手順の中で使う能力を、Principleは今の一手を採るか、まだ完了ではないかの判断を担います。
- **Playbook**・・・ 前置き、手順、Reply行の3部でできています。
- **Skill**・・・ 1つのSkillが1種類の仕事を担います。大半は `/poteto-mode` が手順に応じて呼び、利用者が呼ぶ13件は、Playbookの手順には組み込まれていません。
- **Principle**・・・ 手順や能力ではなく、今の一手と完了かどうか、といった判断基準を定義します。詳細は[第4部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4b3166)で扱います。
- **Non-negotiables**・・・ 作業の中で起きる状況に反応して、PlaybookをまたいでSkillを呼ぶつなぎ役です。
- **サブエージェント**・・・ `poteto-agent` は `/poteto-mode` の流儀で働くサブエージェント、Comment Sickoはコメントを消し、直すべきコードを報告する役です。任せた仕事の責任は主エージェントに残ります。
- **実例の依頼**・・・ 『**Bug fix**』の手順ごとに、再現と調査にcontrol系Skillと `/how`・`/why`、修正に `/architect`、コミットに `/tdd` が呼ばれ、『**Fix Root Causes**』や『**Prove It Works**』などの原則が判断に効きます。

次の[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)では、これらの部品がいつ読み込まれるかを扱います。必要なものを必要なときだけ読む仕組みと、その元にある考え方、利点と弱点を解説します。
