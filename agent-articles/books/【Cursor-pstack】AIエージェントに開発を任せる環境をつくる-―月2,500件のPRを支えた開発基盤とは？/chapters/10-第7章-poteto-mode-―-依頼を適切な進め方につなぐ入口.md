---
title: "第7章 /poteto-mode ― 依頼を適切な進め方につなぐ入口"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:27+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 10
---

# 第7章 /poteto-mode ― 依頼を適切な進め方につなぐ入口

`/poteto-mode` は、pstackの入口です。**依頼を読み、23件のPlaybookから1冊を選び、その手順に沿って作業を進めます**。

利用者は、どのPlaybookを使うかも、どのSkillをどの順で呼ぶかも指定しなくて済みます。利用者がするのは、**ゴールとそれを確かめる方法を、自分の言葉で渡すことだけ**です。

この章では、`/poteto-mode` の呼び出し方、呼び出したときに起きること、依頼をPlaybookに振り分ける規則、良い依頼の書き方を解説していきます。

## この章の構成

この章の構成は次のとおりです。

- `/poteto-mode` は、依頼の先頭に付けて呼び出す
- 呼び出すと、3つのことが起きる
- 依頼は、決まった規則でPlaybookに振り分けられる
- 良い依頼は、目的と完了条件を自分の言葉で書く
- まとめ

## `/poteto-mode` は、依頼の先頭に付けて呼び出す

`/poteto-mode` は、**作業の依頼の先頭に付けて呼び出します**。

