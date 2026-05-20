# 09. 計算関数 (3) 論理・条件式

<script setup>
import quiz from './quiz.json'
</script>

<div class="goal-list">
<p>学習目標</p>

- [ ] IF / CASE / IIF を使い分けられる
- [ ] AND / OR / NOT を活用した複合条件を書ける
- [ ] null セーフな条件式が書ける

</div>

**所要時間目安:** 約 60 分
**演習データ:** Chicago Taxi（料金帯バンド分け 等）

---

## 1. IF / THEN / ELSEIF / ELSE / END

**IF 式** は Tableau における最も汎用的な条件分岐です。条件を上から順に評価し、最初に真になった枝の値を返します。

基本構文は次のとおりです。`END` は必須で、書き忘れると構文エラーになります。

```
IF <条件1> THEN <値1>
ELSEIF <条件2> THEN <値2>
ELSE <既定値>
END
```

料金帯のバンド分けを `trip_total` で行う例です。`<` `>` `>=` といった大小比較を使えるのが IF の特徴です。

```
IF [trip_total] < 10 THEN "Low"
ELSEIF [trip_total] < 25 THEN "Mid"
ELSE "High"
END
```

`ELSE` を省略すると、どの条件にも合致しない行は **NULL** が返ります。意図しない NULL を生まないため、原則として `ELSE` を書くことをおすすめします。

::: tip ELSEIF と ELSE IF
Tableau の予約語は **`ELSEIF`**（1 単語）です。SQL の `ELSE IF` のように分けて書くとエラーになります。
:::

::: info 返り値の型は揃える
`THEN` で返す値は同じ型に揃える必要があります。文字列を返したり数値を返したりする式はエラーになります。数値と NULL の混在は許容されますが、整数と文字列の混在は不可です。
:::

---

## 2. CASE / WHEN / THEN / ELSE / END

**CASE 式** は「ひとつのフィールドの値を、複数の値と等価比較して分岐する」用途に特化した構文です。読みやすさと処理速度の両面で IF よりも有利な場合があります。

```
CASE <フィールド or 式>
  WHEN <値1> THEN <返値1>
  WHEN <値2> THEN <返値2>
  ELSE <既定値>
END
```

`payment_type` を 3 グループに分類する例です。

```
CASE [payment_type]
  WHEN "Cash" THEN "現金"
  WHEN "Credit Card" THEN "カード"
  WHEN "Mobile" THEN "モバイル決済"
  ELSE "その他"
END
```

CASE は **等価比較 (`=`)** しか行えません。`<` `>` のような大小比較や、`AND` / `OR` で複合した条件は書けないため、その場合は IF を使います。

| 比較したい内容 | 推奨構文 |
|----------------|-----------|
| 1 つのフィールドを複数の値と等価比較 | CASE |
| 範囲（`>=`, `<` など）の判定 | IF |
| 複数フィールドを AND / OR で結合 | IF |
| 既定値も必要 | どちらも `ELSE` を必ず付ける |

::: warning CASE では NULL を WHEN にできない
`WHEN NULL THEN ...` のような書き方はマッチしません。NULL の判定は `ISNULL([field])` を使った IF 式で行います。
:::

---

## 3. IIF（3 引数の意味と null 引数）

**IIF 関数** は「条件・真値・偽値」の 3 つを引数に取る、1 行のミニ IF です。短い条件式に向いています。

```
IIF(<条件>, <真のときの値>, <偽のときの値>)
```

例として「`tips` がプラスならチップあり、そうでなければチップなし」を返す式は次のとおりです。

```
IIF([tips] > 0, "Tip", "No Tip")
```

IIF にはオプションの **第 4 引数** があり、条件自体が **NULL** になった場合の戻り値を指定できます。条件式の中に NULL が混ざる可能性があるときに便利です。

```
IIF([tips] > 0, "Tip", "No Tip", "Unknown")
```

第 4 引数を省略した場合、条件が NULL のときの戻り値は **NULL** になります。

| 構文 | 用途 |
|------|------|
| `IIF(cond, a, b)` | 条件が NULL のとき NULL を返す |
| `IIF(cond, a, b, c)` | 条件が NULL のとき `c` を返す |

::: tip 短い分岐は IIF、複雑な分岐は IF
IIF はネストすると読みにくくなりがちです。3 段以上の分岐や複合条件には素直に IF / ELSEIF を使うほうがメンテナンスしやすくなります。
:::

---

## 4. IFNULL / ISNULL / ZN

