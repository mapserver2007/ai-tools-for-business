---
title: "第18章 Architecture ― 境界と依存を設計する6つの原則"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:30+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 23
---

# 第18章 Architecture ― 境界と依存を設計する6つの原則

この章では、次の6つの原則を扱います。

1. [Model the Domain](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md)
2. [Boundary Discipline](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-boundary-discipline/SKILL.md)
3. [Type System Discipline](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-type-system-discipline/SKILL.md)
4. [Make Operations Idempotent](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-make-operations-idempotent/SKILL.md)
5. [Migrate Callers Then Delete Legacy APIs](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md)
6. [Separate Before Serializing Shared State](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md)

6件はArchitecture（設計）のグループの原則で、どれも**エージェントがコードをどんな形（状態の持ち方や、検証を置く場所など）に組み立てるか**を決めます。同梱ガイドのページ [`docs/guide/08-principles.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md) は、6件を「状態、検証、互換性をどこに置くか」を決める原則とまとめています。

6件を使うと、エージェントは、次のように動作します。

- 状態を、いくつもの真偽値の組み合わせではなく、状態機械で持つ
- 外から受け取るデータの検証を、境界に集める
- 呼び出し元をすべて新しいAPIに移したら、その同じ変更の中で古いAPIを消す

!

- **状態機械**・・・ 取りうる状態と、状態から状態への移り方を、あらかじめ決めておく書き方。ある時点では、決められた状態のどれか一つだけを取る  
  たとえば、信号機は、青、黄、赤のどれか一つだけを示し、青→黄→赤の決まった順に移ります。「青と赤が同時につく」ことも、「青から赤へ飛ぶ」こともありません。状態機械は、このような決まりをコードで表します。
- **境界**・・・ フォームの入力やAPIの応答のように、外からデータが入ってくる場所

この章では、6原則を、[第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b)と同じく、ルールと発火条件の観点で1件ずつ解説し、最後に、構造そのものをエージェントへの説明書にするという見方でまとめます。

本章の依頼例も、[第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b)と同じく、原則名を入れた一行の指示にしています。原則名を書かなくても、作業が発火条件に当てはまればエージェントが原則を自分で読んで適用することは、[第17章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/a8e80b)の前提で見たとおりです。

!

本章で依頼例を載せているのは、6件のうち『Separate Before Serializing Shared State』の1件だけです。

本書では、依頼例を、pstackの同梱ガイドや[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)に記載があるものだけにとどめるものとします。原文に依頼例がない原則について本書で依頼例を作ると、pstackが想定していない使い方を示してしまうおそれがあるためです。

## この章の構成

この章の構成は次のとおりです。

- 6原則の一覧
- 『Model the Domain』は、ドメインを条件分岐ではなく構造で表す
- 『Boundary Discipline』は、入力の検証を外との境界に集め、内側は型を信じる
- 『Type System Discipline』は、型で不正な状態を作れなくする
- 『Make Operations Idempotent』は、操作を何度実行しても同じ結果になるように作る
- 『Migrate Callers Then Delete Legacy APIs』は、呼び出し元をすべて移し、その変更の中で古いAPIも消す
- 『Separate Before Serializing Shared State』は、書き込み先の共有をなくすのが先で、ロックは最後の手段
- Architectureの6原則は、構造そのものをエージェントへの説明書にする
- まとめ

## 6原則の一覧

| Principle | 一文の結論 |
| --- | --- |
| 『**Model the Domain**』 | ドメインを、散らばった条件分岐ではなく構造で表す |
| 『**Boundary Discipline**』 | 検証とエラー処理を、外からデータが入る境界に集める。境界の内側のコードは型を信じる |
| 『**Type System Discipline**』 | 型の検査を使い、ありえない状態をコンパイルの時点で作れなくする |
| 『**Make Operations Idempotent**』 | 状態を変える操作を、何度実行しても、途中から実行し直しても、最後は同じ状態になるように作る |
| 『**Migrate Callers Then Delete Legacy APIs**』 | 呼び出し元を新しいAPIに移し、その変更の中で古いAPIも消す |
| 『**Separate Before Serializing Shared State**』 | 書き込み先の共有をなくすのが先。ロックで書き込みを順番待ちにするのは、本当に必要なときだけ |

## 『Model the Domain』は、ドメインを条件分岐ではなく構造で表す

原則『**Model the Domain**』は、実際のドメインを、あちこちの条件分岐の中にばらばらに書くのではなく、データの構造で表すよう求めます。  
エージェントは、状態や分岐が増えそうなとき、**条件分岐（if/else）を追加する前に、ドメインを表す構造を選びます**。

!

- **ドメイン**・・・ そのソフトウェアが扱う業務や対象（例：ネットショップなら注文、在庫、配送）
- **データの構造**・・・ データが持つ項目と、各項目が取る値の型（以下の例の`Order`・`OrderFlags`）
- **ドメインを表す構造**・・・ 業務の実際の決まりと同じ形をした、データの構造

たとえば、実際の注文は、「支払い待ち」「発送待ち」「発送済み」「キャンセル済み」のどれか一つの状態だけを取ります。

上記の注文データの構造を2通りに書くと、次のようになります。

```
// ドメインを表す構造：状態は、status の4つのうちどれか一つだけを取る
type Order = {
  address: string;
  status: "unpaid" | "paid" | "shipped" | "canceled";
};

// ドメインを表していない構造：3つの真偽値で持つ
// isShipped: true と isCanceled: true のような、実際にはない組み合わせも取れてしまう
type OrderFlags = {
  address: string;
  isPaid: boolean;
  isShipped: boolean;
  isCanceled: boolean;
};
```

どちらも、注文が持つ項目と、各項目が取る値を決めているので、データの構造です。  
このうち、実際の注文の決まりと同じ形をしている `Order` だけが、ドメインを表す構造です。

### 散らばった真偽値、繰り返される前提、広がる分岐は、不要な複雑さである

原則は、次の3つを、本来は不要な複雑さと呼びます。

- 散らばった真偽値
- ファイルごとに繰り返される「このデータはこの形のはず」という前提
- ファイルをまたいで広がる分岐

### 3つの複雑さを含むコードでは、ありえない状態が書けてしまう

たとえば、ネットショップの注文を、発送ラベルを作るファイルと、お知らせメールを作るファイルの2つで扱うケースを考えてみましょう。

3つの複雑さをすべて含むコードは、次のようになります。

```
// order.ts：注文の状態を、3つの真偽値で持つ（散らばった真偽値）
type Order = {
  address: string;
  isPaid: boolean;
  isShipped: boolean;
  isCanceled: boolean;
  trackingNo?: string;
};

// label.ts：発送ラベルを作る
function labelText(order: any): string {
  // 「注文には住所があるはず」という前提を、ここで確かめる
  if (!order.address) throw new Error("住所がありません");
  // 状態の分岐
  if (order.isCanceled) return "キャンセル済み";
  if (order.isShipped) return "発送済み";
  if (order.isPaid) return "発送待ち";
  return "支払い待ち";
}

// mail.ts：お知らせメールの件名を作る
function mailSubject(order: any): string {
  // 同じ前提を、別のファイルでもう一度確かめる
  if (!order.address) throw new Error("住所がありません");
  // 同じ分岐が、ファイルをまたいで繰り返される
  if (order.isCanceled) return "ご注文をキャンセルしました";
  if (order.isShipped) return "商品を発送しました";
  if (order.isPaid) return "お支払いを確認しました";
  return "お支払いをお待ちしています";
}
```

このコードでは、`isShipped` と `isCanceled` が同時に `true` という値も書けてしまいます。  
これが**ありえない状態**で、「発送済み」と「キャンセル済み」は、実際の注文では同時に成り立ちません。  
また、`isShipped` が `true` なのに `trackingNo`（追跡番号）がない値も書けてしまいます。

### ドメインを表す構造を選ぶと、ありえない状態が書けなくなり、分岐も減る

エージェントがドメインを表す構造を選ぶと、**ありえない状態はそもそも書けなくなり、条件分岐も減ります**。ドメインを表す構造には、状態機械や、項目を決めた型付きのオブジェクトなどがあります。

同じ注文を、ドメインを表す構造で書くと、次のようになります。

```
// order.ts：注文の形と、取りうる状態を一か所で決める
type OrderStatus =
  | { state: "unpaid" }
  | { state: "paid" }
  | { state: "shipped"; trackingNo: string }
  | { state: "canceled" };

type Order = { address: string; status: OrderStatus };

// 状態ごとの文言を、一つの表にまとめる
const LABEL_TEXT: Record<OrderStatus["state"], string> = {
  unpaid: "支払い待ち",
  paid: "発送待ち",
  shipped: "発送済み",
  canceled: "キャンセル済み",
};

// label.ts：状態ごとの文言を表にまとめ、型を信じて表を引くだけにする
function labelText(order: Order): string {
  return LABEL_TEXT[order.status.state];
}

// mail.ts：状態ごとの件名を表にまとめ、型を信じて表を引くだけにする
const MAIL_SUBJECT: Record<OrderStatus["state"], string> = {
  unpaid: "お支払いをお待ちしています",
  paid: "お支払いを確認しました",
  shipped: "商品を発送しました",
  canceled: "ご注文をキャンセルしました",
};

function mailSubject(order: Order): string {
  return MAIL_SUBJECT[order.status.state];
}
```

このコードでは、3つの複雑さが次のように消えます。

- **散らばった真偽値**・・・ 3つの真偽値の代わりに、`OrderStatus` が4つの状態のどれか一つだけを取ります。「発送済みかつキャンセル済み」は書けません。また、追跡番号は `shipped` のときだけ持ち、`shipped` なら必ず持ちます。
- **繰り返される前提**・・・ 「注文には住所がある」という前提は、`Order` 型に一度だけ書きます。各ファイルは型を信じるので、住所を確かめ直すことはしません。
- **ファイルをまたぐ分岐**・・・ 状態ごとの文言は、表を引くだけで決まります。状態を追加するときは、表に1行追加すれば済み、追加し忘れるとコンパイルの時点でエラーになります。

### 構造は、後から入れ直すのではなく、コードを書くときに選ぶ

エージェントは、**コードを書くときに構造を選びます**。書くときなら、構造を選ぶ手間はほとんどかかりません。

一方、条件分岐で書き終えたコードに後から構造を入れ直す作業は、後回しにされがちです。

後回しにされるのは、入れ直してもコードの挙動は何も変わらず、入れ直す作業がリファクタリングに該当するからです。  
リファクタリングは、新しい機能と違って目に見える成果がないため、開発者もエージェントも、機能の追加を先に行い、リファクタリングを後に回しがちです。

たとえば、送料を決める条件分岐が3つのファイルに広がった後で、参照表に置き換えるケースでは、置き換えても、送料の金額も画面の表示も変わりません。そのため、この置き換えは「今すぐでなくてよい作業」として後に回され、その間にも、新しい機能のたびに条件分岐が増えていきます。

### ルール：散らばった書き方ごとに、代わりの構造が決まっている

この原則が挙げる代表的な置き換えは、次のとおりです。

| 散らばった書き方 | 代わりの構造 |
| --- | --- |
| 状態を表す真偽値（`isLoading`、`isError` など）や、「今どの段階か」の確認が、コードのあちこちにある | 状態機械（取りうる状態と移り方を定めた表し方） |
| 関数にばらばらの引数を渡し、「このデータにはこの項目があるはず」という同じ前提があちこちで繰り返される | 項目を決めた型付きのオブジェクト（例：`User` 型） |
| 種類ごとに処理を分ける同じ条件分岐が、複数のファイルに広がっている | マップや参照表（種類をキーにして、対応する値や処理を引く表）、discriminated union（種類を示すフィールドで見分けられる、型の組み合わせ） |
| 状態を、その場その場で直接書き換えている | reducer（今の状態と操作から、次の状態を計算する関数） |

表の各行を、例とコードで1つずつ見ていきます。

#### 真偽値の代わりに、状態機械を使う

状態を真偽値で持つと、`running`（実行中）と `failed`（失敗）が同時に `true` という矛盾した状態も、コンパイルでエラーにならずに書けてしまいます。  
状態を状態機械で表せば、**その組み合わせはそもそも書けません**。

```
// 前：矛盾した組み合わせが表現できてしまう
type ExportJobFlags = { running: boolean; failed: boolean; retrying: boolean };

// 後：状態ごとに持てるデータが決まる
type ExportJob =
  | { state: "queued" }
  | { state: "running"; attempt: number }
  | { state: "failed"; attempt: number; error: string }
  | { state: "done"; rowCount: number };

// 移り方も決める：失敗したジョブだけが、次の試行として running に戻れる
function retry(job: ExportJob): ExportJob {
  if (job.state !== "failed") return job;
  return { state: "running", attempt: job.attempt + 1 };
}
```

#### ばらばらの引数の代わりに、型付きのオブジェクトを使う

たとえば、会員の名前、メールアドレス、プランを、Welcomeメールを送る関数と請求書を作る関数に、それぞればらばらの引数で渡しているケースの場合、どちらの関数も「会員には名前、メールアドレス、プランがあるはず」という同じ前提を、それぞれの引数の並びで繰り返しています。

エージェントは、会員を表す `User` 型を一つ作り、2つの関数がどちらも `User` を受け取るように直します。  
こうすれば、会員に項目を追加するときも、直すのは `User` 型の一か所だけで済みます。また、名前とメールアドレスを逆の順番で渡してしまう間違いも起きません。

```
// 前：同じ3つの引数を、関数ごとに並べている
function sendWelcomeMail(name: string, email: string, plan: string) { /* ... */ }
function createInvoice(name: string, email: string, plan: string) { /* ... */ }
```

```
// 後：会員の形を User 型に一度だけ書き、2つの関数はこれを受け取る
type User = { name: string; email: string; plan: "free" | "paid" };

function sendWelcomeMail(user: User) { /* ... */ }
function createInvoice(user: User) { /* ... */ }
```

#### 広がった条件分岐の代わりに、参照表や discriminated union を使う

たとえば、注文の種類ごとの送料を、画面、請求、メールの3つのファイルでそれぞれ、条件分岐で決めているケースの場合、エージェントは「種類から送料を引く参照表」を一つ作り、3つのファイルがどれもその表を引くように直します。

こうすれば、注文の種類が増えても、3つのファイルの条件分岐をそれぞれ直す必要はなく、表に1行追加するだけで済みます。

```
type OrderKind = "standard" | "express" | "pickup";
declare const order: { kind: OrderKind };

// 前：画面、請求、メールの3つのファイルに、同じ if/else がある
function shippingFee(kind: OrderKind): number {
  if (kind === "standard") return 500;
  if (kind === "express") return 1200;
  return 0;
}

// 後：種類から送料を引く参照表を一つだけ作り、3つのファイルはこれを引く
const SHIPPING_FEES: Record<OrderKind, number> = {
  standard: 500,
  express: 1200,
  pickup: 0,
};

const fee = SHIPPING_FEES[order.kind];
```

`Record<OrderKind, number>` と書いておくと、注文の種類を型（`OrderKind`）に追加したのに表（`SHIPPING_FEES`）へ行を追加し忘れた場合、コンパイルの時点でエラーになります。

参照表は、種類ごとに「値」が一つ決まるときに向いています。

一方、種類ごとに**持つデータそのものが違う**ときは、エージェントは **discriminated union** を使います。

たとえば、支払い方法が「カード」「銀行振込」「代金引換」の3種類あり、カードのときだけカード番号の下4桁を、銀行振込のときだけ振込先の口座番号を持つケースが、これに該当します。

種類を表す項目と、省略できる項目（optional型）で書くと、「カードなのに口座番号が入っている」という値も書けてしまいます。  
discriminated union で書けば、`kind` の値ごとに持てる項目が決まるので、そうした値は書けません。

```
// 前：どの支払い方法でも、すべての項目を持ててしまう
type PaymentLoose = { method: "card" | "bank" | "cod"; cardLast4?: string; bankAccount?: string };

// 後：kind の値ごとに、持てる項目が決まる
type Payment =
  | { kind: "card"; cardLast4: string }
  | { kind: "bank"; bankAccount: string }
  | { kind: "cod" };

function paymentLabel(p: Payment): string {
  switch (p.kind) {
    case "card":
      return `カード（末尾 ${p.cardLast4}）`;
    case "bank":
      return `銀行振込（口座 ${p.bankAccount}）`;
    case "cod":
      return "代金引換";
  }
}
```

#### その場の書き換えの代わりに、reducer を使う

たとえば、買い物かごの中身を、商品一覧の画面、商品の詳細画面、かごの画面の3か所で、それぞれ直接書き換えているケースでは **reducer** が向いています。  
この場合、かごの中身がどこで、どう変わったのかを知るには、3か所をすべて読む必要があります。

エージェントは、かごへの操作（追加、削除）を型で決め、「今のかごと操作から、次のかごを計算する」reducer を一つ作ります。3か所は、かごを直接書き換えず、操作を reducer に渡すだけにします。  
こうすれば、**かごの中身の変わり方は、reducer の中だけを読めば分かります**。

```
type CartItem = { id: string; price: number };
type Cart = { items: CartItem[] };
declare let cart: Cart;
declare const item: CartItem;
declare const id: string;

// 前：3つの画面で、それぞれ直接書き換えている
cart.items.push(item);
cart.items = cart.items.filter((i) => i.id !== id);

// 後：操作を型で決め、次のかごの計算は reducer の中だけで行う
type CartAction =
  | { type: "add"; item: CartItem }
  | { type: "remove"; id: string };

function cartReducer(cart: Cart, action: CartAction): Cart {
  switch (action.type) {
    case "add":
      return { items: [...cart.items, action.item] };
    case "remove":
      return { items: cart.items.filter((i) => i.id !== action.id) };
  }
}

cart = cartReducer(cart, { type: "add", item });
```

#### 無理に構造を入れない

ただし、原則は、無理に構造を入れることは求めていません。今のコードが分かりやすく、一か所にまとまっていて、これから増える見込みもないなら、エージェントは単純なコードのままにします。

また、エージェントは、**呼び出しの間に1段挟むだけで何も減らさない、共通の関数や型を疑います**。分岐も、重複したルールも、ありえない状態も減らさない共通の関数や型は、読み手が開いて確かめる場所を増やすだけだからです。

### 発火条件

- 状態を持つロジックを書くとき
- 分岐が多いとき
- 「このデータにはこの項目がある」という同じ前提が、複数のファイルで繰り返されるとき

次のようなことが起きていたら、この原則を飛ばした兆候です。

- エージェントが、新しい機能のために、既存の条件分岐の連なりに、分岐をもう一つ追加した
- エージェントが、既存の真偽値と常に値をそろえておく必要のある、2つ目の真偽値を追加した

たとえば、読み込み中を表す `isLoading` があるところに、エラーを表す `isError` を追加したケースの場合、読み込みが失敗したとき、コードは `isError` を `true` にし、同時に `isLoading` を `false` に戻す必要があります。

`isLoading` を戻し忘れると、`isLoading: true` と `isError: true` が同時に成り立ち、画面は「読み込み中なのにエラー」という食い違った状態になります。

このように、2つ目の真偽値を追加すると、どちらかの値を書き換えるたびに、もう一方の値もそろえる必要が生まれます。

`/poteto-mode` の『[Non-negotiables](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#non-negotiables)』も、この原則を求めています（[第8章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/096f3d)）。

『Non-negotiables』は、どんなコードを書くときも、エージェントがまずデータの形を明らかにし、この原則に沿って構造を選ぶよう求めています。**24件の原則のうち、『Non-negotiables』で名指しされているのは、この『Model the Domain』だけです**。

## 『Boundary Discipline』は、入力の検証を外との境界に集め、内側は型を信じる

原則『**Boundary Discipline**』は、**入力の検証、型の絞り込み、エラー処理を、システムの境界に置く**よう求めます。この原則は、境界の例として、CLI引数、設定ファイル、外部API、ネットワークを通して届くデータを挙げています。

境界で確かめた値には型が付いています。そのため、境界の内側のコードは、その型のとおりの値が来ると信頼して使い、同じ確認を繰り返しません。

原則が確認を境界に集めるのは、確認がコードのあちこちに散らばると、次の2つの問題が起きるからです。

- 同じ確認を、何か所にも書くことになる
- 開発者もエージェントも、「どこかで確かめているはずだ」と思い込む。どの確認がどこで行われているかを把握しない限り、確かめていない経路が残っても気づけない可能性がある

次のコードは、確認がコードのあちこちに散らばった例です。注文フォームから届く「数量」が1以上かどうかを、一部の関数だけが確かめています。

```
let stock = 10; // 在庫の数

// 値段を計算する：数量が1以上かを確かめる
function calcPrice(quantity: number): number {
  if (quantity < 1) throw new Error("数量は1以上にしてください");
  return quantity * 500;
}

// 在庫を減らす：「どこかで確かめているはず」として、何も確かめない
function reserveStock(quantity: number) {
  stock = stock - quantity;
}

// 注文画面：calcPrice を先に呼ぶので、確かめてから在庫を減らす
calcPrice(2);
reserveStock(2);

// 別の画面：reserveStock だけを直接呼ぶ
reserveStock(-3); // 在庫が 8 から 11 に増えてしまう
```

注文画面の経路では `calcPrice` が確かめていますが、`reserveStock` だけを呼ぶ経路には確認が1つもありません。  
そのため、`-3` がそのまま届き、在庫を減らすはずの処理で在庫が増えてしまいます。

同じ処理を原則どおりに書くと、次のようになります。

```
let stock = 10; // 在庫の数

// 境界：フォームから届いた値を、ここで一度だけ確かめる
function parseQuantity(input: string): number {
  const quantity = Number(input);
  if (!Number.isInteger(quantity) || quantity < 1) {
    throw new Error("数量は1以上の整数にしてください");
  }
  return quantity;
}

// 内側：確かめた値だけが届くので、確認を書かない
function calcPrice(quantity: number): number {
  return quantity * 500;
}

function reserveStock(quantity: number) {
  stock = stock - quantity;
}

// どの画面も、フォームの値を parseQuantity に通してから使う
const quantity = parseQuantity("-3"); // ここでエラーになり、先へ進まない
calcPrice(quantity);
reserveStock(quantity);
```

確認は `parseQuantity` の1か所だけになり、`calcPrice` の中の確認は要らなくなります。  
また、どの画面もフォームの値を `parseQuantity` に通してから使うので、`-3` のような値は、`calcPrice` にも `reserveStock` にも届きません。

また、原則は、ビジネスロジックを純粋関数として書き、シェルを、純粋関数を呼ぶだけの薄い作りにするよう求めます（詳細は[『シェルが呼ぶだけの純粋関数に切り出す』](#%E3%82%B7%E3%82%A7%E3%83%AB%E3%81%8C%E5%91%BC%E3%81%B6%E3%81%A0%E3%81%91%E3%81%AE%E7%B4%94%E7%B2%8B%E9%96%A2%E6%95%B0%E3%81%AB%E5%88%87%E3%82%8A%E5%87%BA%E3%81%99)を参照）。ロジックをフレームワークから切り離しておけば、**フレームワークを動かさずにロジックだけをテストできる**からです。

### ルール：外から入るデータを境界で検証する

エージェントは、検証をどこに置くかを、次の2つの問いで判断します。

#### 外から入ってきたデータだけを確かめる

1つ目の問いは「このデータは今、システムの境界をまたいでいるか（外から入ってきたところか）」です。  
**またいでいないなら、確認は余分です**。境界のコードは、確かめた値を型の付いた値に変えて内側の関数に渡し、内側の関数はその型を信じます。

たとえば、設定ファイルを読み込む関数が、読み込み時に `batchSize` を正の数だと確かめたなら、`batchSize` を使う内側の関数で `batchSize > 0` を確かめ直す必要はありません。境界で一度確かめれば、内側のすべての関数でその値を安心して使えるからです。

```
type Config = { batchSize: number };

// 境界：設定ファイルを読み込むときに一度だけ確かめ、Config 型の値にする
function parseConfig(raw: { batchSize?: unknown }): Config {
  if (typeof raw.batchSize !== "number" || raw.batchSize <= 0) {
    throw new Error("batchSize は正の数にしてください");
  }
  return { batchSize: raw.batchSize };
}

// 内側：Config 型を信じ、batchSize > 0 を確かめ直さない
function splitIntoBatches(items: string[], config: Config): string[][] {
  const batches: string[][] = [];
  for (let i = 0; i < items.length; i += config.batchSize) {
    batches.push(items.slice(i, i + config.batchSize));
  }
  return batches;
}
```

#### シェルが呼ぶだけの純粋関数に切り出す

2つ目の問いは「この処理は、シェルが呼ぶだけの純粋関数にできるか」です。  
できるなら、エージェントはその処理を純粋関数として切り出します。

!

- **純粋関数**・・・ 同じ引数には常に同じ値を返し、画面やファイルの読み書きのような、プログラムの外とのやり取りをしない関数
- **シェル**・・・ 画面、ファイル、ネットワーク、フレームワークなど、プログラムの外とのやり取りを受け持つ部分。外から値を受け取って純粋関数に渡し、返ってきた結果を外へ出す

たとえば、エージェントは、注文の合計金額の計算を、ボタンを押したときの処理の中に直接書かず、`calcTotal(items)` という関数に切り出し、ボタンの処理からはそれを呼ぶだけにします。こうすれば、画面を動かさずに合計金額の計算だけをテストできるからです。

一方、シェルには計算がないので、シェルの中で間違える余地はほとんどありません。

```
type Item = { price: number; quantity: number };
declare const button: HTMLButtonElement;
declare const totalLabel: HTMLElement;
declare function readItemsFromCart(): Item[];

// 純粋関数：同じ items には、いつも同じ合計を返す。画面には触らない
function calcTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// シェル：画面から値を読み、純粋関数を呼び、結果を画面に書くだけ
button.addEventListener("click", () => {
  const items = readItemsFromCart(); // 画面から読む
  const total = calcTotal(items); // 計算は純粋関数に任せる
  totalLabel.textContent = `${total}円`; // 画面に書く
});
```

### 発火条件

入力の検証やエラー処理を組み込むとき、またはフレームワークと自分のコードをつなぐ部分（アダプタ）を書くときです。

## 『Type System Discipline』は、型で不正な状態を作れなくする

原則『**Type System Discipline**』は、型検査器を、「この値は必ずこの形だ」と証明してくれる道具（原文では proof assistant）として扱います。

エージェントは、型検査器を使って、矛盾した状態や、variant の扱い漏れを、**動かしてから見つけるのではなく、コンパイルの時点でエラーとして止めます**。型が見逃した扱い漏れは、コンパイラが止められたはずの、実行時のエラーになるからです。

!

- **型検査器**・・・ プログラムを動かす前に型の間違いを見つける仕組み（TypeScriptのコンパイラなど）
- **variant**・・・ 直和型を構成する、一つひとつの形（たとえば、`type Status = "success" | "error" | "pending";`では `success`・`error`といった1つ1つの値が variant と呼ばれる）
- **直和型**・・・ いくつかの形のうち、どれか一つを取る値を表す型。TypeScriptのユニオン型（`type FooBar = 'foo' | 'bar'` は foo か bar のいずれか1つの値となる）

### ルール：不正な状態を、型の定義の時点で書けなくする

主なパターンは次のとおりです。

#### ありえない状態を書けなくする

タスクの型を `{ completed: boolean; completedAt?: Date }` にすると、「完了したのに完了日時がない」という意味のない組み合わせも書けてしまいます。

そこでエージェントは、`{ kind: "open" } | { kind: "done"; at: Date }` のような直和型にします。直和型なら、「完了」のときは必ず日時を持つ形しか書けません。

組み合わせが正しいかを後から確かめるより、**ありえない組み合わせを最初から書けなくするほうが確実**だからです。

#### 意味の違う値に印を付ける

エージェントは、`UserId` と `OrderId` をブランド型にして、中身がどちらも文字列でも、互いに取り替えて使えないようにします。

!

**ブランド型**・・・ 文字列や数値のような基本的な値（プリミティブ）に、型の印を付けたもの（以下のコード例の UserId や OrderId がブランド型）

たとえば、ユーザーIDを渡すべき `getUser()` に注文IDを渡したら、コンパイルでエラーになるようにします。取り替えられると、意味の違う値を取り違えてもコンパイルが通ってしまうからです。

```
type UserId = string & { readonly __brand: "UserId" };
type OrderId = string & { readonly __brand: "OrderId" };
type User = { id: UserId; name: string };

declare function getUser(id: UserId): Promise<User>;
declare const orderId: OrderId;

// 中身はどちらも文字列だが、OrderId を渡すとコンパイルでエラーになる
await getUser(orderId);
```

#### 型システムに嘘をつかない

エージェントは、キャストやアサーションで、型の検査をすり抜けません。すり抜けた箇所は、実行中に落ちる危険を抱えたままになるからです。

!

- **キャスト**・・・ 値の型を強制的に別の型とみなさせる書き方（たとえば、`value as unknown as User` のように、型の検査を通らない変換を強制するなど）
- **アサーション**・・・ 「この値は必ずこの型だ」とコンパイラに言い切る書き方（TypeScriptで `as` 句で `as User`などとして記述される）

たとえば、APIから受け取った値を確かめずに `as User` と書くと、コンパイルは通ります。  
しかし、実際の応答に `name` の項目が欠けていても、コードは `name` があるものとして読み進めるため、`user.name` を使うところで実行中に落ちます。

コンパイラが証明できない事実は、エージェントが、値を実際に確かめたり、条件分岐で型を絞り込んだりして、自分で証明します。

#### 扱い漏れの確認はコンパイラに任せる

エージェントは、直和型に新しい variant が追加されたとき、それを扱っていない分岐でコンパイルがエラーになるように書きます。

たとえば、タスクの種類に「キャンセル済み」（`canceled`）を追加したとき、表示する文言を決める関数がそれを扱っていなければ、コンパイルがエラーになります。  
そのため、扱い漏れを人が探して回らずに済みます。

```
// タスクの種類に canceled を追加した
type Task = { kind: "open" } | { kind: "done" } | { kind: "canceled" };

// 前：扱っていない種類は、最後の return "" に流れる。コンパイルはエラーにならない
function labelLoose(task: Task): string {
  if (task.kind === "open") return "未完了";
  if (task.kind === "done") return "完了";
  return ""; // canceled のタスクは、文言が空のまま画面に出る
}

// 後：扱っていない種類があると、コンパイルがエラーになる
function label(task: Task): string {
  switch (task.kind) {
    case "open":
      return "未完了";
    case "done":
      return "完了";
    default: {
      // canceled を case で扱っていないので、この行でコンパイルがエラーになる
      const unhandled: never = task;
      return unhandled;
    }
  }
}
```

前の `labelLoose` は、`canceled` を扱い忘れてもコンパイルが通ります。そのため、画面に空の文言が出て初めて、扱い漏れに気づきます。

後の `label` の `never` は、「ここには、どの値も届かないはず」という意味の型です。

すべての種類を `case` で扱っていれば、`default` に届く値はないので、コンパイルは通ります。

一方、`canceled` を扱い忘れると、`canceled` のタスクが `default` に届くため、`never` の変数に代入する行でコンパイルがエラーになります。エラーの出た場所が、`canceled` の `case` を追加すべき場所です。

#### 型を強めるのは、弱すぎると分かった場所だけにする

ただし、原則は、型をできるだけ細かく書くことを目的にしていません。原則によれば、型の役目は、データをできるだけ細かく表すことではなく、**その型を使うそれぞれの場所が扱うべきケースを、漏れなく示すこと**です。

そのため、エージェントは、型が弱すぎると分かった場所だけで型を強めます。その目印は、実行時のアサーションや、「起きるはずがない」としてエラーを投げる throw 文です。こうした確認を書いた場所は、型が防げたはずのケースを通してしまっている場所だからです。

たとえば、完了したタスクには必ず日時があるはずなのに、`if (!task.completedAt) throw new Error("起きるはずがない")` と書いている場所は、型が「完了なのに日時がない」値を許してしまっている場所です。

### 発火条件

- 型を設計するとき
- 関数のシグネチャ（受け取る引数と返す値の型）をレビューするとき
- 静的型付き言語（TypeScriptのように、動かす前に型を検査する言語）でコードを書くとき

この原則が挙げる判定の問いの一つは、型を、次にこのコードを触るエージェントへの指示として扱っています。

> "If a new variant is added next month, will the compiler tell the next agent where to add a case?" If no, the match isn't exhaustive.
>
> 「来月新しい variant が追加されたとき、コンパイラは次のエージェントに、ケースを追加する場所を教えるか」。教えないなら、その分岐は網羅的ではない。

網羅的な分岐を書いておけば、コンパイラが次のエージェントに直す場所を教えます。そのため、人間が「新しい状態を追加したら、この3か所も直して」と文章で書いておく必要はありません。

`/typescript-best-practices` は、この原則をTypeScriptの具体的な書き方で示したSkillです（[第30章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f9a46)）。

## 『Make Operations Idempotent』は、操作を何度実行しても同じ結果になるように作る

原則『**Make Operations Idempotent**』は、状態を変える操作を、何回実行しても、途中から実行し直しても、**最後には同じ正しい状態に落ち着く（収束する）ように作る**よう求めます。

!

- **冪等（idempotent）**・・・ 同じ操作を何度実行しても、1回だけ実行したときと同じ結果になる性質（例：設定値を5にする操作は、何度実行しても値が5のまま）

原則がこれを求めるのは、**操作は途中で止まるものとして作る必要がある**からです。

コマンド、起動や終了などの手順、処理を繰り返すループは、クラッシュ、再起動、再試行によって、途中で止まったり、もう一度実行されたりすることがよくあります。

そのとき、前回の実行が途中で残したデータやファイルによって次の実行の結果が変わると、開発者は、再起動のたびに「なぜ今回は結果が違うのか」を調べることになります。

冪等性を担保して作っておけば、何回実行し直しても結果は同じなので、再起動のたびに調べる必要はありません。

### ルール：3つの問いで収束を確かめる

エージェントは、操作が冪等かどうかを、次の3つの問いで確かめます。

1. 同じ操作を2回続けて実行したら、結果はどうなるか
2. 前の実行が途中で止まっていたら、次の実行の結果はどうなるか（止まった場所が最初でも、途中でも、終わる直前でも、同じ結果になるか）
3. 何度実行し直しても、最後は同じ状態になる（収束する）か

3つの問いのどれか一つでも、答えが「前回の実行が何を残したかで変わる」になるなら、その操作には**照合（reconciliation）の手順**が必要です。

たとえば、2つ目の問いについて見てみましょう。

1,000行を出力ファイルに書き出す処理で、次の実行が、前回のファイルを残したまま、その末尾に1行目から追加で書き込むケースです。

前回の実行が400行を書いて止まっていれば、ファイルには、前回書いた400行の後ろに、今回書いた1,000行が続きます。前回の400行は、今回の最初の400行と同じ内容なので、同じ行が重複した1,400行のファイルになります。前回の実行が1行も書かずに止まっていれば、ファイルは1,000行です。

このように、前回の実行がどこで止まったかで結果が変わるなら、照合が必要です。

!

- **照合**・・・ 前の実行が残したものを確かめ、何が残っていても正しい状態へそろえる手順

たとえば、途中で止まった実行が、1,000行中400行目までしか書かれていない出力ファイルを残していても、**次の実行がまずそのファイルを見つけて消してから書き出しを始めれば**、前回がどこで止まっていても、結果は毎回同じ1,000行のファイルになります。

### 発火条件

途中で止まったり再試行されたりすることがあるコマンド、起動や終了などの手順、処理を繰り返すループを設計するときです。

## 『Migrate Callers Then Delete Legacy APIs』は、呼び出し元をすべて移し、その変更の中で古いAPIも消す

原則『**Migrate Callers Then Delete Legacy APIs**』は、新しい内部APIのほうが正しい設計だと決めたときに使います。

エージェントは、互換レイヤーを残さず、呼び出し元をすべて新しいAPIに移し、**その同じ変更の中で古いAPIを消します**。

新旧のAPIを両方残すと、同じことをする呼び出し方が2つになり、片付けが遅れ、コードが増えるばかりで減らないからです。

!

**互換レイヤー**・・・ 古いAPIの呼び出し方を使えるように残しておく層

poteto氏は[講演](https://x.com/poteto/status/2102050467505430555)（[第4章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/dc9141)）で、推奨される実装方法を一つに絞る必要がある、と述べています。本書では、この原則を、APIの移行で実装方法を一つに戻す手順と読みます。

### ルール：呼び出し元を洗い出して移し、古いAPIをすぐ消す

主なルールは次のとおりです。

#### 呼び出し元が残っていることを、古いAPIを残す理由にしない

エージェントは、古いAPIの呼び出し元をすべて洗い出して新しいAPIへ移し、古いAPIをすぐに消します。

たとえば、`getUser(id)` を `fetchUser({ id })` に置き換えるなら、エージェントは、`getUser` を呼んでいる箇所をすべて検索して `fetchUser` に書き換え、同じ一連の変更の中で `getUser` を消します。

新旧の呼び方が並んでいると、読み手はどちらを使うべきか迷い、片付けも後回しになるからです。

#### 一時的なつなぎの層は例外にする

古い呼び方を新しいAPIにつなぐ一時的な層（アダプタ）は、どうしても必要なときだけの例外とし、エージェントは、置くときにいつ消すかの期限を決めます。つなぎの層を当たり前に置くと、コードが増えるばかりで減らなくなるからです。

たとえば、古い `getUser(id)` を消さずに、中身を `return fetchUser({ id });` の1行だけにして残した関数が、アダプタです。

#### テストを新しいAPIに合わせる

エージェントは、テストを、新しいAPIが約束する挙動を確かめるように直し、古い実装の内部の作りを守るだけのテストは消します。

たとえば、「`fetchUser({ id })` が、そのIDのユーザーを返すか」を確かめるテストは残し、「古い `getUser` が内部で別の関数を何回呼んだか」だけを確かめるテストは消します。

古い作りを守るテストが残っていると、コードは、消したはずの古い実装の内部の作りに合わせ続けることになるからです。

### 発火条件

古い呼び出し元が残っている状態で、新しい内部APIを導入するときです。

**外部のユーザーがいる公開API（外部API）には、そのままでは、この原則は当てはまりません**。この原則には、次の3つの前提があるからです。

1. 古いAPIを使っている外部のユーザーがいない
2. 古いAPIを消して動かなくなる呼び出し元を、プロジェクトの中で一度にまとめて直しきれる
3. 新しいAPIを入れる目的が、コードを単純にすることやリファクタリングである

## 『Separate Before Serializing Shared State』は、書き込み先の共有をなくすのが先で、ロックは最後の手段

原則『**Separate Before Serializing Shared State**』は、複数の主体（エージェントやWorkerなど）が同じ書き込み先を共有するかもしれない場面で使います。

エージェントは、ロックを追加する前に、**主体どうしが本当に同じ書き込み先を必要としているか**を考え、必要でなければ、書き込み先を主体ごとに分けて共有をなくします。並行した書き込みが生む競合状態は、たまにしか起きず再現しにくいため、原因の調査に時間がかかるからです。

!

- **Serializing（直列化）**・・・ ロックなどを使って、書き込みを一つずつ順番に行わせること
- **ロック**・・・ 一度に一つの処理だけが書き込めるようにする仕組み
- **競合状態**・・・ 複数の処理が同じデータを同時に読み書きし、実行の順番しだいで結果が変わってしまう状態

たとえば、2つの処理A・Bが、値が10のカウンタをそれぞれ1ずつ増やすと、次のようになります。

2つの処理が1ずつ増やしたので本当は12になるはずが、Bは、Aが書き込む前の10をもとに11を書き込むため、11になります。

### ロックは共有をなくさないので、書き込みの直列化は最後の手段にする

この原則は、**書き込みの直列化を、書き込み先を分けられないときの最後の手段としています**。

最後の手段にしているのは、ロックが共有そのものをなくすわけではないからです。  
書き込み先を分ければ、同じ場所に書く主体がいなくなるので、競合状態はそもそも起きません。

一方、ロックを入れても、書き込み先は共有されたままです。すべての主体が、書き込むたびに必ずロックを取らなければならず、ロックを取らずに書き込む処理が1つでも残れば、競合状態がまた起きます。

また、ロックを持ったままの主体が途中で止まると、ロックが外れず、ほかの主体がいつまでも書き込めなくなることもあります。

そのため、**原則は、「ロックが必要だ」と思ったら、すぐにロックを入れるのではなく、まず本当に書き込み先を分けられないのかを見直すよう求めます**。

### 分けられないときも、順番は指示ではなく仕組みで守らせる

**書き込み先を本当に分けられないときも、原則は、順番を守らせる方法を人への指示に頼らず、ロックなどの仕組みで守らせるよう求めます**。

この原則の最初の段落は、次の一文で終わります。

> Instructions and conventions are not concurrency control.
>
> 指示や慣習は並行性の制御ではない。

エージェントに当てはめると、人間が「同じファイルを触らないように」と依頼に書いても、それはエージェントどうしの並行した書き込みを防ぐ仕組みにはなりません。

### ルール：ロックの前に書き込み先を分ける

手順は3つです。

#### 1. 複数の主体が書き換える、共有の場所を見つける

複数の主体が読み書きするファイルや、複数の主体がpushするブランチなどを見つけます。

#### 2. 書き込み先の共有をなくす

エージェントは、書き込み先の共有をなくすことを、基本の対応とします。

まず、主体たちが一つの正式なデータを必要としているのか、それぞれ別々の事実を書き出しているだけなのかを考えます。

そのうえで、各主体に、自分だけが書き込むファイル、キー、ブランチを持たせ、結果は読むときや報告するときにまとめます。

たとえば、2つのWorkerが一つの `state.json` にそれぞれの項目を書くなら、書き込み先を共有しています。`indexer-state.json` と `metrics-state.json` に分ければ、共有ではなくなります。

書き込み先を分ける前と後を図にすると、次のようになります。

```
分ける前（書き込み先を共有している）
WorkerA ─┐
           ├─→ state.json
WorkerB ─┘

分けた後（書き込み先が主体ごとに分かれている）
WorkerA ──→ indexer-state.json
WorkerB ──→ metrics-state.json
```

#### 3. 分けられないときだけ、書き込みを直列化する

書き込み先を一つにしなければ正しく動かないときだけ、書き込みを一つずつ順番に行わせる仕組み（直列化）を入れます。

たとえば、在庫の残り数や座席の予約のように、すべての主体が同じ一つの値を読み書きしなければ正しくならないデータなどが該当します。

原則が挙げる仕組みは、次の4つです。

- **ロックファイル**・・・ 書き込む前に「書き込み中」を示すファイルを作り、書き終えたら消します。ほかの主体は、そのファイルがある間は書き込まずに待ちます。
- **段階を分けて順番に実行する**・・・ 書き込みを段階に分け、前の段階が終わってから次の段階を始めます（例：Aが書き終えてから、Bが書く）。
- **書き込みを一つの主体だけに任せる**・・・ 書き込める主体を1つだけにし、ほかの主体は、その主体に「この値を書いて」と頼みます。
- **アトミックな比較交換**・・・ 「値がまだ10なら11にする」のように、読んだときから値が変わっていないときだけ書き換えます。変わっていたら書き換えず、読み直してやり直します。値の確認と書き換えは、途中でほかの処理に割り込まれない一つの操作（アトミックな操作）として行います。

アトミックな比較交換を、先のカウンタの例に当てはめると、次のようになります。

Bの1回目の書き換えは、Aがすでに値を11にしているので失敗します。Bは11を読み直してやり直すので、最後は正しく12になります。

### 発火条件

並行して動く複数の主体が、同じファイル、ブランチ、キー、状態を持つオブジェクトに書き込むかもしれないときです。

### 依頼の例：並行する試行に、それぞれ専用のworktreeを与える

同梱ガイドのページ [`docs/guide/08-principles.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md) は、並行して進めている2つの試行が同じブランチに書き込もうとしている場面で、次の一行を挙げています。

