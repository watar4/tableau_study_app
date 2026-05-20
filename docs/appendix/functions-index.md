# 関数リファレンス索引

Tableau Desktop の主要な計算関数の早見表です。各関数の詳細は参照先の章を確認してください。

## カテゴリ別

### 数値関数 → [07. 数値・文字列・型変換](/07-functions-numeric-string/)

`ABS` / `ROUND` / `CEILING` / `FLOOR` / `DIV` / `MOD` / `POWER` / `EXP` / `LN` / `LOG` / `SQRT` / `SIGN` / `MIN` / `MAX`

### 文字列関数 → [07. 数値・文字列・型変換](/07-functions-numeric-string/)

`LEFT` / `RIGHT` / `MID` / `LEN` / `FIND` / `CONTAINS` / `STARTSWITH` / `ENDSWITH` / `REPLACE` / `TRIM` / `LTRIM` / `RTRIM` / `UPPER` / `LOWER` / `PROPER` / `SPLIT`
`REGEXP_MATCH` / `REGEXP_EXTRACT` / `REGEXP_EXTRACT_NTH` / `REGEXP_REPLACE`

### 型変換 → [07. 数値・文字列・型変換](/07-functions-numeric-string/)

`INT` / `FLOAT` / `STR` / `DATE` / `DATETIME` / `DATEPARSE` / `MAKEDATE` / `MAKEDATETIME` / `MAKETIME`

### 日付関数 → [08. 日付](/08-functions-date/)

`TODAY` / `NOW` / `DATEPART` / `DATENAME` / `YEAR` / `MONTH` / `DAY` / `WEEK` / `QUARTER` / `DATETRUNC` / `DATEADD` / `DATEDIFF` / `ISDATE`

### 論理関数 → [09. 論理・条件式](/09-functions-logical/)

`IF` / `THEN` / `ELSEIF` / `ELSE` / `END` / `CASE` / `WHEN` / `IIF` / `IFNULL` / `ISNULL` / `ZN` / `AND` / `OR` / `NOT` / `IN`

### 集計関数 → [10. 集計関数](/10-functions-aggregate/)

`SUM` / `AVG` / `MIN` / `MAX` / `COUNT` / `COUNTD` / `MEDIAN` / `VAR` / `VARP` / `STDEV` / `STDEVP` / `PERCENTILE` / `ATTR`
パススルー: `RAWSQL_INT` / `RAWSQL_REAL` / `RAWSQL_BOOL` / `RAWSQL_STR` / `RAWSQL_DATE` / `RAWSQL_DATETIME`

### 表計算関数 → [11. 表計算関数](/11-functions-tablecalc/)

`WINDOW_SUM` / `WINDOW_AVG` / `WINDOW_MIN` / `WINDOW_MAX` / `WINDOW_COUNT` / `WINDOW_MEDIAN` / `WINDOW_VAR` / `WINDOW_STDEV`
`RUNNING_SUM` / `RUNNING_AVG` / `RUNNING_MIN` / `RUNNING_MAX` / `RUNNING_COUNT`
`LOOKUP` / `PREVIOUS_VALUE` / `INDEX` / `FIRST` / `LAST` / `SIZE`
`RANK` / `RANK_DENSE` / `RANK_UNIQUE` / `RANK_MODIFIED`

### LOD 表現 → [12. LOD 表現](/12-lod/)

`{ FIXED ... : ... }` / `{ INCLUDE ... : ... }` / `{ EXCLUDE ... : ... }`

### ユーザー関数

`USERNAME` / `ISMEMBEROF` / `FULLNAME`

---

## アルファベット順早見表

