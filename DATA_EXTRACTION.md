# 演習データ作成手順 (.hyper)

本ドキュメントは、本ツールの **メンテナー向け** 手順書です。
City of Chicago Data Portal から Taxi Trips データを取得し、Tableau Desktop で抽出 (`.hyper`) に変換してリポジトリに同梱するまでの流れをまとめています。

学習者(エンドユーザー) はこの手順を実施する必要はありません。リポジトリ同梱の `.hyper` を Tableau Desktop で開くだけで演習に取り組めます。

---

## 1. 方針

| 項目 | 内容 |
|------|------|
| 取得元 | [City of Chicago Open Data Portal](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew) (Socrata) |
| 期間 | **2023 年 1 月 1 日 ~ 2023 年 12 月 31 日** |
| 取得方法 | SODA API + PowerShell スクリプト ([scripts/download_chicago_taxi.ps1](./scripts/download_chicago_taxi.ps1)) |
| 行数目標 | サンプリングして **約 100 万行前後** |
| ファイルサイズ目標 | **50 MB 以下** (GitHub の単一ファイル制限 100 MB を余裕で下回る) |
| 列 | 全列保持 (緯度経度を含む) |
| 出力先 | `docs/public/data/chicago_taxi_trips.hyper` |
| 再配布 | リポジトリに同梱 (一度作れば学習者は外部接続不要) |
| ライセンス | City of Chicago Open Data Terms (再配布可) |
| GCP / BigQuery | **使わない** (アカウント登録・課金不要) |

---

## 2. 全体の流れ

```
[Chicago Data Portal]
      │
      │ SODA API でページング取得
      ▼
[_work/chicago_taxi_2023_*.csv]   ← Git 管理対象外
      │
      │ Tableau Desktop で取り込み
      ▼
[Tableau Desktop で抽出 + サンプリング]
      │
      ▼
[docs/public/data/chicago_taxi_trips.hyper]  ← Git で配布
```

---

## 3. ステップ A: 動作確認(2023 年 1 ヶ月分)

まず小さく試してフローが通ることを確認します。所要 5〜10 分。

### A-1. ダウンロード

```powershell
cd D:\作成ツール\tableau_study_app
.\scripts\download_chicago_taxi.ps1 -Mode test
```

- 出力: `_work\chicago_taxi_2023_01.csv` (約 30〜60 万行、80〜150 MB)
- 所要 1〜3 分

ログに以下が出れば成功:

```
==== 完了 ====
Rows    : 約 350,000
Size    : 約 100 MB
```

### A-2. Tableau Desktop で取り込み

1. Tableau Desktop を起動 → 「データに接続」 → 「**テキストファイル**」
2. `_work\chicago_taxi_2023_01.csv` を選択
3. データソース画面で全列が認識されることを確認
4. **日時列の型変換**: `Trip Start Timestamp` の列ヘッダーの型アイコン(`Abc`) をクリック → 「**日時**」に変更
5. 同様に `Trip End Timestamp` も日時へ変更

### A-3. 列名のリネーム(本文と一致させる)

本ツール本文では BigQuery 風スネークケースで記述しています。Tableau のデータソース画面で列名を以下のようにリネームします。

| CSV ヘッダー(変更前) | リネーム後 |
|----------------------|-----------|
| Trip ID | trip_id |
| Taxi ID | taxi_id |
| Trip Start Timestamp | trip_start_timestamp |
| Trip End Timestamp | trip_end_timestamp |
| Trip Seconds | trip_seconds |
| Trip Miles | trip_miles |
| Pickup Census Tract | pickup_census_tract |
| Dropoff Census Tract | dropoff_census_tract |
| Pickup Community Area | pickup_community_area |
| Dropoff Community Area | dropoff_community_area |
| Fare | fare |
| Tips | tips |
| Tolls | tolls |
| Extras | extras |
| Trip Total | trip_total |
| Payment Type | payment_type |
| Company | company |
| Pickup Centroid Latitude | pickup_centroid_latitude |
| Pickup Centroid Longitude | pickup_centroid_longitude |
| Pickup Centroid Location | pickup_centroid_location |
| Dropoff Centroid Latitude | dropoff_centroid_latitude |
| Dropoff Centroid Longitude | dropoff_centroid_longitude |
| Dropoff Centroid Location | dropoff_centroid_location |

> リネーム漏れを防ぐため、リネーム後の名前を本ドキュメントから順にコピペすると確実です。

### A-4. 抽出に切替

1. データソース画面右上「接続」 → 「**抽出**」を選択
2. 任意のシートタブ(下部の `Sheet 1`) をクリック
3. 保存ダイアログが開いたら、いったん任意の場所に `chicago_taxi_2023_01.hyper` として保存
4. 「**シートが必要なフィルター追加**」のような警告が出る場合は OK で続行

### A-5. 動作確認

1. シート上で `company` を列、`SUM(trip_total)` を行にドラッグ
2. タクシー会社別の売上が棒グラフで描画されれば成功
3. ファイルサイズが妥当(数 MB〜数十 MB)であることを確認

ここまでで「Chicago Data Portal → CSV → Tableau → .hyper」のフローが動くことを確認できました。

---

## 4. ステップ B: 本番データ(2023 年全年)

### B-1. ダウンロード

