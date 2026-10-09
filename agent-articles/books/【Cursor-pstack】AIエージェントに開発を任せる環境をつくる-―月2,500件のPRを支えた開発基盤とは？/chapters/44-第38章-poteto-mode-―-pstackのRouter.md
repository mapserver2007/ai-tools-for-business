---
title: "第38章 /poteto-mode ― pstackのRouter"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:36+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 44
---

# 第38章 /poteto-mode ― pstackのRouter

`/poteto-mode` は、pstackの入口です。**依頼を読み、23件のPlaybookから1冊を選び、その手順に沿って作業を進めます**（[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)）。

この章では、`/poteto-mode` の本体である [`SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) を扱います。

!

`/poteto-mode` の呼び出し方と依頼の振り分けは[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)で、Playbook・Skill・Principle の役割と『Non-negotiables』の主な条件は[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)で扱いました。この章では、それらの章で扱っていない `/poteto-mode` の本体である `SKILL.md` の内容を解説します。

## この章の構成

この章の構成は次のとおりです。

- `/poteto-mode` とは
- 『Non-negotiables』：必ずすること
- 『Principles』：原則の索引
- 『Autonomy』：尋ねずに進む範囲と、止まる範囲
- 『Subagents』：委任の決まり
- 『Writing the reply』：返答の書き方
- 『Comments』：コメントの書き方
- 『Playbooks』：Playbookの索引
- 自分の流儀に合わせる
- まとめ

## `/poteto-mode` とは

章題の「Router」（振り分け役）は、`/poteto-mode` の、依頼を合うPlaybookへ振り分ける役割を指します。同梱ガイドも、`/poteto-mode` のページ（[`02-poteto-mode.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/02-poteto-mode.md)）に「Route work through `/poteto-mode`」（作業を `/poteto-mode` に通す）という題を付けています。

`/poteto-mode` には、依頼をPlaybookへ振り分ける規則のほかに、**振り分けた後の作業全体に適用される規則**も書かれています。たとえば、次のような規則です。

- コードを書くときは、まずデータの形を決める（原則『[**Model the Domain**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md)』）
- 取り消せない操作の前では、必ず止まる
- 返答は、短い断定文で書く

`SKILL.md` の frontmatter の `description` は、`/poteto-mode` を「poteto氏のエージェントの流儀（poteto's agent style）」と説明し、その流儀が目指すものとして、次の5つを挙げています。

- 簡潔で、かつ詳しい返答（concise, detailed responses）
- 慎重に考えたサブエージェントへの委任（deliberate subagents）
- AIらしさを取り除いた文章（unslopped prose）
- 単純なコード（simple code）
- 検証済みの作業（verified work）

pstackの導入が済んだら（[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)）、利用者は、作業の**依頼を `/poteto-mode` に渡します**。

`/poteto-mode` は、`disable-model-invocation: true` の設定を持つので、利用者が名前で呼んだときだけ実行されます。

`/poteto-mode` が有効になるのは、`/poteto-mode` を付けたメッセージのみです。**毎ターン有効にしたいときは、`Option + Enter`（Mac）か `Alt + Enter`（Windows）で呼んで、Custom Mode（Skillを毎ターン、エージェントのコンテキストに入れ続けるCursorの機能）にします**（[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)、[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)）。

Custom Modeで `/poteto-mode` が有効な間も、Playbookの手順で進めるのは、依頼がPlaybookに当てはまるときや、厳密さが必要なときだけです。

`SKILL.md` の本文は、『Non-negotiables』から『Playbooks』までの7つの節で構成されています。

## 『Non-negotiables』：必ずすること

