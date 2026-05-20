# 10. 計算関数 (4) 集計関数

<script setup>
import quiz from './quiz.json'
</script>

<div class="goal-list">
<p>学習目標</p>

- [ ] 集計関数と非集計の混在エラーの原因を説明できる
- [ ] COUNT と COUNTD の違いを説明できる
- [ ] ATTR の挙動を理解する

</div>

**所要時間目安:** 約 60 分
**演習データ:** Chicago Taxi

---

## 1. 基本（SUM, AVG, MIN, MAX）

**集計関数** は、複数行の値を「ひとつの値にまとめる」関数です。Tableau のビューでは、ディメンションが集計の **粒度** を決め、メジャーは集計関数によって 1 行に圧縮されます。

| 関数 | 戻り値 | 例 |
|------|--------|-----|
| `SUM([field])` | 合計 | `SUM([trip_total])` … 売上合計 |
| `AVG([field])` | 算術平均 | `AVG([trip_miles])` … 平均距離 |
| `MIN([field])` | 最小値（数値・日付・文字列の昇順最小） | `MIN([trip_start_timestamp])` … 最古の乗車日時 |
| `MAX([field])` | 最大値 | `MAX([fare])` … 最高料金 |

ビューに `SUM(trip_total)` を置いて `company` を列に置くと、Tableau は内部で「会社ごとに料金を合計する」クエリを発行します。

```
SUM([trip_total])
```

```
AVG([trip_miles])
```

::: tip 文字列や日付にも MIN/MAX が使える
`MIN([company])` は文字列の昇順で先頭に来る会社名を返します。日付に対する `MIN` は最古日、`MAX` は最新日です。「初回購入日」や「最終取引日」を取り出すときによく使います。
:::

::: info NULL は自動で除外
集計関数は NULL を「無い」ものとして扱います。`SUM` では NULL 行は加算されず、`AVG` では分母にもなりません。NULL を 0 として扱いたい場合は `ZN([field])` を内側に挟みます。
:::

---

## 2. 件数（COUNT, COUNTD）

行数を数える関数には 2 種類あります。違いはとても重要なので必ず使い分けます。

| 関数 | 数えるもの | 例 |
|------|-----------|-----|
| `COUNT([field])` | フィールドが **NULL でない行数** | `COUNT([trip_id])` … 取引数 |
| `COUNTD([field])` | フィールドの **一意な値の数** (DISTINCT COUNT) | `COUNTD([taxi_id])` … 稼働した車両台数 |

```
COUNT([trip_id])
```

```
COUNTD([taxi_id])
```

`COUNT(*)` のような構文は Tableau には無いため、代わりに「NULL になり得ない列」を選ぶか、あるいは `SUM([Number of Records])`（旧）や `COUNT([trip_id])` などを使います。

::: warning COUNTD は重い
COUNTD は内部的に DISTINCT を取るため、データ量が増えると顕著に遅くなります。**抽出データソース** では事前に最適化されますが、ライブ接続ではフィルター後の行数や粒度を意識して使用するか、必要に応じて代替計算（LOD など）を検討します。
:::

---

## 3. 中央値・分散（MEDIAN, VAR, VARP, STDEV, STDEVP）

統計向けの集計関数です。分布の把握や外れ値検知で使います。

| 関数 | 内容 |
|------|------|
| `MEDIAN([f])` | 中央値（50 パーセンタイル） |
| `VAR([f])` | 標本分散（n-1 で割る） |
| `VARP([f])` | 母分散（n で割る） |
| `STDEV([f])` | 標本標準偏差（VAR の平方根） |
| `STDEVP([f])` | 母標準偏差（VARP の平方根） |

```
MEDIAN([trip_total])
```

```
STDEV([trip_miles])
```

`VAR` と `VARP`、`STDEV` と `STDEVP` の違いは、「母集団全体を扱っている」と見るか「標本（サンプル）」と見るかです。サンプルからの推定なら **末尾に P がつかないほう**（VAR / STDEV）を使うのが一般的です。

