---
title: "第23章 依頼に合うPlaybookが存在しない作業のPlaybookを設計する"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/3ce2b2"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:32+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 29
---

# 第23章 依頼に合うPlaybookが存在しない作業のPlaybookを設計する

この章では、[`/figure-it-out`](https://github.com/cursor/plugins/blob/main/pstack/skills/figure-it-out/SKILL.md) を扱います。

`/figure-it-out` は、合うPlaybookがない作業のために、終了条件と検証の仕組みを先に決め、判断の記録を残しながら進める手順を設計するSkillです。

`/figure-it-out` の `SKILL.md` は、エージェントが会話の内容から自分で選んで動かすことを止める設定（`disable-model-invocation: true`）を持っています。このSkillを呼ぶのは、利用者か、合うPlaybookがない作業や大きな作業をこのSkillへ回す `/poteto-mode` です（[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)）。

この章では、`/figure-it-out` を、使いどき、手順、出力の3つの観点で解説します。最後に、よく似たPlaybookとの使い分けをまとめます。

## この章の構成

この章の構成は次のとおりです。

- 使いどき：大きな移行や、席を外して任せる作業
- 手順：Frame から Verify まで、5つの Phase で進む
- 出力：設計したPlaybookと判断の記録のパスを返す
- 依頼の例：席を外している間の作業は、/poteto-mode が /figure-it-out に回す
- /figure-it-out はその作業1回分の進め方を設計し、『Orchestrate』は計画全体を運営する
- まとめ

`/figure-it-out` は、どのPlaybookにも該当しない作業のために、**Playbookそのものを設計するSkill**です。コードを書く前に作業の流れ（どの順に、何を確かめながら進めるか）を設計し、席を外していた人が、戻ってからエージェントの判断を1つずつ確かめられる記録を残します。

## 使いどき：大きな移行や、席を外して任せる作業

利用者が、多くの呼び出し元にまたがる移行や、席を外している間にエージェントに進めてもらい、戻ってから結果を信頼したい作業を任せるときです。

`/poteto-mode` がこうした作業をここへ回す仕組みは[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)で扱いました。

## 手順：Frame から Verify まで、5つの Phase で進む

`/figure-it-out` は、作業を5つの段階（Phase）に分けて進めます。

段階を分けるのは、終了条件を先に決め、確かめる仕組みを作り、判断を記録しながら進めることで、利用者が戻ってきたときに作業を信頼できるようにするためです。

| Phase | 内容 |
| --- | --- |
| A: Frame（枠組みを決める） | 終了条件、作業の範囲、厳密さの水準（作業をどこまで厳密に確かめるか）の3つを決める。終了条件は、成り立つかどうかを確かめられる条件（例：「同期ストアを呼ぶ箇所が0件になっている」）として書く。作業の範囲は、作業単位のおおよその数と手間、調査で見つかった障害を数で示す。厳密さの水準は高めに寄せ、後戻りできない判断ほど高くする |
| B: Design the workflow（手順を設計する） | 作業を単位に分けて順番を決め、作業より先に検証の仕組みを作る。単位は、ほかの単位のマージを待たずにそれ1つだけでマージしても、ビルドとテストが通り、アプリが動く変更にし（例：同期ストアの呼び出し元を、パッケージごとに1本のPRで非同期ストアへ移す。1本だけマージしても、まだ移していない呼び出し元は同期ストアのまま動く）、うまくいくかが最も分からない単位から先に並べる。検証の仕組みを作るときは、変更前の値も記録しておく（例：同期ストアを呼ぶ箇所を数えるスクリプトを先に作り、変更前の件数を記録する）。確認を「変更前の値と変更後の値」の比較にするため |
| C: Run the loop（実験を繰り返す） | 各単位を実験として扱い、終了条件に照らして、実際の成果物（例：テストの実行結果、箇所を数えるスクリプトの出力）で測定する。判定は VERIFIED（確かめられた）、NOT VERIFIED（確かめられなかった）、INCONCLUSIVE（どちらとも言えない）の3つで、INCONCLUSIVE は合格ではない |
| D: Keep the audit trail（判断の記録を残す） | `/show-me-your-work`（[第29章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/724887)）で判断の記録を残す。人が戻ってきたとき、記録と差分があれば、作業を信頼できるかを判断できる |
| E: Verify and hand back（確かめて引き渡す） | 実際のプロダクトで全体を確かめ、繰り返し起きた訂正は lint（コードの書き方を自動で検査する道具）やスクリプトに残す。同じ訂正を文章で繰り返さず、機械に守らせるため（原則『[**Encode Lessons in Structure**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)』、[第21章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dd2d9f)） |

Phase C では、エージェントは、1つの単位ごとに次の実験を繰り返します。

1つの単位を確かめてから次の単位に進むので、確認を最後にまとめて行う場合と異なり、どの単位で失敗したかがすぐに分かります。

このループで単位を確かめるとき、エージェントが見るのは、Workers（作業を任されたエージェント）の自己申告ではなく、成果物そのものです（[第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019)）。たとえば、Worker の「テストは通りました」という報告ではなく、テストを実行した結果そのものを見ます。

同じ考えから、Phase A で決める厳密さの水準も、「念入りに見る」という心がけではなく、**通すべき確認と残すべき成果物で決まります**。厳密さを上げるときは、通らなければ次の単位に進めない確認を増やし、検証の結果や判断の記録のような成果物を多く残します。

## 出力：設計したPlaybookと判断の記録のパスを返す

返答に含めるものは次のとおりです。

- 設計したPlaybook
- 厳密さの水準とその理由
- 判断の記録のパス
- Phase A の終了条件に照らして確かめたこと
- 未解決のこと

## 依頼の例：席を外している間の作業は、/poteto-mode が /figure-it-out に回す

[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)の例は、`/poteto-mode` 経由で `/figure-it-out` に回る依頼です。

```
/poteto-mode i'm stepping away. migrate every caller from the synchronous store
to the new async one, keeping behavior identical. i want to trust it was done
right when i'm back.
// 席を外す。同期ストアの呼び出し元をすべて新しい非同期ストアへ移して。
// 振る舞いは同一に保って。戻ったときに、正しくできたと信頼できるようにして。
```

## /figure-it-out はその作業1回分の進め方を設計し、『Orchestrate』は計画全体を運営する

`/figure-it-out` はその作業1回分の進め方を設計し、『[**Orchestrate**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md)』は複数日の計画全体を運営します。『[**Autonomous run**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autonomous-run.md)』（終了条件を先に決めて、1つのタスクを止まらずに進める）を含めた比較は[第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5)にあります。

## まとめ

- **`/figure-it-out`**・・・ 合うPlaybookがない大きな作業のために、確かめられる終了条件と検証の仕組みを先に作り、単位ごとに確かめて判断の記録を残す手順を設計します。
- **使い分け**・・・ `/figure-it-out` はその作業1回分の進め方を設計し、『**Orchestrate**』は複数日の計画全体を運営します。

次の[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)では、複数のエージェントを並列に動かし、設計と成果物を比べる3つのSkillを扱います。見ていくのは、[`/architect`](https://github.com/cursor/plugins/blob/main/pstack/skills/architect/SKILL.md)、[`/arena`](https://github.com/cursor/plugins/blob/main/pstack/skills/arena/SKILL.md)、[`/swarm`](https://github.com/cursor/plugins/blob/main/pstack/skills/swarm/SKILL.md)です。
