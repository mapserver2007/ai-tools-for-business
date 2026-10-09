---
title: "付録 README with Grill 駆動開発（RGDD）"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/80691b"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:37+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 50
---

# 付録 README with Grill 駆動開発（RGDD）

**RGDD**（**README駆動 with Grill Driven Development**）は、本書の内容とpstackを個人開発で使用するなかで、私が考えついた、開発の進め方です。

RGDDでは、開発者が、**エージェントが読むコンテキストをコードより先に**コードベースに置き、そのコンテキストをエージェントに読ませながら開発します。

!

**コンテキスト**・・・ エージェントが作業のたびに読み直す、主にリポジトリの中のファイルです。  
会話が終わっても消えずに残ります。

[第4章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dc9141)では、コードベースをエージェントの記憶として扱い、次のように書きました。

> エージェントが前回までの判断を引き継ぐための記憶は、モデルの中ではなく**コードベース**に置きます。

RGDDでは、コードのほかに、次のような文書もコンテキストとして使います。

- **README**・・・ 誰が、何のために、どう使うかを書いた文書です（例：使い方やチュートリアル）。
- **`GLOSSARY.md`**・・・ ドメイン用語（そのソフトウェアが扱う業務や対象を表す言葉）とその定義をまとめた文書です（例：「注文」が何を指すか）。
- **ADR**（Architecture Decision Record）・・・ 設計上の判断とその理由の記録です（例：採用するデータベースを選んだ理由）。
- **コーディング規約**・・・ コードの書き方の決まりです（例：`CODING_STANDARDS.md` に書いた決まり）。
- **Feature Map と検証スキル**・・・ 検証スキルは、エージェントがアプリを起動・操作して証拠を取るための、プロジェクト専用のSkillです。Feature Map は、その中に置く、アプリの機能ごとのアクセス方法（たどり着き方）と確かめ方をまとめた文書です（[第39章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7081)）。

開発者は、このうち README、`GLOSSARY.md`、ADR をコードより先に置き、Feature Map と検証スキルは、最初の機能が動いた後にエージェントに作らせます。

この付録では、RGDDの考え方と進め方を解説します。

## この付録の構成

この付録の構成は次のとおりです。

- RGDDは、README駆動開発と /grill-with-docs でコンテキストを作り、開発と検証に使う
- RGDDは、5つのフェーズで、コンテキストに書き足し、確かめて修正・更新する
- 各フェーズが前のフェーズのコンテキストを読んで書き足すので、コンテキストが育ち続ける
- コンテキストを先に置くのは、エージェントが読む手本を最初から正しくするため
- まとめ：コードの前に、コンテキストを置く

!

**コンテキストが育つ**・・・ 作業を重ねるたびに、コンテキストのファイルに用語や判断が書き足され、すでに書かれた内容も確かめられ、修正・更新され続けていくことです。

## RGDDは、README駆動開発と /grill-with-docs でコンテキストを作り、開発と検証に使う

**RGDDでは、開発者が、README駆動開発と、Matt Pocock氏のSkill [/grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) を組み合わせてコンテキストを作り、そのコンテキストを開発と検証に使います**。

!

**README駆動開発**・・・ 想定するユーザーに使い方を説明するREADMEから書き始め、実装とアーキテクチャへ逆算する開発の方法です。