::: info MEDIAN は計算負荷が高め
中央値はソートが必要なため、SUM や AVG に比べて重い処理です。データソースが抽出ファイル（`.hyper`）なら高速ですが、巨大なライブ接続では時間がかかる場合があります。
:::

---

## 4. パーセンタイル（PERCENTILE）

任意の分位点を取り出すには `PERCENTILE` を使います。

```
PERCENTILE([trip_total], 0.5)
```

第 2 引数は 0〜1 の範囲です。`0.5` なら中央値、`0.9` なら 90 パーセンタイルです。**`PERCENTILE([field], 0.5)` は `MEDIAN([field])` と同じ結果** になります。

| 用途 | 式の例 |
|------|--------|
| 中央値 | `PERCENTILE([trip_total], 0.5)` |
| 第 1 四分位数 | `PERCENTILE([trip_total], 0.25)` |
| 第 3 四分位数 | `PERCENTILE([trip_total], 0.75)` |
| 上位 10% の境界 | `PERCENTILE([trip_total], 0.9)` |

::: tip 異常値検知に便利
「99 パーセンタイル超え」を異常値とみなして抽出する、というアプローチでよく使います。SUM や AVG では平均値が外れ値に引っ張られやすいので、PERCENTILE と組み合わせると堅牢になります。
:::

---

## 5. ATTR の役割と「*」表示の意味

**ATTR 関数** は「ビューの粒度に対して、対象フィールドの値が **唯一なら** その値を返し、**複数あれば `*`** を返す」という変わった集計関数です。

```
ATTR([company])
```

ビューの粒度で会社が 1 つしかない場合は会社名が、複数混ざっている場合は文字どおり `*` が表示されます。

<div class="img-placeholder">
  <span class="img-placeholder-tag">画像予定</span>
  <span class="img-placeholder-caption">ATTR が `*` を返している様子</span>
  <span class="img-placeholder-path">docs/public/images/10-functions-aggregate/attr-asterisk.png</span>
</div>

### 主な用途

- **ダッシュボードのタイトルや KPI 数値** に、ディメンション値をそのまま埋め込みたい
- ツールヒントで「ビュー上の集計単位に紐づく属性」を表示したい
- マーク詳細にディメンションを置きたいが、ビューの粒度は維持したい

たとえばダッシュボードのタイトルで「現在表示中の会社: `ATTR([company])`」を出すと、フィルターで 1 社に絞っているときは会社名、複数選んでいるときは `*` になります。

::: info MIN との違い
1 行しかないなら `ATTR` と `MIN` は同じ値を返します。違いは「複数あるとき」で、`MIN` は最小値を、`ATTR` は `*` を返します。「値が混在しているなら混在していると見せる」のが ATTR の哲学です。
:::

---

## 6. 集計と非集計の混在エラー

Tableau でよく遭遇するエラーが **「集計式と非集計式を組み合わせることはできません」** です。

### 原因

下の式を考えてみます。

```
[trip_total] - AVG([trip_total])
```

これは「行レベルの料金」から「集計後の平均」を引こうとしていますが、`[trip_total]` は **行レベル（非集計）**、`AVG([trip_total])` は **集計** です。Tableau は「**ひとつの計算式の中で粒度が混在するのは不正**」と判断します。

### 解決策

#### 解決策 A: 両方を集計にする

「行ごとの差」が欲しいわけではなく「集計値どうしの差」が欲しいなら、両方を集計にします。

```
SUM([trip_total]) - AVG([trip_total]) * COUNT([trip_id])
```

#### 解決策 B: LOD で固定値にする

「データセット全体の平均」と各行の差を見たい場合は **FIXED LOD** で計算します。FIXED は行レベルとしても集計としても扱える便利な特性があります。

```
[trip_total] - { FIXED : AVG([trip_total]) }
```

| 試したいこと | 推奨アプローチ |
|--------------|-----------------|
| 行レベルで差分を見たい | 右辺を FIXED LOD にして全体スカラーに固定 |
| ビュー単位の集計差を見たい | 両辺とも集計関数で揃える |
| 行ごとに動的な平均（カテゴリ別など） | `{ FIXED [カテゴリ] : AVG(...) }` で粒度を指定 |

