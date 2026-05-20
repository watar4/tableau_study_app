# 08. 計算関数 (2) 日付

<script setup>
import quiz from './quiz.json'
</script>

<div class="goal-list">
<p>学習目標</p>

- [ ] DATEDIFF / DATEADD / DATEPART / DATETRUNC の違いを説明し使い分けられる
- [ ] 会計年度・週開始曜日を意識して計算できる
- [ ] 「今日基準で N 日前」のような相対期間計算ができる

</div>

**所要時間目安:** 約 90 分
**演習データ:** NOAA 気象 + Chicago Taxi（時系列）

---

## 1. 日付/日時の基本

Tableau の日付系の型には **DATE** と **DATETIME** の 2 種類があります。

| 型 | 内容 | 例 |
|----|------|----|
| **DATE** | 年月日のみ | `2024-04-15` |
| **DATETIME** | 年月日 + 時分秒 | `2024-04-15 10:30:45` |

Chicago Taxi の `trip_start_timestamp` `trip_end_timestamp` は DATETIME 型です。日付関数の戻り型は引数の型に依存するため、`TODAY()` と `NOW()` のように一見似ている関数でも結果の型が違うことに注意が必要です。

### date_part 文字列

ほとんどの日付関数は、第 1 引数に **どの粒度で処理するか** を表す文字列を取ります。

| 文字列 | 意味 |
|--------|------|
| `'year'` | 年 |
| `'quarter'` | 四半期 |
| `'month'` | 月 |
| `'week'` | 週 |
| `'day'` | 日 |
| `'weekday'` | 曜日 |
| `'hour'` | 時 |
| `'minute'` | 分 |
| `'second'` | 秒 |
| `'iso-year'` `'iso-week'` `'iso-weekday'` | ISO 8601 ベース |

::: warning シングルクォートで括る
`DATEDIFF(day, ...)` ではなく `DATEDIFF('day', ...)` のように、必ず **シングルクォート文字列** にします。
:::

---

## 2. 取得系（TODAY, NOW）

| 関数 | 戻り型 | 内容 |
|------|--------|------|
| `TODAY()` | **DATE** | 実行時点の「日付」（時刻を持たない） |
| `NOW()` | **DATETIME** | 実行時点の「日時」 |

```
// 今日の日付
TODAY()

// 今この瞬間
NOW()
```

::: info 「今」のタイミング
Tableau Desktop でビューを再描画するたびに評価されます。Tableau Server / Cloud では、ダッシュボードを開いた時点で評価されるので、キャッシュが効いている場合は値が古いことがあります。
:::

::: warning DATETIME と DATE は型が違う
`DATEDIFF('day', TODAY(), [trip_start_timestamp])` のように DATE と DATETIME を混ぜても日数差は計算できますが、`TODAY() = [trip_start_timestamp]` のような等号比較では「DATE と DATETIME の比較」となり、DATETIME 側に時刻があるとほぼ一致しません。`DATE([trip_start_timestamp]) = TODAY()` のように DATE に揃えるのが安全です。
:::

---

## 3. 部分抽出（DATEPART, DATENAME, YEAR/MONTH/DAY/WEEK/QUARTER）

日付から構成要素を取り出す関数群です。

### DATEPART（数値で返す）

```
DATEPART('year', [trip_start_timestamp])      // → 2024
DATEPART('month', [trip_start_timestamp])     // → 4
DATEPART('hour', [trip_start_timestamp])      // → 10
DATEPART('weekday', [trip_start_timestamp])   // → 1〜7（既定は日曜=1）
```

### DATENAME（文字列で返す）

```
DATENAME('month', [trip_start_timestamp])     // → "April"（環境のロケールに依存）
DATENAME('weekday', [trip_start_timestamp])   // → "Monday"
```

### 専用関数（DATEPART のショートカット）

| 関数 | 同等 |
|------|------|
| `YEAR(date)` | `DATEPART('year', date)` |
| `MONTH(date)` | `DATEPART('month', date)` |
| `DAY(date)` | `DATEPART('day', date)` |
| `WEEK(date)` | `DATEPART('week', date)` |
| `QUARTER(date)` | `DATEPART('quarter', date)` |

```
// 月別の売上集計用ディメンション
MONTH([trip_start_timestamp])
```