```powershell
.\scripts\download_chicago_taxi.ps1 -Mode full
```

- 出力: `_work\chicago_taxi_2023_full.csv` (約 500〜700 万行、1.2〜1.8 GB)
- 所要 10〜30 分

> 通信エラーで止まった場合: スクリプト末尾に再開オプションは未実装のため、最初からやり直しになります。安定した有線または安定 Wi-Fi 環境で実行することを推奨。

> 高速化したい場合: [App Token](https://data.cityofchicago.org/profile/app_tokens) を取得して `-AppToken xxxxx` でスクリプトに渡すとレート制限が緩和されます。

### B-2. Tableau Desktop で抽出 + サンプリング

ステップ A と同じ手順で `_work\chicago_taxi_2023_full.csv` を取り込み、リネームを実施。

ただし **抽出設定でサンプリングを掛けます**:

1. データソース画面右上「接続」 → 「**抽出**」 → 「**編集**」
2. 抽出ダイアログで:
   - **集計**: オフ(全行保持)
   - **行数**: 「**サンプル**」を選択
   - **N**: **1,000,000** 行
3. 「OK」 → 任意のシートタブをクリック
4. 保存先を以下に指定:

   ```
   docs\public\data\chicago_taxi_trips.hyper
   ```

   > `_work/` ではなく、リポジトリ配下の `docs/public/data/` に保存します。

### B-3. ファイルサイズ確認

エクスプローラーで `docs/public/data/chicago_taxi_trips.hyper` のサイズを確認。

| サイズ | 対応 |
|-------|------|
| 〜 50 MB | そのまま commit OK |
| 50 〜 100 MB | そのまま commit 可だが Git LFS の検討推奨 |
| 100 MB 超 | **Git LFS が必須**。`.gitattributes` に `*.hyper filter=lfs diff=lfs merge=lfs -text` を追加 |

100 MB を超える場合はサンプル行数を絞るのも選択肢です(500,000 行に減らすなど)。

### B-4. 動作確認

1. Tableau Desktop を一度閉じ、`chicago_taxi_trips.hyper` をダブルクリック
2. 行数(100 万行付近) と全列の存在を確認
3. `company` 別 `SUM(trip_total)` を棒グラフで表示、妥当な値か目視チェック

---

## 5. 副演習データ(任意)

文字列関数や日付関数の章では、Chicago Taxi だけだとカバーしきれない部分があります。必要に応じて以下も同様に Chicago Data Portal 経由で取得します。

| 用途 | データセット | 取得元 |
|------|------------|-------|
| 文字列関数 (07章) | USA Names | Kaggle / data.gov 等で公開 |
| 日付関数 (08章) | NOAA 気象 | [NOAA Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) |
| 地理 (任意) | Austin Bikeshare | [Austin Open Data](https://data.austintexas.gov/) |

> 副演習データは必須ではありません。Chicago Taxi 1 種類でも全章カバー可能です。

---

## 6. 章ごとに必要なデータの目安

| 章 | 想定行数 | 主に使う列 |
|----|---------|-----------|
| 01. 基本概念 | 100k〜 | `company` / `trip_total` / `payment_type` |
| 02. 接続 | 100k〜 | (全列、CSV/抽出接続体験用) |
| 03. 抽出 vs ライブ | 100k〜 | (全列) |
| 04. 基本チャート | 500k〜 | 時系列 + 数値 + 地理 |
| 05. フィルター | 500k〜 | `trip_start_timestamp` / `company` |
| 06. 計算基礎 | 500k〜 | `fare` / `trip_miles` |
| 07. 数値/文字列 | 500k〜 | `payment_type` (文字列加工) |
| 08. 日付 | 1M〜 | `trip_start_timestamp` |
| 09. 論理 | 500k〜 | `trip_total` (バンド分け) |
| 10. 集計 | 500k〜 | `trip_total` / `taxi_id` |
| 11. 表計算 | 1M〜 | 時系列で推移 |
| 12. LOD | 1M〜 | `taxi_id` × `trip_total` |
| 13. パラメーター | 500k〜 | 期間切替 |
| 14. ダッシュボード | 500k〜 | KPI / 地理 / 時系列を統合 |
| 15. アクション | 500k〜 | (同上) |
| 16. パフォーマンス | 1M〜 | (全列、抽出最適化体験) |
| 17. 公開 | 任意 | 任意 |
| 18. 総合演習 | 1M〜 | 全列 |

→ 1 種類のサイズ (約 100 万行) でほぼ全章カバー可能です。

---

## 7. ファイル配布のチェックリスト

- [ ] `docs/public/data/chicago_taxi_trips.hyper` を Tableau Desktop で開けることを確認
- [ ] ファイルサイズが 100 MB 以下であることを確認
- [ ] 列名が本ツール本文の記述と一致していることを確認 (特に `company` / `trip_total` / `trip_start_timestamp`)
- [ ] サンプリングしている場合は、本文の「全件」表記を「サンプル」に修正
- [ ] 100 MB 超の場合は Git LFS を導入し、`.gitattributes` に以下を追加:
      ```
      *.hyper filter=lfs diff=lfs merge=lfs -text
      ```
- [ ] README とトップページの出典記載が「City of Chicago Open Data Portal」となっていることを確認