LOD については第 12 章で詳しく扱います。

---

## 7. パススルー関数（概要のみ）

**RAWSQL_** で始まる関数群は、データソースの SQL をそのまま発行できる「**パススルー関数**」です。Tableau の関数では実現できない、データベース固有の関数を呼び出すための逃げ道です。

| 関数 | 戻り値の型 |
|------|-----------|
| `RAWSQL_INT("<SQL>", [field])` | 整数 |
| `RAWSQL_REAL("<SQL>", [field])` | 実数 |
| `RAWSQL_STR("<SQL>", [field])` | 文字列 |
| `RAWSQL_BOOL("<SQL>", [field])` | 真偽 |
| `RAWSQL_DATE("<SQL>", [field])` | 日付 |
| `RAWSQLAGG_*` シリーズ | 集計関数として動作 |

SQL の中の `%1` `%2` … はプレースホルダーで、引数として渡したフィールドに置き換わります。

```
RAWSQL_REAL("LN(%1)", [trip_total])
```

::: warning 抽出データソースでは使えない / データソース依存
RAWSQL はライブ接続限定で、抽出（`.hyper`）に対しては動作しないか、Hyper SQL の文法に縛られるため、互換性に注意が必要です。さらにデータソースの方言（MySQL / Snowflake / BigQuery など）に依存するため、本番では使い回しが利かない場合があります。通常は Tableau 標準関数で十分なケースがほとんどです。
:::

---

## やってみよう

Chicago Taxi データで集計関数の挙動を確認しましょう。

1. **基本の集計**: `company` を列、`SUM(trip_total)` を行に置いて、会社別の売上合計を表示します。
2. **COUNT vs COUNTD**: 同じシートに `COUNT(trip_id)` と `COUNTD(taxi_id)` を行に追加します。「取引件数」と「実車両数」の桁の違いを確認します。
3. **平均と中央値**: 別シートで `AVG(trip_total)` と `MEDIAN(trip_total)` を会社別に並べ、平均と中央値の乖離が大きい会社を探します。外れ値の影響が見えるはずです。
4. **パーセンタイル**: `PERCENTILE([trip_total], 0.99)` を計算フィールドにして、各会社の「上位 1% の料金水準」を確認します。
5. **ATTR の挙動**: ビューに `company` を置かない状態で `ATTR([company])` をテキストに置きます。データ全体なら `*` が出るはずです。フィルターで 1 社に絞ると会社名が出ます。
6. **混在エラーを体感**: 計算フィールドに `[trip_total] - AVG([trip_total])` と書いてエラーになることを確認 → 右辺を `{ FIXED : AVG([trip_total]) }` に書き換えて成功させます。
7. **NULL の扱い**: `tips` には NULL が混ざる場合があります。`AVG([tips])` と `AVG(ZN([tips]))` を並べて差を確認します（NULL を 0 として平均すると分母が増え、値が下がります）。

<div class="img-placeholder">
  <span class="img-placeholder-tag">画像予定</span>
  <span class="img-placeholder-caption">会社別の平均値と中央値の比較</span>
  <span class="img-placeholder-path">docs/public/images/10-functions-aggregate/avg-vs-median.png</span>
</div>

---

## まとめ

- 集計関数は **ビューの粒度** で複数行をひとつの値にまとめる関数。`SUM` / `AVG` / `MIN` / `MAX` が基本。
- **`COUNT`** は NULL でない行数、**`COUNTD`** は一意な値の数。COUNTD は重いので注意。
- **`MEDIAN`** や **`PERCENTILE`** は外れ値の影響を受けにくく、料金などのスキュー分布で有効。
- **`ATTR`** は「ビュー粒度で一意ならその値、複数なら `*`」を返す。ダッシュボードのタイトルなどで活躍。
- **集計と非集計の混在エラー** は粒度の不一致が原因。両辺を集計にするか、LOD で粒度を明示して解決。
- **RAWSQL** はデータベース固有関数を呼ぶ最終手段。データソース依存・抽出非対応に注意。

---

## 章末クイズ

<QuizTrueFalse chapter-id="10-functions-aggregate" :questions="quiz" />