README駆動開発は[「1. READMEで、ユーザーから見た使い方を書く」](#1.-readme%E3%81%A7%E3%80%81%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%81%8B%E3%82%89%E8%A6%8B%E3%81%9F%E4%BD%BF%E3%81%84%E6%96%B9%E3%82%92%E6%9B%B8%E3%81%8F)で、`/grill-with-docs` は[「2. /grill-with-docsで、ドメイン用語とADRを作る」](#2.-%2Fgrill-with-docs%E3%81%A7%E3%80%81%E3%83%89%E3%83%A1%E3%82%A4%E3%83%B3%E7%94%A8%E8%AA%9E%E3%81%A8adr%E3%82%92%E4%BD%9C%E3%82%8B)で説明します。

RGDDの土台にあるのは、冒頭で引用した第4章の、コードベースをエージェントの記憶として扱う考えです。

poteto氏も『The Complete Guide to pstack』[Part 1](https://x.com/poteto/status/2094457600259842065)の節『Keep agents smart with Feature Maps』で、次のように書いています。

> Personally, I think your codebase is the ultimate form of memory. Code is a projection of the decision making you and your team have made and represents the source of truth for what's happened and how things actually work.
>
> 個人的には、コードベースこそ究極の記憶だと考えている。コードは、あなたとチームが下してきた判断を映したもので、何が起きたか、実際にどう動くかについての、正とすべき情報源だ。

同じ節で、poteto氏は、Feature Map を次のように説明しています。

> A Feature Map is just a more compact form of that, designed to save tokens.
>
> Feature Mapは、それ（コードベースという記憶）をより小さくまとめたものにすぎず、トークンを節約するためのものだ。

Feature Map が持つのは、次の内容です。

- どんな機能があり、それぞれ何をするか
- ユーザーの立場から、各機能にどうたどり着くか
- 検証スキルでどう操作するか
- 何が見えれば動いたと言えるか

**RGDDは、コンテキストに持たせる内容を、「誰が、何のために、どう使うか」（README）、「どんな言葉を使うか」（`GLOSSARY.md`）、「なぜそう決めたか」（ADR）まで広げます**。

5つのコンテキストについて、持っているものと、誰が何で作るかを整理すると、次のとおりです。

| コンテキスト | 持っているもの | 作る人・道具 |
| --- | --- | --- |
| README（またはREADMEの役割を果たす文書） | 誰が、何のために、どう使うか | 開発者が書く |
| `GLOSSARY.md` | ドメイン用語とその定義、避ける言い方 | `/grill-with-docs` |
| ADR（`docs/adr/`） | 重要な設計判断とその判断の背景・理由 | `/grill-with-docs` |
| コーディング規約（例：`CODING_STANDARDS.md`） | コードの書き方 | 開発者がリポジトリごとに決めて書く |
| Feature Map と検証スキル | 機能の一覧、ユーザーから見たたどり方、確かめ方 | [`/create-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) |

!

- **ドメイン用語**・・・ そのソフトウェアが扱う業務や対象を表す言葉です（例：料理の注文アプリなら「注文」「取り消し」）。
- **避ける言い方**・・・ 同じものを指す別の言葉のうち、使わないと決めた言葉です（例：「注文」を用語に選んだ場合、「購入」「取引」が「避ける言い方」に該当します）。`GLOSSARY.md` では、用語の定義の下に書きます。

コーディング規約は、5つのフェーズの中で作るものではなく、エージェントが [`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md)（依頼を適切な進め方につなぐ、pstackの入口のSkill。[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)）でコードを書くときに従う決まりなので、次の節で見る5つのフェーズには含めません。

また、**READMEは、必ずしも `README.md` という名前である必要はありません**。

ユーザーから見た使い方を書き、ほかのコンテキストの出発点になる文書であれば、仕様書などでもREADMEの役割を果たせます。

## RGDDは、5つのフェーズで、コンテキストに書き足し、確かめて修正・更新する

開発者は、RGDDを次の5つのフェーズで進めます。

1. READMEで、ユーザーから見た使い方を書く
2. `/grill-with-docs` で、ドメイン用語とADRを作る
3. `/poteto-mode` で開発する
4. `/thermos` でレビューする
5. `/create-verification-skill` で検証する

各フェーズは、**コンテキストに書き足すか、コンテキストに残るものを確かめて修正・更新するか**のどちらかを受け持ちます。

以下、各フェーズについて「何を作るか」「使う道具」「残るコンテキスト」の順に説明します。

### 1. READMEで、ユーザーから見た使い方を書く

- **何を作るか**・・・ アプリのユーザーの立場から、使い方やチュートリアルを書いたREADMEです。実装の話はまだ書きません。
- **使う道具**・・・ RGDDでは、SkillやCLIなどの道具を使わず、開発者が自分でREADMEを書きます。一方、[第41章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7549a7)の[要点5](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7549a7#%E8%A6%81%E7%82%B95%EF%BC%9A%E4%BD%BF%E3%81%84%E6%96%B9%E3%82%92%E5%85%88%E3%81%AB%E6%9B%B8%E3%81%8F)（使い方を先に書く）では、次のように、エージェントに書かせる形を紹介しました。

  > 人間は、実装の前に、エージェントに**READMEやチュートリアルで使い方を書かせ**、そこからAPIや内部設計を逆算させます。
- **残るコンテキスト**・・・ 「誰が、何のために、どう使うか」といった、アプリの使い方のコンテキストです。ほかのコンテキストの出発点になります。

例：料理の注文アプリのREADME

ユーザーから見た使い方だけを書き、実装の話は書きません。

```
# かんたん注文

近所の店に、スマートフォンから料理を注文できるアプリです。

## できること

- メニューから料理を選んで、注文する
- 注文の状況（受付済み、調理中、受け取り可能）を確かめる
- 受け取る前なら、注文を取り消す

## 使い方

1. アプリを開き、店を選ぶ
2. メニューから料理を選び、「注文する」を押す
3. 状況が「受け取り可能」になったら、店で受け取る
```

RGDDでこのフェーズを最初に置くのは、**次のフェーズで `/grill-with-docs` が質問を重ねるときの題材を、先に用意しておくため**です。

ユーザーから見た使い方が書かれていれば、`/grill-with-docs` は、その使い方の曖昧なところを具体的に質問でき、開発者も具体的に答えられます。

たとえば、上のREADMEの例には「受け取る前なら、注文を取り消す」とあります。`/grill-with-docs` は、ここから「調理中の注文も取り消せますか？」のように、READMEだけでは決まっていないことを質問できます。

### 2. /grill-with-docsで、ドメイン用語とADRを作る

- **何を作るか**・・・ ドメイン用語をまとめた `GLOSSARY.md` と、設計上の判断を残すADRです。
- **使う道具**・・・ Matt Pocock氏の `/grill-with-docs` です。エージェントが自分から選ぶSkillではないので、開発者が名前で呼んで始めます。
- **残るコンテキスト**・・・ ドメイン用語とその定義といった前提知識（`GLOSSARY.md`）と、設計上の判断とその理由といった過去の意思決定（ADR）です。

`/grill-with-docs` は、**計画や設計を詰めるために開発者に徹底的に質問を重ね、その過程でADRと用語集（`GLOSSARY.md`）を作るSkill**です。

`/grill-with-docs` は、手順の中で次の2つのSkillを呼びます。

- **[`/grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)**・・・ 計画や設計について開発者に質問を重ね、決めることを詰めます。
- **[`/domain-modeling`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md)**・・・ 用語の食い違いや曖昧な言い方を指摘し、決まった用語をすぐ `GLOSSARY.md` に書きます。判断をADRにすることを提案するのは、次の3つがそろうときだけです。
  - 覆しにくい
  - 文脈がないと意外に見える
  - 本当に選択肢を比べて選んだ

`/domain-modeling` がADRにすることを提案する3つの条件の意味と、料理の注文アプリでの例は、次のとおりです。

例：ADRにする3つの条件

表の「意味」は、`/domain-modeling` の [`ADR-FORMAT.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/ADR-FORMAT.md) の節『When to offer an ADR』を訳したものです。「例」は、[フェーズ1](#1.-readme%E3%81%A7%E3%80%81%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%81%8B%E3%82%89%E8%A6%8B%E3%81%9F%E4%BD%BF%E3%81%84%E6%96%B9%E3%82%92%E6%9B%B8%E3%81%8F)のREADMEの例（料理の注文アプリ）の「注文のデータを店ごとに別のデータベースに保存する」という判断に当てはめたもので、本書が作りました。

| 条件 | 意味（`ADR-FORMAT.md`） | 例 |
| --- | --- | --- |
| 覆しにくい | 後から考えを変えると、大きな手間がかかる | 後から1つのデータベースにまとめるには、全店のデータを移し替える必要がある |
| 文脈がないと意外に見える | 後からコードを読んだ人が「なぜこんな作りにしたのか」と思う | 同じ注文のデータなのに、店ごとに保存先が分かれている |
| 本当に選択肢を比べて選んだ | ほかに現実的な案があり、はっきりした理由で1つを選んだ | 1つのデータベースにまとめる案と比べ、障害の影響を1つの店にとどめるために分けた |

逆に、どれか1つでも欠ける判断は、ADRにしません。

たとえば「注文一覧を新しい順に並べる」という判断は、すぐ戻せて、誰も理由を疑問に思わないので、ADRにしません。`ADR-FORMAT.md` は、その理由を次のように書いています。

> If a decision is easy to reverse, skip it: you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."
>
> 判断が簡単に戻せるなら、ADRにしない。戻せばよいだけだからだ。意外でないなら、誰も理由を疑問に思わない。本当の選択肢がなかったなら、「当たり前のことをした」以上に記録することはない。

`/grilling` は、決めることを、前提になる決定から順に整理し、今すぐ答えられる質問をまとめて尋ねます。`/grilling` の進め方の詳細と例は、次のとおりです。

例：/grilling の質問の進め方

`/grilling` は、決めることを、木の形（原文では design tree）に整理します。木の枝は、「親の決定が決まると、初めて決められるようになる決定」を表します。

[フェーズ1](#1.-readme%E3%81%A7%E3%80%81%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%81%8B%E3%82%89%E8%A6%8B%E3%81%9F%E4%BD%BF%E3%81%84%E6%96%B9%E3%82%92%E6%9B%B8%E3%81%8F)のREADMEの例（かんたん注文）で、決めることを木にすると、次のようになります（本書が作った例です）。

たとえば、Q3「取り消せる期間を、客にどう見せるか」は、Q1「取り消せる期間」が決まらないと答えられません。期間が「受付済みの間だけ」か「受け取る前まで」かで、見せ方が変わるからです。同じように、Q4「通知を許可していない客に、どう知らせるか」は、Q2で「プッシュ通知で知らせる」と決まってから出てくる質問です。

`/grilling` は、この木の質問を、何回かのまとまり（原文では round）に分けて尋ねます。1回のまとまりで尋ねるのは、**答えるのに必要な親の決定が、すべて決まっている質問**です。原文は、この質問の集まりを frontier と呼び、次のように説明しています。

> The **frontier** is every decision whose prerequisites are already settled: the questions you can ask *now* without guessing at answers you haven't heard yet.
>
> frontier とは、前提となる決定がすでに決まっている、すべての決定のことだ。まだ聞いていない答えを推測せずに、今すぐ尋ねられる質問である。

上の木では、1回目のまとまりは、親の決定を待たずに答えられるQ1とQ2です。エージェントは、Q1とQ2に番号と推奨の答えを添えて、一度に尋ねます。

開発者がQ1とQ2に答えると、Q3とQ4に答えられるようになります。エージェントは、2回目のまとまりとして、Q3とQ4を尋ねます。

**1回目のまとまりの例**

上の木の1回目のまとまり（Q1とQ2）を、`/grilling` の [`SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) が示す書式（質問に番号を付け、推奨の答えを添える）で書いたものです。

```
❓ **Q1** - **取り消せる期間**: READMEには「受け取る前なら、注文を取り消す」とあります。調理中の注文も取り消せますか？

➡️ 取り消せるのは「受付済み」の注文だけにする（調理を始めた料理が無駄になるため）

---

❓ **Q2** - **受け取り可能の知らせ方**: 状況が「受け取り可能」になったことを、客にどう知らせますか？

➡️ アプリのプッシュ通知で知らせる
```

開発者がQ1に「受付済みだけ」と答えると、「取り消し」という用語の定義が決まります。そこで `/domain-modeling` が、その定義を `GLOSSARY.md` に書きます。

このフェーズで、**エージェントは、開発者と決めたドメイン用語を、会話の中だけで終わらせず、ファイル（`GLOSSARY.md`）に書いて残せます**。

会話の中で決めた用語は、会話が終わると次のエージェントに引き継がれません。

一方、`GLOSSARY.md` に書いた用語は、次のエージェントも読めます。

また、エージェントは、`/grill-with-docs` で設計を詰めている間、開発者の言葉を `GLOSSARY.md` の用語の定義と照らし合わせます。

開発者が定義と食い違う言い方をすると、エージェントはその場で指摘します（`/domain-modeling` の [`SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md) の節『Challenge against the glossary』）。

> When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately.
>
> ユーザー（Skillを使う人。RGDDでは開発者）が `GLOSSARY.md` の既存の用語と食い違う言葉を使ったら、その場で指摘する。

食い違いを見分ける手がかりになるのが、`GLOSSARY.md` の「避ける言い方」（原文では `_Avoid_`）です。`/domain-modeling` の [`GLOSSARY-FORMAT.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/GLOSSARY-FORMAT.md) は、同じものを指す言葉が複数あるときは、最もよい1つを用語に選び、ほかの言葉を避ける言い方として書くよう定めています（節『Rules』）。

> When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
>
> 同じ概念を指す言葉が複数あるときは、最もよい1つを選び、ほかの言葉を `_Avoid_` の下に挙げる。

たとえば、`GLOSSARY.md` が「注文」を定義し、「購入」を避ける言い方に挙げているとします（`GLOSSARY-FORMAT.md` の例）。

開発者が「購入」と言うと、エージェントはそれを、定義と食い違う言い方として指摘します。

このフェーズで作られる `GLOSSARY.md` とADRは、たとえば次のような短い文書です。

例：GLOSSARY.md

書き方は、`/domain-modeling` の `GLOSSARY-FORMAT.md` が示す形に合わせています。用語ごとに、短い定義と、避ける言い方を書きます。

```
# 注文

客が店に料理を注文し、受け取るまでを扱う。

## 用語

**注文**:
客が店に出した、料理の注文。
_避ける言い方_: 購入、取引

**取り消し**:
「受付済み」の注文を、客がやめること。調理中の注文は取り消せない。
_避ける言い方_: キャンセル
```

例：ADR（docs/adr/0001-separate-database-per-store.md）

書き方は、`/domain-modeling` の [`ADR-FORMAT.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/ADR-FORMAT.md) が示す形に合わせています。ADRは、何を決めたかと、その理由を書く短い文書で、1段落でもかまいません。

```
# 注文のデータは、店ごとに別のデータベースに保存する

1つの店で障害が起きても、ほかの店の注文に影響しないようにするため、注文のデータを店ごとに別のデータベースに分けて保存する。1つのデータベースにまとめる案も比べたが、障害の影響が全店に広がるので採らなかった。
```

このADRは、折りたたみ「例：ADRにする3つの条件」の表で、3つの条件に当てはめた判断を記録したものです。

### 3. `/poteto-mode` で開発する

- **何を作るか**・・・ 実際のコードです。
- **使う道具**・・・ 開発には `/poteto-mode`（[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)）を使います。開発者がコードの仕組みや、これまでの経緯を知りたいときは、次のSkillを使います（[第22章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/788746)）。
  - [`/how`](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md)・・・ 仕組みを調べる
  - [`/why`](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md)・・・ 設計の理由を調べる
  - [`/recall`](https://github.com/cursor/plugins/blob/main/pstack/skills/recall/SKILL.md)・・・ 最近の作業の経緯を、チャット履歴などから集める
- **残るコンテキスト**・・・ コードそのものと、PRです。PRは、機能追加やバグ修正などのPlaybook（作業の種類ごとの手順書。[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)）の最後の手順で、エージェントが作ります。

開発のフェーズでは、**エージェントが、ここまでに作ったコンテキストとコーディング規約（開発者が用意している場合のみ使用）を読みながらコードを書きます**。

フィードバックへの対応、QA、不具合修正のような、軽い作業や定型の作業では、私は、Grok Bot（AIのBotアプリ。[第5章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/b6ac2d)）から、Cloud Agents（Cursorのクラウド上でエージェントを動かす機能）を起動して作業させています。

Grok Bot には作業そのものをさせず、Cloud Agents を起動させる点は、poteto氏の使い方と同じです。

[第39章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7081)では、poteto氏の使い方を次のように書きました。

> **Grok Bot から依頼する場合、poteto氏は、Botに作業そのものをさせません。代わりに、Cloud Agents（Cursorのクラウド上でエージェントを動かす機能）のエージェントを起動するよう、Botに頼みます**。

README、`GLOSSARY.md`、ADR、コーディング規約はリポジトリに置いてあるので、Cloud Agents も含め、作業するエージェントはどれもこれらを読めます。

**[フェーズ2](#2.-%2Fgrill-with-docs%E3%81%A7%E3%80%81%E3%83%89%E3%83%A1%E3%82%A4%E3%83%B3%E7%94%A8%E8%AA%9E%E3%81%A8adr%E3%82%92%E4%BD%9C%E3%82%8B)で作ったADRは、開発の途中で、開発者が `/why` で判断の理由を聞くときにも役立ちます**。

`/why` は、調べる情報源の種類ごとに、調べ方を書いたファイルを持っています。

そのうち、ソース管理の履歴の調べ方を書いたファイルには、`docs/adr/` などに置かれたADRを探す手順があります。

そのため、ADRに理由が書かれていれば、`/why` はそれを答えの根拠にできます。

ADRのない判断でも、`/why` は理由を組み立てます。ソース管理の履歴と、チケットやチャットなどを並列に調べ、そこに残った手がかりを使います。チケットやチャットは、MCP（エージェントを外部のツールやデータにつなぐ仕組み）でつながったものを調べます。

それでも手がかりが見つからなければ、何を調べたかを示したうえで、理由が分からなかった（Unknown）と報告します。

### 4. `/thermos` でレビューする

- **何を作るか**・・・ レビュー指摘の一覧です。
- **使う道具**・・・ Cursorのプラグイン [`/thermos`](https://github.com/cursor/plugins/tree/main/thermos) です。
- **残るコンテキスト**・・・ 指摘をエージェントが直した後のコードです。なお、**`/thermos` の手順は、指摘を1つの一覧にまとめるところまで**で、コードを直す手順は含みません。

`/thermos` は、[フェーズ3](#3.-%2Fpoteto-mode-%E3%81%A7%E9%96%8B%E7%99%BA%E3%81%99%E3%82%8B)でエージェントが書いたコードの差分を、2つのサブエージェントに並列で監査させます。

!

**サブエージェント**・・・ `/thermos` を実行しているエージェント（主エージェント）から作業を任されて動く、別のエージェントです。

2つの監査は次のとおりです。

- **セキュリティと正しさの監査**（例：不具合、既存の機能を壊す変更、セキュリティの穴）
- **厳しいコード品質の監査**（例：保守のしにくさ、ファイルの肥大化、不要な抽象化）

2つの監査が終わると、`/thermos` は結果を、重複を除いて1つの一覧にまとめます。

2つのサブエージェントが同じ問題を指摘した場合は、その指摘をより重要なものとして扱います。

RGDDがこのフェーズを置くのは、**場当たり的な回避策（問題の原因を直さずに、その場しのぎで問題を避ける書き方）や保守しにくい作りを、マージされてコードとして残る前に取り除くため**です。コードに残った回避策は、次のエージェントが正しい実装例だと思ってコピーするからです。

[第4章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dc9141)は、このことを次のように書いています。

> 何でも記憶として残せばよいわけではありません。場当たり的な回避策を残すと、**次のエージェントがそれを正しい実装例だと思ってコピーし、そのコピーがまた次のコピーを生んで、望ましくないパターンが静かに広がっていきます**。

### 5. `/create-verification-skill` で検証する

- **何を作るか**・・・ アプリを操作する小さなCLIと Feature Map を含む、プロジェクト専用の検証スキルです（[第39章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7081)）。
- **使う道具**・・・ pstack の [`/create-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) と、作った検証スキルと Feature Map を最新に保つ [`/maintain-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md)（[第26章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/03ebca)）です。
- **残るコンテキスト**・・・ どんな機能があり、ユーザーの立場から各機能にどうたどり着き、どう確かめるか、というコンテキストです。

`/create-verification-skill` は Feature Map を、目次の `features/README.md` と、機能ごとのファイルで作ります。

目次は機能ごとのファイルへのリンクを持ちます。機能ごとのファイルは、ユーザーの立場から、次の4つを書いたものです。

- その機能が何か
- どうたどり着くか
- 検証スキルのCLIでどう操作するか
- 何が見えれば動いたと言えるか

例：機能ごとのファイル（pstack の見本の抜粋）

`/create-verification-skill` の [`references/feature-map-example/`](https://github.com/cursor/plugins/tree/main/pstack/skills/create-verification-skill/references/feature-map-example) にある見本のうち、メモアプリの「メモを作る」機能のファイルを、一部を省いて訳したものです。

```
# メモを作る

ブラウザかCLIから、タイトル付きのメモを保存できる。書きかけの下書きを取り消すことも、保存したメモを別の画面から確かめることもできる。

## Sub-features

- `create-open` ブラウザの各入口から、空の編集画面を開く
- `create-save` タイトルと本文を保存する

## How to get to it (user POV)

- ブラウザのツールバーの `New note` ボタンを選ぶ
- 入力欄の外にフォーカスがあるときに、ブラウザで `n` を押す
- ターミナルで `notes create --title <title> --body <body>` を実行する

## Driving it with control-notes

- **編集画面を開く。** `New note` を選ぶ。`control-notes browser click --role button --name "New note"` を実行する。`Note editor` という名前のフォームが現れ、`Title` の入力欄にフォーカスが移る。
- **内容を入れる。** タイトルと本文を入力する。`control-notes browser fill --role textbox --name "Title" --value "Release checklist"` と `control-notes browser fill --role textbox --name "Body" --value "Tag and publish"` を実行する。`Save note` ボタンが押せるようになる。
- **メモを保存する。** `Save note` を選ぶ。`control-notes browser click --role button --name "Save note"` を実行する。`Note saved` という表示が現れ、見出しが `Release checklist` になる。

## Gotchas

- 入力欄にフォーカスがあるときに `n` を押すと、新しい編集画面は開かず、文字が入力される。
```

見出しの下の説明の段落が「その機能が何か」、`How to get to it (user POV)` が「どうたどり着くか」、`Driving it with control-notes` が「どう操作するか」と「何が見えれば動いたと言えるか」に当たります。

`control-notes` は、この見本の検証スキルが持つ、アプリを操作するCLIです。`Sub-features` は細かい機能を短いIDで1行ずつ並べた一覧、`Gotchas` は検証の作業を無駄にしたり結果を無効にしたりする落とし穴の一覧です。4つの見出しは、どの機能のファイルでも同じ英語の見出しを、同じ順番で使います。

Feature Map の目次 `features/README.md` は、[フェーズ1](#1.-readme%E3%81%A7%E3%80%81%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%81%8B%E3%82%89%E8%A6%8B%E3%81%9F%E4%BD%BF%E3%81%84%E6%96%B9%E3%82%92%E6%9B%B8%E3%81%8F)のREADMEと名前は同じでも、役割が異なります。

[フェーズ1](#1.-readme%E3%81%A7%E3%80%81%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%81%8B%E3%82%89%E8%A6%8B%E3%81%9F%E4%BD%BF%E3%81%84%E6%96%B9%E3%82%92%E6%9B%B8%E3%81%8F)のREADMEは、これから作るものの使い方を、開発者が書いた文書です。

一方、Feature Map の `features/README.md` は、できあがったアプリについて、エージェントが `/create-verification-skill` の手順に沿って作る目次です。

『The Complete Guide to pstack』[Part 1](https://x.com/poteto/status/2094457600259842065)は、検証スキルを最も重要なスキルとし、最初に作るものとして挙げています（[第39章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7081)）。**RGDDでも同様の考えです**。

ただし、ゼロからアプリを作る場合、動かして確かめる対象のアプリがまだないので、ここでは最後のフェーズに持ってきています。

!

**既にアプリがある場合には、本書では `/create-verification-skill` で検証スキルと Feature Map を作成することを強く推奨します。**

`/create-verification-skill` の [`SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) も、動くアプリを前提にしています。アプリがそのままではビルドや起動ができない場合、この `SKILL.md` はエージェントに、検証スキルを作る前にそれを直すか、その状態を正確に報告するよう求めています（節『1. Interview the repo, not the user』）。

そこでRGDDでは、**最初の機能が動いた時点で**、開発者が `/create-verification-skill` を実行し、エージェントに検証スキルを作らせます。

その後は、エージェントが毎回のタスクでその検証スキルを使って変更を確かめ、開発者が `/maintain-verification-skill` で検証スキルと Feature Map を最新に保ちます。

私は、『The Complete Guide to pstack』[Part 1](https://x.com/poteto/status/2094457600259842065)の推奨どおり、`/maintain-verification-skill` を最低でも1日1回実行しています。実行は、Grok Bot のメンテナー用のBotに任せています。

このBotも、Part 1が勧めるとおり、[Dr Eggbot](https://x.ai/bot/marketplace/bots/dr-eggbot-v2)（[第39章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7081#dr-eggbot-%E3%81%A7%E6%AF%8E%E6%97%A5%E3%81%AE%E5%AE%9F%E8%A1%8C%E3%82%92%E4%BB%95%E7%B5%84%E3%81%BF%E3%81%AB%E3%81%99%E3%82%8B)）に頼んで作りました。

> I recommend running /maintain-verification-skill at least once a day to ensure that your agents always have the latest details on controlling your app.
>
> エージェントが、アプリを操作するための最新の情報を常に持てるよう、/maintain-verification-skill を少なくとも1日1回実行することを勧める。

## 各フェーズが前のフェーズのコンテキストを読んで書き足すので、コンテキストが育ち続ける

コンテキストが育ち続けるのは、RGDDの各フェーズが、**前のフェーズが残したコンテキストを読んだうえで、コンテキストに書き足すか、コンテキストに残るものを確かめて修正・更新する**からです。

| フェーズ | 読むもの | 書き足すコンテキスト、確かめて修正・更新するもの |
| --- | --- | --- |
| 1. README | なし | 誰が、何のために、どう使うか |
| 2. `/grill-with-docs` | README | 用語、判断（ADR） |
| 3. `/poteto-mode` | README、`GLOSSARY.md`、ADR、コーディング規約 | コード、PR |
| 4. `/thermos` | [フェーズ3](#3.-%2Fpoteto-mode-%E3%81%A7%E9%96%8B%E7%99%BA%E3%81%99%E3%82%8B)で書いたコードの差分 | 差分の問題（エージェントが直してからコードに残す） |
| 5. `/create-verification-skill` | 動くアプリ | Feature Map、確かめ方 |

開発を続ける間も、開発者とエージェントは、次のようにコンテキストに書き足し、確かめて修正・更新していきます。

- **新しい用語や判断が出てきたとき**・・・ 開発者が [`/grill-with-docs`](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) でもう一度設計を詰めます。エージェントは用語を `GLOSSARY.md` に追加し、次の3つがそろう判断は、ADRにすることを提案します。
  - 覆しにくい
  - 文脈がないと意外に見える
  - 本当に選択肢を比べて選んだ
- **レビューで差分の問題が見つかったとき**・・・ `/thermos` の指摘をエージェントが直してから、コードとして残します。
- **機能が増えたとき**・・・ 開発者が `/maintain-verification-skill` を実行します。Feature Map に欠けている機能などの直すべき点が見つかれば、エージェントが修正を1つのPRにまとめます。

コンテキストに書き足し、確かめて修正・更新していくこの進め方の一番の狙いは、**エージェントのために、適切なコンテキストを、過去のコンテキストも含めて残し続けること**です。

この狙いは、[第4章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dc9141)で見た「庭師」の考え方から来ています。第4章では、コードベースを記憶として保つ仕事を、次のように書きました。

> 講演では、この環境を維持する仕事が「**庭師**」にたとえられています。庭は植物を増やすだけでは保てず、不要な枝や雑草を取り除き、望ましいものが育つようメンテナンスし続ける必要があります。
>
> コードベースも同じで、**知識を追加するだけでなく、古い回避策や悪い実装例を取り除き続けなければなりません**。

RGDDでは、開発者とエージェントが、この庭師の仕事を、コードだけでなく README、`GLOSSARY.md`、ADR、Feature Map にも行います。

- **書き足す**・・・ 新しく決まった用語や判断を、`GLOSSARY.md` やADRに書き足します。庭で言えば、望ましいものを育てる仕事です。
- **確かめて修正・更新する**・・・ 古くなった用語の定義や、アプリと食い違った Feature Map を、確かめて直します。庭で言えば、不要な枝や雑草を取り除く仕事です。

過去のコンテキストを残すのは、主にADRの役割です。ADRには、判断とその理由が残るので、後から判断を変えても、なぜ前はそう決めたのかを次のエージェントが読めます。

[`/domain-modeling`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md) の [`ADR-FORMAT.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/ADR-FORMAT.md) は、判断を見直したときのために、ADRの先頭に状態（原文では Status）を書いてよいとしています。状態には、提案中（proposed）、採用（accepted）、廃止（deprecated）、別のADRに置き換えた（superseded by ADR-NNNN）の4つがあります。

「別のADRに置き換えた」という状態があることから、本書では、判断を変えるときは古いADRを消さずに残し、新しいADRを足すものと読みます。

例：判断を変えたときのADR

[フェーズ2](#2.-%2Fgrill-with-docs%E3%81%A7%E3%80%81%E3%83%89%E3%83%A1%E3%82%A4%E3%83%B3%E7%94%A8%E8%AA%9E%E3%81%A8adr%E3%82%92%E4%BD%9C%E3%82%8B)のADRの例（0001）の判断を、後から変えた場合を想定しています。状態の書き方は、`ADR-FORMAT.md` が挙げる4つの状態に合わせています。

古いADRは消さずに、状態だけを「0002に置き換えた」に変えます。

docs/adr/0001-separate-database-per-store.md

```
---
status: superseded by ADR-0002
---

# 注文のデータは、店ごとに別のデータベースに保存する

1つの店で障害が起きても、ほかの店の注文に影響しないようにするため、注文のデータを店ごとに別のデータベースに分けて保存する。1つのデータベースにまとめる案も比べたが、障害の影響が全店に広がるので採らなかった。
```

新しいADRには、何を決め直したかと、その理由を書きます。

docs/adr/0002-single-database-for-orders.md

```
---
status: accepted
---

# 注文のデータを、1つのデータベースにまとめる

店が300を超え、店ごとのデータベースを運用しきれなくなったため、注文のデータを1つのデータベースにまとめる。0001で避けようとした、障害の影響が全店に広がる問題は、データベースを複数の場所に複製しておくことで抑える。
```

次のエージェントは、0002を読めば今の判断が分かり、0001を読めば、なぜ以前は店ごとに分けていたのかが分かります。

## コンテキストを先に置くのは、エージェントが読む手本を最初から正しくするため

コンテキストを残すと、決めたことを次のエージェントに引き継げます。

そのコンテキストをコードより先に置くのは、**エージェントが読む手本を、最初から正しいものにしておくため**です。

本書では、RGDDとは逆にコードから先に書き始めると、コンテキストは、後からコードを読み解いて作るしかなくなると考えています。

そのとき、コードに紛れ込んだ場当たり的な回避策まで、正しいコンテキストとして残ってしまうおそれがあります。

コードに残った回避策は、次のエージェントの手本になります（[フェーズ4](#4.-%2Fthermos-%E3%81%A7%E3%83%AC%E3%83%93%E3%83%A5%E3%83%BC%E3%81%99%E3%82%8B)）。

## まとめ：コードの前に、コンテキストを置く

- **RGDDとは何か**・・・ README、`GLOSSARY.md`、ADR をコードより先に置き、それらをエージェントに読ませながら開発する進め方です。
- **どんな順番で進めるのか**・・・ README → `/grill-with-docs` → `/poteto-mode` → `/thermos` → `/create-verification-skill` の5つのフェーズで進めます。
- **なぜコンテキストが育ち続けるのか**・・・ どのフェーズも、コンテキストに書き足すか、確かめて修正・更新するからです。
- **なぜコンテキストを先に置くのか**・・・ エージェントが読む手本を、最初から正しいものにしておくためです。

最後の「[おわりに](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f903e4)」では、本書の結論と、読み終えた後の最初の一歩を書きます。
