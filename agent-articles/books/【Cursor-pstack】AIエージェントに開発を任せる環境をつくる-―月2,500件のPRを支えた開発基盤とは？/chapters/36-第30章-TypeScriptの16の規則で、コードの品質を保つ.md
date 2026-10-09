---
title: "第30章 TypeScriptの16の規則で、コードの品質を保つ"
book_title: "【Cursor pstack】AIエージェントに開発を任せる環境をつくる ―月2,500件のPRを支えた開発基盤とは？"
source_url: "https://zenn.dev/sc30gsw/books/080faba713547b/viewer/4f9a46"
author: "kaito"
published_at: "2026-10-02"
retrieved_at: "2026-10-06T23:37:34+09:00"
site: "zenn.dev"
content_type: "article"
chapter_position: 36
---

# 第30章 TypeScriptの16の規則で、コードの品質を保つ

この章では、[`/typescript-best-practices`](https://github.com/cursor/plugins/blob/main/pstack/skills/typescript-best-practices/SKILL.md) を扱います。

`/typescript-best-practices` は、エージェントが、TypeScriptのコードで、ありえない状態（例：読み込み中なのにエラーもある値）を型で書けなくし、外から受け取るデータを、入ってくる場所で一度だけ検証するためのSkillです。

この章から[第32章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8960d3)までの3章では、エージェントが書いたコードの品質を保つ、次の3つのSkillを1つずつ扱います。

1. `/typescript-best-practices`（この章）
2. [`/tdd`](https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md)（[第31章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ad5727)）
3. [`/no-comments`](https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md)（[第32章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/8960d3)）

本書では、3つのSkillを、**コードを書いたエージェント自身の注意だけに頼らず、書いた本人以外に確かめさせるSkill**と整理します。`/typescript-best-practices` で、本人の代わりに確かめるのは、コンパイラです。

この章では、`/typescript-best-practices` を、役割、使いどき、規則、依頼の書き方の4つの観点で解説します。

## この章の構成

この章の構成は次のとおりです。

- 役割：『Type System Discipline』を TypeScript の具体的な書き方にする
- 使いどき：TypeScriptのファイルを扱う作業で、利用者が名前で呼ぶ
- 規則：TypeScript の書き方の16の規則
- 依頼の書き方：TypeScriptのファイルを扱う作業で、`/typescript-best-practices` と入力する
- まとめ

## 役割：『Type System Discipline』を TypeScript の具体的な書き方にする

`/typescript-best-practices` は TypeScript の規則集です。

[第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b)の原則『[**Type System Discipline**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-type-system-discipline/SKILL.md)』は、不正な状態をなぜ型で書けなくするのかを説明しています。このSkillは、不正な状態を型で書けなくする方法を、TypeScript の書き方で示します。

このSkillは、`SKILL.md` の冒頭で、Skillに定義されている規則を使う前に、まずこの原則を適用するようエージェントに求めています。

## 使いどき：TypeScriptのファイルを扱う作業で、利用者が名前で呼ぶ

このSkillは、エージェントがTypeScriptのファイル（`.ts` や `.tsx`）を読んだり編集したりする作業のためのSkillです。**このSkillは、自動では読み込まれないので、TypeScriptのファイルを扱う作業では、利用者が `/typescript-best-practices` と入力して呼びます**。

同梱ガイドの[`05-build-and-clean.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/05-build-and-clean.md)は、次のように案内しています。

> It doesn't load on its own, so type `/typescript-best-practices` when a task touches `.ts` or `.tsx` files.
>
> このSkillは、自動では読み込まれない。そのため、作業が `.ts` や `.tsx` のファイルに触れるときは、`/typescript-best-practices` と入力せよ。

`SKILL.md` の `paths`（対象にするファイルの種類を書く設定）は、TypeScriptのファイルを指しています。ただし、`disable-model-invocation: true` の設定も持つので（[第25章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/46bd1f)）、エージェントが会話の内容からこのSkillを選んで動かすことはありません。

また、`/poteto-mode` の手順も、このSkillを呼びません。そのため、**利用者が `/typescript-best-practices` と入力しない限り、このSkillは読み込まれません**。

## 規則：TypeScript の書き方の16の規則

このSkillの中身は、16の規則と、[`references/patterns.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/typescript-best-practices/references/patterns.md) のコード例です。

!

**`references/patterns.md`**・・・ `SKILL.md` に定義されている規則ごとのコード例をまとめたファイル

16の規則のうち、「本物のテスト」と「構造化したログ（Structured telemetry）」を除く、14の規則のコード例が載っている

同梱ガイドの [`docs/guide/05-build-and-clean.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/05-build-and-clean.md) は、このSkillを、**型システムの原則を TypeScript の具体的な規則にしたもの**と説明しています。

16の規則を順にまとめると、次のようになります。

| 規則 | 概要 |
| --- | --- |
| [discriminated union](#1.-discriminated-union-%E3%81%A7%E3%80%81%E3%81%82%E3%82%8A%E3%81%88%E3%81%AA%E3%81%84%E7%8A%B6%E6%85%8B%E3%82%92%E6%9B%B8%E3%81%91%E3%81%AA%E3%81%8F%E3%81%99%E3%82%8B) | 状態ごとに持てる項目を型で決め、「読み込み中なのにエラーもある」のような矛盾した値を書けなくする |
| [ブランド型](#2.-%E3%83%96%E3%83%A9%E3%83%B3%E3%83%89%E5%9E%8B%E3%81%A7%E3%80%81%E6%84%8F%E5%91%B3%E3%81%AE%E7%95%B0%E3%81%AA%E3%82%8B%E5%80%A4%E3%81%AE%E5%8F%96%E3%82%8A%E9%81%95%E3%81%88%E3%82%92%E9%98%B2%E3%81%90) | 中身が同じ文字列でも、意味の異なる値（例：IDとただの文字列）を型で区別し、取り違えを防ぐ |
| [構成で表す（Constructive modeling）](#3.-%E4%B8%8D%E6%AD%A3%E3%81%AA%E5%80%A4%E3%82%92%E7%B5%84%E3%81%BF%E7%AB%8B%E3%81%A6%E3%82%89%E3%82%8C%E3%81%AA%E3%81%84%E5%BD%A2%E3%81%A7%E3%80%81%E5%9E%8B%E3%82%92%E4%BD%9C%E3%82%8B) | 「空でない配列」のように条件のある値は、条件を満たさない値を作れない型で表す |
| [最も単純で済む型（Simplest total type）](#4.-%E5%9E%8B%E3%82%92%E5%BC%B7%E3%81%8F%E3%81%99%E3%82%8B%E3%81%AE%E3%81%AF%E3%80%81%E3%82%86%E3%82%8B%E3%81%84%E5%9E%8B%E3%81%AE%E3%81%9B%E3%81%84%E3%81%A7%E7%84%A1%E7%90%86%E3%81%8C%E7%94%9F%E3%81%98%E3%82%8B%E7%AE%87%E6%89%80%E3%81%A0%E3%81%91%E3%81%AB%E3%81%99%E3%82%8B) | 型を厳しくするのは、今の型のままでは無理な書き方が必要になる箇所だけにする |
| [`any` より `unknown`](#5.-%E5%A4%96%E3%81%8B%E3%82%89%E5%8F%97%E3%81%91%E5%8F%96%E3%82%8B%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AF-unknown-%E3%81%A7%E5%8F%97%E3%81%91%E3%82%8B) | 外から受け取るデータは、中身を確かめるまで使えない型で受ける |
| [型ガードより先にスキーマ（Schemas before guards）](#6.-%E5%9E%8B%E3%82%AC%E3%83%BC%E3%83%89%E3%82%92%E6%89%8B%E3%81%A7%E6%9B%B8%E3%81%8F%E5%89%8D%E3%81%AB%E3%80%81%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%82%B9%E3%82%AD%E3%83%BC%E3%83%9E%E3%81%AE%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA%E3%82%92%E4%BD%BF%E3%81%86) | データを確かめる処理を手で書く前に、プロジェクトで使っている検証用のライブラリを使う |
| [`as` を使わない](#7.-as-%E3%81%AF%E3%80%81%E5%80%A4%E3%82%92%E7%A2%BA%E3%81%8B%E3%82%81%E3%81%9F%E5%BE%8C%E3%81%AB%E3%81%A0%E3%81%91%E6%9B%B8%E3%81%8F) | 中身を確かめずに「この値はこの型だ」と決めつける書き方をしない |
| [型の絞り込みの優先順位（Narrowing hierarchy）](#8.-%E5%9E%8B%E3%81%AE%E7%B5%9E%E3%82%8A%E8%BE%BC%E3%81%BF%E3%81%AB%E3%81%AF%E3%80%81%E5%84%AA%E5%85%88%E3%81%99%E3%82%8B%E9%A0%86%E7%95%AA%E3%81%8C%E3%81%82%E3%82%8B) | 値の型を確かめる方法は、安全なものから順に選ぶ |
| [型ガード（Type guards）](#9.-%E5%9E%8B%E3%82%AC%E3%83%BC%E3%83%89%E3%81%AF%E3%80%81%E5%90%8D%E5%89%8D%E3%81%AE%E3%81%A8%E3%81%8A%E3%82%8A%E3%81%AB%E5%80%A4%E3%82%92%E7%A2%BA%E3%81%8B%E3%82%81%E3%82%8B) | 「この型か」を判定する関数は、名前のとおりに本当に確かめる |
| [網羅性チェック](#10.-%E7%B6%B2%E7%BE%85%E6%80%A7%E3%83%81%E3%82%A7%E3%83%83%E3%82%AF%E3%81%A7%E3%80%81case-%E3%81%AE%E6%9B%B8%E3%81%8D%E5%BF%98%E3%82%8C%E3%82%92%E3%82%B3%E3%83%B3%E3%83%91%E3%82%A4%E3%83%AB%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E3%81%99%E3%82%8B) | 状態の種類を増やしたとき、その種類の処理の書き忘れを、コンパイルエラーで知らせる |
| [`as` より `satisfies`](#11.-as-%E3%81%AE%E4%BB%A3%E3%82%8F%E3%82%8A%E3%81%AB-satisfies-%E3%81%A7%E3%80%81%E5%9E%8B%E3%81%AB%E5%90%88%E3%81%86%E3%81%8B%E3%82%92%E7%A2%BA%E3%81%8B%E3%82%81%E3%82%8B) | 値が型に合うかを、値の細かい情報を失わずに確かめる |
| [境界での検証](#12.-%E3%83%87%E3%83%BC%E3%82%BF%E3%81%8C%E5%85%A5%E3%81%A3%E3%81%A6%E3%81%8F%E3%82%8B%E5%A0%B4%E6%89%80%E3%81%A7%E4%B8%80%E5%BA%A6%E3%81%A0%E3%81%91%E6%A4%9C%E8%A8%BC%E3%81%97%E3%80%81%E5%86%85%E5%81%B4%E3%81%A7%E3%81%AF%E5%9E%8B%E3%82%92%E4%BF%A1%E3%81%98%E3%82%8B) | 外から来たデータは、入口で一度だけ確かめ、内側では確かめ直さない |
| [既存の型から導く（Schema-derived types）](#13.-%E6%96%B0%E3%81%97%E3%81%84%E5%9E%8B%E3%82%92%E6%9B%B8%E3%81%8F%E5%89%8D%E3%81%AB%E3%80%81%E6%97%A2%E5%AD%98%E3%81%AE%E5%9E%8B%E3%81%8B%E3%82%89%E5%B0%8E%E3%81%8F) | 新しい型を書く前に、すでにある型から必要な部分を取り出す |
| [引数はオブジェクトで渡す（Object args）](#14.-%E5%BC%95%E6%95%B0%E3%81%AF%E3%80%81%E4%BD%8D%E7%BD%AE%E3%81%A7%E4%B8%A6%E3%81%B9%E3%81%9A%E3%81%AB%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%A7%E6%B8%A1%E3%81%99) | 引数に名前を付けて渡し、順番の取り違えを防ぐ |
| [本物のテスト](#15.-%E6%89%8B%E5%85%83%E3%81%A7%E5%8B%95%E3%81%8B%E3%81%9B%E3%82%8B%E3%82%82%E3%81%AE%E3%81%AF%E3%80%81%E3%83%A2%E3%83%83%E3%82%AF%E3%81%AB%E3%81%9B%E3%81%9A%E6%9C%AC%E7%89%A9%E3%81%A7%E3%83%86%E3%82%B9%E3%83%88%E3%81%99%E3%82%8B) | 手元で動かせるものは、偽物に置き換えずに本物でテストする |
| [構造化したログ（Structured telemetry）](#16.-%E8%A8%BA%E6%96%AD%E3%81%AE%E6%83%85%E5%A0%B1%E3%81%AF%E3%80%81%E6%A7%8B%E9%80%A0%E5%8C%96%E3%81%97%E3%81%9F%E3%83%AD%E3%82%B0%E3%81%A7%E6%AE%8B%E3%81%99) | 調査に使える情報を決まった形でログに残し、`console.log` を残さない |

各規則を、`references/patterns.md` のコード例で見ていきます。例のコメントは日本語にしています。

### 1. discriminated union で、ありえない状態を書けなくする

discriminated union は、種類ごとに形の異なるデータ（variant）を、`kind` のような種類を示すフィールドで見分ける型です（[第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b)）。

!

**variant**・・・ 1つの型がとりうる形の1つ1つ  
たとえば、この後の `DiffState` では、`{ kind: "loading" }`、`{ kind: "ready"; diff: GitDiff }`、`{ kind: "error"; error: string }` の3つが variant

`references/patterns.md` は、真偽値と、省略できる項目（optional なフィールド）で作った型を、悪い例にしています。

悪い例では、`loading: true` と `error` を同時に持つ「読み込み中なのにエラーもある」値が書けます。良い例では、`kind` ごとに持てる項目が決まるので、正しい3つの状態しか書けません。

```
// 差分（変更されたファイルの一覧）
type GitDiff = { files: string[] };

// 悪い例：真偽値と省略できる項目の組み合わせでは、矛盾した状態も書けてしまう
type DiffStateLoose = { loading: boolean; diff?: GitDiff; error?: string };

// 良い例：正しい状態だけが存在できる
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

このように、状態によって持つ項目が変わるなら、真偽値と省略できる項目ではなく、discriminated union で書く必要があります。

### 2. ブランド型で、意味の異なる値の取り違えを防ぐ

ブランド型は、文字列のような基本的な値に `& { readonly __brand: "AgentId" }` のような印を付けた型です（[第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b)）。エージェントIDを渡すべき関数に、確かめていない文字列を渡すといった取り違えを、コンパイルの時点で防ぎます。

次の例では、データの入口の `parseAgentId` が、文字列がUUIDの形かを一度だけ確かめてから `AgentId` にします。`as` を使うのは、確かめた後の1か所だけです。

```
type AgentId = string & { readonly __brand: "AgentId" };

// 文字列がUUIDの形かを確かめる
declare function isUUID(input: string): boolean;

// 境界：文字列を確かめてから、AgentId にする
function parseAgentId(input: string): AgentId {
  if (!isUUID(input)) throw new Error(`Invalid agent id: ${input}`);
  // 確かめた後なので、as を使ってよい
  return input as AgentId;
}

// 内側：AgentId しか受け取らず、IDを確かめ直さない
function focusAgent(id: AgentId): void {
  /* 入力は確かめ済みとして扱う */
}

// 通る
focusAgent(parseAgentId("3f2b8c1e-9a4d-4e6b-8f1a-2c5d7e9b0a13"));
// 確かめていない文字列なので、コンパイルでエラーになる
focusAgent("3f2b8c1e-9a4d-4e6b-8f1a-2c5d7e9b0a13");
```

印の形は `readonly __brand: "X"` にそろえ、新しい書き方を作りません。

このように、中身の型が同じ型でも、意味によって扱いが変わる値なら、ブランド型にし、境界で確かめてから型を付ける必要があります。

### 3. 不正な値を組み立てられない形で、型を作る

この規則（原文では Constructive modeling）は、ゆるい型に実行時のチェックを足して不正な値を防ぐのではなく、正しい部品だけで型を組み立てます。

```
// 空でない配列：最初の要素が必ずある
type NonEmpty<T> = [T, ...T[]];

// 悪い例：T[] で受け、空かどうかのチェックを、呼び出す側がそれぞれ繰り返す
function pickWinnerLoose(entries: string[]): string {
  if (entries.length === 0) throw new Error("no entries");
  return entries[Math.floor(Math.random() * entries.length)];
}

// 良い例：空の値は、この型では存在できない
function pickWinner(entries: NonEmpty<string>): string {
  return entries[Math.floor(Math.random() * entries.length)];
}

// T[] で受け取った値は、型ガードで一度だけ絞り込む。その後は型が事実を運ぶ
const isNonEmpty = <T>(arr: T[]): arr is NonEmpty<T> => arr.length > 0;
```

このように、不正な値を実行時に弾くより先に、不正な値を組み立てられない型を定義する必要があります。

### 4. 型を強くするのは、ゆるい型のせいで無理が生じる箇所だけにする

この規則（原文では Simplest total type）は、すべての型を強くすることは求めません。配列に対するどの操作も、空の配列を含むすべての入力で結果を返せる間は、`T[]` のままにします。

型を強くするのは、ゆるい型のせいで、使う箇所に無理が生じるときだけです。無理の兆候は、`!`（non-null アサーション演算子）、`arr[0] as T`（型アサーション）、「起きないはずの」エラーの3つです。

```
type NonEmpty<T> = [T, ...T[]];
type Session = { id: string; startedAt: Date };

// T[] のままでよい例：空の配列でも 0 を返せる
const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0);

// 悪い例：配列が空のときの扱いを、! でコンパイラから隠している
function newestSessionLoose(sessions: Session[]): Session {
  return sessions.at(0)!;
}

// 良い例：引数の型を強くすると、! が要らなくなる
function newestSession(sessions: NonEmpty<Session>): Session {
  return sessions[0];
}
```

`references/patterns.md` は、戻り値を `Session | undefined` に弱めることも、もう1つの正しい書き方として挙げています。

このように、型を強くするかどうかは、ゆるい型のせいで `!`（non-null アサーション演算子） などを書かされているかで決める必要があります。

### 5. 外から受け取るデータは unknown で受ける

`any` で受けた値は、確かめなくても使えてしまいます。`unknown` で受けた値は、型を確かめるまで使えないので、エージェントは検証を飛ばせません。

```
// 悪い例：any で受けると、確かめずに使えてしまう
function handleLoose(input: any) {
  // foo がなくても、コンパイルは通る
  return input.foo.bar;
}

// 良い例：unknown で受け、型を絞り込んでから使う
function handle(input: unknown) {
  if (typeof input === "object" && input !== null && "foo" in input) {
    // ここでは、input に foo があることをコンパイラが確かめている
  }
}
```

このように、値の形が実行するまで分からないなら、`unknown` で受け、型を絞り込んでから使う必要があります。

### 6. 型ガードを手で書く前に、リポジトリのスキーマのライブラリを使う

外から受け取るデータについて、項目を1つずつ確かめる型ガード（値がその型かを確かめて真偽値を返す関数）を手で書く前に、エージェントは、リポジトリで使っている実行時スキーマのライブラリと、既存のスキーマを探します。

スキーマ1つに検証を任せ、TypeScript の型はスキーマから導きます。スキーマ、同じ形のインターフェース、型ガードの3つを別々に持つと、どれかを直し忘れて食い違うからです。

```
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  role: z.enum(["admin", "member"]),
});

// 型は、スキーマから導く
type User = z.infer<typeof UserSchema>;

function parseUser(input: unknown): User {
  return UserSchema.parse(input);
}
```

このように、外から受け取るデータは、リポジトリがすでに使っているスキーマで検証し、型もそこから導く必要があります。

### 7. as は、値を確かめた後にだけ書く

`as`（型アサーション） は、値を確かめずに「この値はこの型だ」とコンパイラに言い切る書き方です。実際の値の型が異なっていてもコンパイルは通るので、その値を使うコードが、実行時にエラーで止まるおそれがあります。

`references/patterns.md` は、この規則の例を、スキーマで確かめる形で示しています。

```
import { z } from "zod";

declare const data: unknown;

// 悪い例：確かめずに、User だと言い切っている
const user = data as User;

// 悪い例：id があるかどうかしか確かめていないのに、User だと言い切る型ガードを手で書いている
function isUser(data: unknown): data is User {
  return typeof data === "object" && data !== null && "id" in data;
}

// 良い例：スキーマで確かめ、型はスキーマから導く
const userSchema = z.object({ id: z.string(), name: z.string() });
type User = z.infer<typeof userSchema>;

function parseUser(data: unknown): User {
  return userSchema.parse(data);
}
```

2つ目の悪い例の `isUser` は、「`id` があるかどうか」しか確かめていません。それでも、`true` を返せば、コンパイラは値を `User` として扱うので、`name` がない値も `User` として通ってしまいます。

型を先に決めている場合は、スキーマの変数に、そのスキーマが確かめる型を、型注釈（`: z.ZodType<User>` のように、変数の型を書いたもの）として付けます。こうすると、型より確かめる範囲が狭いスキーマを、コンパイラが拒否します。

```
import { z } from "zod";

type User = { id: string; name: string };

// 下のオブジェクトから name を消すと、この代入はコンパイルできなくなる
const userSchema: z.ZodType<User> = z.object({ id: z.string(), name: z.string() });
```

既存のコードから `as` を取り除くときは、エージェントは、TypeScript が型を推論できない理由を突き止めます。

- 種類を示すフィールドがない → フィールドを追加し、discriminated union にする
- 元の型が広すぎる（例：`Record<string, unknown>`） → 型を絞り込む
- 境界に型がない → そのデータのスキーマでパース（データを読み取り、決めた形になっているかを確かめて、型の付いた値に変換）するか、スキーマがない部分にスキーマを追加する
- 型では本当に表せない → ブランド型か `satisfies` を使う

このように、`as` を書くなら、その前に値を確かめる必要があります。

### 8. 型の絞り込みには、優先する順番がある

`references/patterns.md` は、型を絞り込む方法を、次の順に優先しています。

1. 種類を示すフィールドでの `switch` や `if`（コンパイラが自動で絞り込む）
2. `in` 演算子（`"key" in obj` で、その項目を持つ variant に絞り込む）
3. `typeof` と `instanceof`（基本的な値とクラスのインスタンスに使う）
4. 自作の型ガード（上の3つで足りないときに使う）
5. `as`（値を確かめた後だけに使う）

次のコードは、5つの方法をそれぞれ使った例です。

```
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number };

// 1. 種類を示すフィールドでの switch：kind を見れば、コンパイラが自動で絞り込む
function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.radius ** 2;
    case "rect":
      return s.width * s.height;
  }
}

// 2. in 演算子：radius を持つのは円だけなので、ここでは円に絞り込まれる
function areaByIn(s: Shape): number {
  if ("radius" in s) return Math.PI * s.radius ** 2;
  // ここでは長方形に絞り込まれる
  return s.width * s.height;
}

// 3. typeof と instanceof：基本的な値や、クラスのインスタンスに絞り込む
function describe(value: string | number | Date): string {
  if (typeof value === "string") return value;
  if (value instanceof Date) return value.toISOString();
  // ここでは number に絞り込まれる
  return value.toFixed(2);
}

// 4. 自作の型ガード：上の3つでは確かめられない条件（空でない文字列か）を、関数で確かめる
function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.length > 0;
}

// 5. as：値を確かめた後だけに使う
type AgentId = string & { readonly __brand: "AgentId" };
declare function isUUID(input: string): boolean;

function toAgentId(input: string): AgentId {
  if (!isUUID(input)) throw new Error(`Invalid agent id: ${input}`);
  return input as AgentId;
}
```

このように、型を絞り込むときは、より上の方法を使用する必要があります。

### 9. 型ガードは、名前のとおりに値を確かめる

型ガードは、命名したとおりに、値を確かめなければなりません。確かめない型ガードは、安全だと命名された陰に不具合を隠すので、`as` より悪い書き方です。名前は `isX` か `hasX` にします。

```
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number };

// 種類を示すフィールドを実際に確かめている
function isCircle(s: Shape): s is Shape & { kind: "circle" } {
  return s.kind === "circle";
}
```

このように、型ガードを書くなら、その型ガードの名前が主張することを、中で本当に確かめる必要があります。

### 10. 網羅性チェックで、case の書き忘れをコンパイルエラーにする

`switch` の `default` に `const _exhaustive: never = x;` を書き、variant を1つ増やしたのに、その variant を扱う `case` を書き忘れたとき、コンパイルがエラーになるようにします（[第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b)）。

```
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number };

function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.radius ** 2;
    case "rect":
      return s.width * s.height;
    default: {
      // Shape に variant を追加して case を書き忘れると、ここでコンパイルエラーになる
      const _exhaustive: never = s;
      return _exhaustive;
    }
  }
}
```

値を返さない `switch` では、`return _exhaustive;` の代わりに `void _exhaustive;` と書きます。

このように、variant ごとに処理を分けるなら、`default` で網羅性を確かめる必要があります。

### 11. as の代わりに satisfies で、型に合うかを確かめる

`satisfies` は、リテラル型（`"dark"` のような、特定の値だけを表す型）を広げずに、値が型に合うかを確かめます。

```
type Config = { theme: "dark" | "light"; cols: number };

// 悪い例：as では theme の型が "dark" | "light" に広がり、"dark" だという情報が失われる
const configLoose = { theme: "dark", cols: 3 } as Config;

// 良い例：satisfies は型に合うかを確かめ、リテラル型も保つ
const config = { theme: "dark", cols: 3 } satisfies Config;
// config.theme の型は string ではなく "dark"
```

このように、値が型に合うかを確かめたいだけなら、`as` ではなく `satisfies` を使う必要があります。

### 12. データが入ってくる場所で一度だけ検証し、内側では型を信じる

データが入ってくる場所で、そのデータをドメイン型にパース（決まった形に読み取って変換すること）し、内側のコードでは、型の付いた値を確かめ直さずに使います。この規則は、原則『[**Boundary Discipline**](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-boundary-discipline/SKILL.md)』（[第18章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/cdc49b)）に沿っています。

!

**ドメイン型**・・・ アプリが扱う業務上の概念（ユーザーIDや注文など）を表す型  
たとえば、外から受け取った注文のデータを、2通りの型で持つと、次のコード例のようになる

```
// ドメイン型：注文が持つ項目と、各項目の型が決まっている
type Order = { id: string; userId: string; total: number };

// ドメイン型ではない：どんな項目があるかが分からず、使うたびに確かめる必要がある
type RawOrder = Record<string, unknown>;
```

境界での検証では、データが入ってくる場所のコードが、`RawOrder` のような値を一度だけ確かめて `Order` にし、内側のコードは `Order` だけを扱います。

このように、外から来たデータは、入口で一度だけ検証し、内側では型を信じる必要があります。

### 13. 新しい型を書く前に、既存の型から導く

OpenAPI の定義、GraphQL のスキーマ、データベースのマイグレーションがすでにデータの形を定義しているなら、エージェントは、同じ形の型を書き直さず、そこから生成された型から導きます。

```
// 生成された型（本来は生成されたモジュールから import する）
type ChecksMessage = {
  totalCount: number;
  checks: { name: string; status: string }[];
  updatedAt: string;
};

// 悪い例：同じ形を書き直しているので、スキーマが変わると食い違う
type CheckSummary = {
  totalCount: number;
  checks: { name: string; status: string }[];
};
function renderChecksLoose(s: CheckSummary) {
  /* ... */
}

// 良い例：生成された型から、必要な項目だけを取り出す
function renderChecks(s: Pick<ChecksMessage, "totalCount" | "checks">) {
  /* ... */
}
```

新しいインターフェースを書く前に、`Pick`、`Omit`、`Parameters`、`ReturnType`、`Awaited`、`typeof` を使えないかを確かめます。

このように、元になる定義があるなら、型を書き直さず、そこから導く必要があります。

### 14. 引数は、位置で並べずにオブジェクトで渡す

引数をオブジェクトで渡すと、どの値が何の引数かが名前で分かり、引数の順番を取り違えることもなくなります。

```
type Selection = {
  startLineNumber: number;
  startColumn: number;
  endLineNumber: number;
  endColumn: number;
};
declare const uri: string;
declare function openFileLoose(uri: string, selection: Selection): void;
declare function openFile(args: { uri: string; selection: Selection }): void;

// 悪い例：2つの引数を入れ替えても、型が合えばコンパイルが通る
openFileLoose(uri, {
  startLineNumber: 10,
  startColumn: 1,
  endLineNumber: 10,
  endColumn: 1,
});

// 良い例：順番に左右されず、それぞれの値が何かが名前で分かる
openFile({
  uri,
  selection: {
    startLineNumber: 10,
    startColumn: 1,
    endLineNumber: 10,
    endColumn: 1,
  },
});
```

ただし、1フレームごとの描画、トークナイザ、パーサのように、何度も繰り返し実行される箇所では、この規則を使いません。呼び出すたびに引数のオブジェクトを作ると、そのたびにメモリを確保する手間がかかり、繰り返しの回数が多い箇所では、処理の速さに響くからです。

!

- **1フレームごとの描画**・・・ アニメーションやゲームのように、画面を1秒間に数十回描き直す処理
- **トークナイザ**・・・ 文字列を、単語や記号のような意味のある最小の単位（トークン）に区切るプログラム
- **パーサ**・・・ トークンの並びなどを読み取り、プログラムが扱える構造に組み立てるプログラム

まとめると、引数が複数あるなら、繰り返し実行される箇所を除いて、オブジェクトで渡す必要がある、ということです。

### 15. 手元で動かせるものは、モックにせず本物でテストする

エージェントは、手元で動かせるものはモック（本物の部品の代わりに使う偽の部品）にせず、本物を動かしてテストします。モックにするのは、手元で動かせないもの（例：外部の決済サービス）だけです。画面は、実際にビルドして動かして確かめます。

```
declare function test(name: string, fn: () => Promise<void>): void;
declare function expect<T>(actual: T): { toBe(expected: T): void };
declare function makeTempDir(): Promise<string>;
declare function saveNote(dir: string, text: string): Promise<void>;
declare function loadNote(dir: string): Promise<string>;
declare const fakeFs: { writeFile: { calledTimes: number } };

// 悪い例：手元で動かせるファイルの保存まで偽物に置き換え、偽物が呼ばれた回数だけを確かめている
test("メモを保存する", async () => {
  await saveNote("/notes", "買い物");
  expect(fakeFs.writeFile.calledTimes).toBe(1);
});

// 良い例：一時ディレクトリに本物のファイルを書き、読み戻して中身を確かめる
test("保存したメモを読み戻せる", async () => {
  const dir = await makeTempDir();
  await saveNote(dir, "買い物");
  expect(await loadNote(dir)).toBe("買い物");
});
```

### 16. 診断の情報は、構造化したログで残す

エージェントは、IDから不具合を調べられるだけの情報を持つ、構造化したログ（決まった項目を持つログ）で、診断の情報を残します。リリースするコードに `console.log` を残しません。

```
declare const logger: {
  error(event: string, fields: Record<string, unknown>): void;
};
declare const orderId: string;
declare const userId: string;
declare const err: Error;

// 悪い例：文字列だけでは、どの注文で、なぜ失敗したのかを後から探せない
console.log("payment failed");

// 良い例：出来事の名前と、調べるときに使うIDや理由を、決まった項目で残す
logger.error("payment_failed", { orderId, userId, reason: err.message });
```

良い例のログなら、不具合を調べる人やエージェントは、`orderId` で検索して、その注文で何が起きたかをたどれます。

このように、診断の情報は、後からIDでたどれる形のログで残す必要があります。

## 依頼の書き方：TypeScriptのファイルを扱う作業で、`/typescript-best-practices` と入力する

同梱ガイドの[`05-build-and-clean.md`](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/05-build-and-clean.md)は、TypeScriptのファイルを扱う作業では `/typescript-best-practices` と入力するよう案内しています。

## まとめ

- **確かめる役**・・・ コードを書いたエージェントの代わりに、コンパイラが型の誤りを見つけます。
- **使いどき**・・・ TypeScriptのファイルを扱う作業で、利用者が `/typescript-best-practices` と入力して呼びます。自動では読み込まれません。
- **規則**・・・ ありえない状態を型で書けなくし、外から受け取るデータを、入ってくる場所で一度だけ検証します。

次の[第31章](https://zenn.dev/sc30gsw/books/080faba713547b/viewer/ad5727)では、コードの品質を保つ3つのSkillの2つ目として、不具合を直す前に、修正前に失敗するテストを書く [`/tdd`](https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md) を扱います。