::: tip 数値で取るか文字列で取るか
- ソートしたい・計算に使う → `DATEPART`（数値）
- ラベル表示したい・ヒューマンリーダブル → `DATENAME`（文字列）
:::

---

## 4. 切り捨て / 丸め（DATETRUNC）

`DATETRUNC(date_part, date, [週開始曜日])` は、指定粒度より細かい部分を「捨てる」関数です。

| 例 | 結果（`2024-04-15 10:30:45` を入力） |
|----|------|
| `DATETRUNC('year', ...)` | `2024-01-01 00:00:00` |
| `DATETRUNC('quarter', ...)` | `2024-04-01 00:00:00` |
| `DATETRUNC('month', ...)` | `2024-04-01 00:00:00` |
| `DATETRUNC('week', ...)` | その週の日曜 (既定) `00:00:00` |
| `DATETRUNC('day', ...)` | `2024-04-15 00:00:00` |
| `DATETRUNC('hour', ...)` | `2024-04-15 10:00:00` |

```
// 月初に丸める（月次集計の軸として便利）
DATETRUNC('month', [trip_start_timestamp])
```

::: info DATETRUNC は DATETIME を返す
ビューで「月」表示にしたいだけならフィールドを右クリック → 「月」を選べばよいですが、計算式の中で「月初日付」を値として使いたい場合に `DATETRUNC` が役立ちます。
:::

---

## 5. 加算減算（DATEADD）

`DATEADD(date_part, n, date)` は、指定粒度で `n` だけ進める／戻す関数です。`n` が負なら過去方向です。

```
// 30 日後
DATEADD('day', 30, TODAY())

// 1 か月前
DATEADD('month', -1, TODAY())

// 乗車終了の 10 分後
DATEADD('minute', 10, [trip_end_timestamp])
```

### 月末日の保持

月単位の加算で月末日が存在しない場合は、その月の最終日に丸められます。

```
DATEADD('month', 1, MAKEDATE(2024, 1, 31))   // → 2024-02-29（うるう年なので 29 日）
DATEADD('month', 1, MAKEDATE(2023, 1, 31))   // → 2023-02-28
```

::: warning ロールバックされない
`2024-01-31` に 1 か月足して `2024-02-29` になったあと、さらに 1 か月足しても **`2024-03-29`** であり、`2024-03-31` には戻りません。連続加算時は注意が必要です。
:::

---

## 6. 差分（DATEDIFF）

`DATEDIFF(date_part, 開始, 終了, [週開始曜日])` は、開始から終了までの差を **指定粒度の整数で** 返します。`DATEDIFF('day', a, b)` は `b - a` の日数です（順序に注意）。

```
// 今日から見て何日前の乗車か（過去なら正の値）
DATEDIFF('day', [trip_start_timestamp], TODAY())

// 乗車時間（秒）
DATEDIFF('second', [trip_start_timestamp], [trip_end_timestamp])
```

### 境界をまたぐ単位

`DATEDIFF` は「単位の境界をいくつまたいだか」を数えるため、24 時間に満たなくても日数が増えることがあります。

```
DATEDIFF('day', "2024-04-15 23:00", "2024-04-16 01:00")
// → 1（実時間は 2 時間でも、日付の境界を 1 回またぐ）
```

これは月差・年差でも同じで、`DATEDIFF('year', '2024-12-31', '2025-01-01')` は `1` を返します。

### 週開始曜日

`DATEDIFF('week', ..., ..., 'monday')` のように第 4 引数で週の開始日を指定できます。`'sunday'` `'monday'` などの文字列です。省略時はデータソースの設定（既定は日曜開始）に従います。

::: tip 「正味の経過日数」が欲しい場合
境界跨ぎのカウントではなく、実時間ベースで日数を出したいときは秒で取って割ります:
```
DATEDIFF('second', a, b) / 86400.0
```
:::

---

## 7. 構築（MAKEDATE, MAKEDATETIME, MAKETIME）

数値や既存の日付・時刻を組み合わせて新しい日時を作ります。07 章でも触れた関数群です。

| 関数 | 例 |
|------|----|
| `MAKEDATE(年, 月, 日)` | `MAKEDATE(2024, 4, 15)` → `2024-04-15` |
| `MAKEDATETIME(日付, 時刻)` | `MAKEDATETIME(TODAY(), MAKETIME(9, 0, 0))` |
| `MAKETIME(時, 分, 秒)` | `MAKETIME(10, 30, 0)` |