『[Non-negotiables](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#non-negotiables)』は、「こういう状況になったら、必ずこうする」という決まりの一覧です。主な決まりは[『第8章 Non-negotiablesが、3つの部品をつなぐ』](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d#non-negotiables%E3%81%8C%E3%80%813%E3%81%A4%E3%81%AE%E9%83%A8%E5%93%81%E3%82%92%E3%81%A4%E3%81%AA%E3%81%90)で見ました。

『Non-negotiables』の冒頭には、すべての決まりに共通する次の規則があります。

- エージェントは、返答の中で、判断に影響した原則の名前と、その原則で変えた選択を挙げる
- 挙げてよいのは、このセッションで、その原則のSkillファイルを全文読んだ原則だけ

たとえば、[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)の実例（再試行が実行の途中に入ると、エクスポートが重複した行を書き出す不具合）を直した後なら、返答には次のような一節が入ります。

```
Fix Root Causes に従い、再試行のたびに書き出し済みの行をもう一度書き込む箇所を直しました。書き出した後で重複を取り除く処理は足していません。
Make Operations Idempotent に従い、書き込みを行のキーで上書きする形に変えました。同じ実行を2回しても、行数は変わりません。
```

つまり、次のような返答は上記2つの規則を満たしません。

```
Fix Root Causes と Make Operations Idempotent に従いました
```

このように、原則の名前だけを並べた返答からは、原則に従って何を決めたのかが分からないためです。また、何を決めたかを書けない場合、エージェントは、実際には原則を使っていない可能性もあります。

利用者は、原則の名前とエージェントの判断を見れば、エージェントがどの基準で何を決めたかを確認できます。

**第8章で見た決まりと、この共通の規則のほかに、次の決まりがあります**。

| 状況 | 必ずすること | 詳細 |
| --- | --- | --- |
| エージェントが利用者に「どのやり方がよいか」を尋ねそうになった | 尋ねる前に、その問いの答えが、実行すれば判明する事実か、人が決める判断かを分類する | [第41章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7549a7) |
| コードを書く | まずデータの形を明らかにし、構造を選ぶ。原則『[**Model the Domain**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md)』に従う | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| 作業を並列に展開する | 網羅、競争、関門（検証ゲート）、探索の分割は `/swarm`、土台を選んで良い部分を移植する設計やコードの比較は `/arena` | [第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346) |
| 意見が割れる設計 | マージする前に `/interrogate` を使う | [第28章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880) |
| 自明でない複数手順の作業 | スループット・チェックポイントを書く。『[**Feature**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md)』の手順3と同じ | [第12章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b) |
| ベンチマークを実行する、自分で性能を測る、測った高速化や性能の低下を報告する | 数値を報告したり、数値をもとに判断したりする前に、`/benchmark-checklist` で数値を点検する | [第27章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/167c91) |
| PRの状態を尋ねる依頼 | Cursor の組み込みの `/autopilot` Skill（以前の名称は babysit）ではなく、『[**Babysit**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/babysit.md)』を使う。PRを開いただけでは使わない | [第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e) |
| チェックがすべて通ったPRのスタックマージを依頼された | 『[**Shipping**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/shipping.md)』を実行する。チェックがすべて通っても安全とはみなさず、PRごとに独立して確かめてからマージする | [第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e) |
| Bugbot や、エージェントによるセキュリティレビューのコメント | 鵜呑みにせず、指摘ごとに、直す（fix）、却下する（dismiss）、質問する（ask）に仕分ける。Bugbotなどは本物の不具合も見つけるが、問題でない指摘や細かすぎる指摘も混じるため | [第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e) |
| 作業中にSkillが壊れている | 作業を止めず、黙って回避もせず、そのSkill専用のPRで直す | [第13章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0) |

!

- **データの形**・・・ データがどんな項目を持ち、どんな状態を取るか
- **スループット・チェックポイント**・・・ 作業を「どう並列に分けられるか」を検討した結果を、TODOリストに記録する際の4つの項目。先に済ませる手順、並列に進められる作業、共有して書き換える状態、安全に分けられる最小の単位の4つ
- **PRの状態を尋ねる依頼**・・・ 「check on PR X（PR Xを見ておいて）」「get it green（チェックを全部通して）」のような依頼
- **網羅**・・・ 複数の範囲をWorkerに割り振り、漏れなく確かめる分け方
- **競争**・・・ 同じ課題を複数のWorkerに競わせる分け方
- **関門**・・・ 原文では gauntlet。pstackのファイルに定義はなく、本書では、1つの変更に検証を何本も並べ、すべての検証に通ることを求める分け方と定義（[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)）
- **探索の分割**・・・ 探す場所を複数に分け、各Workerに1か所ずつ調べさせる分け方（例：不具合の原因を探すとき、疑わしいモジュール1つ1つに対して、1体ずつWorkerを割り振って調べさせる）
- **スタック**・・・ 親子関係でつながったPRの列（PRの上に次のPRを積み重ねた並び）。2本目以降のPRは1つ下のPRのブランチをマージ先にし、一番下のPRだけが `main` などの本流のブランチ（trunk）をマージ先にする（[第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e)）
- [**Bugbot**](https://cursor.com/ja/docs/bugbot)・・・ Cursorが提供する、PRを自動でレビューする機能

### 尋ねる前に、答えが事実か判断かを分ける

表の決まりのうち、**原文が最も長く説明しているのは、1つ目の「尋ねる前に分類する」です**。

エージェントは、利用者に「どのやり方がよいか」「どう作るべきか」を尋ねそうになったら、尋ねる前に、その問いの答えが以下の「どちらに該当するのか」を分類します。

- **実行すれば分かる事実**・・・ 挙動、処理にかかる時間、レイアウト、出力、性能など。エージェントは人間に尋ねず、自分で確かめます。確かめ方は、依頼が振り分けられたPlaybookによって、次の2つに分かれます。
  - 『[**Investigation**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/investigation.md)』以外のPlaybook・・・ 『[**Prototype**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/prototype.md)』Playbookで試して、その結果で決めます。
  - 『**Investigation**』Playbook・・・ プロトタイプは作らず、調査を続け、コードなどを読んで見つけた根拠から答えます。
- **人が決める判断**・・・ 試しても答えが出ない、プロダクトの判断や好み。エージェントは、この判断だけを人間に尋ねます。

『**Investigation**』でプロトタイプを作らないのは、『Investigation』が、コードを変えずに調べ、根拠を添えた回答を、利用者に渡す調査だからです（[第10章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ea525d)）。

#### 利用者が作業を一任したとき

利用者がエージェントに作業を一任した場合、エージェントは、作業の途中で出てくる判断を、利用者に尋ねずに自分で決定し、作業を続けます。そして、作業の最後に利用者へ返す報告の中で、自分で下した判断を伝えます。

報告に何を書くかは、判断の種類によって次の2つに分かれます。

- **任された範囲の判断**・・・ テストの置き場所や関数の分け方など、作業の中でエージェントが下した判断。報告では、どの選択肢を採用したかを伝えます。
- **人が決める判断**・・・ 試しても答えが出ない、プロダクトの判断や好み。エージェントは、利用者に尋ねる代わりに、ひとまず妥当と考える選択肢を選んで作業を進めます。報告では、選んだ選択肢とその理由を詳しく説明するとともに、ほかの選択肢を選びたいときに、利用者が次にどんな指示を出せばよいかを、平易な言葉で伝えます。

ただし、作業を一任された場合でも、次の2つでは、エージェントは止まり、利用者の判断を待ちます。

- 利用者が、あらかじめ止まるよう指定した確認点（例：マージの前）
- この章の[『Autonomy』の節](#%E3%80%8Eautonomy%E3%80%8F%EF%BC%9A%E5%B0%8B%E3%81%AD%E3%81%9A%E3%81%AB%E9%80%B2%E3%82%80%E7%AF%84%E5%9B%B2%E3%81%A8%E3%80%81%E6%AD%A2%E3%81%BE%E3%82%8B%E7%AF%84%E5%9B%B2)で見る『Always pause』の一覧（共有ブランチへの force-push やデプロイのような、取り消せない操作）

## 『Principles』：原則の索引

『[Principles](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#principles)』は、24の原則の索引です。**各項目には、原則名、原則を適用する条件、原則の要点が、順に書かれています**。

24の原則は、次の5つに分類されています。

| 分類 | 原則 | 本書の章 |
| --- | --- | --- |
| Core | Laziness Protocol、Foundational Thinking、Redesign from First Principles、Attack the Premise、Subtract Before You Add、Minimize Reader Load、Outcome-Oriented Execution、Experience First、Exhaust the Design Space、Build the Lever | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| Architecture | Model the Domain、Boundary Discipline、Type System Discipline、Make Operations Idempotent、Migrate Callers Then Delete Legacy APIs、Separate Before Serializing Shared State | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| Verification | Prove It Works、Fix Root Causes、Sequence Work into Verifiable Units、Test Behavior, Not Implementation、Explain the Number | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| Delegation | Guard the Context Window、Never Block on the Human | [第20章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/c155cc) |
| Meta | Encode Lessons in Structure | [第21章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dd2d9f) |

エージェントは、`/poteto-mode` で作業を始めるときに、まずこの索引を読み、今の作業に当てはまる原則を選びます。索引は `/poteto-mode` の `SKILL.md` の中にあるので、`/poteto-mode` が読み込まれれば、索引も一緒に読まれます（[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)）。

たとえば、『Model the Domain』の項目は、次のとおりです。

原則名の後に、原則を適用する条件（状態を持つロジックを書くときなど）と、原則の要点（構造でドメインを表す）が続きます。

```
- **Model the Domain** (**principle-model-the-domain**). Writing stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a structure (state machine, typed model, table or registry, reducer, boundary, the right collection) instead of scattered conditionals.
// 状態を持つロジックを書くとき、または分岐が多いコードや、同じ形の前提をファイルをまたいで繰り返すコードを書くとき。散らばった条件分岐ではなく、構造（状態機械、型付きのモデル、表や登録簿、reducer、境界、適切なコレクション）でドメインを表す。
```

エージェントは、適用すると決めた原則について、索引にある原則の要点だけで済ませず、その原則のSkillファイル（`SKILL.md`）を全文読みます。

この規則は、`/poteto-mode` の `SKILL.md` の節『[Principles](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#principles)』の冒頭に、書かれています。

> Read the leaf skill in full for any principle you apply.
>
> 適用する原則は、そのSkillファイルを全文読む。

また同 `SKILL.md` の節『[Non-negotiables](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#non-negotiables)』の冒頭にも、次の一文があります。

> Cite only principles whose leaf SKILL.md you read this session.
>
> 挙げてよいのは、このセッションで、その原則の `SKILL.md` を読んだ原則だけ。

つまり、エージェントは、Skillファイルを読んでいない原則の名前を、返答で挙げないよう、制御されています。

!

**索引だけを先に読み、原則の全文は適用するときに読む**、という読み込みの仕組みは[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)で、各原則の中身は[第4部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4b3166)（[第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b)から[第21章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dd2d9f)）で扱っています。

## 『Autonomy』：尋ねずに進む範囲と、止まる範囲

『[Autonomy](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#autonomy)』は、**尋ねずに進める作業と、必ず止まる作業**を分け、利用者に意見を求められたときの答え方も定めています。次の4つの段落でできています。

| 段落 | 規則 |
| --- | --- |
| 『Just do it.』 | MCPツールは、尋ねずに自由に使ってよい。取り消せる作業と、外部への行動（チームのチャットへの投稿、チケットの更新、評価（『Eval』、[第13章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0)）の開始）も、尋ねずに進める |
| 『Always pause』 | 取り消せない操作（共有ブランチへの force-push、デプロイ、データの削除、顧客へのメッセージ）では必ず止まる |
| 『Session overrides』 | 「止まらないで」「もう寝る」「終わるまで回して」「全部任せる」と指示されたら、止まらずに進み続ける |
| 『No is an acceptable answer.』 | 次の条件のとき（利用者に「これをするべきか」と聞かれたとき、作業の追加を提案されたとき、やり方の案を見せられたとき）、エージェントは自分の考えを正直に回答する。賛成できない場合、断ったり反論したりする（例：「これは入れる価値がない」と答える）。利用者の案だからといって賛成はせず、率直に意見を言う |

『Session overrides』の指示を受けても、エージェントは、表の2行目の『Always pause』に当たる作業（取り消せない操作）では止まります。この例外は、『Session overrides』の段落ではなく、『Non-negotiables』の決まりに書かれています（この章の[「利用者が作業を一任したとき」](#%E5%88%A9%E7%94%A8%E8%80%85%E3%81%8C%E4%BD%9C%E6%A5%AD%E3%82%92%E4%B8%80%E4%BB%BB%E3%81%97%E3%81%9F%E3%81%A8%E3%81%8D)）。

## 『Subagents』：委任の決まり

『[Subagents](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#subagents)』は、主エージェントが、タスクの一部をサブエージェントに委任するときの決まりです。主に次の3つを定めています。

- **委任先**・・・ どのサブエージェントに委任するか
- **既定値**・・・ サブエージェントを起動するたびに使う設定
- **新しく起動するか、再開するか**・・・ 新しい仕事を、新しいサブエージェントに渡すか、既存のサブエージェントを再開して渡すか

まず、委任先です。主エージェントは、Playbookの手順の中でサブエージェントを起動するとき、既定では `poteto-agent` を使います。ただし、`/how`、`/why`、`/interrogate`、`/reflect`、`/swarm` は、複数のモデルでレビューするために、どのサブエージェントを起動するかを自分で決めています。主エージェントは、これらのSkillが選んだサブエージェントを `poteto-agent` に置き換えません。

!

**`poteto-agent`**・・・ pstackに入っているサブエージェントです（[`agents/poteto-agent.md`](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md)）。作業を始める前に、`/poteto-mode` の `SKILL.md` を、Principleの索引も含めて全文読みます。そのため、主エージェントと同じ `/poteto-mode` の規則で働きます。

`poteto-agent` の説明（description）は、使い方を次のように定めています。主エージェントは、新しい仕事のたびに、新しい `poteto-agent` を起動します。既存の `poteto-agent` を再開するのは、この章の『Subagents』の節で見る、限られた場合だけです。

次に、既定値です。主エージェントは、どのサブエージェントを起動する場合でも、サブエージェントを起動する度に同じ設定を使います。既定値には、次の4つがあります。

- **バックグラウンドで動かす**・・・ 主エージェントは、サブエージェントの作業が終わるのを待たずに、自分の作業を続けられます。
- **agent mode で動かす**・・・ agent mode は、ファイルの編集やツールの実行ができるモードです。読み取り専用のモードで動かすと、サブエージェントはMCPのツールを使えなくなります。
- **依頼文には、ファイルの中身ではなく、ファイルのパスを書く**・・・ サブエージェントは、渡されたパスのファイルを自分で開いて読みます。
- **役割ごとにモデルを指定する**・・・ サブエージェントをどのモデルで動かすかを、役割ごとに明示します。役割と既定のモデルは[『第36章 役割の一覧』](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0#%E5%BD%B9%E5%89%B2%E3%81%AE%E4%B8%80%E8%A6%A7)のとおりで、`/setup-pstack` で変えられます。

**エージェントは、すべての委任で、この既定値に従います**。

4つ目の、モデルの指定には、コードを書く作業を任せるときの決まりがあります。主エージェントは、変更の難しさで委任先のモデルを分けます。

- **最も難しい変更**（複数の箇所にまたがる設計、込み入った並行処理、細かな誤りに気づきにくいアルゴリズム）・・・ 判断力が最も高いモデル（既定では `claude-opus-5-5-xhigh`）に渡します。指示があいまいで判断が要る作業でも、手順が細かく決まっていて、そのとおりに進めるだけの作業でも、最も難しい変更であれば、主エージェントはこのモデルに渡します。
- **些細な機械的編集**（例：名前の置き換え）・・・ コードを書くための、応答の速いモデル（既定では `grok-4.7-xhigh-fast`）に渡します。

委任先のモデルは、`/setup-pstack` が書き出すルールファイルで変えられます。エージェントは、委任する内容に応じて、ルールファイルの次の行を読み、委任先のモデルを決めます。

- **最も難しい変更を委任するとき**・・・ `hardest tasks` の行
- **各Playbookのコードを委任するとき**・・・ そのPlaybookの行（`feature, refactoring`、`bug-fix`、`perf-issue`、`hillclimb`）
- **文章と判断を委任するとき**・・・ `judgment and prose` の行

ルールファイルに行がない役割は、既定のモデルのままです。行に `inherit-parent` か `auto` と書かれた役割は、親のチャットのモデルで動きます（[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)）。

『Subagents』は、サブエージェントから返ってきた結果の扱い方も定めています。

[第6章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/33f073)で見たセカンドオピニオン（同じ依頼文を別のモデルに渡すこと）の定義も、この『Subagents』に書かれています。『Subagents』は、**別のモデルと答えが一致すれば、それは信頼できる強い手がかりだ**と定めています。

最後に、新しく起動するか、再開するかです。『Subagents』は、この点を次のように定めています。

> **Fresh subagents by default.** Give new work to a fresh subagent with consolidated scope, meaning the original brief, every later directive, and the prior agent's report and branch.
>
> **既定では、新しいサブエージェントに渡す。** 新しい仕事は、依頼の範囲をまとめ直したうえで、新しく起動したサブエージェントに渡せ。まとめ直すとは、最初の依頼文、その後に出したすべての指示、前のサブエージェントの報告と作業したブランチを、1つにまとめることである。

この決まりは、新しい仕事のすべてに当てはまります。原文は、新しい仕事として、次の4つを挙げています。

- 修正のラウンド（レビューで見つかった問題を直す、1回分の作業）
- 追加の作業（終わった作業に続けて頼む作業）
- 再試行（うまくいかなかった作業のやり直し）
- キュー（これから取りかかる作業の列）にある、次の作業

既存のサブエージェントを再開して仕事を渡してよいのは、新しい仕事に、そのサブエージェントだけが持っている状態がどうしても必要で、その状態をほかへ移すのに手間がかかるときだけです。原文は、その状態として、次の3つを挙げています。

- そのサブエージェントの手元のチェックアウト（作業のために取り出した、リポジトリのファイル）
- まだコミットしていない変更
- そのサブエージェントが動かし続けているプロセス（例：開発サーバー、スマートフォンのアプリを動かすシミュレーター、PRを見張る『Babysit』の処理）

なお、動いているサブエージェントに、止まるよう指示したり、待つよう指示したりすることは、ここでいう「再開」には当たりません。

PRの担当のような役割も、1体のサブエージェントに固定されません。たとえば、あるPRを担当するサブエージェントが、修正を1回終えて戻ってきたとします。そのPRで次の修正が必要になったら、主エージェントは、戻ってきたサブエージェントを再開せず、新しいサブエージェントを起動して、同じPRの担当を引き継がせます。PRの担当という役割は続きますが、その役割を務めるサブエージェントは、回ごとに新しくなります。

この決まりの最後に、原文は次のように書いています。

> Interrupt-chained resumes silently drop directives, so fire a fresh subagent with consolidated scope rather than trusting a "done" summary.
>
> 途中で止めては再開する、ということを繰り返すと、サブエージェントは、受け取った指示を何も言わずに落とす。だから、「終わった」という報告を信じず、依頼の範囲をまとめ直して、新しいサブエージェントを起動せよ。

つまり、何度も止めて再開させたサブエージェントが「終わった」と報告しても、主エージェントは、その報告を信頼しません。最初の依頼文から最新の指示までを1つの依頼文にまとめ直し、新しいサブエージェントに渡し直します。

## 『Writing the reply』：返答の書き方

『[Writing the reply](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#writing-the-reply)』は、**返答の規則を、書き終えてからではなく、書いている最中に守る**よう定めています。

> Write the reply clean as you draft it. A cleanup pass after drafting does not remove these patterns.
>
> 返答は、書きながら整える。書き終えた後でまとめて見直しても、こうした書き方は取り除けない。

書き終えた後でまとめて見直しても、次の表の規則に反する書き方は直しきれずに残る、と『Writing the reply』には記載があります。

引用の「こうした書き方」に該当する規則は、次の7つです。

| 規則 | 中身 |
| --- | --- |
| 短い断定文 | 一文に、伝えたいことを一つだけ書き、句点で終える |
| 長いダッシュ（em dash、`—`）を使わない | 箇条書きや見出しも、ダッシュでつながず文として書く（例：`main.js — 保存処理` ではなく、「`main.js` は保存処理を受け持つ。」と書く） |
| 文の途中のコロンを使わない | unslop の規則14（[第33章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b)）と同じ。リストの前のコロンは可 |
| 短く書くことを、内容を削る言い訳にしない | 文は短くするが、Playbook が返答に書くよう求めている項目は削らない（例：細かい経緯、トレードオフ、選んだ案、まだ決まっていないこと） |
| 使う人と、次にコードを担当する人への影響を先に書く | 実装の詳細より先に、その作業が誰のためのものか（例：アプリのユーザー、ライブラリを使う同僚）と、その人にとって何が変わるかを書く。続けて、次にこのコードを担当するエンジニアが何を引き継ぐかを書く |
| リンクや引用を捏造しない | トランスクリプト（エージェントとの会話の記録）の参照も捏造しない。リンクは、このセッションで作ったか読んだものだけ。PRのリンクは `https://github.com/<owner>/<repo>/pull/<number>` の形で書く |
| 主張に証拠かラベルを付ける | measured（測定した）、inferred（推論した）、guess（推測）。予測や、確かめていない原因は guess とする。自分で実行できる確認を、人間に任せない |

どのPlaybookも、最後はこの規則で書いた返答で終わります。

たとえば、[README](https://github.com/cursor/plugins/blob/main/pstack/README.md) には、「スクロールのずれ」の依頼例があります。

```
/poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro first, then fix and verify.
// このPRには気づきにくいバグがある。アイドル中でも750msごとにスクロールがずれる。まず再現して、それから直して、確かめて。
```

「スクロールのずれ」の依頼で不具合を直した後の返答を、規則に反する形と、規則に沿う形で書くと、次のようになります。

```
前：直りました: 原因はタイマーだったので止めておきました、たぶんもう大丈夫だと思います。

後：アイドル中にスクロールがずれる不具合は、もう起きません（measured）。
原因は、750msごとに位置を書き換えるタイマーでした（measured）。
次にこのコードを受け持つ人は、タイマーを追加するとき、アイドル中に位置を書き換えないかを確かめる必要があります（inferred）。
```

前の返答は、文の途中にコロンがあり、一文に伝えたいことが3つ入り、「直りました」が測定なのか推測なのかも分かりません。後の返答は、アプリのユーザーにとって何が変わったかを先に書き、次にこのコードを受け持つ人が引き継ぐことも書き、主張ごとにラベルを付けています。

このように、規則に沿って書いた返答なら、利用者は、一文ごとに、何が変わり、それをどう確かめたかを読み取れます。

## 『Comments』：コメントの書き方

『[Comments](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#comments)』は、[前節](#%E3%80%8Ewriting-the-reply%E3%80%8F%EF%BC%9A%E8%BF%94%E7%AD%94%E3%81%AE%E6%9B%B8%E3%81%8D%E6%96%B9)の返答の規則を、コードのコメントにも当てはめるよう定めています。返答と同じく、**コメントも、書き終えてから直すのではなく、書いている最中に規則を守ります**。

そのうえで、**コメントを残すのは、コードを読んでも分からない理由だけ**としています。たとえば、「ライブラリの不具合を避けるため」のような理由が残されるコメントに該当します。

また、この規則は、検証やテストのスクリプトについても決まりを定めています。

スクリプトには、`// Phase 1: add cards`（段階1：カードを追加する）のような、処理の段階を説明するコメントを書きません。何を確かめているかは、アサーション（条件が成り立つかを確かめ、成り立たなければスクリプトを失敗させる文）やログに出す文字列で示します。

次の例は、カードを2枚追加してアプリを再起動し、カードが残っているかを確かめるスクリプトです。

```
// 前：段階を説明するコメントで手順を示す
async function checkBefore() {
  // 段階1：カードを追加する
  await addCards(2);
  // 段階2：アプリを再起動する
  await restartApp();
  assert((await countCards()) === 2, "失敗");
}

// 後：アサーションの文字列で、何を確かめたかを示す
async function checkAfter() {
  await addCards(2);
  await restartApp();
  assert((await countCards()) === 2, "再起動しても、カードが保存されている");
}
```

前の書き方では、アサーションが失敗しても「失敗」としか出ません。何を確かめていたのかは、コメントを読まなければ分かりません。

後の書き方なら、失敗したとき、「再起動しても、カードが保存されている」ことを確かめられなかったと、実行結果の文字列から分かります。

このように、手順の説明をコメントではなくアサーションの文字列に書けば、説明は実行結果にも残ります。

『Comments』の規則は、テストのスクリプトに限らず、エージェントが作るすべてのファイルに当てはまります。サブエージェントに書かせたコードの変更も含みます。

書いたコメントが本当に必要かは、レビューの前に実行する `/no-comments`（[第32章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8960d3)）が確かめます。

## 『Playbooks』：Playbookの索引

『[Playbooks](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#playbooks)』は、依頼に合うPlaybookを選ぶための索引です。**各項目には、Playbook名、そのPlaybookを使う作業、Playbookのファイルの場所が書かれています**。エージェントは、依頼に合うPlaybookを索引から選び、そのファイルを開いて、手順をTODOリストに一字一句写します。

!

- **TODOリスト**・・・ エージェントが作業の始めに作る、その作業でやることの一覧（計画）です。Cursorでは、チャットの画面に表示されます。利用者は、この一覧を見て、エージェントがどの手順を進め、どの手順を飛ばしたか（`skip: <理由>`）を確かめられます（同梱ガイド [`01-setup.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md)）。

索引の前には、Playbookの使い方と、振り分けの規則が書かれています。[『第7章 依頼は、決まった規則でPlaybookに振り分けられる』](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d#%E4%BE%9D%E9%A0%BC%E3%81%AF%E3%80%81%E6%B1%BA%E3%81%BE%E3%81%A3%E3%81%9F%E8%A6%8F%E5%89%87%E3%81%A7playbook%E3%81%AB%E6%8C%AF%E3%82%8A%E5%88%86%E3%81%91%E3%82%89%E3%82%8C%E3%82%8B)でも扱いましたが、`/poteto-mode` の中心となる規則なので、ここでも示します。

### Playbookの使い方

エージェントは、次の順にPlaybookを使います。

1. 依頼に合うPlaybookを索引から選び、そのファイルを開く
2. TODOリストを作り、最初の項目に、そのPlaybookの手順を一字一句写す。Playbookの手順にはない依頼の場合、必要な作業（例：`--json` フラグを追加する依頼なら、「テキストの出力が1バイトも変わっていないか確かめる」）は、写した手順の後ろに追加する
3. やらないと決めた手順も消さずに残し、`skip: <理由>` という形式で1行添える

### 振り分けの規則

基本的には、依頼の種類に合うPlaybook1冊が選ばれます。ただし、作業が大きいときは、依頼の種類より作業の大きさで振り分け先が決まります。

| 依頼の性質 | 振り分け先 |
| --- | --- |
| 1つのPlaybookに当てはまる、通常の規模の作業 | そのPlaybook |
| 大きな作業や、複数の箇所にまたがる作業（例：多くの呼び出し箇所にまたがる移行） | [`/figure-it-out`](https://github.com/cursor/plugins/blob/main/pstack/skills/figure-it-out/SKILL.md) |
| 利用者が席を外し、後で結果を確かめたい作業 | `/figure-it-out` |
| 当てはまるPlaybookがない作業 | `/figure-it-out` |
| 何日も続き、多数のPRと多数のサブエージェントを、1体のコーディネーターがまとめる作業 | 『[**Orchestrate**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md)』 |
| 止まらずに最後まで進めたい作業のうち、1体のエージェントが1回のセッションの中で終えられる作業（例：「終わるまで続けて」と頼む作業） | 『[**Autonomous run**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autonomous-run.md)』 |

表の2行目と3行目の作業は、『Feature』などのPlaybookに当てはまる場合でも、`/figure-it-out` へ回ります。

`/figure-it-out` は、その作業のためだけにPlaybookを設計するSkillです。決まった手順をなぞるのではなく、作業ごとに、次の3つをします。

- どこまで厳密に確かめるかを決める。作業が大きいほど、また失敗したときの影響が大きいほど、厳しくする
- 作業を、1つずつ取り込める小さな単位に分け、最も不確かな単位から進める
- 各段階で何を判断したかを、`/show-me-your-work` で記録に残す

2行目の、大きな作業を回す理由は、原文には書かれていません。本書では、作業の大きさに合わせて、厳密さや作業の分け方を決める必要があるため、と推測しています。

3行目の、席を外して後で確かめたい作業を `/figure-it-out` へ回すのは、利用者が作業が終わった後で、まとめて結果を確かめることができるからです（同梱ガイド [`07-overnight.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/07-overnight.md)）。そのため、エージェントが何をなぜ決めたかを、後からトレースできる必要があります。`/figure-it-out` は、コードを書く前に進め方を設計し、判断の記録を残すので、この必要を満たします。

『Orchestrate』との違いは、`/figure-it-out` が1回の作業の進め方を設計するのに対し、『Orchestrate』は何日も続く作業全体を運営する点です。

### 23件の索引

索引の23件を、本書で作業の種類ごとに分類すると、次のとおりです。

| 分類 | Playbook | 本書の章 |
| --- | --- | --- |
| 調べる | 『[**Investigation**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/investigation.md)』、『[**Runtime forensics**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/runtime-forensics.md)』、『[**Trace forensics**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/trace-forensics.md)』 | [第10章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ea525d) |
| 直す・改善する | 『[**Bug fix**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)』、『[**Perf issue**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/perf-issue.md)』、『[**Hillclimb**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md)』 | [第11章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6fcb42) |
| つくる | 『**Feature**』、『[**Refactoring**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/refactoring.md)』、『**Prototype**』、『[**Visual parity**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/visual-parity.md)』 | [第12章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b) |
| Skillを扱う | 『[**Authoring or modifying a skill**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md)』、『[**Eval**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md)』 | [第13章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0) |
| 届ける | 『[**Opening a PR**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md)』、『**Babysit**』、『**Shipping**』 | [第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e) |
| 長く動かす | 『[**Autonomous run**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autonomous-run.md)』、『[**Session pickup**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/session-pickup.md)』、『[**Pause safely**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/pause-safely.md)』、『[**Worktree and simulator cleanup**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/worktree-cleanup.md)』 | [第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609) |
| 多数のPRを運用する | 『[**Multi-phase or multi-PR plan**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md)』、『[**Orchestrate**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md)』、『[**Autopilot-full**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-full.md)』、『[**Autopilot-stack**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-stack.md)』 | [第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5) |

## 自分の流儀に合わせる

`/poteto-mode` はpoteto氏の流儀なので、利用者にそのまま合うとは限りません。

**合わなければ、[`/automate-me`](https://github.com/cursor/plugins/blob/main/pstack/skills/automate-me/SKILL.md)（[第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f)）で自分用のモード（`/poteto-mode` のように、自分の流儀をまとめたSkill）を作るか、pstack を fork（リポジトリを自分のアカウントに複製すること）する**必要があります。

`/automate-me` は、最近のトランスクリプトから、返答、委任、検証、コード、文章などについて繰り返し現れる利用者の流儀を見つけ出し、`<your-name>-mode`（例：`tomato-mode`）のSkillを下書きします。

`/automate-me` を使えば、利用者は、pstack を土台にしたまま、`/poteto-mode` と並べて、依頼を振り分ける自分用のSkillを持てます。

Playbook や Principle そのものを書き換えたいなら、本書では、pstack を fork して、自分の版を持つことを推奨します。

README は冒頭で「fork it. improve it. make it yours.」（fork して、改良して、自分のものにして）と書き、fork と改良を歓迎しています。

## まとめ

- **`/poteto-mode` の役割**・・・ 依頼をPlaybookへ振り分けるpstackの入口（Router）です。`SKILL.md` には、振り分けた後の作業全体にかかる規則も書かれています。
- **『Non-negotiables』**・・・ 状況ごとに、エージェントが必ず実行することの一覧です。たとえば、エージェントは、利用者に尋ねる前に、答えが実行すれば分かる事実か、人が決める判断かを分類します。
- **『Principles』と『Playbooks』**・・・ 24の原則と23件のPlaybookの索引です。エージェントは、索引から当てはまるものを選び、そのファイルを開いて読みます。
- **『Autonomy』と『Subagents』**・・・ エージェントは、取り消せない操作の前では必ず止まり、すべての委任で既定値（主エージェントが、サブエージェントを起動する度に、使用する設定）に従います。
- **『Writing the reply』と『Comments』**・・・ エージェントは、返答とコメントの規則を、書き終えてからではなく、書いている最中に守ります。
- **自分の流儀への変え方**・・・ `/automate-me` で自分用のモードを作るか、pstack を fork します。

これで[第5部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2a4af5)は終わりです。ここまでで、pstackのPlaybook、Principle、Skillをすべて解説しました。[第6部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/b22889)では、ここまでの部品を、自分のプロジェクトでどの順番に使い始めるかを扱います。最初の[第39章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7081)では、エージェントが自分のアプリを動かして変更を確かめるための検証スキルを扱います。
