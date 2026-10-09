---
title: "第3部 Playbookで作業を進める"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/72f8ee"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:28+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 13
---

# 第3部 Playbookで作業を進める

第3部では、pstackの全Playbook（23件）を網羅的に取り扱います。

!

この部は読み飛ばしても構いません。関心のある章だけを読む使い方を推奨します。

各Playbookの原文は、[pstack](https://github.com/cursor/plugins/tree/main/pstack)のリポジトリでいつでも読めます。pstackは頻繁に更新されるため、すべてを先に読むより、必要になったときに該当する章と原文のファイルを参照するほうが確実です。

## 第3部で分かること

- 各Playbookが、どんな依頼のときに選ばれるか（例：『[**Bug fix**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)』は、「まず再現して」と書いた依頼で選ばれる）
- 各Playbookの手順と、各手順で何を求めているか（例：『[**Hillclimb**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md)』は、「1つの変更、1回の測定、採用か取り消し」を繰り返す）
- 似ているPlaybookとの違い（例：原因を知るだけなら『[**Runtime forensics**](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/runtime-forensics.md)』、直すなら『Bug fix』）

Playbookは、熟練したエンジニアなら自然に踏む仕事の手順を、型にした作業手順書です。

たとえば、バグ修正なら「再現→原因の特定→修正→同じ場所での確認」という順序が書かれています。手順が決まっていれば、どのエージェントが担当しても、同じ順序で作業を進められます。

Playbookは [`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) の中の参照ファイルで、利用者は直接呼びません。それでも中身を知っていると、**依頼にどんな言葉を入れればよいかが分かります**。

!

本書で紹介する依頼の例は、pstackの原文（[同梱ガイド](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/README.md)、[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)、poteto氏のX記事）に載っているものだけです。原文に依頼の例がないPlaybook（Runtime forensics、Trace forensics、Hillclimb、Pause safely）には、依頼の例を載せていません。このうちHillclimbは、同梱ガイドに書かれている「依頼で渡す内容」だけを説明しています。

## この部の章

| 章 | 役割 | 扱うPlaybook |
| --- | --- | --- |
| [第10章 問題を調べ、再現する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ea525d) | 調べて答えや診断を返す。コードは変えない | [Investigation](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/investigation.md)、[Runtime forensics](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/runtime-forensics.md)、[Trace forensics](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/trace-forensics.md) |
| [第11章 不具合を直し、性能を改善する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6fcb42) | 実行時の証拠をもとに、不具合や遅さを直す | [Bug fix](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)、[Perf issue](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/perf-issue.md)、[Hillclimb](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md) |
| [第12章 機能・構造・見た目をつくり直す](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b) | 機能を追加する、振る舞いを保って構造を変える、試して決める、見た目をそろえる | [Feature](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md)、[Refactoring](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/refactoring.md)、[Prototype](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/prototype.md)、[Visual parity](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/visual-parity.md) |
| [第13章 Skillを作り、評価する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0) | エージェントの働き方を決めるSkillを書き、その効果を測る | [Authoring or modifying a skill](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md)、[Eval](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md) |
| [第14章 PRを作成し、変更を本番へ届ける](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e) | PRを作り、merge-ready まで運び、検証済みの範囲を本番に入れる | [Opening a PR](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md)、[Babysit](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/babysit.md)、[Shipping](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/shipping.md) |
| [第15章 長時間の作業をエージェントに任せる](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609) | 1つの長い作業を止めずに進め、止めて再開し、後片付けをする | [Autonomous run](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autonomous-run.md)、[Pause safely](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/pause-safely.md)、[Session pickup](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/session-pickup.md)、[Worktree and simulator cleanup](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/worktree-cleanup.md) |
| [第16章 多数のPRを計画し、複数のエージェントで運用する](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5) | 何本ものPRにまたがる作業を計画し、複数のエージェントで運用する | [Multi-phase or multi-PR plan](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md)、[Orchestrate](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md)、[Autopilot-full](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-full.md)、[Autopilot-stack](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-stack.md) |

[第10章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ea525d)から[第12章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b)は、調べる、直す、作るという一つの変更を作る流れです。[第13章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0)はエージェントの働き方を改善するPlaybook、[第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e)は変更を本番へ届けるPlaybook、[第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609)と[第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5)は長時間・複数エージェントの作業として回すPlaybookです。

## 全Playbookの早見表

| Playbook | 概要 | 使う場面 | 解説 |
| --- | --- | --- | --- |
| [Investigation](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/investigation.md) | ソースコードや変更の履歴を読んで質問に答え、引用つきの説明か推奨を返す | 利用者が「Xはどう動くか」「Yはなぜこう作られたか」のような、コードや履歴を読めば答えが出る質問をするとき | [第10章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ea525d) |
| [Runtime forensics](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/runtime-forensics.md) | 動いているプロセスを計測して実行時の症状の原因を診断し、修正はせずに診断を返す | メモリリークやアイドル中のCPU空転などの症状が今も起きていて、エージェントが動いているプロセスを計測できるとき | [第10章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ea525d) |
| [Trace forensics](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/trace-forensics.md) | 事後に渡されたプロファイルやダンプを、プログラムを再実行せずに読み、原因を診断する | 利用者の環境で取得したcpuprofile、trace、spindump、heap snapshotなどの成果物だけがあるとき | [第10章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ea525d) |
| [Bug fix](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md) | 報告された不具合を再現して根本原因を突き止め、実行時の証拠で必要と確かめた最小限の変更で直す | 利用者が受け取る結果そのものが間違っている不具合を、エージェントが直すとき | [第11章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6fcb42) |
| [Perf issue](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/perf-issue.md) | 実際に測った遅さのトレースを取り、ベースラインと比べて性能を改善する | 動作に誤りはないが処理が遅く、利用者が1回の修正で性能を改善したいとき | [第11章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6fcb42) |
| [Hillclimb](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md) | 一つの指標を、「1つの変更、1回の測定、採用か取り消し」の繰り返しで目標まで改善する | 利用者が一つの指標を、1回の修正ではなく、目標に届くまで繰り返し改善したいとき | [第11章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/6fcb42) |
| [Feature](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md) | 扱うデータの形を先に決めてから、新しい振る舞いや変更した振る舞いを実装する | 利用者が機能の追加や、既存の振る舞いの変更を依頼するとき | [第12章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b) |
| [Refactoring](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/refactoring.md) | 今の振る舞いを保ったまま、名前の変更、抽出、重複の除去、移動などでコードの構造を変える | 利用者が振る舞いを変えずに、コードの構造だけを変えたいとき | [第12章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b) |
| [Prototype](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/prototype.md) | 捨てる前提のプロトタイプを作り、観察した結果で設計の判断を下す | レイアウトや挙動などの設計判断を、人に聞かずに、実際に作って観察した結果で低コストで決めたいとき | [第12章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b) |
| [Visual parity](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/visual-parity.md) | ベースラインの見た目を仕様とし、UIの見た目を画像差分がゼロになるまでピクセル単位でそろえる | 2つの実装の見た目を一致させるときや、スタイリングの仕組みを移行するとき | [第12章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/f1e85b) |
| [Authoring or modifying a skill](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md) | 決められた手順で `SKILL.md` を書き、作業中の判断を変える指示だけを残す | 利用者やエージェントが `SKILL.md` を新しく書く、または直すとき | [第13章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0) |
| [Eval](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md) | Skill、構造、プロンプトの変更がエージェントの行動に与える効果を、採用する前に盲検で測る | 利用者やエージェントが、Skillやプロンプトの変更を採用する前に、その変更が効くかを確かめたいとき | [第13章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8263c0) |
| [Opening a PR](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md) | 小さく順序立てたコミット、Conventional Commits 形式のタイトル、Briefing形式の本文で、すぐレビューできるPRを作る | ほかのPlaybookの作業の最後に、エージェントが変更をPRにするとき | [第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e) |
| [Babysit](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/babysit.md) | コンフリクト、レビューのスレッド、CIの失敗を片付け、PRやスタックを merge-ready まで運ぶ | 利用者が「緑にして」「PR X の様子を見て」のように、PRの状態について依頼するとき | [第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e) |
| [Shipping](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/shipping.md) | CIが通ったスタックの各PRを、コードを書いていないエージェントに検証させ、ルートから続く検証済みの範囲だけを1つずつマージする | 利用者が、CIが通ったスタックを本番に入れるよう頼むとき | [第14章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/45a56e) |
| [Autonomous run](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autonomous-run.md) | 終了条件を先に決め、その条件が満たされるまで、長いタスクを止まらずに進める | 利用者が「終わるまで回して」「/loop で X まで回して」のように、長いタスクを完了まで任せるとき | [第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609) |
| [Pause safely](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/pause-safely.md) | 作業を安全な区切りで止め、何も知らないエージェントが再開できる記録を残す | 利用者が明示的に止めるよう指示したとき、オフラインになるとき、Cursorを再起動するとき、会話のコンパクションが迫っているとき | [第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609) |
| [Session pickup](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/session-pickup.md) | 前のエージェントのトランスクリプト、Cloud AgentsのURL、pushされたブランチを読み、済んだ作業の続きから再開する | 利用者が、前のエージェントが途中まで進めた作業の再開や引き継ぎを依頼するとき | [第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609) |
| [Worktree and simulator cleanup](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/worktree-cleanup.md) | 使われていないことを確かめてから、マージ済みや放棄されたgit worktreeと古いiOSシミュレーターを消し、ディスクの空き容量を増やす | 利用者が、何がディスクを使っているかを尋ねるときや、worktreeやシミュレーターの片付けを依頼するとき | [第15章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/7d7609) |
| [Multi-phase or multi-PR plan](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md) | コードを書かずに、PRごとの検証方法まで決めたチェックリスト形式の計画書を作る | 複数のフェーズやスタックしたPRにまたがる作業を、エージェントが始める前に計画するとき | [第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5) |
| [Orchestrate](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md) | 何日も続き、多数のPRとサブエージェントが動くプロジェクトの管理を、コードを書かない1体のコーディネーターエージェントに任せる | 利用者が、1体のエージェントが動ける期間では終わらないプロジェクトを、1つのチャットに任せるとき | [第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5) |
| [Autopilot-full](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-full.md) | 互いに独立したPRのキューを、PRごとのオーナーに任せ、コーディネーターエージェントの検証の判定を通ったものから運用者の確認なしでマージする | 運用者が互いに独立したPRのキューを任せ、エージェントにマージの権限を渡せるとき | [第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5) |
| [Autopilot-stack](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-stack.md) | Autopilot-fullと同じ手順でPRを作って検証し、マージせずに1本のスタックにして運用者に渡す | 運用者がマージ前にレビューしたいとき、変更どうしが依存しているとき、エージェントにマージの権限を渡せないとき | [第16章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8a8dd5) |