NULL を扱うための 3 つの関数は、よく似ていますが目的が異なります。

| 関数 | 戻り値 | 主な用途 |
|------|--------|----------|
| `ISNULL([f])` | 真偽値 | NULL かどうかを判定する |
| `IFNULL([f], <代替値>)` | 元の値か代替値 | NULL を任意の値に置換する（文字列・数値・日付なんでも） |
| `ZN([f])` | 数値（NULL なら 0） | **数値型限定** で NULL を 0 に置換する |

`pickup_community_area` が NULL の場合に "Unknown" を表示する例です。

```
IFNULL(STR([pickup_community_area]), "Unknown")
```

NULL かどうかの真偽判定で分岐したい場合は `ISNULL` を使います。

```
IF ISNULL([dropoff_community_area]) THEN "降車エリア未記録"
ELSE STR([dropoff_community_area])
END
```

数値計算で NULL を 0 として扱いたい場面では `ZN` が便利です。たとえば「`tips` が記録されていない行は 0 円扱い」にする場合です。

```
ZN([tips])
```

::: warning ZN は数値型限定
`ZN` は文字列や日付に対しては使えません。文字列や日付の NULL 置換には `IFNULL` を使います。
:::

::: info SUM の中の NULL は自動的にスキップされる
集計関数（SUM, AVG など）は NULL 行を自動で無視します。`SUM([tips])` と `SUM(ZN([tips]))` は通常同じ結果になりますが、平均（AVG）では分母の数が変わるため結果が異なる点に注意します。
:::

---

## 5. 論理演算子（AND / OR / NOT）

複数の条件を組み合わせるには **論理演算子** を使います。Tableau では `AND` `OR` `NOT` のキーワードを使用します（`&&` `||` `!` は使えません）。

| 演算子 | 意味 | 例 |
|--------|------|-----|
| `AND` | すべての条件が真のときに真 | `[fare] > 10 AND [tips] > 0` |
| `OR` | いずれかの条件が真のときに真 | `[payment_type] = "Cash" OR [payment_type] = "Mobile"` |
| `NOT` | 真偽を反転する | `NOT ISNULL([tips])` |

### 優先順位

優先順位は **NOT > AND > OR** の順です。同じ式に `AND` と `OR` が混在すると、`AND` が先にまとまります。

```
[fare] > 10 AND [tips] > 0 OR [payment_type] = "Cash"
```

上記は「(`fare` > 10 AND `tips` > 0) OR `payment_type` = "Cash"」と評価されます。意図と合っているか不明瞭な場合は **括弧** で明示するのが安全です。

```
([fare] > 10 AND [tips] > 0) OR [payment_type] = "Cash"
```

![論理演算子の優先順位と括弧の必要性](/images/09-functions-logical/operator-precedence.png)

::: tip 短絡評価には依存しない
プログラミング言語のような「`AND` は左が偽なら右を評価しない」という短絡評価は、Tableau の最適化エンジン次第で挙動が変わる可能性があります。「左で NULL チェック → 右で値を参照」のような書き方ではなく、`IFNULL` や `ISNULL` を先に処理してから論理式に渡すほうが安全です。
:::

---

## 6. IN 述語（Tableau の書き方）

「値が一覧のどれかに当てはまるか」を簡潔に表すには **IN 述語** を使います。OR をいくつも連結するより読みやすくなります。

```
[payment_type] IN ('Cash', 'Credit Card', 'Mobile')
```

これは次の OR 連結と同じ意味です。

```
[payment_type] = 'Cash'
OR [payment_type] = 'Credit Card'
OR [payment_type] = 'Mobile'
```

数値リストでも使えます。

```
[pickup_community_area] IN (8, 28, 32, 76)
```

`NOT` と組み合わせれば「リストに含まれない」も表現できます。

```
NOT ([payment_type] IN ('Unknown', 'No Charge'))
```

::: info IN の中身は定数のみ
IN の中に書ける値はリテラル（定数）のみです。フィールド名やパラメーターを含めることはできません。動的な選択肢にしたい場合は、パラメーターと組み合わせた IF 式を使います。
:::

---

## 7. パフォーマンスの目安（CASE vs IF）

CASE と IF は機能的に書き換え可能なことが多いですが、パフォーマンス特性には差が出る場合があります。

| 観点 | CASE | IF |
|------|------|-----|
| 等価比較のみ | 高速になりやすい | CASE と同等または僅かに低速 |
| 大小比較 / 複合条件 | 使えない | 唯一の選択肢 |
| 可読性 | 値の一覧が見やすい | 条件が複雑だと冗長 |
| データソース最適化 | SQL 側の `CASE` に直接マッピングされやすい | 同様にマッピングされる |