```
separate before serializing shared state. give each attempt its own worktree, no locks.
// separate before serializing shared state で。試行ごとに専用の worktree を与えて。ロックは使わないで。
```

!

- **worktree**・・・ 一つのGitリポジトリから、別のブランチを取り出した作業ディレクトリを追加で作る機能。ブランチごとに別のディレクトリで同時に作業できる

## Architectureの6原則は、構造そのものをエージェントへの説明書にする

poteto氏は講演で、エージェントへの信頼を高める方法の一つとして、コードベースそのものの構造を改善することを挙げています。エージェントが、フォルダ、型、プロセスの境目を見れば、どこで何をしてよいかが分かるようにする、という方法です。

講演では、これを**構造そのものがエージェントへの説明書になる設計**としています。

6原則は、それぞれの判断を、型、状態機械、ファイルの分け方などの構造として残します。各原則について、レビューで聞く一言と、判断を構造として残す先を示すと、次のとおりです。

| 原則 | レビューで聞く一言 | 構造として残す先 |
| --- | --- | --- |
| 『**Model the Domain**』 | 「2つ目の真偽値が増えていないか」 | 状態機械、discriminated union、参照表 |
| 『**Boundary Discipline**』 | 「このデータは今、境界をまたいでいるか（外から入ってきたところか）」 | 境界ごとのパース関数（外から来たデータを検証し、型の付いた値に変える関数） |
| 『**Type System Discipline**』 | 「新しい variant が追加されたら、コンパイラは教えてくれるか」 | 直和型、ブランド型、`never` による網羅性の確認 |
| 『**Make Operations Idempotent**』 | 「2回実行したら、途中で止まったら、どうなるか」 | 照合の手順 |
| 『**Migrate Callers Then Delete Legacy APIs**』 | 「古いAPIはいつ消えるか」 | 呼び出し元の移行と同じ一連の変更での、古いAPIの削除 |
| 『**Separate Before Serializing Shared State**』 | 「この書き込み先に書き込む主体は一つだけか」 | 主体ごとのファイル、ブランチ、worktree |

## まとめ

- 『**Model the Domain**』は、散らばった分岐と真偽値を、状態機械や参照表にまとめます。エージェントは、コードを書くたびにこの原則を適用します。
- 『**Boundary Discipline**』は、検証を境界に集め、境界の内側のコードでは型を信じます。
- 『**Type System Discipline**』は、ありえない状態をコンパイルの時点で作れなくします。
- 『**Make Operations Idempotent**』は、3つの問いを使って、再試行や再起動があっても同じ最終状態に収束する操作を作るよう求めます。
- 『**Migrate Callers Then Delete Legacy APIs**』は、呼び出し元の移行と古いAPIの削除を同じ一連の変更で済ませます。本書では、これを、推奨される実装方法を一つに保つ原則だと読みます。
- 『**Separate Before Serializing Shared State**』は、ロックで直列化（書き込みを一つずつ順番に行わせること）する前に、書き込み先の共有そのものをなくします。
- 本書では、6件はどれも、構造そのものをエージェントへの説明書にする原則だと読みます。

次の[第19章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/1fb019)では、何をもって完了の証明とするかを決める、Verificationの4原則を扱います。
