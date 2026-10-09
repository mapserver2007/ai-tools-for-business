---
title: "第13章 Skillを作り、評価する"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:28+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 17
---

# 第13章 Skillを作り、評価する

この章では、次の2つのPlaybookを扱います。

1. [Authoring or modifying a skill](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md)
2. [Eval](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md)

2つとも、アプリのコードではなく、**エージェントの働き方を決めるSkillについて扱います**。

『Authoring or modifying a skill』は、Skill（`SKILL.md`）を書くときや直すときに、『Eval』は、そのSkillの変更に効果があったかを測定するときに使います。

この章では、2つの分担と、それぞれの使い方を順に解説します。

## この章の構成

この章の構成は次のとおりです。

- 2つのPlaybookは、Skillを書く手順と効果を測る手順を分担する
- 『Authoring or modifying a skill』は、決められた手順でSkillを書き、作業中の判断を変える指示だけ残す
- 『Eval』は、評価だと気づかせずに、変更がエージェントの行動に与える効果を測る
- まとめ

## 2つのPlaybookは、Skillを書く手順と効果を測る手順を分担する

同梱ガイドの「Make it yours」のページ（[`docs/guide/09-make-it-yours.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/09-make-it-yours.md)）は、Skillについて2つのことを求めています。

- **エージェント向けの文章は、人間向けより基準を高くする**・・・ 役に立たない一文も、将来どこかのエージェントが従う指示になるからです。
- **Skillの編集は、実験としてテストする**・・・ Skillの編集は、将来のすべてのセッションに影響するからです。

書くほうが『**Authoring or modifying a skill**』、効果を測定するほうが『**Eval**』です。

Authoring or modifying a skillの手順には、複数のエージェントを使う指示はありません。  
一方、Evalでの作業に必要なものは次の3つです。

- **候補**・・・ 変更を入れた環境で作業するエージェントです。
- **審査員**・・・ 候補の出力を採点する、候補とは別のエージェントです。
- **手がかりを取り除いた作業環境**・・・ 評価だと気づかれる手がかり（ディレクトリ名やファイル名など）を取り除いた作業環境です。

## 『Authoring or modifying a skill』は、決められた手順でSkillを書き、作業中の判断を変える指示だけ残す

『**Authoring or modifying a skill**』は、**`SKILL.md` を新しく書く、または直すとき**に通すPlaybookです。

同梱ガイドは、`SKILL.md` を自由に書き下ろすことをよくある失敗に挙げ、このPlaybookを通せば検証とレビューが行われる、としています。

### 4つの手順

手順は次のとおりです。

1. create-skill を使う
2. Skillを検証する
3. Skillの構造を変えるならテストケースを用意する
4. 『[Opening a PR](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md)』でPRを作成（[第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e)）

ここからは、各手順を1つずつ見ていきます。

!

- **frontmatter**・・・ Markdownファイルの先頭に `---` で囲んで書く、名前や説明などのメタデータ

#### 1. create-skill を使う

Cursorに組み込まれている、`SKILL.md` を書くためのSkill。

#### 2. Skillを検証する

frontmatterに `name` と `description` があること、参照先のファイルが存在すること、他のSkillへのリンクが解決することを確かめる。

手順2で確かめるのは、機械的に合否が出るものだけです。**Skillの変更がエージェントの行動を変えるかを確かめるのは、『Eval』の役目**です。

#### 3. Skillの構造を変えるならテストケースを用意する

文調のような主観的な変更なら省略。

#### 4. 『[Opening a PR](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md)』でPRを作成（[第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e)）

### 要点は「迷ったら削る」という文章の規律

このPlaybookの要点は、手順の後に置かれた**文章の規律**です。

> When in doubt, delete. Keep only prose that changes a decision.
>
> 迷ったら削る。判断を変える文章だけを残す。

Skillを書くエージェントは、一文ごとに「この文でエージェントのどの判断が変わるか」を問い、答えられない文は消します。

主な規律は次のとおりです。

- **理由の説明を省略する**・・・ 指示は「何をするか」を中心に書き、理由がないと指示の意味や適用条件が分からない場合に限定して、理由を説明します。
- **中身を写さず、情報源を指し示す**・・・ 型、README、設定ファイルのような、コードベースに実在する情報源を示します（原則『[**Encode Lessons in Structure**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)』、[第21章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dd2d9f)）。
- **他のSkillに委ねる**・・・ 他のSkillの中身は書き写さず、そのSkillのパスを示して任せます。
- **繰り返す作業をSkillにする**・・・ 何度も同じ作業をしているなら、新しいSkillを提案します。

エージェントが作業の途中で壊れたSkillに気づいたら、作業は止めず、黙認して回避することもせず、**そのSkillだけ修正し、PRを出します**。

機能開発のPRに混ざったSkillの編集は、レビューで気づかれにくく、『Eval』で効果を測ることもできないためです。

### 検証スキルや自分用のSkillには、専用の入口がある

目的によっては、このPlaybookではなく専用の入口を使います。

| 入口 | どんなときに使うか | 詳しい章 |
| --- | --- | --- |
| `/create-verification-skill` | アプリの挙動を確かめるSkillを新しく作りたい | [第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca) |
| `/maintain-verification-skill` | 検証スキルに書かれた手順が、アプリの今の挙動と合わなくなった | [第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca) |
| `/automate-me` | 自分の作業の進め方を、過去のセッションの記録からSkillにまとめたい | [第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f) |
| `/reflect` | セッションから学んだことを既存Skillに残したい | [第34章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f70847) |

### 依頼の書き方：作りたいSkillを普通の言葉で書く

依頼は普通の言葉で足ります。

```
/poteto-mode write a skill for verifying database migrations in this repo
// このリポジトリのデータベースマイグレーションを検証するSkillを書いて。
```

## 『Eval』は、評価だと気づかせずに、変更がエージェントの行動に与える効果を測る

『**Eval**』は、Skill、構造、プロンプトの変更がエージェントの行動にどう影響するかを、**採用する前にテストする**Playbookです。

『Eval』を実行するエージェントは、実験を設計し、結果をまとめる役を担います。ここでいう実験とは、変更したSkillを別のエージェントに実際の作業で使わせ、その仕事ぶりを採点することです。

実験では、課題を解くエージェントを複数体起動します。このエージェントを**候補**と呼びます。

- **候補ごとに作業用のディレクトリを分ける**・・・ 各ディレクトリには、変更したSkillと、プロジェクトの骨組みを置いておきます。候補どうしが互いの作業に影響しないようにするためです。
- **候補ごとに別のモデルを使う**・・・ たとえば、1体目はOpus、2体目はGrokで動かします。モデルにはそれぞれ偏りがあり、1つのモデルだけで試すと、その偏りが結果に混ざるからです。
- **全員に同じ依頼を与える**・・・ 依頼が異なると、結果の違いが変更によるものか、依頼によるものか分からなくなるからです。

候補の作業が終わったら、候補とは別のモデルで動く**審査員**が、どの候補の出力かを知らない状態で採点します。

変更前と変更後の2つの版を比べることもできます。その場合は、1体の審査員が、どちらの版の出力かを知らないまま、両方を同じ基準で一度に採点します。

!

- **盲検**・・・ 評価の対象に、評価されていることや比べている条件を知らせずに行う試験のやり方

### 7つの手順

1. **実験の枠組みを決める**・・・ テストする変更と、成功とみなす行動を書く。審査員用の採点基準（ルーブリック）を3〜6項目で作り、候補には見せない
2. **評価の手がかりを取り除いた環境を用意する**・・・ 候補ごとに作業ディレクトリを用意し、テストする変更を入れておく。プロジェクトの骨組みや、候補が自然に読むSkillなど、本物のタスクならあるはずのコンテキストも置く
3. **自然なプロンプトを一つ書く**・・・ 利用者が与えそうな依頼にし、何を測っているかを漏らさない
4. **N体の候補を並列に起動する**・・・ [`/arena`](https://github.com/cursor/plugins/blob/main/pstack/skills/arena/SKILL.md) の手順に従い、候補ごとに異なるモデルを使う
5. **盲検の審査員を1体起動する**・・・ 候補とは別のモデルファミリーを使い、モデル名は見せない
6. **指示をたどったかは、自己申告ではなく記録から確かめる**・・・ 候補がSkillから指し示されたファイルを順にたどって従ったかは、会話の記録で実際に開いたファイルとコードの形から採点する
7. **実験を設計したエージェントが、すべての出力を自分で読む**・・・ 審査員の判定と比べ、食い違いはモデルの偏りかルーブリックのあいまいさの表れとみて、結論をまとめる

!

- **モデルファミリー**・・・ 同じ開発元が同じ系列として出している、一群のモデル（例：OpenAIのGPT系、xAIのGrok系など）

### 要点は、手順より先に置かれた盲検化のルール

同梱ガイドによれば、このPlaybookは、「評価されていると知ったエージェントの振る舞いが変わる」という失敗を中心に作られています。この失敗を**観察者効果**と呼びます。

盲検化のルールは、情報が漏れる経路ごとに3つに分けられます。

- **候補が目にする文字列**・・・ `eval`、`test`、`judge` などの語を、ディレクトリ名、ファイル名、プロンプトに入れません。名前は利用者が付けそうなものにし、プロンプトは普通の依頼に見せます。
- **候補が答える内容**・・・ どのSkillやファイルを使ったかを列挙させず、他の候補がいることも伝えません。
- **審査員が目にする情報**・・・ 出力には、どのモデルのものか分からないラベルを付けて見せ、モデル名は伏せます。2つの版を比べるときは、1体の審査員が両方を1回で、同じ尺度で採点します。

### 依頼の書き方：両方の版に同じタスクを与え、候補を盲検のままにするよう書く

同梱ガイドの依頼例は、変更前と変更後の2つの版を比べる使い方で、両方の版に同じタスクを与えることと、候補を盲検のままにすることを伝えています。

```
/poteto-mode run the eval playbook on this skill change. same task for both variants, candidates stay blind.
// このSkillの変更に Eval Playbook を実行して。両方の版に同じタスクを与えて。候補は盲検のままにして。
```

## まとめ

- **2つのPlaybookの分担**・・・ Skillを作成・編集する『**Authoring or modifying a skill**』と、効果を測る『**Eval**』です。
- **Authoring or modifying a skill**・・・ `create-skill` で書き、機械的に検証してPRにします。要点は「迷ったら削る。判断を変える文章だけを残す」です。壊れたSkillは、そのSkillの修正だけを含む独立したPRで直します。
- **Eval**・・・ 変更を採用する前に、行動への効果を確かめます。候補は評価されていると知らず、審査員はモデル名を知りません。採点は候補の自己申告ではなく、実際に開いたファイルを示す会話の記録から行います。

次の[第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e)では、PRを作る『**Opening a PR**』、PRをマージできる状態まで運ぶ『[**Babysit**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/babysit.md)』、検証済みのものだけを本流のブランチ（trunk）へ取り込む『[**Shipping**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/shipping.md)』を見ていきます。
