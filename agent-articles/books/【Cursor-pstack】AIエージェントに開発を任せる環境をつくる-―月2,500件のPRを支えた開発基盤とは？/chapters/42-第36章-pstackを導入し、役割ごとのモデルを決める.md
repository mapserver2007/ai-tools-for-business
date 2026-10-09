---
title: "第36章 pstackを導入し、役割ごとのモデルを決める"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:35+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 42
---

# 第36章 pstackを導入し、役割ごとのモデルを決める

この章では、[`/setup-pstack`](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md) を扱います。

`/setup-pstack` は、pstackが起動するサブエージェントの**役割ごとに、使うモデルを決めるSkill**です。利用者は、pstackのプラグインを入れたら、最初にこのSkillを実行します。

ここでの役割とは、`bug-fix`（『Bug fix』Playbookでコードを書くサブエージェント）、`judgment and prose`（文章と判断を受け持つサブエージェント）、`arena runners`（`/arena` が同じ課題を解かせる候補のサブエージェント）のような、サブエージェントが受け持つ役割のことです。

この章では、pstackの導入方法と、`/setup-pstack` の進め方、`/setup-pstack` が書き出すルールファイルを解説します。

!

この章でpstackの導入方法も扱うのは、導入が、`/setup-pstack` と同じく、pstackを使い始めるときに最初に行うことだからです。