```
// 年・月の数値ディメンションから月初日を作る
MAKEDATE([year], [month], 1)
```

```
// 開始タイムスタンプから「その日の朝 9 時」を作る
MAKEDATETIME(DATE([trip_start_timestamp]), MAKETIME(9, 0, 0))
```

---

## 8. 判定（ISDATE）

`ISDATE(文字列)` は、引数の **文字列** が日付として解釈できるかどうかを真偽値で返します。

```
ISDATE("2024-04-15")     // → true
ISDATE("not a date")     // → false
ISDATE("2024-02-30")     // → false（存在しない日）
```

データクレンジングや、`DATEPARSE` 前のバリデーションに使えます。

::: info ISDATE の引数は文字列限定
`ISDATE` は文字列を受け取って判定する関数です。既に日付型のフィールドに対しては使用できません（必要があれば `STR()` で文字列化してから渡します）。
:::

---

## 9. 曜日（WEEKDAY）

Tableau には独立した `WEEKDAY()` 関数は **ありません**。曜日を取り出すには `DATEPART('weekday', ...)` または `DATENAME('weekday', ...)` を使います。

```
// 曜日番号（既定で 日=1, 月=2, ... 土=7）
DATEPART('weekday', [trip_start_timestamp])

// 曜日名（ロケール依存）
DATENAME('weekday', [trip_start_timestamp])
```

### 曜日番号で土日を判定

```
// 週末フラグ
[曜日番号] = 1 OR [曜日番号] = 7
```

ここで `[曜日番号]` は `DATEPART('weekday', [trip_start_timestamp])` を別フィールドにしたものです。

::: warning 既定は日曜=1
Tableau の `'weekday'` 番号は **既定で日曜が 1** です。月曜始まりが必要な場合は `'iso-weekday'` を使うか、`DATEPART('weekday', date, 'monday')` のように週開始曜日を指定します（関数によりサポート状況が異なるため、確実なのは ISO 系の date_part か、データソースプロパティでの設定変更です）。
:::

---

## 10. 会計年度の設定

業務データでは「会計年度」が暦年と一致しないことがよくあります。たとえば日本企業の多くは 4 月始まりです。

### データソース単位の設定

データペインで日付ディメンション（または接続全体）を右クリック → 「**既定のプロパティ**」 → 「**会計年度の開始**」 → 「4 月」を選択すると、以後 `YEAR()` などが会計年度ベースで返るようになります。

<div class="img-placeholder">
  <span class="img-placeholder-tag">画像予定</span>
  <span class="img-placeholder-caption">既定のプロパティ → 会計年度の開始</span>
  <span class="img-placeholder-path">docs/public/images/08-functions-date/fiscal-year.png</span>
</div>

### 個別フィールドでの上書き

ビュー内のピル（例: `YEAR(trip_start_timestamp)`）を右クリック → 「**会計年度の開始**」で、そのピル限定で会計年度を切り替えられます。

::: info 計算式で明示的に作る場合
データソースの設定に依存しない計算が欲しい場合は、次のように手で組みます:
```
IF MONTH([trip_start_timestamp]) >= 4
THEN YEAR([trip_start_timestamp])
ELSE YEAR([trip_start_timestamp]) - 1
END
```
:::

---

## 11. よくある計算例

### 経過日数

```
// 今日から見て何日経過したか
DATEDIFF('day', [trip_start_timestamp], TODAY())
```

### MTD（月初〜今日）

```
// 今日と同じ月で、今日以下の日付だけを true
DATETRUNC('month', [trip_start_timestamp]) = DATETRUNC('month', TODAY())
AND [trip_start_timestamp] <= NOW()
```

これをフィルターに置いて true を選択すれば MTD の集計になります。

### YTD（年初〜今日）

```
YEAR([trip_start_timestamp]) = YEAR(TODAY())
AND [trip_start_timestamp] <= NOW()
```

### 前年同月比

```
// 当月売上
IF DATETRUNC('month', [trip_start_timestamp]) = DATETRUNC('month', TODAY())
THEN [trip_total] END
```

```
// 前年同月売上
IF DATETRUNC('month', [trip_start_timestamp]) = DATEADD('month', -12, DATETRUNC('month', TODAY()))
THEN [trip_total] END
```

両者をそれぞれ `SUM()` で集計し、比率を出せば前年同月比になります。

