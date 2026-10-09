---
title: "第6章 pstackは何を解決するのか"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/33f073"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:27+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 9
---

# 第6章 pstackは何を解決するのか

pstackは、「AIが雑なコードを書きすぎる」という問題への答えとして作られたプラグインです。[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)の言葉を借りれば、「**速く進みたいなら、まず深く進む**」というコンセプトにあるように、少ないコードで高品質なプロダクトを開発するための道具です。

この章では、pstackが向き合う問題とその答え方、中身と[第1部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/86acbc)の4つのテーマとの対応、そして使いどころを解説します。

!

[第1部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/86acbc)の4つのテーマ

1. 成果物を確かめて信頼すること（[第2章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/27a183)）
2. 検証の道具・作業手順・コードの構造によって信頼を高めること（[第3章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a88ea5)）
3. コードベースを過去の判断を引き継ぐ記憶として扱うこと（[第4章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dc9141)）
4. それらを土台に自動化すること（[第5章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/b6ac2d)）

## この章の構成

この章の構成は次のとおりです。

- pstackはどんな問題を解決しようとしているのか
- pstackはその問題にどう答えているのか
- pstackには何が入っていて、何が入っていないのか
- pstackの部品は、講演の4つのテーマとどう対応するのか
- pstackは、どんな作業に、どう使えばよいのか
- まとめ：雑なコードの問題に、「まず深く」で答える

## pstackはどんな問題を解決しようとしているのか

pstackが解決しようとしているのは、**AIが雑なコード（slop）を書きすぎる**という問題です。

pstackは、poteto氏が公開しているCursor向けのプラグインで、READMEの冒頭がこの問題提起から始まります。

> there's a growing sense that ai writes too much slop code. i agree. i don't want to ship like a team of twenty slop artists. throughput without quality is not a goal i aspire to. if you want to go fast, go deep first.
>
> AIは雑なコード（slop）を書きすぎるという感覚が広がっている。自分もそう思う。雑なコードを量産する20人のチームのようには働きたくない。品質を伴わない処理量は、自分が目指すものではない。速く進みたいなら、まず深く進むことだ。

そして、pstackはpoteto氏が考える「my answer」だと明言しています。

## pstackはその問題にどう答えているのか

pstackの答えは、以下の3つの方針です。

1. **少なく書く**
2. **1体のエージェントと深く仕事をし、良質で検証可能なコードを書くと信頼できたら、並列化する**
3. **モデルを役割で使い分ける**

READMEでは、問題提起に続く、太字で始まる以下の3つの段落が、この3つの方針に該当します。

- **pstack is my answer.**・・・ コード行数を最大化するのではなく、より少なく、より質の高いコードを書くこと
- **pstack gives you fearless parallelism.**・・・ 1体のエージェントと深く仕事をし、良質で検証可能なコードを書くと信頼できるなら、自信を持って並列化できること
- **cursor gives you the best of all worlds.**・・・ どのモデルにも長所と短所があるが、pstackではどのモデルも使えること。また、多くのSkillは複数モデルを組み合わせ、それぞれの強みを活かしていること

### 少なく書くことは、証拠を削ることではない

1つ目の方針は、行数を最大にすることはむしろ目的の逆だ、という立場です。原則では、『[**Laziness Protocol**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-laziness-protocol/SKILL.md)』（最小の変更を選び、削除を優先する原則。[第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b)）がこの方針に該当します。

