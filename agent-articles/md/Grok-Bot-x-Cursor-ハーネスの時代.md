---
title: "Grok Bot x Cursor: ハーネスの時代"
source_url: "https://x.com/bossriceshark/status/2094074367324168595"
author: "Matt Rice (@bossriceshark)"
published_at: "2026-08-30"
retrieved_at: "2026-08-31T22:19:07+09:00"
site: "x.com"
content_type: "article"
original_language: "en"
---

# Grok Bot x Cursor: ハーネスの時代

あなたは [@Bot](https://x.com/@Bot)

 に話しかける。Bot が Cloud Agent を起動する。重い作業は Cursor が担う。

私の見方はこうだ。

Cursor にはもともと優れた Cloud Agent 基盤があった。ただ、ほとんどの人はそのタブに一日中張りついてはいない。

Grok Bot は、それを実際に起動するための手段だ。

仕事を Bot に伝える。Bot が Cloud Agent を起動する。あなたは PR をレビューする。

セットアップコストはおよそ 1/20 に感じた。大きな解放だ。

レーンはこうだ:

誰かが Grok Bot に話しかける。Bot が Cursor Cloud Agent を起動する。

同じ動き。その上に載せる仕事が違うだけだ。

Bot はコーディングすべきではない。

リポジトリ作業の課金は Cursor プランが持つ。Grok Bot の週次バケットはそのまま残る。メーターが違う。

Bot が設計する。Cursor が重い作業を担う。

すべての Cloud Agent は /poteto-mode で動く。

## 動き方

古いループ: Cursor を開く、リポジトリを選ぶ、プロンプトを書く、スレッドを見守る。

新しいループ: Bot に Cloud Agent を起動するよう伝える。それは [cursor.com/agents](https://cursor.com/agents)

 に現れる。Bot はマネージャーのまま。リポジトリ作業は Cursor プランが支払う。あなたは PR に判断を加える。

- あなたは 1 つの Bot と話す
- Bot が Cloud Agent を起動し、規模を決め、監視する
- それらのエージェントは /poteto-mode で動く
- Cursor が重い作業を担う
- あなたと Bot がレビューする
## 1. Kun Chen — 工場

[@kunchenguid](https://x.com/kunchenguid/status/2091638832307536357)

 は大量のオープンソース（24k+ スター）を抱え、Issue と PR に溺れていた。

彼は Grok Bot でリポジトリを書かせたわけではない。Firstmate という Bot にソフトウェア工場を回せと伝えた。Firstmate が crewmates と話す。Crewmates が Cursor Cloud Agent を回すので、コーディングが共有 Bot VM を奪い合わない。判断と PR は Kun に戻ってくる。

後の実績: 自動化を立てたあと、625 件のユニークな項目をトリアージした。331 Issue、294 PR。

> **[図]** Firstmate のチャット画面。Captain 宛てに Grok Ship のトリアージ自動化結果が報告されている。625 件（Issue 331、PR 294）を処理し、Issue は ready-for-pr 214、already fixed 41、既存 PR への誘導 35、その他 41。PR はマージ済みまたはマージ可能 68、作者待ち 67、CI またはコンフリクト 60、その他 99。

なぜ良いか: Cloud Agent が工場を横にスケールさせる。Bot は船長のまま。Kun が判断を加える。彼は本音も言った — Grok Bot なしでもできるが、これほど簡単でメンテが少なくはない、と。

これを貼る:

```setup Grok Ship for me. follow GROK_SHIP.md in this github repo: kunchenguid/grok-ship

Whenever you launch a Cursor Cloud Agent, run /poteto-mode on it.
You manage. Cursor does the repo work. Bring PRs back to me.
```

テンプレート: [github.com/kunchenguid/grok-ship](https://github.com/kunchenguid/grok-ship)

セットアップスレッド: [x.com/kunchenguid/status/2090463366762676732](https://x.com/kunchenguid/status/2090463366762676732)

## 2. Ian Nuttall — Bot がモデルを選ぶ

[@iannuttall](https://x.com/iannuttall/status/2089320585146802335)

 は、みんな Grok Bot を開発にどう使っているか尋ね、自分で答えた。

Bot に頼む。Bot は Cursor Cloud Agent を使う。彼の Bot はデフォルトを Opus から外し、次のようにルーティングし始めた:

- 計画は Fable
- 実装は Sol 5.6
- 汎用は Grok 4.6
すべて Bot が管理する。彼はモデル選択を渡り歩かない。そのスタックでは Sol はおしまいだ。

OpenAI は Cursor 上のモデルを縮小している。停止案は 11月12日。だから Ian がちょうど組んだ実装枠は、すでに期限がついている。Sol は優れたモデルだ。私は本当に好きだ。ただ、このハーネスにはもう長くは残らない。

動き自体は変わらない。どの仕事にどのモデルかを Bot に伝えればよい。Cloud Agent は起動する。メニューが変わったら実装役を差し替える。それがハーネスの本質だ。

> **[図]** Conductor という Bot とのモバイルチャット。ユーザーが昨日 Keep ブランチで作業していた内容の確認を依頼している。Bot はワークスペース「Mobile input visibility fix」がスリープ中であること、Claude Fable 5 で 17:30 頃に開始したこと、コミット `ef745ef: fix(app): keep mobile overlays visible above the software keyboard` がワークスペースブランチにのみあり、push も PR もないことを報告している。

数日後、彼はテネリフェのハンモックから投稿した。サポートは Grok Bot。バグは Cursor のバックグラウンドエージェント。プリミティブは同じだ。チケット上のモデル名だけが動く部分だ。

なぜ良いか: これが私が言い続けている 2+2=5 だ。同じ仕事に 2〜3 のモデルをルーティングできるハーネスが優位だ。Cursor がそのハーネス。Bot は、それをスマホから実際に起動する手段だ。Sol がメニューから消えるのはシグナルであり、エージェントタブに住み直す理由ではない。

これを貼る:

Ian は実装枠に Sol を書いた。アカウントから OpenAI モデルがすでに消えているなら、そこには Grok 4.6 Extra High を置け。

```For this repo, launch Cursor Cloud Agents and route the work:
- Fable for the plan
- Sol 5.6 for implementation
- Grok 4.6 for general purpose

Every Cloud Agent runs /poteto-mode.
You manage the agents. I review the PR.
Do not write the code on your own computer.
```

## 3. Nick + Brandon — マネージャーはマネージャーのまま

多くの人のスイッチが入った使い方のハックだ。

[@BStarr119](https://x.com/BStarr119/status/2091147114411610182)

 は Grok Bot の週次バケットを全部燃やし、Cursor Ultra はほとんど使っていなかった。彼はスキルを保存し、Bot は管理だけするようにした。重い作業は長時間稼働の Grok 4.6 Cloud Agent として起動する。

投稿した結果: Bot 使用量の 5% を食っていたジョブが 1% 未満になった。スループットは同等以上。支払うのは Ultra だ。

[@thedogfather](https://x.com/thedogfather/status/2093725258620518829)

 は同じスキルを Heavy Lift Cloud Agents として書き起こした。Bot はコードを書かない、ブラウズしない、VM を食わない。スコープし、起動し、監視し、修正を求め、納品する。

> **[図]** 「Same heavy job. Different outcome.」という比較図。左（WITHOUT THE SKILL）は週次 Grok Bot 使用量のバッテリーが空で、未完成の車体と「Weekly Grok Bot usage exhausted. Nothing to show.」。右（WITH THE SKILL）はバッテリーが満タンで、完成した車と「Weekly limit preserved. Cloud Agent did the grind.」。スキルなしでは Bot 枠を使い果たし、スキルありでは週次上限を残したまま Cloud Agent が重い作業を担う、という対比。

なぜ良いか: メーターが二つある。Grok Bot の週次使用量が一つ。Cursor モデルに対する Cursor プラン使用量がもう一つで、こちらのプールは厚い。Bot が自分のコンピュータでコードを書くと、間違った請求を燃やす。Bot が Cloud Agent を起動すれば、Cursor が持ち上げ、Bot は安く済む。

これを貼る:

```Save this as a skill called "Heavy Lift Cloud Agents".

For any heavy lifting (coding, multi-file edits, long research, VM work, parallel jobs) do not execute the work yourself on the Grok Bot computer.

Act only as management: break the task into goals, size the agent, launch one or more Cursor Cloud Agents.

Every Cloud Agent runs /poteto-mode.
Prefer long-running / background / parallel.
Monitor, request revisions, return only the final result or an approval ask.

Never perform the heavy compute yourself.
Burn the Cursor plan, not the Grok Bot weekly bucket.
```

ガイド: [tlgenapp.com/gbot-skills](https://www.tlgenapp.com/gbot-skills)

Bot が無視するなら、プロンプトに use heavy lift を足せ。

## 4. Kevin Parko — eng Bot はリポジトリを書かない

[@n2parko](https://x.com/n2parko/status/2088664030789681260)

 は SpaceXAI のプロダクト。社内で Grok Bot を使い、Cursor の構築を助けた。

重要な一文: 社内でマージされた PR のうち、Grok Bot が二桁パーセントを占めた。

彼の eng manager Bot はコードを書かない。仕事を分解して委譲する。IC の eng Bot が Cursor Cloud Agent を回し、出力をゴールと照合する。

> **[図]** 開発向けチャット。ユーザーが「look into how we implemented speech to text in the editor」と依頼し、エージェントは everysphere の STT パスをリポジトリマップから調べ始めている。Slack 検索はノイズが多く、repo dig 待ち。下部にタスク「Map editor speech-to-text」が Running と表示され、「Open in Cursor」ボタンがある。

なぜ良いか: これは Bot に名前を付けた Heavy Lift だ。メモリは分かれている。マネージャーはマネージャーのまま。Cloud Agent が IC だ。

これを貼る:

```You are the eng manager. You do not write the repo.

Break this job down. Launch Cursor Cloud Agents for the IC work.
Every Cloud Agent runs /poteto-mode.
Check the PR against the goal. Bring me the diff, not the play-by-play.
```

より長い PM 向けセットアップ: [x.ai/bot/guides/grok-bot-for-pms](https://x.ai/bot/guides/grok-bot-for-pms)

## 5. Krista Letz — 複数を回す

[@kristaletz](https://x.com/kristaletz/status/2089103618121314689)

 は Enterprise GTM の記事を書いた。PR を出す仕事とは違うが、プリミティブは同じだ。

Bot に並列タスク用の Cloud Agent を複数起動するよう伝え、それをスキルにする。彼女にはコードベースに接続した「Cursor 10x engineer」Bot もあり、エンジニアに ping せず顧客にその場で答えられる。

> **[図]** macOS 上のメッセージング画面。左サイドバーに「Olive - Chief of...」や Fun / GTM Team / Customers などのセクションがあり、チャット「reads」が開いている。本のレビュー会話（London Falling など）が表示され、サイドバーのコンテキストメニューで Pin、Move to、Mark as Unread などが選べる。

なぜ良いか: 並列 Cloud Agent が、Bot をシングルスレッドに感じさせなくする手段だ。Ian はその問いを口に出した。Krista はただ実行している。

これを貼る:

```Split this into parallel Cursor Cloud Agents. One agent per workstream.
Every Cloud Agent runs /poteto-mode.
You coordinate. I only want a status when something needs a decision.
Save that as a skill so I don't have to retype it.
```

## 正直な限界

解放は本物だ。雑に回すと請求も本物だ。

[@kloss_xyz](https://x.com/kloss_xyz/status/2093747045458968590)

 は、Bot 起動の Cloud Agent が最初の返信のあと静かに fast に切り替わり、cursor-grok-4.6-high-fast として課金されることを見つけた。7 日で 10 億トークンを燃やした。

> **[図]** Cursor の使用量ダッシュボード。総トークン 1B、Included 26.7M、On-demand 977.9M。8月23日〜29日の累積トークン推移で、27日以降に急増し Today（8月29日）で約 10 億に達している。凡例の主因は cursor-grok-4.6-high-fast。ほかに gemini-2.5-flash、cursor-grok-4.6-high、cursor-grok-4.5-high-fast、cursor-grok-4.5-high、claude-4.5-sonnet。

フォローアップを送る前に model フィールドを確認せよ。Cloud Agent 設定では、本当に使いたいモデルだけを有効にしておけ。

彼は Bot メーターを食うルーチンも監査した — 15 分 cron は 1 日 96 回、休止中の Bot がまだ Web にアクセスする、同じ質問に 3 つの Bot が答えるグループチャット。それらの習慣のコストが $1,048 だった。Kun の工場をスケールする前に読む価値がある。

ほかに繰り返し見かける小さなもの:

- Bot 起動のエージェントは、エージェント一覧でソースフィルタをオンにするまで隠れることがある（@piotrpliszko）
- チームのトグル「review cloud agents」はオンのままにする必要がある
- 作業を Cloud Agent に送らなければ、Bot は自分のコーディング課金を食う
たぶん一度はやる。そのあと Heavy Lift を入れて、間違ったメーターを燃やすのをやめろ。

## 私が回している方法

仕事を Bot に伝える。Cloud Agent を起動するよう伝える。Cursor エージェントは常に /poteto-mode で動かすルールを Bot に設定する。

他スタックを締め出す話ではない。オラクルが必要なときは Fable も出す。

Grok Bot × Cursor Cloud Agents は、エージェントタブを見つめなくても本物のリポジトリ作業を動かす、私が知っている中でセットアップコストが最も低い方法だ。

Cursor には基盤があった。Bot が、それを実際に起動するものにした。

私たちはハーネスの時代にいる。

## 一つ試せ

貼り付けブロックを一つ選べ。二つでも三つでも。

Grok Bot に渡せ。本物のリポジトリを指せ。

Cursor を起動するたびに /poteto-mode を走らせろ、と伝えろ。