「同じフィールドを複数の値で分岐する」場合は CASE のほうが意図が明確で、Tableau / データベース双方の最適化も効きやすいです。一方、`AND` や範囲比較が必要なら IF 一択です。

::: tip まずは可読性優先
パフォーマンス差はデータ量が小さいうちはほぼ体感できません。可読性を優先し、ボトルネックが見つかったら個別に書き換える方針が現実的です。
:::

---

## 8. よくある実装パターン

### パターン 1: 数値のバンディング（料金帯分け）

連続値を区分（バンド）に分ける処理は IF が定番です。

```
IF [trip_total] < 10 THEN "1. ～$10"
ELSEIF [trip_total] < 25 THEN "2. $10～25"
ELSEIF [trip_total] < 50 THEN "3. $25～50"
ELSE "4. $50～"
END
```

並び順を制御したいので、先頭に番号を付けるのがコツです。Tableau は文字列を昇順ソートするため、`1.` `2.` …の番号で意図した順序になります。

### パターン 2: 距離帯のステータス分類

複数フィールドの組み合わせで分類する場合は IF + AND が向いています。

```
IF [trip_miles] < 1 THEN "ご近所"
ELSEIF [trip_miles] < 5 AND [trip_seconds] < 900 THEN "短距離・短時間"
ELSEIF [trip_miles] < 5 THEN "短距離・渋滞"
ELSE "長距離"
END
```

### パターン 3: NULL セーフな比較

NULL が混じる列との比較は、明示的に `IFNULL` / `ISNULL` で処理しておくとバグが減ります。

```
IF ISNULL([tips]) THEN "未記録"
ELSEIF [tips] = 0 THEN "チップなし"
ELSE "チップあり"
END
```

<div class="img-placeholder">
  <span class="img-placeholder-tag">画像予定</span>
  <span class="img-placeholder-caption">料金帯バンドを色分けした棒グラフ</span>
  <span class="img-placeholder-path">docs/public/images/09-functions-logical/fare-band-bar.png</span>
</div>

---

## やってみよう

Chicago Taxi データを使って、本章で学んだ条件式を実際に書いてみましょう。

1. **計算フィールドを作成**: データペインで右クリック →「計算フィールドの作成」→ 名前を `料金帯` とします。
2. **IF 式を入力**: 上の「パターン 1」をそのまま貼り付け、エラーが出ないことを確認します。
3. **ビューに配置**: `料金帯` を「列」、`COUNT(trip_id)` を「行」にドラッグして、件数の分布を確認します。
4. **支払方法を分類**: `支払分類` という名前で計算フィールドを作成し、CASE で `payment_type` を 3 グループに分けます。マークの「色」に配置すると、料金帯ごとの支払構成比が見えます。
5. **IIF で 2 値判定**: `チップ有無` という計算フィールドを `IIF([tips] > 0, "Tip", "No Tip", "Unknown")` で作成。条件 NULL 時の "Unknown" がどんなときに出るか、データに NULL があるか確認します。
6. **ZN を使う**: `ZN([tips])` と `[tips]` の AVG をそれぞれ別のシートで作成し、平均値が異なることを観察します（ZN 版は分母が全行になる）。
7. **IN 述語**: フィルターとして直接掛けるのではなく、`主要会社フラグ = [company] IN ('Flash Cab', 'Taxi Affiliation Services', 'Sun Taxi')` のような真偽値フィールドを作って、マークの色や形状に使ってみます。
8. **動作確認**: 上で作った計算フィールドをツールヒントに置いて、いくつかのマークの値を一行ずつ追って確認します。

---

## まとめ

- **IF** は範囲比較や複合条件を含めて使える最も汎用的な分岐構文で、`END` を忘れない。
- **CASE** は「1 つの値を複数の値と等価比較」する場合に読みやすく、最適化されやすい。
- **IIF** は短い 2 分岐に向き、第 4 引数で条件 NULL 時の値を指定できる。
- NULL 操作は **`ISNULL` / `IFNULL` / `ZN`** を使い分け、特に `ZN` は数値専用。
- 論理演算子は **NOT > AND > OR** の優先順位。混在する場合は括弧で明示する。
- **IN 述語** で OR の羅列を簡潔に書ける。中身は定数のみ。

---

## 章末クイズ

<QuizTrueFalse chapter-id="09-functions-logical" :questions="quiz" />