ただし、「少なく書く」は、証拠のためのコードまで削ることではありません。『**Bug fix**』Playbook（[`playbooks/bug-fix.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)）の前置きは、削る対象を次のように決めています。

> Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix.
>
> 入れるすべての行は、実行時の証拠にたどれる。「役に立つかもしれない」念のための対策は仮説であり、修正ではない。

エージェントは、「念のため」の変更を加えず、実際に動かして確かめた問題を直すために必要な変更だけを入れます。

一方で同Playbookは、「コミットの並べ方を決める手順（手順5）」で、失敗する再現のテストを修正より先にコミットするよう求めています（テストが高くつく場合などは省けます）。**削るのは、根拠のない「念のため」の対策や変更で、不具合を確かめる再現テストなど証拠のためのコードまで削るわけではありません**。

### 並列化は、1体のエージェントの成果物を信頼できてから

2つ目の方針は、1体のエージェントに深く取り組ませ、検証できる良いコードを書くと信頼できて初めて、自信を持って並列化できる、ということです。poteto氏は『The Complete Guide to pstack』[Part 1](https://x.com/poteto/status/2094457600259842065)でも、検証スキルを使って何件かPRをマージできたあとに並列化を考える、という「信頼 → 並列化」の順で書いています。

### モデルは、役割で使い分ける

3つ目の方針について、READMEは、0.15.15時点の既定値で、モデルを次のように振り分けるとしています。

- **コードを書く委任先**（Feature、Refactoring、Bug fix、Perf、Hillclimb）・・・ Grok（xAIのモデル）
- **最も難しい変更、文章、判断**・・・ Opus 5.5（Anthropicのモデル）
- **パネル（同じ問いを複数のモデルに解かせて比べる仕組み）**・・・ Opus 5.5とGrokの2つ

この割り当ては `/setup-pstack` で変えられます。割り当ての仕組みは[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)で扱います。

もう一つ、複数のモデルを使うことは、好みの問題だけではありません。[`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) の節『[Subagents](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#subagents)』は、セカンドオピニオンを次のように定義しています。

> A second opinion is the same prompt against a different model. Agreement is high-signal.
>
> セカンドオピニオンとは、同じプロンプトを別のモデルに投げることである。答えの一致は、信頼度の高い合図になる。

エージェントは、同じ問いを別のモデルにも解かせ、答えが一致するかで確かめます。

たとえば、不具合の原因の見立てをOpus 5.5とGrok 4.7に別々に出させ、同じ原因を挙げれば、その見立ては一方だけの答えより信頼できる、という使い方になります。**pstackでは、モデルを分けることが、確かめる手段の一つになっています**。

## pstackには何が入っていて、何が入っていないのか

0.15.15時点のpstackには**5種類の部品**が入っています。一方で、**Playbookの手順が使う一部のSkillは別のプラグインやCursor本体にあり、pstackには含まれません。また計画書を書くためのSkillも含まれていません**。

### 入っているのは、5種類の部品

件数はすべて0.15.15（[commit `df58112`](https://github.com/cursor/plugins/pull/511)）時点の値です。

| 部品 | 件数 | 置き場所 | 役割 |
| --- | --- | --- | --- |
| Playbook | 23 | `skills/poteto-mode/playbooks/*.md` | 作業の種類ごとの手順書。`/poteto-mode` の中の参照ファイル |
| Principle | 24 | `skills/principle-*/SKILL.md` | 判断の基準。1原則1ファイルの短いSkill |
| Skill | 27 | `skills/*/SKILL.md`（Principleを除く） | 呼び出して使う能力。`/poteto-mode` と `/setup-pstack` を含む |
| subagent | 2 | [`agents/poteto-agent.md`](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md)、[`agents/comment-sicko.md`](https://github.com/cursor/plugins/blob/main/pstack/agents/comment-sicko.md) | 主エージェントが起動する別のエージェントの定義 |
| 同梱ガイド | 10ページ | [`docs/guide/*.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/README.md) | pstackに同梱されているガイド。最初のタスクから夜間の実行まで、依頼例つきで案内する |

読み違えやすい点が3つあります。

- **Playbookは、Skillではありません**・・・ Playbookは `/poteto-mode` が依頼に合わせて開く参照ファイルで、単独では呼び出せません。poteto氏も『The Complete Guide to pstack』[Part 2](https://x.com/poteto/status/2097732320606507506)で、PlaybookはSkillではなく `/poteto-mode` の中の参照ファイルだと説明しています。この違いは[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)で扱います。
- **Principleは、形式上はSkillです**・・・ ただしREADMEでは「skills」の表に入っておらず、別に「principles」の表があります。本書でも、Skill 26件とPrinciple 24件を分けて数えます。
- **同梱ガイドは、X上の『The Complete Guide to pstack』とは別物です**・・・ 本書では、`docs/guide/` を「同梱ガイド」、X上の記事を『The Complete Guide to pstack』Part 1／Part 2と呼び分けます。

### 手順が名前で頼る一部のSkillは、同梱されていない

`/poteto-mode` は、同梱していないSkillも名前で参照しています。それがないと、手順の一部が実行できません。一覧はREADMEの節『[not shipped here](https://github.com/cursor/plugins/blob/main/pstack/README.md#not-shipped-here)』にあります。

| 参照されるもの | 実際の置き場所 | `/poteto-mode` での使われ方 |
| --- | --- | --- |
| `/deslop`（`deslop` skill） | [`cursor-team-kit`](https://github.com/cursor/plugins/tree/main/cursor-team-kit) プラグイン | コミットの前にAIらしい雑なコードを取り除く |
| `control-cli` | `cursor-team-kit` プラグイン | CLIやTUI（ターミナルの中で動く、画面を持つアプリ）を操作して確かめる |
| `control-ui` | `cursor-team-kit` プラグイン | ブラウザ、Electron（デスクトップアプリを構築するためのフレームワーク）、WebのUIを操作して確かめる |
| `/create-skill` | Cursorの組み込み | `SKILL.md`を書くときの作法 |
| `/autopilot`（以前の名称は `/babysit`） | Cursorの組み込み | PRの状況確認（pstackでは『[**Babysit**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/babysit.md)』Playbookを使う。[第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e)） |

READMEは、一式をそろえたいなら `cursor-team-kit` もあわせて入れるよう勧めています。

特に大事なのは `control-cli` と `control-ui` です。この2つは、『**Bug fix**』Playbookの「不具合を自分で再現する手順（手順1）」で使う、アプリ操作用のSkillです。pstackだけを入れた状態では、アプリを操作して再現し、確かめる手段がないことがあります。

自分のアプリ専用の検証スキル（`/create-verification-skill` で作る `verify-<app>`）があれば、それが操作手段になります。どちらもないなら、[第39章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7081)の手順で、まず検証スキルを用意します。

### 計画書を書くためのSkillは、「最良の仕様はコード」という立場から入っていない

pstackに計画用の専用Skillがないのは、poteto氏が計画書よりコードを仕様とする立場を取っているからです。READMEの節『[why are there no planning skills?](https://github.com/cursor/plugins/blob/main/pstack/README.md#why-are-there-no-planning-skills)』は、Cursorのプランモードがpstackとよく合うとしたうえで、「最良の仕様はコードである」と書いています（[第41章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7549a7)）。

同じ箇所には、計画を作りたいなら `/poteto-mode` で扱えるが既定ではない、ともあります。poteto氏は『The Complete Guide to pstack』Part 2で、計画をしないわけではなく、コードを通じて計画しているのだと補い、抽象的な計画を敵対的にレビューすることはしない、とも書いています。

pstackの中で「コードでの計画」を担っているのは、次の3つです。

- **『Prototype』Playbook**（[`playbooks/prototype.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/prototype.md)）・・・ 使い捨てのプロトタイプで、設計や振る舞いの判断を安く決めます。`/poteto-mode` の節『[Non-negotiables](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#non-negotiables)』は、**実行すれば観察できる事実を人に尋ねそうになったら、このPlaybookで小さくプロトタイプを作り、動かした結果を見て決める**よう求めています。
- **[`/architect`](https://github.com/cursor/plugins/blob/main/pstack/skills/architect/SKILL.md)**・・・ 実装に入る前に、その関数を使うコードが何を渡し、何を受け取るかを決め、それに合う型やモジュールの分け方を設計するSkillです。
- **『Multi-phase or multi-PR plan』Playbook**（[`playbooks/multi-phase-plan.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md)）・・・ 計画書が必要な場合の受け皿です。ただしこのPlaybookは、最初の手順で、1〜2ファイルで方針が明らかな変更なら計画を省くよう書いています。その次の手順では、計画書を書く前に、未解決の疑問をプロトタイプで解くよう求めています。

3つ目の『[**Multi-phase or multi-PR plan**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md)』Playbookは、計画書を作るためのPlaybookです。それでも、文章を書く前にプロトタイプを動かすよう求めています。**コードを仕様とする立場は、Skillの有無だけでなく、Playbookの手順にも表れています**。計画の扱いは[第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5)と[第42章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/166acb)で詳しく扱います。

## pstackの部品は、講演の4つのテーマとどう対応するのか

[第1部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/86acbc)で1章ずつ扱った[講演](https://x.com/poteto/status/2102050467505430555)の4つのテーマには、pstackの中にそれぞれ対応する部品があります。本書での対応は次のとおりです。

| 講演のテーマ（[第1部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/86acbc)の章） | pstackで担う部品 | 例 |
| --- | --- | --- |
| 信頼：成果物を検証する（[第2章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/27a183)） | 検証スキル、Verification（検証）グループの原則（[第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019)） | `/create-verification-skill`、『[**Prove It Works**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md)』 |
| 信頼を高める方法：検証と手順を再現可能にする（[第3章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a88ea5)） | Playbook、手順を支えるSkill | 『**Bug fix**』、`/tdd`、`/show-me-your-work` |
| 記憶としてのコードベース：判断と制約を残す（[第4章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dc9141)） | Meta・Architectureグループの原則（[第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b)、[第21章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dd2d9f)）、記録を扱うSkill | 『[**Encode Lessons in Structure**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)』、`/reflect`、`/correct`、`/why` |
| 自動化：土台の上に積む（[第5章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/b6ac2d)） | 自動化向けのPlaybook | 『[**Autonomous run**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autonomous-run.md)』、『[**Orchestrate**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md)』 |

pstackは、手順（Playbook）と判断基準（Principle）と能力（Skill）を分けて持ち、入口の `/poteto-mode` からまとめて呼び出します。この仕組みは[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)から[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)で扱います。

## pstackは、どんな作業に、どう使えばよいのか

pstackは、**厳密さが必要な作業**に使います。使い始めに覚えるのは、**`/setup-pstack` と `/poteto-mode` の2つだけ**です。

### 向くのは、厳密さが必要な作業

READMEは、`/poteto-mode` を「厳密さが必要なことをするときはいつでも」（whenever you're doing anything that requires rigor）使うよう勧めています。反対に、`/poteto-mode` の `SKILL.md` は、**雑談のような軽いやりとり（Casual turn）には適用しない**よう書いています（[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)）。

これをもとにすると、向く作業と向かない作業は次のように分けられます。

- **向く作業**・・・ 再現と確認が必要な不具合修正、関数やモジュールの境界をまたぐ設計を伴う機能追加、席を外して任せたい長い作業など
- **向かない作業**・・・ 1行のtypo修正や、答えが一言で済む質問など

ただし、向く作業でも、アプリを動かして確かめる手段がなければ、pstackの手順は実行できません。『**Bug fix**』Playbookが求める「自分で再現する」も、「同じ操作面（不具合が起きたのと同じ画面やコマンド）で確かめる」も、確かめる手段が前提だからです。**まず検証スキルを用意し、それからpstackを使う**という順序になります。

## まとめ：雑なコードの問題に、「まず深く」で答える

- **解決しようとしている問題**・・・ pstackは「AIが書く雑なコード」への答えとして作られています。READMEは「速く進みたいなら、まず深く進む」と書いています。
- **問題への答え方**・・・ 少なく書く、1体のエージェントと深く仕事をし、良質で検証可能なコードを書くと信頼できたら、並列化する、モデルを役割で使い分ける、の3つの方針です。
- **入っているもの、入っていないもの**・・・ 0.15.15時点で、Playbook 23件、Principle 24件、Skill 27件、サブエージェント2件、同梱ガイド10ページが入っています。`/deslop`、`control-cli`、`control-ui` は `cursor-team-kit` に、`/create-skill` はCursor本体にあり、特に操作用のSkillがないと再現と検証ができません。計画用のSkillがないのは「最良の仕様はコード」という立場を取るからで、この立場は計画のPlaybookの手順にも表れています。
- **講演の4つのテーマとの対応**・・・ 信頼、信頼を高める方法、記憶としてのコードベース、自動化の4つに、それぞれ対応する部品があります。
- **使いどころと使い始め方**・・・ 厳密さが必要な作業に使います。使い始めに覚えるのは `/setup-pstack` と `/poteto-mode` の2つです。

次の[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)では、入口である `/poteto-mode` を詳しく見ます。呼び出し方と呼び出したときに起きること、依頼をPlaybookに振り分ける規則、良い依頼の書き方を解説します。
