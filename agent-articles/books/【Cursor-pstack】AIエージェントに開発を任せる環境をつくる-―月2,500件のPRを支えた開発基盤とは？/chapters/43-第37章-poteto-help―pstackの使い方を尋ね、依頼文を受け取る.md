---
title: "第37章  /poteto-help―pstackの使い方を尋ね、依頼文を受け取る"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/77207a"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:35+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 43
---

# 第37章  /poteto-help―pstackの使い方を尋ね、依頼文を受け取る

この章では、[`/poteto-help`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md) を扱います。

`/poteto-help` は、pstackの使い方についての質問に答えるSkillです。回答と一緒に、次の2つも示します。

- **利用者が次のメッセージとしてエージェントにそのまま送れる依頼文**
- **回答の根拠になったSkillや同梱ガイド（[`docs/guide`](https://github.com/cursor/plugins/tree/main/pstack/docs/guide)）のページへのリンク（出典のリンク）**

たとえば、利用者が「このブランチのレビューには、どのSkillを使えばよいか」と尋ねると、`/poteto-help` は、使うSkillと、そのSkillを使うための依頼文の例と、出典のリンクを返します。

`/poteto-help` は、このような助けを求める質問（原文では help question）には答えますが、**質問に出てきた作業（たとえばブランチのレビュー）は始めません**。

前の[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)の `/setup-pstack` は、pstackを使い始めるときに最初に実行するSkillでした。一方、`/poteto-help` は、利用者がpstackを使い始めたばかりのときや、どのSkill、Playbook、Principleを使えばよいか迷ったときに使うSkillです。

この章では、`/poteto-help` について、役割、使いどき、手順、依頼の書き方の4つの観点で解説します。

## この章の構成

この章の構成は次のとおりです。

- 役割：質問に答え、依頼文と出典のリンクを示す
- 使いどき：pstackを使い始めたばかりのときや、どのSkill、Playbook、Principleを使えばよいか迷ったとき
- 手順：利用者が何を求めているかを見極め、求めていることに合わせて回答する
- 依頼の書き方：`/poteto-help` の後に、質問を書く
- まとめ

## 役割：質問に答え、依頼文と出典のリンクを示す

`/poteto-help` は、利用者の質問に、次の3つを返します。

- **質問への回答**
- **利用者が使用する依頼文**・・・ 回答に合う依頼文の例を1つ、コードブロックで示す
- **出典のリンク**・・・ 回答の根拠になったSkillや同梱ガイドのページへのリンク

### 助けを求める質問には作業を始めずに答え、作業の依頼なら作業を進める

`/poteto-help` の [`SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md) は、助けを求める質問に作業を始めずに答える理由を、次のように書いています。

> For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.
>
> 助けを求める質問なら、作業は始めるな。利用者が尋ねたのは「どうすればよいか」であり、pstackの実行は実際にトークンを使うので、依頼文を送るのは利用者に任せよ。

トークンとは、AIのモデルが読み書きする文章の量を数える単位です。トークンを多く使うほど、費用も多くかかります。pstackは、サブエージェントやパネル（同じ問いを複数のモデルに解かせて比べる仕組み。[第6章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/33f073)）を動かす分だけ、トークンを余分に使います。そのため、`/poteto-help` は、作業を始めるかどうかを利用者に任せます。

一方、作業の依頼について、`/poteto-help` は質問として扱いません。たとえば、「pstackでこの不具合を直して」という prompt は、作業の依頼に該当します。この場合、エージェントは、[`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md)（[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)）の `SKILL.md` を読み、その手順に従って作業を進めます。あわせて、エージェントは利用者に、`/poteto-mode` をCustom Mode（Skillを毎ターン、エージェントのコンテキストに入れ続けるCursorの機能。[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)）にすれば有効なままになることを、一度だけ伝えます。

### 質問とマッピングされたファイルを、引用する前に読む

`/poteto-help` の [`SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md) には、利用者の質問と、エージェントが行う回答の根拠になるファイル（`/blast-radius` の `SKILL.md`、`07-overnight.md` など）とのマッピングが書かれています。ここでいうマッピングとは、「この質問には、このファイルを読んで答える」という対応のことです。

つまり、`/poteto-help` は、想定した質問ごとに、どのファイルを読んで答えるかを、あらかじめ決めている、ということです。

マッピング先には、次の7種類があります。

- Skill
- Playbook
- Principle
- 同梱ガイドのページ
- **README**・・・ pstackのREADMEです。エージェントは、導入について聞かれたときに、インストールのコマンド（`/add-plugin pstack`）と、始めるための2つの手順（`/setup-pstack` の実行と、`/poteto-mode` の使い方）が書かれた節を示します。
- **Cursorのドキュメント**・・・ Cursorのskillsのドキュメントです。エージェントは、`/poteto-mode` を毎ターン有効にする方法（Custom Mode）が話題になったときに、このドキュメントを示します。
- **`/poteto-help` 自身の参照ファイル**・・・ 次の2つがあります。
  - [`references/prompting.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/references/prompting.md): 依頼文の書き方の手引きです。エージェントは、利用者が送る依頼文を一緒に考えるときに、この手引きを読みます。また、エージェントは、作業が依頼と違う方向に進んだとき（例：再現だけを頼んだのに、エージェントが直し始めたとき）にも、エージェントの動作を1行で修正するための依頼文を探すために、この手引きを読みます。
  - [`references/recipes.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/references/recipes.md): 依頼文のサンプル集です。サンプルには、`<symptom>`（症状）のように、利用者ごとに中身が変わる部分が空けてあります。エージェントは、利用者の質問に合うサンプルを選び、空けてある部分に利用者の実際の内容を入れて、選んだサンプルを返答の依頼文の例にします。たとえば、エージェントは、不具合のサンプル `/poteto-mode <symptom>. repro first, then fix and verify.` の `<symptom>` に、「再試行の後、ユーザーに通知が2回届く」という利用者の症状を入れます。

種類ごとに、例を1つずつ挙げます。

| 種類 | `SKILL.md` の記述（原文） | 訳 | マッピング先 |
| --- | --- | --- | --- |
| Skill | Know what a small diff could break outside itself | 小さな差分が、差分の外で壊しうるものを知りたい | [`/blast-radius`](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md)（[第28章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880)） |
| Playbook | "babysit this pr" | このPRの面倒を見て | 『[Babysit](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/babysit.md)』（[第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e)） |
| Principle | The reply claims success from a green build | 返答が、ビルドが通ったことだけを根拠に成功と言っている | 『[Prove It Works](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md)』（[第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019)） |
| 同梱ガイド | An overnight run moved but finished nothing | 夜通し動かした作業が、進みはしたが何も終わっていない | [`07-overnight.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/07-overnight.md) |
| README | The README and guide page 1 have the details. | 詳しくは、READMEと同梱ガイドの1ページ目にある | [README](https://github.com/cursor/plugins/blob/main/pstack/README.md) |
| Cursorのドキュメント | Link Cursor's skills docs when this comes up. | この話題になったら、Cursorのskillsのドキュメントへのリンクを示す | [Cursorのskillsのドキュメント](https://cursor.com/docs/skills) |
| 参照ファイル | For a run that drifts, `references/prompting.md` has one-line steers. | 作業がずれたときは、`references/prompting.md` に、エージェントの動作を1行で修正するための依頼文がある | [`references/prompting.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/references/prompting.md) |

エージェントが利用者の質問に、答えるために必要な詳しい情報は、`/poteto-help` の `SKILL.md` ではなく、マッピングされたファイルに書かれています。そのため、エージェントは、**マッピングされたファイルの内容を回答に引用する前に、マッピングされたファイルを読みます**。

`/poteto-help` の `SKILL.md` の記述と、マッピングされたファイルの内容が食い違うときは、エージェントは、マッピングされたファイルの方を信頼します。

## 使いどき：pstackを使い始めたばかりのときや、どのSkill、Playbook、Principleを使えばよいか迷ったとき

[README](https://github.com/cursor/plugins/blob/main/pstack/README.md) は、`/poteto-help` の使いどきを、次のように説明しています。

> you're new to pstack, or unsure which skill, playbook, or principle fits.
>
> pstackを使い始めたばかりのとき、または、どのSkill、Playbook、Principleが合うか分からないとき。

**`/poteto-help` が動くのは、利用者が `/poteto-help` と入力したときだけです**。`/poteto-help` は `disable-model-invocation: true` の設定を持つので（[第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f)）、エージェントが会話の内容から自分でこのSkillを選ぶことはありません。また、`/poteto-mode` もPlaybook（作業の種類ごとの進め方を定めた手順書）も、手順の中で `/poteto-help` を呼びません。

## 手順：利用者が何を求めているかを見極め、求めていることに合わせて回答する

手順は次のとおりです。

1. 利用者が「何を求めているか」と「利用者の環境」の2つを確かめる
2. 利用者の質問が、5つの場面の「どれに該当するか」に合わせて回答する
3. 質問への回答、利用者が使用する依頼文、出典のリンクの順に返答する

ここからは、各手順を1つずつ見ていきます。

### 1. 利用者が「何を求めているか」と、「利用者の環境」の2つを確かめる

エージェントはまず、利用者のメッセージとそれまでの会話から、利用者が何を求めているかを読み取ります。  
`/poteto-help` は、利用者が求めることを、次の5つの場面に分けています（カッコ内は原文）。

- pstackを導入するとき（Get set up）
- `/poteto-mode` で作業を始めるとき（Start a task with `/poteto-mode`）
- 作業に合うSkillを選ぶとき（Pick a skill for a situation）
- 作業がうまくいかなかったとき（Fix a run that went wrong）
- pstackを自分用にしたいとき（Make pstack my own）

エージェントは、利用者の質問が「どの場面のものか」を判断できるときは、聞き返さずに、`SKILL.md` のその場面の節（例：節『[Get set up](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md#get-set-up)』、節『[Pick a skill](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md#pick-a-skill)』など）に沿って回答します。  
たとえば、「PRのレビューにはどのSkillを使えばよいか」は、「[Pick a skill](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md#pick-a-skill)」の場面の質問です。

エージェントがどの場面の質問かを判断できないときは、**5つの場面を選択肢として示し、利用者に1つだけ質問します**。そして、利用者が選んだ場面についてだけ回答します。

ただし、利用者の環境によって、適切な回答が変わることがあります。  
そこで、エージェントは次の2つを確かめ、確かめた結果によって、回答が変わるときだけ、その結果を利用者に伝えます。

- **`~/.cursor/rules/pstack-models.mdc`（`/setup-pstack` が書き出す、役割ごとのモデルを決めたルールのファイル）があるか**・・・ このファイルがなければ、利用者はまだ `/setup-pstack`（[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)）を実行していないと判断できます。その場合、エージェントは、どの役割のサブエージェントも既定のモデルで動くことを、利用者に伝えます。
- **プロジェクトに検証スキルがあるか（`verify-*` という名前のSkillか、アプリを動かす別の仕組みがあるか）**・・・ どちらもなければ、エージェントには、アプリを決まった手順で動かして確かめる方法がありません。そのため、利用者が `/poteto-help` に尋ねた質問が、変更が正しく動くことを確かめる方法についてのもの（例：「この修正が動くことを、どう確かめればよい？」）なら、エージェントは、回答の中で `/create-verification-skill`（[第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca)）を紹介します。

`~/.cursor/rules/pstack-models.mdc` がないときは、エージェントは、役割ごとのモデルと推論の予算（役割のモデルの推論の強さ（Effort Level）を、一度に決める設定。[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)）を今決めるかを、利用者に尋ねることがあります。

エージェントが尋ねるのは、ルールファイルがないことがエージェントの回答に関係する場合で、次の3つです。

- 利用者が、pstackを使い始めたばかりのとき
- 利用者の質問が、導入や費用についてのとき
- どのモデルが動くかによって、エージェントの回答が変わるとき

エージェントが、「モデルを今決めるか」を利用者に尋ねるのは、1つのチャットで1回までです。  
また、エージェントが、利用者の質問が「どの場面のものか」を判断できないときは、「モデルを今決めるか」の質問を、5つの場面から選ぶ質問と一緒に尋ねます。

「モデルを今決めるか」の質問で、エージェントが示す選択肢は、次の2つです。

- **今決める**・・・ エージェントは、利用者に `/setup-pstack` と入力するよう伝え、利用者の質問にも回答する
- **後で決める**・・・ エージェントは、利用者の質問に回答し、利用者が `/setup-pstack` を実行するまでは、どの役割も既定のモデルで動くことを、回答に1行添える

### 2. 利用者の質問が、5つの場面のどれに当たるかに合わせて回答する

エージェントが回答する内容は、場面ごとに決まっています。  
ここからは、5つの場面それぞれで、エージェントが「何を回答するか」を見ていきます。最後に、5つの場面のほかに回答が決まっている、PlaybookとPrincipleについての質問を見ます。

#### pstackを導入するとき

利用者がpstackの導入について尋ねたときは、エージェントは、まず次の3つの手順を回答します。

1. チャットで `/add-plugin pstack` と入力するか、サイドバーの Customize から、pstackをインストールする
2. `/setup-pstack` を実行する。`/setup-pstack` は、推論の予算を利用者に尋ね、役割ごとにモデルを割り当て、ルールを書き出す。このルールは、新しいチャットから効く
3. `/poteto-mode` で、作業の目的と、合否が出る確認方法を書いて、実際の作業を1つ始める

**利用者がpstackをインストールしただけでは、何も変わりません**。利用者がSkillを呼ぶまで、pstackは動かないからです。ただし、`/setup-pstack` だけは、利用者が名前を入力しなくても、「configure pstack models」（pstackのモデルを設定して）のような利用者の言葉から、エージェントが自動で読み込みます。

また、エージェントは、依頼文の書き方の手引き（[`references/prompting.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/references/prompting.md)）に沿って、利用者の最初の依頼文を一緒に考えることを申し出ます。

費用（トークンの使用量）が心配な利用者には、エージェントは、トークンがどこで使われ、どうすれば減らせるかを回答します。  
pstackがトークンを余分に使うのは、主にサブエージェントとパネル（同じ問いを複数のモデルに解かせて比べる仕組み）が原因です。  
トークンの使用量を減らす方法は、次の4つがあります。

- `/setup-pstack` を実行し直し、推論の予算を小さくするか、安いモデルを選ぶ
- 役割を `auto` か `inherit-parent`（[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)）にして、チャットのモデルで動かす。チャットが Auto（Cursorがモデルを自動で選ぶ設定）や安いモデルで動いているときに、トークンを減らせる
- パネルの役割（`arena runners` など、パネルに複数のモデルを並べる役割。[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)）に並べるモデルを減らす。並べたモデル1つにつき、サブエージェントが1つ起動する
- `/poteto-mode` は、厳密さが必要な作業にだけ使う

pstackがCursor以外のツールでも動くかを尋ねられたときの回答も、この場面に含まれています。pstackはCursor向けに作られています。pstackのSkillは、Agent Skills（複数のAIツールで共通に使えるSkillの書き方）の形式で書かれているので、ほかのツールでも読めます。ただし、作業を進めるSkill（例：`/poteto-mode`・`/how`・`/why`・`/teach`）の多くは、役割（例：コードを書く役割、文章と判断を受け持つ役割）を持つCursorのサブエージェントを起動します。また、起動したサブエージェントは、`/setup-pstack` で役割ごとに決めたモデルで動きます（[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)）。

さらに、Custom Modeと `/loop`（エージェントを繰り返し起こし直すCursor組み込みのコマンド。[第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609)）はCursorの機能です。そのため、ほかのツールでは、サブエージェントを起動する部分や、Custom Mode、`/loop` が動かない場合があります。

#### `/poteto-mode` で作業を始めるとき

利用者が `/poteto-mode` での作業の始め方を尋ねたときは、エージェントは、まず `/poteto-mode` の動き方を回答します。`/poteto-mode` は、作業に合うPlaybookを選び、その手順をTODOリスト（エージェントが作業の始めに作る、その作業でやることの一覧）に写し、手順で必要になったときにほかのSkillを実行します。飛ばした手順も、`skip: <理由>` としてリストに残ります。そのうえで、エージェントは、主に次の3つを回答します。

- **良い依頼文には、目的と完了条件を書く**・・・ 依頼文に、使うSkillは並べません。利用者が自分でSkillを並べると、Playbookなら踏むはずの手順が抜けたり、入れ替わったりしやすいからです。依頼文の書き方は、[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)で扱いました。
- **会話の途中で別の作業に移るときは、「新しいタスク」（new task）と伝える**・・・ そう伝えると、`/poteto-mode` はPlaybookを選び直します。
- **`/poteto-mode` が有効なままになるかは、呼び出し方で決まる**・・・ 違いは、次のとおりです。

| 呼び出し方 | `/poteto-mode` の効き方 |
| --- | --- |
| Custom Modeにせず、メッセージに `/poteto-mode` を付けて送る | そのメッセージにだけ効き、会話が進むと効き目が薄れる |
| `Option + Enter`（Mac）か `Alt + Enter`（Windows）、または `Use as Mode` | Custom Modeになり、毎ターンコンテキストに入る |

!

- **Custom Mode**・・・ Skillを、毎ターン、エージェントのコンテキストに入れ続けるCursorの機能。利用者がモードを抜けるまで続く
- **Use as Mode**・・・ Skillの一覧から、そのSkillをCustom Modeとして使う操作

Custom Modeにした `/poteto-mode` は、雑談のターンには適用されません。また、Cursorのドキュメントは、Custom ModeをAgents Window（複数のエージェントを並べて管理する画面）とCLI（ターミナルから使うCursor）で使えると説明しています。Agents WindowとCLI以外の場所では、エージェントは、新しい作業のたびに `/poteto-mode` を付けるよう勧めます。

`/poteto-mode` を有効なままにする方法が話題になったときは、エージェントは、[Cursorのskillsのドキュメント](https://cursor.com/docs/skills)へのリンクも示します。

また、`/poteto-mode` は、Playbookの手順で起動するサブエージェントに、`poteto-agent`（`/poteto-mode` のルールを読んでから作業を始めるサブエージェント。[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)）を使います。利用者が自分の依頼でエージェントにサブエージェントを起動させる場合にも、サブエージェントに `/poteto-mode` のルールを読んでから作業させることができます。サブエージェントにルールを読ませたい場合、利用者は、依頼文の中に `subagent_type: "poteto-agent"` と記述して、サブエージェントを起動するよう、エージェントに頼みます。依頼文の例は、次のとおりです（本書で作成した例です）。

```
subagent_type: "poteto-agent" のサブエージェントを起動して、src/auth/ の認証処理を読ませ、問題点を報告させてください。
```

`subagent_type` は、エージェントがサブエージェントを起動するときに、どの種類のサブエージェントを使うかを指定する項目です。READMEによれば、`poteto-agent` は、親のエージェント（サブエージェントを起動する側のエージェント）が `subagent_type: "poteto-agent"` を指定して起動します。`poteto-agent` の定義は、pstackに同梱されたファイル（[`agents/poteto-agent.md`](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md)）に書かれているため、利用者が設定ファイルを用意する必要はありません。

#### 作業に合うSkillを選ぶとき

作業に合うSkillを尋ねられたとき、**エージェントが基本として勧めるのは `/poteto-mode` です**。`/poteto-mode` は、Playbookの手順で必要になったときに、ほかのSkillの多くを自動で実行するからです。

ただし、利用者が、Playbookが行う作業より多くのことや、その一部だけを望むときは、エージェントは、目的に合うSkillを直接勧めます。たとえば、Playbookの手順を踏まずに、コードの動き方の説明だけがほしいときは、`/how` が合います。

Skillを勧める前に、エージェントは、そのSkillの `SKILL.md` を読みます。そして、そのSkillを使うための依頼文の例を1つ示します。

目的に合うSkillを直接勧めるとき、エージェントは、節『[Pick a skill](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/SKILL.md#pick-a-skill)』にある対応表から、利用者の質問・依頼に合うSkillを選びます。  
対応表は、次のとおりです。

利用者がしたいことと、使うSkillの対応表（Pick a skill）

| 利用者がしたいこと | Skill |
| --- | --- |
| 自明でない作業を、厳密に進める | `/poteto-mode`（[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)） |
| 今のコードの動き方や、新しいコードを置く場所を知る | `/how`（[第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746)） |
| コードがこの形になっている理由や、数値の出どころを知る | `/why`（[第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746)） |
| 変更や仕組みを、分かりやすく説明してもらう | `/teach`（[第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746)） |
| ある話題についての、自分の最近の作業を思い出す | `/recall`（[第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746)） |
| 小さな差分が、差分の外で壊しうるものを知る | `/blast-radius`（[第28章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880)） |
| 関数の境界をまたぐコードを書く前に、型とモジュールの形を決める | `/architect`（[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)） |
| 1つの課題に複数の案を出させ、良い部分を1つにまとめる | `/arena`（[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)） |
| 複数のクラウドのエージェントに、範囲を分けて並列に確かめさせるか、同じ仕事を競わせる | `/swarm`（[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)） |
| 異なるモデルに差分をレビューさせ、壊そうとさせる | `/interrogate`（[第28章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880)） |
| 手元で安く動くテストがあるとき、テストを先に書いて不具合を直す | `/tdd`（[第31章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ad5727)） |
| `.ts` や `.tsx` の作業に、TypeScriptの規則を当てる | `/typescript-best-practices`（[第30章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f9a46)） |
| レビューの前に、書いた本人ではない審査役（Comment Sicko）に、コードの中のコメントを消させる | `/no-comments`（[第32章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8960d3)） |
| 文章から、AIが書いたと分かる癖を取り除く | `/unslop`（[第33章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b)） |
| ドキュメント、RFC、README、PRの説明、コミットメッセージを、決まった基準で書く | `/technical-writing`（[第33章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b)） |
| 直前の返答を、平易な言葉で伝え直してもらう | `/bro`（[第33章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/44857b)） |
| エージェントに、アプリを決まった手順で動かして確かめる方法を与える | `/create-verification-skill`（[第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca)） |
| 検証スキルと、その Feature Map（機能ごとに、操作の仕方と確かめる結果をまとめた文書）を、今のアプリに合わせ直す | `/maintain-verification-skill`（[第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca)） |
| 性能の数値を、報告する前や、その数値をもとに作業する前に点検する | `/benchmark-checklist`（[第27章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/167c91)） |
| 大きな変更や、多くの箇所にまたがる変更、席を離れている間に任せて後で確かめたい変更を進める | `/figure-it-out`（[第23章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/3ce2b2)） |
| 作業の間に判断の記録を残し、後で確かめる | `/show-me-your-work`（[第29章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/724887)） |
| 役割ごとのモデルと、推論の予算を決める | `/setup-pstack`（[第36章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8487f0)） |
| 自分の仕事の進め方を、`/poteto-mode` のような自分用のモードのSkillにする | `/automate-me`（[第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f)） |
| 終えた作業で分かったことを、Skillの修正に反映する | `/reflect`（[第34章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f70847)） |
| エージェントが、このリポジトリで同じ間違いを繰り返さないようにする | `/correct`（[第35章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/fe17ab)） |
| ボタンを押すと、webhook 経由で Grok Bot を起こすページを作る | `/make-bot-ui`（[第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f)） |
| pstackの中で、どこに何があるかを知る | `/poteto-help`（この章） |

対応表にないSkillがpstackにあるときは、エージェントは、そのSkillの frontmatter（`SKILL.md` の先頭にある設定欄）の `description`（Skillの説明）を読んで勧めます。Principle（`principle-*`）は、対応表ではなく、後の「[PlaybookとPrincipleについての質問](#playbook%E3%81%A8principle%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%E3%81%AE%E8%B3%AA%E5%95%8F)」で扱います。

また、`/poteto-help` は、取り違えやすいSkillやPlaybookを、次のように区別しています。

- **`/how`、`/why`、`/teach`**・・・ `/how` はコードが何をしているかを、`/why` はその理由を説明する。`/teach` は、その一方か両方を動かし、結果を分かりやすく説明する（[第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746)）
- **`/arena` と `/swarm`**・・・ `/arena` は、すべてのエージェントに同じ課題を与え、良い部分をまとめる。`/swarm` は、複数のエージェントに、仕事を範囲に分けて担当させるか、同じ仕事を競わせ、1つの報告を返す（[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)）
- **`/architect`**・・・ 設計を決めると、すぐに実装に進む。実装の前に設計を確かめたいときは、「with checkpoint」と付ける（[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)）
- **`/interrogate` と `/blast-radius`**・・・ `/interrogate` は差分そのものをレビューする。`/blast-radius` は差分の外で壊れるものを探し、その変更が安全だと言える1つの事実を確かめる（[第28章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/997880)）
- **`/recall` と『Session pickup』**・・・ `/recall` は、最近の複数のチャットからコンテキストを組み立て直す。特定の1つのチャットやブランチの作業を再開するのは、『Session pickup』Playbookの役目（[第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746)、[第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609)）
- **`/figure-it-out`、『Orchestrate』、『Autonomous run』**・・・ `/figure-it-out` は、厳密に進める1回の作業を設計する。『Orchestrate』Playbookは、何日も続き、多くのPRにまたがる作業を運用する。『Autonomous run』Playbookは、1つの作業を、終わりの条件を満たすまで進める（[第23章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/3ce2b2)、[第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5)、[第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609)）

さらに、`/poteto-help` は、pstackに含まれないものも挙げています。

- `/deslop`、`control-cli`、`control-ui` は、`cursor-team-kit` という別のプラグインのSkill
- `/loop` と `/create-skill` は、Cursorに組み込まれた機能
- pstackに `/orchestrate` というSkillはない。『Orchestrate』は `/poteto-mode` のPlaybook。`/` のメニューに `/orchestrate` が出るなら、それはほかのプラグインのSkill

#### 作業がうまくいかなかったとき

作業がうまくいかなかったときの回答は、症状ごとに決まっています。

| 症状 | 直し方 |
| --- | --- |
| 数ターンで、モードが効かなくなった | Custom Modeにせずに始めたため。Custom Modeで始めるか、作業のたびに `/poteto-mode` を付ける |
| 質問が、前の作業の次の手順として扱われた | 「新しいタスク」（new task）と伝えるか、このターンにはモードを使わなくてよいと伝える |
| モデルを変えたのに、効かなかった | `/setup-pstack` のルールは新しいチャットから効く。新しいチャットを始める |
| 思ったより費用がかかった | 「pstackを導入するとき」の回答にある、トークンを減らす4つの方法を使う |
| Skillが自動で読み込まれなかった | 利用者の言葉から自動で読み込まれるのは `/setup-pstack` だけ。ほかのSkillは、利用者が入力したときか、`/poteto-mode` が動かしたときに読み込まれる。ただし、`/poteto-mode` がすべてのSkillを動かすわけではない |
| 並列に動かしたエージェントが、互いのファイルを上書きした | エージェントごとに worktree を分けるか、それぞれが自分のマシンを持つクラウドのエージェントで動かす |
| 夜通し動かした作業が、進みはしたが何も終わっていない | `/loop` には、時間の長さではなく、合否が出る確認方法を渡す |
| エージェントの返答が、ビルドが通ったことだけを根拠に成功と言っている | 実際のコマンドの出力、操作の流れ、保存された値、プロファイル（性能の計測結果）のどれかを見せるよう頼む。Principle『Prove It Works』（[第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019)）の考え方 |

!

- **worktree**・・・ 1つのリポジトリに、作業ディレクトリを追加で作るgitの機能（[第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b)）

#### pstackを自分用にしたいとき

pstackを自分用にしたいときの回答は、次の4つです。

- `/automate-me`（[第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f)）で、自分の作業の履歴から、`/poteto-mode` と並べて使う自分用のモードのSkillを作る
- 作業の後に `/reflect`（[第34章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f70847)）を使い、分かったことを、主に既存のSkillの修正案にする（`/reflect` の `SKILL.md` によれば、まれに、新しいSkillを作る案にもなる）。Skillに反映されるのは、利用者が承認した案だけ
- `/poteto-mode write a skill for <作業の流れ>` で、『Authoring or modifying a skill』Playbookを動かす。Skillを変えた効果は、『Eval』Playbookで測る。このとき、テストを受けるエージェントには、テスト中であることを知らせない（どちらも[第13章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0)）
- うまく動かないSkillは、問題が起きた機能開発のPRの中では直さず、そのSkillを直すための別のPRで直す

#### PlaybookとPrincipleについての質問

5つの場面のほかに、`/poteto-help` は、PlaybookとPrincipleについての質問への回答も決めています。

##### Playbookについての質問

Playbookは `/poteto-mode` の中にある手順書で、Skillではないので、`/` で呼び出せません。`/poteto-mode` が有効なときに、利用者が作業を説明すれば、合うPlaybookが選ばれます。  
次のような言い方をすれば、利用者はPlaybookを直接選べます。

言い方と、動くPlaybook（原文の箇条書きを、本書で表にしたもの）

| 言い方 | 動くPlaybook |
| --- | --- |
| 「babysit this pr」（このPRの面倒を見て）、「check on pr 123」（PR 123の状態を確認して） | 『Babysit』 |
| 「land the stack」（スタックをtrunkに取り込んで） | 『Shipping』 |
| 「take over this branch」（このブランチを引き継いで） | 『Session pickup』 |
| 「pause safely」（安全に一時停止して） | 『Pause safely』 |
| 「full autopilot on this queue」（このキューをfull autopilotで進めて） | 『Autopilot-full』 |
| 「stack them, don't ship」（スタックにして、本番には入れないで） | 『Autopilot-stack』 |
| 「run the eval playbook」（Eval Playbookを実行して） | 『Eval』 |

ただし、表の言い方は、`/poteto-mode` を付けて使います。`/poteto-mode` を付けずに使うと、Playbookではなく、同じ仕事をするCursor自身のSkillが動くことがあるからです。

表にないPlaybookを動かすときは、利用者は、`/poteto-mode` が有効なときに作業を依頼する必要があります。`/poteto-mode` は、利用者が説明した作業を、`/poteto-mode` の `SKILL.md` の節『[Playbooks](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#playbooks)』（[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)）の各項目と照らし合わせて、合うPlaybookを選びためです。各項目には、そのPlaybookを使う作業（例：『Bug fix』なら、報告された不具合を再現し、原因を突き止めて直す作業）が書かれています。また、一部の項目には、そのPlaybookを選ばせる言い方の例（例：『Prototype』の「mock it up」）も書かれているので、その例を参考にPlaybookを起動すると良いと思います。

計画の立て方を尋ねられたとき、エージェントは、**pstackには計画を書くための専用のSkillがない**ことを伝えます。そのうえで、エージェントは、計画を立てる方法として、次の3つを示します。

- CursorのPlan Mode（実装の前に計画を立てるCursorのモード）を、pstackと一緒に使う
- 何段階にも分かれる作業や、スタックしたPR（前のPRの上に次のPRを重ねる並べ方）にまたがる作業なら、`/poteto-mode` に計画を頼む。このとき、『Multi-phase or multi-PR plan』Playbookが動く（[第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5)）
- 設計についての問いなら、『Prototype』Playbook（[第12章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b)）か `/architect`（[第24章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/2ad346)）を使う

##### Principleについての質問

Principleは、作業中の判断の決まりを1つだけ書いた、短いSkillです（[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)）。`/poteto-mode` は、Principleを読み、返答の中で、判断に影響したPrincipleの名前と、そのPrincipleによって変わった選択を挙げます（[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)）。利用者がPrincipleを直接呼ぶことは、ほとんどありません。代わりに、利用者は、「apply prove it works. show me the real output.」（『Prove It Works』を当てはめて。実際の出力を見せて）のように、Principleの名前を使って、作業の方向を修正することができます。なお、`/principle-<名前>` と入力すれば、必要なときにPrincipleを読み込むこともできます。

Principleについての質問には、エージェントは、同梱ガイドの [`08-principles.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md) を示します。このページには、24件のPrincipleの一覧があります（`/poteto-help` の `SKILL.md` には、Principleの一覧はありません）。

Principleの一覧（24件。詳しくは[第4部](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4b3166)）

| Principle | 概要 | 解説 |
| --- | --- | --- |
| [Laziness Protocol](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-laziness-protocol/SKILL.md) | コードの削除を優先し、問題を解決する最小の変更を選ぶ | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Subtract Before You Add](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-subtract-before-you-add/SKILL.md) | 機能を追加する前に、使われていないコードや重複した検証などの複雑さを削る | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Minimize Reader Load](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-minimize-reader-load/SKILL.md) | 読み手がたどる間接参照の層と、覚えておく必要があるコードの状態を減らす | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Foundational Thinking](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-foundational-thinking/SKILL.md) | ロジックを書く前に、データ構造と土台（CI、lint、テスト基盤、共有の型など）を決める | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Redesign from First Principles](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-redesign-from-first-principles/SKILL.md) | 新しい要件を既存の設計に後付けせず、最初からあった前提として設計を組み直す | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Attack the Premise](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-attack-the-premise/SKILL.md) | 同じ前提に立つ修正をさらに重ねず、次の修正を書く前に、その前提そのものを疑う | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Outcome-Oriented Execution](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-outcome-oriented-execution/SKILL.md) | 移行途中のコードの整合性を保つための一時的なコードより、確かめられる最終形を優先する | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Experience First](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-experience-first/SKILL.md) | 実装の都合より、ユーザーの体験を選び、機能を少なく作ってよく仕上げる | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Exhaust the Design Space](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-exhaust-the-design-space/SKILL.md) | 形の異なる2〜3案のプロトタイプを作り、並べて比べてから設計を決める | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Build the Lever](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-build-the-lever/SKILL.md) | 手作業の代わりに、作業をする道具か、作業の正しさを証明する道具（codemod、スクリプト、生成器、サブエージェントが従うSkill）を作る | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Model the Domain](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md) | ドメインを、散らばった条件分岐ではなく構造（状態機械、型付きのオブジェクト、参照表、reducerなど）で表す | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Boundary Discipline](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-boundary-discipline/SKILL.md) | 検証とエラー処理を外からデータが入る境界に集め、境界の内側のコードでは、型の付いた値を確かめ直さずに使い、業務のロジックを純粋関数に保つ | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Type System Discipline](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-type-system-discipline/SKILL.md) | 型の検査を使い、ありえない状態をコンパイルの時点で作れなくする | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Make Operations Idempotent](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-make-operations-idempotent/SKILL.md) | 状態を変える操作を、何度実行しても、途中から実行し直しても、最後は同じ状態になるように作る | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Migrate Callers Then Delete Legacy APIs](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | 呼び出し元を新しいAPIに移し、その変更の中で古いAPIも消す | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Separate Before Serializing Shared State](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md) | 複数の主体が共有する書き込み先を先に分け、分けられないときだけ、ロックなどで書き込みを直列化する | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Prove It Works](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md) | 作業の結果を、ビルドの成功のような代理指標ではなく、実際に動かした機能や実際の値を直接見て確かめる | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Fix Root Causes](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-fix-root-causes/SKILL.md) | 不具合の症状を隠すガードを追加せず、症状を起こした根本原因を突き止めて直す | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Sequence Work into Verifiable Units](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-sequence-verifiable-units/SKILL.md) | 作業を確かめられる小さな単位に分け、各単位のチェック（テストなど）が通ってから次へ進み、コミットを正しさを示す順に並べる | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Test Behavior, Not Implementation](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-test-behavior-not-implementation/SKILL.md) | コードを、そのコードを使う側と同じ方法で呼び、観察できる結果を、テストに直接書いた期待値と比べる | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Explain the Number](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-explain-the-number/SKILL.md) | 測った数値を信じる前に「何がその数値を頭打ちにしているか」を突き止め、エラーやキャッシュなど、別のものを測った可能性を証拠で消す | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Guard the Context Window](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-guard-the-context-window/SKILL.md) | 大きな出力や文書をサブエージェントに読ませ、主スレッドには要約だけを置く | [第20章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/c155cc) |
| [Never Block on the Human](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-never-block-on-the-human/SKILL.md) | 元に戻せる作業は人間の確認を待たずに進めて結果を見せ、元に戻せない操作だけを実行する前に人間に確認する | [第20章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/c155cc) |
| [Encode Lessons in Structure](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) | 繰り返し必要になる修正を、文章の指示ではなく仕組み（lintのルール、メタデータのフラグ、実行時チェック、スクリプト）に組み込む | [第21章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dd2d9f) |

### 3. 質問への回答、利用者が使用する依頼文、出典のリンクの順に返答する

エージェントは、次の順で返答します。

1. 質問への回答
2. 利用者が使用する依頼文の例を1つ、コードブロックで示す
3. 出典のリンク

`/poteto-help` に同梱された依頼文のサンプル集（[`references/recipes.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/references/recipes.md)）の中に、利用者の質問に合うサンプルがあれば、エージェントは、そのサンプルの空けてある部分に利用者の実際の内容を入れて、返答の依頼文の例にします。また、エージェントは、利用者がpstackの全体像を求めない限り、返答を短くします。

サンプル集は、Understand（理解する）、Build（作る）、Design and plan（設計し、計画する）、Review and ship（レビューし、マージする）、Away and back（席を外し、戻る）の5つの節に分かれています。各サンプルには、`<operation>`（操作）や `<time>`（時間）のように、利用者ごとに中身が変わる部分が `<>` で空けてあります。たとえば、Buildの節の性能改善のサンプルと、エージェントが空けてある部分に利用者の実際の内容を入れた依頼文は、次のとおりです（後者は、本書で作成した例です）。

```
/poteto-mode <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.
// <fixture> で <operation> に <time> かかる。原因をトレースし、測った原因を直して、変更前と変更後を見せて。

/poteto-mode search takes 3s on the 10k-item fixture. trace it, fix the measured cause, show me before and after.
// 1万件のフィクスチャで検索に3秒かかる。原因をトレースし、測った原因を直して、変更前と変更後を見せて。
```

さらに、エージェントは、利用者が依頼文を考えるのを手伝う前や、作業が依頼と違う方向に進んだときは、依頼文の書き方の手引き（[`references/prompting.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-help/references/prompting.md)）を読みます。そして、エージェントは、依頼文の書き方の手引きに沿って、利用者と一緒に依頼文を考えたり、エージェントの動作を1行で修正するための依頼文を示したりします。

エージェントが沿う内容は、次の7つの節に分かれています。

- **依頼文に入れるもの**（Put in）・・・ 目的、作業が終わったことを判定する確認方法（合否が出るもの）、見せてほしい証拠（例：実際のコマンドの出力）、利用者がすでに知っていること（例：症状、再現手順、ログ）、実際の制約（例：「repro first」「don't change any code yet」）
- **依頼文に入れないもの**（Leave out）・・・ やり方、Skillや手順の一覧、利用者が考える原因（エージェントが問題を言い直すまでは入れない）
- **先にコンテキストを読み込ませる**（Load the context first）・・・ 分かりにくい報告は、作業の前に、エージェントに自分の言葉で言い直させる。新しいチャットでは、`/recall` で以前の作業を集めさせる。見慣れないコードを変える前に、`/how` で仕組みを、`/why` で理由を調べさせる。`/teach` に、選んだ方法が正しいことを説明させる
- **計画の前に設計する**（Design before the plan）・・・ 最初の設計をそのまま採らず、いくつかの案をプロトタイプにさせて、証拠から選ぶ。未解決の問いには、プロトタイプで答えを出させる。共有パッケージやAPIは、先にREADMEかチュートリアルを書かせる。計画は、設計が決まってから頼む
- **続きの依頼は短くする**（Follow up short）・・・ チャットが作業を覚えていれば、「do it」「continue」だけで依頼になる。話題が変わるときは、「new task」で始める
- **席を外す前に伝えること**（Before stepping away）・・・ 「im going to bed」のように席を外すことを伝える。毎回確かめられる完了条件を書き、`/loop` に渡す。指定したブランチから新しいworktreeを作らせる。エージェントが止まって尋ねそうなことに、先に答えておく。判断の記録を頼む。行き詰まったときに止める条件を伝える
- **エージェントの動作を1行で修正するための依頼文**（Steer in one line）・・・ 目的を伝え直す。Principleの名前を挙げる

## 依頼の書き方：`/poteto-help` の後に、質問を書く

利用者は、`/poteto-help` の後に、質問を書きます。pstackの[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)と、同梱ガイドの[`README.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/README.md)は、次の例を挙げています。

```
/poteto-help which skill should i use to review this branch?
// このブランチのレビューには、どのSkillを使えばよい？
```

同梱ガイドの[`10-recipes-and-pitfalls.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/10-recipes-and-pitfalls.md)は、次の例を挙げています。

```
/poteto-help how do i get poteto-mode to stay on every turn?
// poteto-mode を毎ターン有効にするには、どうすればよい？
```

同ページでは、上記の依頼をすると、質問への回答と、利用者が使用する依頼文と、出典のリンクが返ってくると説明しています。

## まとめ

- **役割**・・・ pstackの使い方についての質問に、回答と、利用者が使用する依頼文と、出典のリンクを返します。
- **使いどき**・・・ pstackを使い始めたばかりのときや、どのSkill、Playbook、Principleを使えばよいか迷ったときに、利用者が `/poteto-help` と入力して使います。
- **手順**・・・ エージェントは、利用者が何を求めているかを見極め、次の5つの場面の「どれに該当するか」に合わせて回答します。
  - pstackを導入するとき
  - `/poteto-mode` で作業を始めるとき
  - 作業に合うSkillを選ぶとき
  - 作業がうまくいかなかったとき
  - pstackを自分用にしたいとき
- **依頼の書き方**・・・ 利用者は、`/poteto-help` の後に、知りたいことを普段の言葉で書きます。

次の[第38章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f8911)では、pstackのRouter（振り分け役）である [`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) を扱います。`/poteto-mode` は、利用者が依頼した作業を、その作業に合うPlaybookへ振り分けるSkillです。