**`/poteto-mode` が有効になるのは、`/poteto-mode` を付けたメッセージのみです**。そのため、毎ターン有効にしたいなら、メッセージのたびに `/poteto-mode` を付ける必要があります（[後の項](#%E6%9C%89%E5%8A%B9%E3%81%AB%E3%81%AA%E3%82%8B%E3%81%AE%E3%81%AF%E3%80%81%E4%BB%98%E3%81%91%E3%81%9F%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8%E3%81%AE%E3%81%BF)）。毎ターン付けるのが手間なら、`/poteto-mode` を[Custom Mode](https://cursor.com/docs/skills)として固定できます。

!

0.15.9までのREADMEは、`/poteto-mode` を sticky mode（一度呼ぶと、後のターンでも有効なままになるモード）と説明していました。

> `/poteto-mode` is also a sticky mode: once entered it stays on across turns, applying itself when a playbook matches or the task needs rigor and staying out of the way otherwise. opt out any time by saying so.
>
> `/poteto-mode` は持続するモードでもある。一度入ると、ターンをまたいで有効なままになり、Playbookに当てはまるときや厳密さが必要なときに自ら適用され、それ以外では邪魔をしない。やめたいときは、いつでもそう言えばよい。

0.15.10以降のREADME（本書が扱う0.15.15を含む）では、この説明が消え、Custom Modeにしない場合、**`/poteto-mode` が有効になるのは、付けたメッセージのみ**、と記載されています。

> plain enter attaches it to one message only.
>
> 普通のEnterでは、1つのメッセージにだけ付く。

そのため、0.15.15では、Custom Modeにしない限り、一度付けただけの `/poteto-mode` が、後のターンまで有効なままになることはありません。

### 基本は、依頼文の頭に付けるだけ

pstackの[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)は、`/poteto-mode` を自明でない作業に対する、すべての既定の入口と位置づけ、次のような例を挙げています。

```
/poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro first, then fix and verify.
// このPRには気づきにくいバグがある。アイドル中でも750msごとにスクロールがずれる。まず再現して、それから直して、確かめて。
```

この依頼には、どのPlaybookやSkillを使うかは書かれていません。書かれているのは、起きている症状（アイドル中でも750msごとにスクロールがずれる）と、してほしい作業（まず再現し、直し、確かめる）だけです。

どのPlaybookやSkillを使うかは `/poteto-mode` が依頼の内容から選ぶので、**利用者は、症状と、してほしい作業を書けばよいだけです**。

`/poteto-mode` を適用するかどうかは、[次の項](#cursor%E3%81%A7%E3%81%AF%E3%80%81custom-mode%E3%81%A8%E3%81%97%E3%81%A6%E5%9B%BA%E5%AE%9A%E3%81%A7%E3%81%8D%E3%82%8B)で見る `reminder` が決めています。`reminder` は、新しいタスクで、Playbookに当てはまるときや厳密さが必要なときだけ `/poteto-mode` を適用し、雑談などの軽い依頼や質問には適用しないと定めています。

そのため、`/poteto-mode` を付けるか迷ったときは、付けておくと良いと私は考えています。軽い依頼や質問なら、エージェントはPlaybookの手順を踏まずに答えます。

### Cursorでは、Custom Modeとして固定できる

依頼のたびに `/poteto-mode` を入力するのが手間なら、`/poteto-mode` を[Custom Mode](https://cursor.com/docs/skills)として固定できます。Custom Modeとは、Skillを、毎ターン、エージェントのコンテキストに入れ続けるCursorの機能です。

`/poteto-mode` を補完するときに、Enterではなく `Option + Enter`（Mac）か `Alt + Enter`（Windows）を押すと、Skillが[Custom Mode](https://cursor.com/docs/skills)として追加されます。

Skillの一覧から `Use as Mode` を選んでも、同じようにCustom Modeにすることができます。

Custom Modeにすると、**利用者がモードを抜けるまで、`/poteto-mode` が毎ターンコンテキストに入ります**。どのターンで使うかは、次の `reminder`（新しいターンのたびにエージェントに渡される、短い指示）が決めます。

!

READMEは、Custom Modeを、Cursorの Agents Window（複数のエージェントを並べて管理する画面）とCLI（ターミナルから使うCursor）で使える機能と説明しています。`/poteto-help`（[第37章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/77207a)）は、それ以外の場所では、新しい作業のたびに `/poteto-mode` を付けるよう案内しています。

リマインダーの文面は、[`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) の frontmatter に `reminder` として書かれています。

```
mode: true
reminder: New task? Playbook match or rigor needed -> apply /poteto-mode. Casual turn or user opts out -> don't.
# 新しいタスクで、Playbookに当てはまるか厳密さが必要なら /poteto-mode を適用する。雑談のターンや、利用者がやめると言った場合は適用しない。
```

**この1行があるので、[Custom Mode](https://cursor.com/docs/skills)で固定したままでも、雑談などの軽い依頼・質問のターンや、利用者がモードをやめると言った場合には、エージェントはPlaybookの手順を踏みません**。

### 有効になるのは、付けたメッセージのみ

`/poteto-mode` が有効になるのは、`/poteto-mode` を付けたメッセージのみです。同梱ガイドの[`01-setup.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md)は、会話が進むにつれて、**`/poteto-mode` の効き目が薄れていく**、と記載しています（原文は it fades as the chat moves on）。

エージェントは会話が進むほど、前のメッセージのことを忘れる傾向があるためです。

同じ会話で作業を続けるときに、毎ターン `/poteto-mode` を有効にしておきたいなら、前の項のCustom Modeにします。Custom Modeをやめるときは、モードを抜けます。その場でだけ外したいときは、やめたいと伝えます。

Custom Modeにしておけば、同じ会話の中で作業を続けるときは、依頼が短くても構いません。同梱ガイドの[`02-poteto-mode.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/02-poteto-mode.md)には、次のような例が並んでいます。

```
/poteto-mode do it
// それで進めて
```

```
continue
// 続けて
```

```
keep going until done
// 終わるまで続けて
```

同ページでは、短い依頼で足りるのは、作業の組み立て（手順）をPlaybookが持ち、Custom Modeが「`/poteto-mode` を毎ターンコンテキストに入れておくからだ」と説明しています。**利用者の言葉は何をしたいか（意図）を伝え、手順どおりに厳密に進める役目はSkillが受け持ちます**。

ただし、Custom Modeで `/poteto-mode` が有効なままだと、同じ会話で別の話題に移ったときに、前のタスクの続きとして扱われることがあります。話題を変えるときの頼み方は、この章の「[話題を変えるときは『新しいタスク』と言う](#%E8%A9%B1%E9%A1%8C%E3%82%92%E5%A4%89%E3%81%88%E3%82%8B%E3%81%A8%E3%81%8D%E3%81%AF%E3%80%8C%E6%96%B0%E3%81%97%E3%81%84%E3%82%BF%E3%82%B9%E3%82%AF%E3%80%8D%E3%81%A8%E8%A8%80%E3%81%86)」で扱います。

## 呼び出すと、3つのことが起きる

`/poteto-mode` を呼び出すと、**Playbookの手順をTODOリストに写し、手順に応じてほかのSkillを呼び、決まった書き方で返答する**、という3つのことが起きます。

!

**TODOリスト**・・・ エージェントが作業の始めに作る、その作業でやることの一覧（計画）です。Cursorでは、チャットの画面に表示されます。利用者は、この一覧を見て、エージェントがどの手順を進め、どの手順を飛ばしたか（`skip: <理由>`）を確かめられます（同梱ガイド [`01-setup.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md)）。

READMEは、3つを次のように説明しています。

1. 依頼をPlaybookに照らし合わせ、TODOリストを開く。最初の項目は、そのPlaybookの手順を一字一句写したものになる
2. 手順が進むにつれて、必要なほかのSkillへ振り分ける
3. 利用者に向けて、AIらしさを取り除いた返答を書く

### 1. Playbookの手順を、そのままTODOリストに写す

`/poteto-mode` の中心にある規則です。`/poteto-mode` の節『[Playbooks](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#playbooks)』は、最初にこう定めています。

> Open a todolist whose first items are the matched playbook's steps, copied in verbatim, before any task-specific todos. A step you choose not to do stays in the list with a one-line `skip: <reason>`.
>
> TODOリストを開き、その最初の項目には、選んだPlaybookの手順を一字一句写す。タスク固有のTODOはその後ろに置く。やらないと決めた手順もリストに残し、`skip: <理由>` を1行添える。

エージェントは、**Playbookの手順を要約せずにそのまま作業の一覧にし、やらない手順も理由を添えて残します**。

この規則には、以下の2つの効き目があります。

- **Playbookの順序が、そのまま作業の骨組みになること**・・・ エージェントが自分の判断で手順を要約したり、組み立て直したりする余地が小さくなります。
- **飛ばした手順が見えること**・・・ やらない手順も `skip: <理由>` として残るので、人間は結果だけでなく、途中のエージェントの判断も点検できます。同梱ガイドの[`01-setup.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md)も、TODOリストを見れば、エージェントが何をやらないと決めたかが分かると書いています。

### 2. 手順が求めるときに、ほかのSkillを呼ぶ

Playbookの各手順には、どこでどのSkillを使うかが書かれています。`/how` や `/architect` は、起動時にまとめて呼ばれるのではなく、手順がその場面に来たときに呼ばれます。この仕組みは[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)と[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)で扱います。

### 3. 返答は、決まった書き方で書く

返答の書き方は、`/poteto-mode` の節『[Writing the reply](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#writing-the-reply)』が定めています。たとえば以下のような規則です。

- 一文一義の短い断定文にする
- 誰のための作業で何が変わるかを先に書く
- 主張には証拠か「測定した・推論した・推測」のラベルを付ける

すべてのPlaybookはこの書き方の返答で終わり、各Playbookの末尾にある「Reply」行には、そのPlaybookで報告する内容が書かれています。規則の全体は[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)で扱います。

## 依頼は、決まった規則でPlaybookに振り分けられる

振り分けの基本は、**依頼の種類（調べるだけの質問、不具合、新しい振る舞いなど）を見て、合うPlaybookを1冊選ぶこと**です。

ただし、**作業が大きいときは、依頼の種類より作業の大きさで振り分け先が決まります**。『[**Feature**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md)』などのPlaybookに当てはまる依頼でも、`/figure-it-out` や『[**Orchestrate**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md)』へ回ります。

### よくある振り分け先は5つのPlaybookと例外1つ

振り分けの全体像は、まず代表的なPlaybook5つと、当てはまるPlaybookがない場合の例外1つ（[`/figure-it-out`](https://github.com/cursor/plugins/blob/main/pstack/skills/figure-it-out/SKILL.md)）を押さえれば十分です。同梱ガイドの`02-poteto-mode.md`にある振り分けの図を、日本語にして描き直すと次のようになります。

図にあるのは代表的な振り分け先だけです。ほかに、以下の作業のPlaybookがあります。

- 指標の継続的な改善
- 実行時の症状や取得済みトレースの診断
- プロトタイプ
- 見た目の一致
- Skillの作成と評価
- 長時間の自律実行
- PRの作成
- PRの見守りと本番への反映
- PRキューの自動運転
- プロジェクト規模の統括
- 作業の引き継ぎと中断
- 複数フェーズの計画
- worktree（1つのリポジトリから、作業用のコピーを複数作るgitの機能）の掃除

23件の詳細は[第3部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/72f8ee)で扱います。

図では、依頼の種類を判定する前に、「Principlesの一覧を読む」段があります。Principleの読み方は[第9章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6b7496)で扱います。

### 大きな作業は `/figure-it-out` へ、プロジェクト規模の作業は『Orchestrate』へ回る

作業が大きいときは、個別のPlaybookより優先して、`/figure-it-out` か『**Orchestrate**』Playbookへ回ります。`/poteto-mode` の『Playbooks』にある2つの規則で、どちらも作業の大きさで振り分け先を変えるものです。

1つ目は `/figure-it-out` です。規則の原文は次のとおりです。

> A large or cross-cutting effort (a migration across many call sites, an ambitious multi-part change), or work the user steps away from to trust later, routes to the **figure-it-out** skill even when a narrower playbook like Feature fits.
>
> 大きく横断的な作業（多くの呼び出し箇所にまたがる移行、野心的な複数部分からなる変更）や、利用者が席を外してあとで信頼したい作業は、『Feature』のような狭いPlaybookが当てはまっても、figure-it-out のSkillへ回る。

エージェントは、**依頼の言葉より作業の大きさを優先して、振り分け先を決めます**。

どのPlaybookにも当てはまらない作業も `/figure-it-out` へ回ります。

`/figure-it-out` は、そのタスクのための厳密で監査可能なPlaybookを設計するSkillです。

2つ目は『**Orchestrate**』です。対象は、何日も続くプロジェクト規模の作業で、積み重なった多数のPRを、1体のコーディネーターエージェントと多数のサブエージェントで進めるものです。

2つの違いは、`/figure-it-out` がその作業1回分の進め方（Playbook）を設計するのに対し、『**Orchestrate**』は何日も続く作業全体を運営する点です。

ただし『**Orchestrate**』の説明には、1体のエージェントがセッションの予算内で終えられる作業は『[**Autonomous run**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autonomous-run.md)』へ回すよう、明示されています。

これらの規則をまとめると、次のとおりです。

| 依頼の性質 | 振り分け先 |
| --- | --- |
| 1つのPlaybookに当てはまる、通常の規模の作業 | 該当するPlaybook |
| 大きく横断的な作業、席を外してあとで確認したい作業、該当するPlaybookがない作業 | `/figure-it-out` |
| 複数日、多数のPR、多数のサブエージェントを使う継続的なプログラム | 『**Orchestrate**』 |
| 1体で終えられる長いタスク（「終わるまで続けて」など） | 『**Autonomous run**』 |

## 良い依頼は、目的と完了条件を自分の言葉で書く

同梱ガイド（[`docs/guide/`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/README.md)）の勧めをまとめると、良い依頼の書き方は以下の4つです。

1. **ゴールと確かめ方を書く**
2. **Skillを列挙しない**
3. **作業時間を完了条件にしない**
4. **話題を変えるときは「新しいタスク」と言う**

### 手順ではなく、ゴールを書く

同梱ガイドの`02-poteto-mode.md`は、依頼に詳しい仕様書は必要ないと説明しています。何が問題になっているか、何を実現したいか、そしてすでに分かっていることで作業の助けになる情報を伝えれば足ります。

ガイドには、次の不具合の依頼例があります。

```
/poteto-mode users get two notifications after a retry. repro first, then fix and verify.
// 再試行の後、ユーザーに通知が2回届く。まず再現して、それから直して、確かめて。
```

ガイドは、この「まず再現して」を丁寧さの飾りではなく、**Playbookが守る本物の制約**として扱うと説明しています。実際、この依頼は『[**Bug fix**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)』Playbookに振り分けられ、TODOリストは再現の手順から始まります。

同梱ガイドの目次も、覚えておくことを一つだけ挙げるなら、**ゴールとそれを確かめる方法を自分の言葉で渡すこと**だ、とまとめています。

確かめ方の書き方は、[第2章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/27a183)で見た同梱ガイドの例（「テキスト出力は1バイトも変えない。JSONはパースできる」）が参考になります。どちらも、エージェント自身が実行して合否を判定できる形になっています。

依頼に書くとよいものは、確かめ方だけではありません。『The Complete Guide to pstack』[Part 2](https://x.com/poteto/status/2097732320606507506)の依頼例には、受け取りたい結果の形（分かっていること、使ったデータ、有力な仮説を分けて示す）や、レビューのタイミング（進める前に確認させて）まで書かれたものがあります。

### 依頼文に入れると良い5つの項目

同梱ガイドの`02-poteto-mode.md`は、依頼文に入れると良いものを、次の5つにまとめています。**全部を入れる必要はなく、どれも1文で書けます**。

- **目的**・・・ 何が問題になっているか、何を実現したいか
- **完了条件**・・・ 合否が出る形で書く。たとえば「6万行のテスト用データの全行がエクスポートされること」は、合否が出る。「もっと良くして」や「1時間取り組んで」は、合否が出ないので、完了条件にならない
- **確認したい証拠**・・・ 実際のコマンドの出力、操作の流れの動画、保存された値、変更前と変更後の数値
- **すでに分かっていること**・・・ 症状、再現の手順、ログの1行、リンク。エージェントが探す手間を省ける
- **本物の制約**・・・ エージェントが必ず守る条件。たとえば、「まず再現して」「まだコードを変えないで」「振る舞いは変えないで」「進める前に確認させて」のように、エージェントの動きを変える言葉

ガイドは、5つをすべて含む依頼として、次の例を挙げています。

```
/poteto-mode the csv export drops its last row since yesterday's deploy. failing job id is 4812. repro first, then fix. done means the 60k-row fixture exports every row. show me the row counts before and after.
// 昨日のデプロイ以降、CSVのエクスポートで最後の行が抜ける。失敗したジョブのIDは4812。まず再現して、それから直して。完了条件は、6万行のテスト用データの全行がエクスポートされること。変更前と変更後の行数を見せて。
```

また、ガイドは、**次の2つは書かないよう**勧めています。

- **やり方**・・・ 何を実現するかなどの目的だけを書き、エージェントが利用者の思いつくやり方より、良い方法を見つける余地を残す
- **原因についての自分の推測**・・・ 最初の依頼には書かない。推測を書くと、エージェントは、利用者が指した場所だけを探すようになる。エージェントに問題を自分の言葉で言い直させてから、推測を伝える

2つを書かない理由は、『The Complete Guide to pstack』[Part 2](https://x.com/poteto/status/2097732320606507506)に書かれています。poteto氏は、最新のモデルは人よりうまくコードを書けるので、**何を実現したいかは伝えつつ、利用者が思いつかない方法で解く自由を残したい**、と述べています。やり方を細かく指示すると、この自由がなくなります。

推測を後回しにして、先にエージェントに言い直させるのも、同じ考えからです。Part 2は、言い直させると、次の3つが得られると説明しています。

- 雑多な会話を、整理された問題の説明にまとめさせられる
- **エージェントの誤解に、コードを書き始める前に気づいて直せる**
- 利用者の思い込みや、間違っているかもしれない仮説で、エージェントを誤った方向に導かずに済む

この節の内容についての詳細は[第40章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/b4b9a1#%E8%A6%81%E7%82%B92%EF%BC%9A%E5%AE%9F%E8%A3%85%E5%89%8D%E3%81%AB%E3%80%81%E5%95%8F%E9%A1%8C%E3%82%92%E8%A8%80%E3%81%84%E7%9B%B4%E3%81%95%E3%81%9B%E3%82%8B)で詳しく解説します。

### Skillを列挙しない

同梱ガイドの`02-poteto-mode.md`は、依頼でSkillを列挙することを落とし穴に挙げています。

> **Pitfall:** don't enumerate skills in your prompt ("use /how, then /architect, then /arena..."). The playbook already sequences them, and a hand-written sequence usually reorders or drops steps the playbook would have kept. Name a skill only when you want to override a specific choice.
>
> **落とし穴：** 依頼でSkillを列挙しない（「/howを使って、次に/architect、次に/arena……」）。順番はPlaybookがすでに決めていて、手書きの順番は、Playbookなら残したはずの手順を入れ替えたり落としたりしがちだ。Skillの名前を書くのは、特定の選択を上書きしたいときだけにする。

たとえば、不具合の依頼に「/howで調べて、/architectで設計して」と書くと、『**Bug fix**』Playbookが最初に置いている「自分で再現する」手順が、手書きの順番から抜け落ちるおそれがあります。ガイドの目次も冒頭で、**pstackはエージェントを細かく管理するのをやめたときに最もよく働く**、と書いています。

「[手順ではなく、ゴールを書く](#%E6%89%8B%E9%A0%86%E3%81%A7%E3%81%AF%E3%81%AA%E3%81%8F%E3%80%81%E3%82%B4%E3%83%BC%E3%83%AB%E3%82%92%E6%9B%B8%E3%81%8F)」の項で見た「まず再現して」のような言葉は、Playbookが守る制約として扱われます。**制約は依頼に書き、どう進めるかという手順はPlaybookに任せる**、という分担です。

### 「何時間続けるか」は、完了条件にならない

席を外すときは、「完了条件」を書いてから離れます。同梱ガイドの`02-poteto-mode.md`には、次の例があります。

```
/poteto-mode im stepping away. keep going until the migration check reports zero old callers. log your decisions.
// 席を外す。移行チェックが古い呼び出し元ゼロを報告するまで続けて。判断を記録して。
```

同梱ガイドの夜間実行のページ（[`07-overnight.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/07-overnight.md)）は、**時間を完了条件にすることを落とし穴に挙げています**。

「4時間これに取り組んで」はエージェントに確かめるものを何も与えず、朝には結果ではなく4時間分の動きが残るだけだからです。夜間の実行は[第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609)で取り上げます。

上の例のゴール「移行チェックが古い呼び出し元ゼロを報告する」は、エージェント自身が実行して合否を出せる判定です。このように、**完了条件には、時間の代わりに、実行して合否が出る判定を書きます**。

### 話題を変えるときは「新しいタスク」と言う

長い会話には、前のタスクのコンテキストがたまります。そのため同梱ガイドの`02-poteto-mode.md`は、話題を変えるときに「新しいタスク」と言うよう勧めています。

```
/poteto-mode new task. figure out why the cache entry survives logout. don't change any code yet.
// 新しいタスク。ログアウト後もキャッシュのエントリが残る理由を突き止めて。まだコードは変えないで。
```

つまり、**「新しいタスク」はPlaybookを選び直させる合図**です。

これを言わずに話題を変えると、進行中のPlaybookが新しい質問を前の作業の続きとして扱うことがあります。

## まとめ

- **呼び出し方**・・・ `/poteto-mode` は、依頼の先頭に付けて呼ぶpstackの入口で、自明でない作業すべての既定の入口です。有効になるのは、`/poteto-mode` を付けたメッセージのみです。毎ターン有効にしたいときは、Cursorでは `Option + Enter`（Windowsでは `Alt + Enter`）で[Custom Mode](https://cursor.com/docs/skills)として固定します。
- **呼び出したときに起きること**・・・ Playbookを選んでその手順をTODOリストに一字一句写し、手順に応じてSkillを呼び、決まった書き方で返答します。飛ばした手順は `skip: <理由>` として残るので、途中で点検できます。
- **振り分けの規則**・・・ 基本は依頼の種類で1冊を選びます。大きな作業は `/figure-it-out`、継続的なプロジェクト規模の作業は『**Orchestrate**』へ回ります。
- **良い依頼の書き方**・・・ ゴールと確かめ方を自分の言葉で書き、Skillを列挙せず、作業時間を完了条件にせず、話題を変えるときは「新しいタスク」と言います。

次の[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)では、`/poteto-mode` の中で働く3つの部品、Playbook、Skill、Principleを扱います。3つの役割の違いを解説し、本書の実例の依頼を例に、『**Bug fix**』Playbookの各手順でSkillとPrincipleがどこで働くかをたどります。