pstackに入っているSkillと、別のプラグインとして入れる必要があるSkillは、[『第6章 手順が名前で頼る一部のSkillは、同梱されていない』](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/33f073#%E6%89%8B%E9%A0%86%E3%81%8C%E5%90%8D%E5%89%8D%E3%81%A7%E9%A0%BC%E3%82%8B%E4%B8%80%E9%83%A8%E3%81%AEskill%E3%81%AF%E3%80%81%E5%90%8C%E6%A2%B1%E3%81%95%E3%82%8C%E3%81%A6%E3%81%84%E3%81%AA%E3%81%84)で扱いました。

## この章の構成

この章の構成は次のとおりです。

- pstackを導入する
- 役割の一覧
- 全体の流れ
- 使えるモデルを検出する
- 前回のルールファイルを読む
- 推論の予算を選ぶ
- inherit-parent と auto
- 書き出す前に、使えるモデルかを確かめる
- パネルの役割
- 書き出すファイル
- 再実行したときに残る行
- 検証スキルの作成の提案
- まとめ

## pstackを導入する

pstackの導入は、コマンド1つと短い会話で終わります。

1. Cursor のチャットで、次のコマンドを実行します。

   ```
   /add-plugin pstack
   ```
2. 続けて、次のコマンドで `/setup-pstack` を実行し、`/setup-pstack` の質問に答えます。何を聞かれ、何が決まるかは、この章の次の節から解説します。

   ```
   /setup-pstack
   ```
3. `/setup-pstack` が終わったら、新しいチャットを始めます。**`/setup-pstack` が書き出すモデルのルールは、新しいチャットから適用される**からです。

## 役割の一覧

`/setup-pstack` がモデルを決める役割は、次の17個です（pstack version `0.15.15` 時点）。役割の名前は、ルールファイルに書かれる原文の名前です。

| 役割 | 受け持つサブエージェント | 既定のモデル |
| --- | --- | --- |
| `feature, refactoring` | 『Feature』『Refactoring』Playbookで、コードを書く | `grok-4.7-xhigh-fast` |
| `bug-fix` | 『Bug fix』Playbookで、コードを書く | `grok-4.7-xhigh-fast` |
| `perf-issue` | 『Perf issue』Playbookで、コードを書く | `grok-4.7-xhigh-fast` |
| `hillclimb` | 『Hillclimb』Playbookで、コードを書く | `grok-4.7-xhigh-fast` |
| `judgment and prose` | 文章を書き、判断する | `claude-opus-5-5-xhigh` |
| `hardest tasks` | 最も難しい変更（複数の箇所にまたがる設計、込み入った並行処理、細かな誤りに気づきにくいアルゴリズム）のコードを書く | `claude-opus-5-5-xhigh` |
| `how explorer` | `/how` で、コードを手分けして調べる | `grok-4.7-xhigh-fast` |
| `how explainer` | `/how` で、調べた結果を1つの説明にまとめる | `claude-opus-5-5-xhigh` |
| `why investigators` | `/why` で、Gitの履歴やチケットなどの情報源を手分けして調べる | `grok-4.7-xhigh-fast` |
| `why synthesizer` | `/why` で、調べた結果を1つの答えにまとめる | `claude-opus-5-5-xhigh` |
| `reflect tooling` | `/reflect` で、道具の視点から会話を読む | `grok-4.7-xhigh-fast` |
| `reflect judgment, divergent, synthesizer` | `/reflect` で、判断と発散の視点から会話を読み、結果を仕分ける | `claude-opus-5-5-xhigh` |
| `arena runners` | `/arena` で、同じ課題を解く候補 | `claude-opus-5-5-xhigh`、`grok-4.7-xhigh-fast` |
| `arena cross-judge pool` | `/arena` で、候補の成果物を採点する判定役（この中から1つを選ぶ） | `claude-opus-5-5-xhigh`、`grok-4.7-xhigh-fast` |
| `swarm workers` | `/swarm` で、並列に動くWorker | `grok-4.7-xhigh-fast` |
| `architect runners` | `/architect` で、設計案を作る | `claude-opus-5-5-xhigh`、`grok-4.7-xhigh-fast` |
| `interrogate reviewers` | `/interrogate` で、差分の弱点を探す | `claude-opus-5-5-xhigh`、`grok-4.7-xhigh-fast` |

既定のモデルが2つ並んでいる役割では、値にモデルのリストを書きます。この章の後の節で、1つずつ説明します。

## 全体の流れ

`/setup-pstack` は、推論の予算と役割ごとのモデルを尋ね、その答えを `~/.cursor/rules/pstack-models.mdc` という**常に適用されるルールに書き出すSkill**です。

!

- **推論の予算**・・・ 原文では budget。役割のモデルの推論の強さを、一度に決める設定
- **スラッグ**・・・ `claude-opus-5-5-xhigh` のような、モデルを指定する識別子
  - 例：`claude-opus-5-5-xhigh` は、Claude Opus 5.5 をEffort Level `xhigh` で動かす指定
- **推論の強さ（Effort Level）**・・・ モデルが推論にかける手間の段階。スラッグの中の `max`、`xhigh`、`high`、`medium`、`low` の語で表し、左ほど強い

pstack の各Skillは、このルールを読んで、役割ごとのモデルを決めます。

行がない役割は、そのSkillの既定のモデルで動きます。

そのため、利用者が変えるのは、既定のモデルから変えたい役割だけで済みます。たとえば、`bug-fix` の役割だけを別のモデルで動かしたいなら、`bug-fix` の行だけを変えます。

また、ある役割を既定のモデルに戻したいときは、ルールファイルからその役割の行を消します。

`/setup-pstack` は、次の順に進みます。

## 使えるモデルを検出する

最初に、`/setup-pstack` は、利用者が使えるモデルのスラッグを調べます。調べ方は、次のとおりです。

- **基本の調べ方**・・・ 今のチャットで、サブエージェントに渡せるスラッグを調べます。原文は、これを確実な方法としています。
- **APIやCLIがある場合**・・・ Cursor が、利用者の使えるモデルを一覧にするAPIやCLIを用意していれば、漏れがないよう、そちらを優先します。
- **何も見つからない場合**・・・ 利用者に、自分が使えるスラッグをチャットに貼ってもらうよう頼みます。

ここで見つかったスラッグを、この章では「使えるモデル」と呼びます。

## 前回のルールファイルを読む

過去に、`/setup-pstack` を実行していれば、そのとき書き出したルールファイル（`~/.cursor/rules/pstack-models.mdc`）がすでにあります。その場合、`/setup-pstack` は、そのファイルの `# budget` の行（前回選んだ予算）と各役割の値を読み、今回の選び直しの出発点にします。

ただし、前回のルールファイルには、すでに廃止された役割の行（たとえば `how critics` の行）が残っていることがあります。廃止された役割とは、今の pstack が書き出すファイルに並んでいない役割です（書き出すファイルの中身は、この章の[『書き出すファイル』](#%E6%9B%B8%E3%81%8D%E5%87%BA%E3%81%99%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB)で示します）。

`/setup-pstack` は、こうした行を捨てます。どの行を捨てたかは、`/setup-pstack` が、役割とモデルの一覧を示すときに利用者に伝えます。

## 推論の予算を選ぶ

推論の予算は、**すべての役割のモデルを、どのEffort Levelで動かすか**を一度に決める設定です。スラッグの中の `max`、`xhigh`、`high`、`medium`、`low` の語で表します。`max` が最も強く、`low` が最も弱い段階です。

利用者は、予算を次の4つから選びます。  
予算ごとに、そろえるEffort Levelが決まっています。

| 予算 | そろえるEffort Level | `claude-opus-5-5-xhigh` は、どう変わるか |
| --- | --- | --- |
| unlimited | `max` にそろえる | `claude-opus-5-5-max` |
| large | `xhigh` にそろえる | `claude-opus-5-5-xhigh` |
| medium | `high` にそろえる | `claude-opus-5-5-high` |
| small | `medium` にそろえる | `claude-opus-5-5-medium` |

既定のモデルは、どれも `large` と同じ `xhigh` で動きます。予算を尋ねる際、`/setup-pstack` は、前回のルールファイルに予算が記録されていれば、その予算を、今の予算として利用者に示します。前回のルールファイルがなければ、`large` が既定のモデルと同じであることを利用者に伝えます。

### スラッグのEffort Levelを、予算のEffort Levelに置き換える

`unlimited`、`large`、`medium`、`small` のどれを選んでも、`/setup-pstack` は、すべての役割のスラッグについて、Effort Levelの語だけを、予算のEffort Levelに置き換えます。Effort Levelの語は、スラッグの末尾にあります。末尾が `fast` なら、その直前です。

たとえば、`small`（予算のEffort Levelは `medium`）を選ぶと、次のように変わります。

- `claude-opus-5-5-xhigh` → `claude-opus-5-5-medium`
- `grok-4.7-xhigh-fast` → `grok-4.7-medium-fast`

`unlimited`（予算のEffort Levelは `max`）を選ぶと、`claude-opus-5-5-xhigh` は `claude-opus-5-5-max` に変わります。一方、Grok のスラッグには `xhigh` より強い段階がないので、置き換えた後の `grok-4.7-max-fast` は、使えるモデルの中にありません。そのため、`/setup-pstack` は、この章の[『置き換えたモデルが使えないときは、同じ系統の中で代わりを選ぶ』](#%E7%BD%AE%E3%81%8D%E6%8F%9B%E3%81%88%E3%81%9F%E3%83%A2%E3%83%87%E3%83%AB%E3%81%8C%E4%BD%BF%E3%81%88%E3%81%AA%E3%81%84%E3%81%A8%E3%81%8D%E3%81%AF%E3%80%81%E5%90%8C%E3%81%98%E7%B3%BB%E7%B5%B1%E3%81%AE%E4%B8%AD%E3%81%A7%E4%BB%A3%E3%82%8F%E3%82%8A%E3%82%92%E9%81%B8%E3%81%B6)で説明する仕組みに従い、`grok-4.7-xhigh-fast` をそのまま使います。

`arena runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast` のように、1つの役割に複数のモデルを並べた行では、並んだスラッグをすべて置き換えます。こうした役割は、この章の[『パネルの役割』](#%E3%83%91%E3%83%8D%E3%83%AB%E3%81%AE%E5%BD%B9%E5%89%B2)で説明します。

`inherit-parent` と `auto` はスラッグではないので、置き換えません。

### 置き換えたモデルが使えないときは、同じ系統の中で代わりを選ぶ

置き換えた後のスラッグが、検出でき、かつ使用可能なモデルの中にないこともあります。たとえば、`claude-opus-5-5-medium` が使えないことがあります。

その場合、`/setup-pstack` は、次の順に代わりのモデルを決めます。

1. 同じ系統（原文では family）の、使えるモデルを探す
2. そのうち、予算のEffort Levelと同じか、それより弱いものの中で、最も強いものを使う
3. 1つも見つからなければ、その役割を、利用者が選び直す役割として示す

たとえば、`small`（予算のEffort Levelは `medium`）を選び、使える Claude のモデルが `claude-opus-5-5-high` と `claude-opus-5-5-low` だけだったとします。

- `high` は、目標の `medium` より強いので、使いません。
- `low` は、目標の `medium` より弱いので、使えます。

そのため、`/setup-pstack` は `claude-opus-5-5-low` を使います。

このように、代わりのモデルは同じ系統の中からしか選ばないので、**予算を変えても、モデルの系統は変わりません**。たとえば、Claude で動いていた役割が、予算を変えたことで Grok に変わることはありません。

### 最後に、役割とモデルの一覧を確かめる

置き換えが終わると、`/setup-pstack` は、すべての役割と、それぞれに割り当てたモデルの一覧を見せます。選び直す必要がある役割には、その印が付いています。

利用者は、そのまま受け入れるか、特定の役割のモデルを変えるかを選びます。モデルを変えるときは、使えるモデル、`inherit-parent`、`auto` のどれかを選びます。

## inherit-parent と auto

`inherit-parent` と `auto` は、どちらも、**その役割のサブエージェントを、親のチャットと同じモデルで動かす指定**です。親のチャットとは、サブエージェントを起動した元のチャットです。

この2つを書いた役割では、各Skillは、サブエージェントを起動するときにモデルを指定しません。モデルを指定されなかったサブエージェントは、親のチャットと同じモデルで動きます。

そのため、Auto（Cursor がモデルを自動で選ぶ設定）でチャットを使っている利用者は、役割に `inherit-parent` か `auto` を書けば、サブエージェントも Auto で動かせます。

## 書き出す前に、使えるモデルかを確かめる

利用者が一覧を確かめ終えると、`/setup-pstack` は、ルールファイルを書き出す前に、書き出すスラッグが、この章の[『使えるモデルを検出する』](#%E4%BD%BF%E3%81%88%E3%82%8B%E3%83%A2%E3%83%87%E3%83%AB%E3%82%92%E6%A4%9C%E5%87%BA%E3%81%99%E3%82%8B)で検出した使えるモデルに含まれているかを確かめます。

含まれていないスラッグが1つでもあれば、`/setup-pstack` は書き出さずに止まり、利用者にその役割のモデルを選び直してもらいます。**`/setup-pstack` は、使えると確認していないスラッグを、ルールファイルに書きません**。

この確認があるのは、ルールファイルに書いたスラッグが、サブエージェントを起動するときに、そのままモデルの指定として渡されるからです。

`inherit-parent` と `auto` は、モデルのスラッグではないので、この確認の対象になりません。いつでもルールファイルに書けます。

## パネルの役割

どのフロンティアモデル（各社の最先端のモデル）にも強みと弱みがあります。そこで、pstackの多くのSkillは、複数のモデルを組み合わせて、それぞれのモデルの強みを活かします（[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)）。

そのために複数のモデルを並べる役割を、`/setup-pstack` は、パネルの役割（原文では panel roles）と呼びます。パネルとは、同じ問いを複数のモデルに解かせて比べる仕組みです（[第6章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/33f073)）。

パネルの役割は、次の3つです。

- **`arena runners`**・・・ `/arena` が、同じ課題を解かせる候補のサブエージェント
- **`architect runners`**・・・ `/architect` が、コードを書く前に設計案を作らせるサブエージェント
- **`interrogate reviewers`**・・・ `/interrogate` が、差分の弱点を探させるレビュアーのサブエージェント

### 並べたモデルの数だけ、サブエージェントが起動する

パネルの役割の値には、モデルを `,` で区切って並べます。**並べたモデルの数だけ、サブエージェントが起動します**。

たとえば、`arena runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast` なら、`/arena` は、2つのモデルで1体ずつ、合わせて2体のサブエージェントを起動します。

リストに `inherit-parent` や `auto` を書いたときも、1項目につき1体のサブエージェントが起動します。そのサブエージェントは、親のチャットのモデルで動きます。

### モデルを並べても、パネルの役割ではないもの

ルールファイルには、パネルの役割ではないのに、値にモデルを並べる行が1つあります。`arena cross-judge pool` です。

`arena cross-judge pool` は、`/arena` の判定役（候補の成果物を採点するエージェント。[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)）のモデルの候補を並べた行です。`/arena` は、候補がすべて書き終えた後、`arena cross-judge pool` の行に並んだモデルの中から1つのモデルを選び、判定役として起動します。選ぶときは、できるだけ親のチャットと系統の異なるモデルを選びます。

また、`swarm workers` も、パネルの役割ではありません。`swarm workers` は、`/swarm` が起動するすべてのWorkerが使う既定のモデルで、値に書くモデルは1つです。

例外は、競争や比較（原文では race or comparison）のために、Workerごとに別のモデルを割り当てる場合です。たとえば、モデルの競争（原文では model race）では、同じ課題を、別々のモデルで動くWorkerに解かせ、どのモデルが最もよい結果を出すかを比べます。

この場合、`/swarm` は、Workerを起動する前に、Workerごとに使うモデルを決めます。そのWorkerは、`swarm workers` のモデルではなく、決められたモデルで動きます。

## 書き出すファイル

`/setup-pstack` は、実行するたびに、ルールファイルを丸ごと新しく書き直します。前回のファイルに、行を書き足したり、一部の行だけを書き換えたりはしません。

予算に `large` を選び、すべての役割を既定値のまま受け入れたときに `/setup-pstack` が書き出すファイルは、次のとおりです（pstack version `0.15.15` 時点）。

```
---
description: pstack per-role model choices (overrides skill defaults)
alwaysApply: true
---
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Task `model`). Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: grok-4.7-xhigh-fast
bug-fix: grok-4.7-xhigh-fast
perf-issue: grok-4.7-xhigh-fast
hillclimb: grok-4.7-xhigh-fast
judgment and prose: claude-opus-5-5-xhigh
hardest tasks: claude-opus-5-5-xhigh
how explorer: grok-4.7-xhigh-fast
how explainer: claude-opus-5-5-xhigh
why investigators: grok-4.7-xhigh-fast
why synthesizer: claude-opus-5-5-xhigh
reflect tooling: grok-4.7-xhigh-fast
reflect judgment, divergent, synthesizer: claude-opus-5-5-xhigh
arena runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
arena cross-judge pool: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
swarm workers: grok-4.7-xhigh-fast
architect runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
interrogate reviewers: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
```

READMEによれば、pstackは、既定で、コードを書く役割にはGrokを、最も難しい変更を受け持つ役割と、文章と判断を受け持つ役割にはClaude Opus 5.5を割り当てています。上記のファイルでは、それぞれ、`grok-4.7-xhigh-fast`（`feature, refactoring`・`bug-fix`・`perf-issue`・`hillclimb`）と `claude-opus-5-5-xhigh`（`hardest tasks`・`judgment and prose`）が該当します。

パネルの役割の既定のモデルは、`claude-opus-5-5-xhigh` と `grok-4.7-xhigh-fast` の2つです。

ちなみに私の最新の設定は以下です。

こだわりは調査役と説明役でモデルを分けている点と、`/arena`の採点役にClaudeモデルを含めていないことです。  
モデルが異なれば、人格も異なるためです。

```
---
description: pstack per-role model choices (overrides skill defaults)
alwaysApply: true
---
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Task `model`). Alias entries in a panel list still count toward its fan-out.
# budget: medium (high)
feature, refactoring: grok-4.7-high
bug-fix: grok-4.7-high
perf-issue: grok-4.7-high
hillclimb: grok-4.7-high
judgment and prose: claude-opus-5-5-high
hardest tasks: claude-opus-5-5-high
how explorer: grok-4.7-high
how explainer: claude-opus-5-5-medium
why investigators: grok-4.7-high
why synthesizer: claude-opus-5-5-medium
reflect tooling: claude-sonnet-5-5-high
reflect judgment, divergent, synthesizer: claude-opus-5-5-medium
arena runners: claude-opus-5-5-high, muse-spark-1.3-max, grok-4.7-high, claude-sonnet-5-5-high
arena cross-judge pool:  gpt-5.6-sol-medium, grok-4.7-high, muse-spark-1.3-max
swarm workers: grok-4.7-high
architect runners: claude-opus-5-5-high, muse-spark-1.3-max, grok-4.7-high, claude-sonnet-5-5-high
interrogate reviewers: claude-opus-5-5-medium, muse-spark-1.3-max, grok-4.7-high, claude-sonnet-5-5-high
```

## 再実行したときに残る行

`/setup-pstack` を再実行すると、各役割のモデルは、前回のルールファイルを見て、次のように決まります。

- **前回、既定のモデルのままだった役割**・・・ 既定のモデルから、改めて決めます。
- **前回、利用者が既定から変えていた役割**・・・ 次の3つのどれかを変えていた役割は、その変更を引き継ぎます。
  - モデルの系統（例：`bug-fix` を Grok から Claude に変えた）
  - パネルの役割に並べるモデルの一覧（例：`arena runners` に並べるモデルを足した、または減らした）
  - `inherit-parent` か `auto` にした

ただし、引き継いだ役割でも、スラッグのEffort Levelは、今回選んだ予算のEffort Levelに置き換わります。また、Effort Levelだけを変えていた役割（例：`claude-opus-5-5-xhigh` を `claude-opus-5-5-high` にした）は、引き継がれず、今回選んだ予算のEffort Levelに戻ります。

たとえば、前回の実行で、`bug-fix` だけを既定の `grok-4.7-xhigh-fast` から `claude-opus-5-5-xhigh` に変えていたとします。再実行すると、`bug-fix` は Claude の系統のまま引き継がれ、Effort Levelだけが今回選んだ予算に合わせて置き換わります（`large` なら `claude-opus-5-5-xhigh`、`small` なら `claude-opus-5-5-medium`）。ほかの役割は既定のモデルから決め直されます。

**利用者は、自分で変えた役割を、再実行のたびに選び直さずに済みます**。

### 既定のモデルが変わる前に書き出したルールファイルには、古い既定のモデルが残る

この仕組みには、注意点があります。

pstackの既定のモデルは、バージョンによって変わることがあります。たとえば、pstack version `0.15.15` では、`gpt-5.6-sol-max` が既定のモデルから外れ、`reflect tooling` の既定のモデルは `grok-4.7-xhigh-fast` になりました。既定のモデルが変わる前に書き出したルールファイルには、その当時の既定のモデルを書いた行があり、その行のモデルは今の既定のモデルとは異なる可能性があります。

そのため、再実行しても、`/setup-pstack` は、その行を「既定と異なるモデルが書かれた行」として残します。その役割は、古い既定のモデルのまま動き続けます。

既定のモデルが変わる前に `/setup-pstack` を実行したことがあるなら、次のどちらかをしてから、`/setup-pstack` を再実行します（[README](https://github.com/cursor/plugins/blob/main/pstack/README.md) と同梱ガイド）。

- 当時の既定のモデルが書かれた役割の行を消す
- ルールファイル（`~/.cursor/rules/pstack-models.mdc`）を丸ごと消す

## 検証スキルの作成の提案

`/setup-pstack` は、最後に、エージェントがプロジェクトのアプリを実際に動かして、変更が動くことを確かめられるかを調べます。調べるのは、次の2つがプロジェクトにあるかです。

- **検証スキル**・・・ エージェントがアプリを起動し、操作し、証拠を取るための、プロジェクト専用のSkill（[第3章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a88ea5)）。`/create-verification-skill` で作ると、`verify-<アプリ名>` という名前になります。
- **既存のハーネス**・・・ 本物のアプリを動かして確かめるために、プロジェクトにすでにある仕組み

どちらもなければ、`/setup-pstack` は、`/create-verification-skill` で検証スキルを作ることを、一度だけ提案します。

`/setup-pstack` は、提案の文面で、検証スキルを作る目的を「**エージェントがユーザーと同じようにアプリを操作して、変更が動くことを証明できるようにするため**」と伝えます。

- **利用者が受け入れた場合**・・・ `/setup-pstack` は `/create-verification-skill` を呼びます。
- **利用者が断った場合**・・・ `/setup-pstack` は、検証スキルの作成を重ねて勧めることはせず、そのまま設定を終えます。検証スキルは、利用者が後から `/create-verification-skill` を実行すれば、いつでも作れます。

`/create-verification-skill` が検証スキルを作る手順は[第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca)で、検証スキルを作って自分のアプリで使い始める流れは[第39章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7081)で扱います。

## まとめ

- **書き出すもの**・・・ `/setup-pstack` は、役割ごとのモデルを、使えると確認したスラッグだけを使用し、1つのルールファイルに書き出します。
- **推論の予算**・・・ 予算を変えても、モデルの系統は変えずに、Effort Levelだけを変えます。既定のモデルは、`large` と同じ `xhigh` で動きます。
- **適用の時点**・・・ ルールは新しいチャットから適用されるので、実行後は新しいチャットを始める必要があります。

次の[第37章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/77207a)では、pstackの使い方に迷ったときに質問できる [`/poteto-help`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md) を扱います。