| 関数 | カテゴリ | 用例 | 章 |
|------|---------|------|-----|
| `ABS` | 数値 | `ABS(-5) → 5` | 07 |
| `AND` | 論理 | `A AND B` | 09 |
| `ATTR` | 集計 | `ATTR([payment_type])` 一意なら値、複数なら `*` | 10 |
| `AVG` | 集計 | `AVG([trip_total])` | 10 |
| `CASE` | 論理 | `CASE [pay] WHEN "Cash" THEN ... END` | 09 |
| `CEILING` | 数値 | `CEILING(3.2) → 4` | 07 |
| `CONTAINS` | 文字列 | `CONTAINS([company], "Cab")` 大文字小文字区別 | 07 |
| `COUNT` | 集計 | `COUNT([trip_id])` NULL を除く件数 | 10 |
| `COUNTD` | 集計 | `COUNTD([taxi_id])` 重複を除く件数 | 10 |
| `DATE` | 型変換 | `DATE("2024-04-15") → 2024-04-15` | 07 |
| `DATEADD` | 日付 | `DATEADD('month', 1, dt)` | 08 |
| `DATEDIFF` | 日付 | `DATEDIFF('day', a, b) → b-a の日数` | 08 |
| `DATENAME` | 日付 | `DATENAME('month', dt) → "April"` (ロケール依存) | 08 |
| `DATEPART` | 日付 | `DATEPART('year', dt) → 2024` | 08 |
| `DATEPARSE` | 型変換 | `DATEPARSE("yyyy-MM-dd", str)` フォーマット必須 | 07 |
| `DATETIME` | 型変換 | `DATETIME("2024-04-15 10:30")` | 07 |
| `DATETRUNC` | 日付 | `DATETRUNC('month', dt) → 月初` | 08 |
| `DIV` | 数値 | `DIV(10, 3) → 3` 整数除算 | 07 |
| `ELSE` | 論理 | `IF cond THEN x ELSE y END` | 09 |
| `ELSEIF` | 論理 | `IF c1 THEN x ELSEIF c2 THEN y ELSE z END` | 09 |
| `END` | 論理 | IF / CASE の終端(必須) | 09 |
| `ENDSWITH` | 文字列 | `ENDSWITH([company], "Cab")` | 07 |
| `EXP` | 数値 | `EXP(1) → 2.718...` | 07 |
| `FIND` | 文字列 | `FIND([str], "Cab") → 位置 (見つからなければ 0)` | 07 |
| `FIRST` | 表計算 | パーティション内 先頭からの距離 (負の値) | 11 |
| `FIXED` | LOD | `{ FIXED [company] : SUM([trip_total]) }` | 12 |
| `FLOAT` | 型変換 | `FLOAT("3.14") → 3.14` | 07 |
| `FLOOR` | 数値 | `FLOOR(3.8) → 3` | 07 |
| `FULLNAME` | ユーザー | 現在のユーザーのフルネーム | — |
| `IF` | 論理 | `IF cond THEN x ELSE y END` | 09 |
| `IFNULL` | 論理 | `IFNULL([field], 0)` | 09 |
| `IIF` | 論理 | `IIF(cond, true_val, false_val, null_val)` | 09 |
| `IN` | 論理 | `[pay] IN ('Cash', 'Mobile')` | 09 |
| `INCLUDE` | LOD | `{ INCLUDE [seg] : SUM(...) }` ビューに含めて細かく集計 | 12 |
| `INDEX` | 表計算 | 現在行の位置 (1 始まり) | 11 |
| `INT` | 型変換 | `INT(-3.5) → -3` 0 方向への切り捨て | 07 |
| `ISDATE` | 日付 | `ISDATE([str]) → TRUE/FALSE` | 08 |
| `ISMEMBEROF` | ユーザー | `ISMEMBEROF("グループ名") → TRUE/FALSE` | — |
| `ISNULL` | 論理 | `ISNULL([field]) → TRUE/FALSE` | 09 |
| `LAST` | 表計算 | パーティション内 末尾からの距離 | 11 |
| `LEFT` | 文字列 | `LEFT([str], 3)` | 07 |
| `LEN` | 文字列 | `LEN([str])` 文字数 (バイト数ではない) | 07 |
| `LN` | 数値 | 自然対数 | 07 |
| `LOG` | 数値 | `LOG([n], base)` | 07 |
| `LOOKUP` | 表計算 | `LOOKUP(SUM([x]), -1)` 1 つ前の値 | 11 |
| `LOWER` | 文字列 | `LOWER([str]) → 全部小文字` | 07 |
| `LTRIM` | 文字列 | `LTRIM([str])` 左側の空白を除去 | 07 |
| `MAKEDATE` | 型変換 | `MAKEDATE(2024, 5, 1) → 2024-05-01` | 07 |
| `MAKEDATETIME` | 型変換 | `MAKEDATETIME(date, time)` | 07 |
| `MAKETIME` | 型変換 | `MAKETIME(10, 30, 0)` | 07 |
| `MAX` | 集計 / 数値 | 行レベル: `MAX(a, b)` / 集計: `MAX([field])` | 10 / 07 |
| `MEDIAN` | 集計 | `MEDIAN([field])` 中央値 | 10 |
| `MID` | 文字列 | `MID([str], 開始, 長さ)` | 07 |
| `MIN` | 集計 / 数値 | `MIN(a, b)` / `MIN([field])` | 10 / 07 |
| `MOD` | 数値 | `MOD(10, 3) → 1` 余り | 07 |
| `NOT` | 論理 | `NOT cond` | 09 |
| `NOW` | 日付 | `NOW()` 現在日時(時刻含む) | 08 |
| `OR` | 論理 | `A OR B` | 09 |
| `PERCENTILE` | 集計 | `PERCENTILE([x], 0.5)` = MEDIAN | 10 |
| `POWER` | 数値 | `POWER(2, 10) → 1024` | 07 |
| `PREVIOUS_VALUE` | 表計算 | 前の表計算結果を参照(累計実装などに) | 11 |
| `PROPER` | 文字列 | `PROPER([str]) → 単語の頭文字を大文字に` | 07 |
| `QUARTER` | 日付 | `QUARTER([dt]) → 1〜4` | 08 |
| `RAWSQL_*` | 集計 (パススルー) | 元 DB の関数を呼び出す | 10 |
| `RANK` | 表計算 | 同順位を共有、次を飛ばす (1,2,2,4) | 11 |
| `RANK_DENSE` | 表計算 | 同順位を共有、次を飛ばさない (1,2,2,3) | 11 |
| `RANK_MODIFIED` | 表計算 | 同順位は最後の順位を共有 (1,3,3,4) | 11 |
| `RANK_UNIQUE` | 表計算 | 同順位でも一意な順位 (1,2,3,4) | 11 |
| `REGEXP_EXTRACT` | 文字列 | キャプチャグループに一致する部分文字列 | 07 |
| `REGEXP_EXTRACT_NTH` | 文字列 | N 番目のキャプチャグループを取得 | 07 |
| `REGEXP_MATCH` | 文字列 | 一致するかの TRUE/FALSE | 07 |
| `REGEXP_REPLACE` | 文字列 | 一致部分を置換 | 07 |
| `REPLACE` | 文字列 | `REPLACE([str], "old", "new")` | 07 |
| `RIGHT` | 文字列 | `RIGHT([str], 3)` | 07 |
| `ROUND` | 数値 | `ROUND(123.456, 1) → 123.5` 四捨五入 | 07 |
| `RTRIM` | 文字列 | 右側の空白を除去 | 07 |
| `RUNNING_AVG` | 表計算 | 累積平均 | 11 |
| `RUNNING_COUNT` | 表計算 | 累積件数 | 11 |
| `RUNNING_MAX` | 表計算 | 累積最大値 | 11 |
| `RUNNING_MIN` | 表計算 | 累積最小値 | 11 |
| `RUNNING_SUM` | 表計算 | 累計 | 11 |
| `SIGN` | 数値 | `SIGN(n) → -1 / 0 / 1` | 07 |
| `SIZE` | 表計算 | パーティション内のマーク数 | 11 |
| `SPLIT` | 文字列 | `SPLIT([str], ",", 2)` 区切り 2 番目を返す | 07 |
| `SQRT` | 数値 | 平方根 | 07 |
| `STARTSWITH` | 文字列 | `STARTSWITH([str], "Flash")` | 07 |
| `STDEV` | 集計 | 標本標準偏差 | 10 |
| `STDEVP` | 集計 | 母集団標準偏差 | 10 |
| `STR` | 型変換 | `STR([n]) → "123"` | 07 |
| `SUM` | 集計 | `SUM([trip_total])` | 10 |
| `THEN` | 論理 | IF / CASE と一緒に使う | 09 |
| `TODAY` | 日付 | `TODAY()` 今日の日付 | 08 |
| `TRIM` | 文字列 | 前後の空白を除去 | 07 |
| `UPPER` | 文字列 | `UPPER([str]) → 全部大文字` | 07 |
| `USERNAME` | ユーザー | 現在のユーザー名 | — |
| `VAR` | 集計 | 標本分散 | 10 |
| `VARP` | 集計 | 母集団分散 | 10 |
| `WEEK` | 日付 | `WEEK([dt])` 年内の週番号 | 08 |
| `WHEN` | 論理 | `CASE x WHEN 'a' THEN ...` | 09 |
| `WINDOW_AVG` | 表計算 | ウィンドウ内平均 | 11 |
| `WINDOW_COUNT` | 表計算 | ウィンドウ内件数 | 11 |
| `WINDOW_MAX` | 表計算 | ウィンドウ内最大値 | 11 |
| `WINDOW_MEDIAN` | 表計算 | ウィンドウ内中央値 | 11 |
| `WINDOW_MIN` | 表計算 | ウィンドウ内最小値 | 11 |
| `WINDOW_STDEV` | 表計算 | ウィンドウ内標準偏差 | 11 |
| `WINDOW_SUM` | 表計算 | ウィンドウ内合計 (移動平均などに) | 11 |
| `WINDOW_VAR` | 表計算 | ウィンドウ内分散 | 11 |
| `YEAR` | 日付 | `YEAR([dt]) → 2024` | 08 |
| `ZN` | 論理 | 数値の NULL を 0 に変換 | 09 |

---

## 関連リソース

- 公式の関数リファレンス: https://help.tableau.com/current/pro/desktop/ja-jp/functions_all_categories.htm
- 各章末のクイズで関数の挙動を理解度チェックできます