### 「直近 N 日」フィルター

```
DATEDIFF('day', [trip_start_timestamp], TODAY()) <= 30
AND DATEDIFF('day', [trip_start_timestamp], TODAY()) >= 0
```

### 月初・週初・四半期初

```
DATETRUNC('month', [trip_start_timestamp])     // 月初
DATETRUNC('week', [trip_start_timestamp])      // 週初（日曜開始）
DATETRUNC('quarter', [trip_start_timestamp])   // 四半期初
```

<div class="img-placeholder">
  <span class="img-placeholder-tag">画像予定</span>
  <span class="img-placeholder-caption">月別売上と前年同月の並列表示例</span>
  <span class="img-placeholder-path">docs/public/images/08-functions-date/yoy-compare.png</span>
</div>

---

## やってみよう

Chicago Taxi の `trip_start_timestamp` を使って、日付関数を一通り触ってみましょう。

1. **データに接続**
   - `chicago_taxi_trips.hyper` に接続。`trip_start_timestamp` がデータペインで「カレンダーアイコン」になっていることを確認します。
2. **月初日に丸めて月次集計を作る**
   - 計算フィールド `月初日`:
     ```
     DATETRUNC('month', [trip_start_timestamp])
     ```
   - これを列、`SUM([trip_total])` を行に置いて折れ線グラフを作ります。
3. **曜日別の乗車件数**
   - 計算フィールド `曜日名`:
     ```
     DATENAME('weekday', [trip_start_timestamp])
     ```
   - 並び順用に `曜日番号 = DATEPART('weekday', [trip_start_timestamp])` も作り、`曜日名` を `曜日番号` でソートします。
4. **乗車時間（分）を DATEDIFF で出す**
   - 計算フィールド `乗車時間 (分)`:
     ```
     DATEDIFF('minute', [trip_start_timestamp], [trip_end_timestamp])
     ```
   - `trip_seconds` を 60 で割った値とほぼ一致することを確認します。
5. **「直近 30 日」フィルター**
   - 計算フィールド `直近30日フラグ`:
     ```
     DATEDIFF('day', [trip_start_timestamp], TODAY()) BETWEEN 0 AND 30
     ```
   - フィルターに掛けて、最新 30 日分だけを抽出します（データの最新日付に応じて調整）。
6. **会計年度（4 月始まり）を作る**
   - 計算フィールド `会計年度`:
     ```
     IF MONTH([trip_start_timestamp]) >= 4
     THEN YEAR([trip_start_timestamp])
     ELSE YEAR([trip_start_timestamp]) - 1
     END
     ```
   - これを列に、`SUM([trip_total])` を行に置いて、暦年集計と並べて比較します。
7. **前年同月比の計算**
   - 上の「11. よくある計算例」の「当月売上」「前年同月売上」をそれぞれ計算フィールドにして、ビュー上で比率 `当月 / 前年同月` を出します。
8. **時間帯別の傾向を見る**
   - 計算フィールド `時間帯`:
     ```
     DATEPART('hour', [trip_start_timestamp])
     ```
   - 列に置き、行に `COUNT([trip_id])` でピーク時間帯を可視化します。

---

## まとめ

- 日付系には **DATE** と **DATETIME** の 2 種類があり、`TODAY()` は DATE、`NOW()` は DATETIME を返します。等号比較では型を揃えるのが安全です。
- `DATEPART` `DATENAME` は構成要素の抽出、`DATETRUNC` は粒度に揃えた切り捨て、`DATEADD` `DATEDIFF` は加減算と差分という、4 つの基本関数を押さえれば大半の日付計算は組み立てられます。
- `DATEDIFF` は **境界をまたいだ回数** をカウントします。実時間で日数を出したい場合は秒差を 86400 で割るなど工夫が必要です。
- 月単位の `DATEADD` は **月末日が存在しない場合に丸められ**、その後ロールバックされない点に注意します。
- `WEEKDAY()` という関数は存在せず、`DATEPART('weekday', date)` を使います。既定は日曜=1 です。
- 会計年度は **データソースの既定プロパティ** か、ピル単位の右クリックメニューで切り替えられます。計算式で明示するなら `IF MONTH(...) >= 4 ...` で組みます。

---

## 章末クイズ

<QuizTrueFalse chapter-id="08-functions-date" :questions="quiz" />
