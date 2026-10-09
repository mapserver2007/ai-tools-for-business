---
title: "第4部 Principleがエージェントの判断を支える"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4b3166"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:29+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 21
---

# 第4部 Principleがエージェントの判断を支える

第4部では、pstackの全Principle（24件）を網羅的に取り扱います。

!

この部は読み飛ばしても構いません。関心のある章だけを読む使い方を推奨します。

各Principleの原文は、[pstack](https://github.com/cursor/plugins/tree/main/pstack)のリポジトリでいつでも読めます。pstackは頻繁に更新されるため、すべてを先に読むより、必要になったときに該当する章と原文のファイルを参照するほうが確実です。

## 第4部で分かること

- 各Principleが何を選び、何を避けるか、それが必要な理由（例：『[**Prove It Works**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md)』は、ビルドが通っただけでは完了とせず、書き出したファイルや画面を直接確かめる）
- 各Principleが当てはまる場面と、当てはまらない場面（例：『[**Outcome-Oriented Execution**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-outcome-oriented-execution/SKILL.md)』は、計画済みの移行では使うが、区切りのない普段の小さな修正には使わない）
- 依頼の中で、Principleの名前を使ってエージェントの作業の方向を変える方法（例：`apply prove it works.` と書き、実際にインポートを流して、書き込まれたレコードを見せるよう求める）

Principleは、**エージェントが作業の途中で下す判断の基準**です。Playbookは作業の順番を決めますが、エージェントが各手順を進める中には、「この抽象化を追加すべきか」「コンパイルが通った今、完了と言ってよいか」といった判断が残ります。こうした場面で、エージェントは、Principleに沿って「この変更を入れるか」「まだ完了と言えないか」を決めます。

24件のPrincipleは、扱う判断の種類ごとに、次の5つのグループに分かれています。グループが分かれているので、読み手は、いま迷っている判断の種類から、読むべき章を選べます。

| グループ | 件数 | 扱う判断 |
| --- | --- | --- |
| Core（中核） | 10 | どれだけ作るか、いつ設計を見直すか |
| Architecture（設計） | 6 | 状態、検証、互換性をどこに置くか |
| Verification（検証） | 5 | 何をもって証明するか |
| Delegation（委任） | 2 | 並列の作業と委任を、どう破綻させずに進めるか |
| Meta（仕組み自体の改善） | 1 | 仕組みそのものをどう改善するか |

Principleは、利用者が明示的に呼び出すものではなく、**エージェントが、作業が当てはまる場面かどうかを判定して読むもの**です。

`/poteto-mode`（作業を始めるときに使うSkill。[第7章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4fda7d)）は、手順が複数ある作業の始めに、Principleの索引を読みます。

索引は `/poteto-mode` の `SKILL.md` にある一覧で、各Principleの名前と、当てはまる場面（例：『Prove It Works』なら「作業を終えた後、完了を宣言する前」）が1行ずつ書かれています。エージェントは、作業がその場面に当てはまったPrincipleについて、本体の `SKILL.md` を全文読んでから適用し、返答の中で、適用したPrincipleの名前と、それによって変わった判断を挙げます。

**エージェントが作業の始めに読むのは、Principleの名前と当てはまる場面の一覧だけです**。本文は、作業がその場面に当てはまったときにだけ読み、判断に使います。そのため、24件すべての本文を毎回読み込まずに済み、コンテキストを無駄に使いません。

利用者は、この仕組みを、**依頼にPrincipleの名前を書くこと**で明示することもできます。エージェントが当てはまる場面を見落としているときに、依頼にPrincipleの名前を一言書けば、エージェントはその名前が指すルールに沿って作業の方向を修正できます。

Principleの名前を一言書くことは、長い指示を書くより正確に伝わります。名前が、そのPrincipleの `SKILL.md` に書かれた完全なルールを指すので、利用者が具体的なPrincipleの中身を伝え直す必要がないからです。

たとえば、ビルドが通っただけで完了を宣言しようとしているエージェントには、同梱ガイド（pstackに同梱されている `docs/guide/` のガイド。[第6章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/33f073)）の [`docs/guide/08-principles.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md) にある例のように書きます。

```
apply prove it works. run the real import flow and show me the written records.
// prove it works を適用して。実際のインポートを流して、書き込まれたレコードを見せて。
```

## この部の章

| 章 | 役割 |
| --- | --- |
| [第17章 Core ― 作業の進め方を決める10の原則](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) | 作る量、設計の見直し方、プロトタイプの作り方、道具を作るかどうか |
| [第18章 Architecture ― 境界と依存を設計する6つの原則](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) | データ構造、外から来たデータを境界（フォームの入力やAPIの応答のように、外からデータが入ってくる場所）で確かめること、型、冪等性（同じ操作を何度しても結果が変わらない性質）、古いAPIからの移行、共有状態 |
| [第19章 Verification ― 実際の挙動で確かめる5つの原則](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) | 完了を本物の出力で確かめる、不具合の原因を直す、小さく確かめながら進む、振る舞いをテストする、測った数値が何を測ったかを確かめる |
| [第20章 Delegation ― 委任と並列化を扱う2つの原則](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/c155cc) | エージェントのコンテキストを守る、人間の確認を待たずに進む |
| [第21章 Meta ― 仕組み自体を改善する原則](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dd2d9f) | 教訓を、文章ではなく仕組みで残す |

この部では、pstackの同梱ガイドの並びに合わせて、Coreを最初に置いています。

## 全Principleの早見表

| Principle | 概要 | 発火条件 | 解説 |
| --- | --- | --- | --- |
| [Laziness Protocol](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-laziness-protocol/SKILL.md) | コードの削除を優先し、問題を解決する最小の変更を選ぶ | エージェントがリファクタリングや差分の大きさの見積もりをするとき、または抽象化や層の追加、新しい値を何層にもまたいで受け渡すことをしたくなったとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Subtract Before You Add](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-subtract-before-you-add/SKILL.md) | 機能を追加する前に、使われていないコードや重複した検証などの複雑さを削る | エージェントが、機能や処理の追加、リファクタリング、書き直しを、どの順番で進めるかを決めるとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Minimize Reader Load](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-minimize-reader-load/SKILL.md) | 読み手がたどる間接参照の層と、覚えておく必要があるコードの状態を減らす | エージェントが処理を追いにくいコードをレビューするとき、またはそうしたコードを書いたり、構成を組み直したりするとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Foundational Thinking](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-foundational-thinking/SKILL.md) | ロジックを書く前に、データ構造と土台（CI、lint、テスト基盤、共有の型など）を決める | エージェントがロジックを書く前に中心の型やデータ構造を選ぶとき、土台と機能のどちらを先に作るかを決めるとき、または並行して動く複数の主体が何を共有するかを考えるとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Redesign from First Principles](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-redesign-from-first-principles/SKILL.md) | 新しい要件を既存の設計に後付けせず、最初からあった前提として設計を組み直す | エージェントが新しい要件を今ある設計に組み込むとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Attack the Premise](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-attack-the-premise/SKILL.md) | 同じ前提に立つ修正をさらに重ねず、次の修正を書く前に、その前提そのものを疑う | 一つの前提を共有する2つ以上の修正が、同じ gate（修正が通らなければならないテストやチェック）で落ちたとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Outcome-Oriented Execution](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-outcome-oriented-execution/SKILL.md) | 移行途中のコードの整合性を保つための一時的なコードより、確かめられる最終形を優先する | エージェントが、段階の区切りがあらかじめ決まっている、計画済みの書き直しや移行を進めているとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Experience First](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-experience-first/SKILL.md) | 実装の都合より、ユーザーの体験を選び、機能を少なく作ってよく仕上げる | エージェントが、プロダクト、UX、機能の範囲について、どちらかを取ればどちらかを諦めるトレードオフを選ぶとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Exhaust the Design Space](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-exhaust-the-design-space/SKILL.md) | 形の異なる2〜3案のプロトタイプを作り、並べて比べてから設計を決める | エージェントが、コードベースに前例のないUIの操作を作るとき、実現できる方法が複数あるアーキテクチャを選ぶとき、または使い心地が理屈より感覚で決まるプロダクトの設計を判断するとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Build the Lever](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-build-the-lever/SKILL.md) | 手作業の代わりに、作業をする道具か、作業の正しさを証明する道具（codemod、スクリプト、生成器、サブエージェントが従うSkill）を作る | エージェントが、編集、移行、分析、チェックを問わず、見ればすぐ分かる数か所の修正より手間のかかる作業をするとき | [第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b) |
| [Model the Domain](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md) | ドメインを、散らばった条件分岐ではなく構造（状態機械、型付きのオブジェクト、参照表、reducerなど）で表す | エージェントが状態を持つロジックを書くとき、分岐が多いコードを書くとき、または「このデータにはこの項目がある」という同じ前提を複数のファイルで繰り返しているとき | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Boundary Discipline](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-boundary-discipline/SKILL.md) | 検証とエラー処理を外からデータが入る境界に集め、境界の内側のコードでは、型の付いた値を確かめ直さずに使い、業務のロジックを純粋関数に保つ | エージェントが入力の検証やエラー処理を組み込むとき、またはフレームワークと自分のコードをつなぐ部分（アダプタ）を書くとき | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Type System Discipline](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-type-system-discipline/SKILL.md) | 型の検査を使い、ありえない状態をコンパイルの時点で作れなくする | エージェントが型を設計するとき、関数のシグネチャをレビューするとき、または静的型付き言語でコードを書くとき | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Make Operations Idempotent](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-make-operations-idempotent/SKILL.md) | 状態を変える操作を、何度実行しても、途中から実行し直しても、最後は同じ状態になるように作る | エージェントが、途中で止まったり、再起動や再試行で実行し直されたりすることがあるコマンド、起動や終了などの手順、処理を繰り返すループを設計するとき | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Migrate Callers Then Delete Legacy APIs](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | 呼び出し元を新しいAPIに移し、その変更の中で古いAPIも消す | エージェントが、古い呼び出し元が残っている状態で、新しい内部APIを導入するとき | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Separate Before Serializing Shared State](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md) | 複数の主体が共有する書き込み先を先に分け、分けられないときだけ、ロックなどで書き込みを直列化する | 並行して動く複数の主体が、同じファイル、ブランチ、キー、状態を持つオブジェクトに書き込むかもしれないとき | [第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b) |
| [Prove It Works](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md) | 作業の結果を、ビルドの成功のような代理指標ではなく、実際に動かした機能や実際の値を直接見て確かめる | エージェントが作業を終え、完了を宣言しようとするとき | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Fix Root Causes](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-fix-root-causes/SKILL.md) | 不具合の症状を隠すガードを追加せず、症状を起こした根本原因を突き止めて直す | エージェントが不具合をデバッグするとき | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Sequence Work into Verifiable Units](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-sequence-verifiable-units/SKILL.md) | 作業を確かめられる小さな単位に分け、各単位のチェック（テストなど）が通ってから次へ進み、コミットを正しさを示す順に並べる | エージェントが複数の段階がある作業（一括の修正、移行、似た編集の連続）をするとき、またはコミットやPRを並べる順番を決めるとき | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Test Behavior, Not Implementation](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-test-behavior-not-implementation/SKILL.md) | コードを、そのコードを使う側と同じ方法で呼び、観察できる結果を、テストに直接書いた期待値と比べる | エージェントがテストを書くとき、変えるとき、または残すかどうかを決めるとき | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Explain the Number](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-explain-the-number/SKILL.md) | 測った数値を信じる前に「何がその数値を頭打ちにしているか」を突き止め、エラーやキャッシュなど、別のものを測った可能性を証拠で消す | エージェントが、測った数値（高速化、性能の低下、スループット、レイテンシ、評価の結果）を、信じたり、報告したり、その数値をもとに作業したりする前 | [第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019) |
| [Guard the Context Window](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-guard-the-context-window/SKILL.md) | 大きな出力や文書をサブエージェントに読ませ、主スレッドには要約だけを置く | 大きな出力、長いファイル、同じファイルの読み直しで、エージェントのコンテキストが埋まってきたとき、またはエージェントが仕事を複数のサブエージェントに分けて並列に進める計画を立てるとき | [第20章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/c155cc) |
| [Never Block on the Human](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-never-block-on-the-human/SKILL.md) | 元に戻せる作業は人間の確認を待たずに進めて結果を見せ、元に戻せない操作だけを実行する前に人間に確認する | エージェントが、元に戻せる作業について「Xをしてもいいですか」と人間に聞きたくなったとき | [第20章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/c155cc) |
| [Encode Lessons in Structure](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) | 繰り返し必要になる修正を、文章の指示ではなく仕組み（lintのルール、メタデータのフラグ、実行時チェック、スクリプト）に組み込む | エージェントが、同じ指示を2回目に書いていると気づいたとき、または同じ訂正が繰り返されていると気づいたとき | [第21章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dd2d9f) |
