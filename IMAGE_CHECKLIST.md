# スクリーンショット撮影チェックリスト

全 57 枚の画像プレースホルダ一覧です。Tableau Desktop で撮影し、指定パスに保存すれば、`scripts/replace_image_placeholders.py` を実行するだけで本文側のプレースホルダが Markdown 画像構文に自動で置き換わります。

## ワークフロー

1. 章を 1 つ選び、下記の「**保存先**」に従って Tableau Desktop でスクリーンショットを撮影
2. 撮影した画像を `docs/public/images/<章ID>/` 配下に PNG で保存
3. ある程度溜まったら以下を実行:
   ```powershell
   python scripts\replace_image_placeholders.py
   ```
4. 置き換わった章を `npm run docs:dev` で確認 → コミット
5. main へ push すれば GitHub Pages に自動反映

## チェックリスト

### 01. Tableau の基本概念 (6 枚)

- [ ] ディメンションとメジャーのペイン
  - `docs/public/images/01-basics/dim-measure-pane.png`
- [ ] 緑(連続/軸) と 青(不連続/ヘッダー) の見た目比較
  - `docs/public/images/01-basics/green-vs-blue.png`
- [ ] 列・行・フィルター・ページのシェルフ
  - `docs/public/images/01-basics/shelves.png`
- [ ] マークカード 6 シェルフの全景
  - `docs/public/images/01-basics/mark-card.png`
- [ ] アナリティクスペインのオブジェクト一覧
  - `docs/public/images/01-basics/analytics-pane.png`
- [ ] データソース 〜 ストーリーの階層図(手書きでも可)
  - `docs/public/images/01-basics/workbook-structure.png`

### 02. データ接続 (5 枚)

- [ ] スタート画面の接続ペイン
  - `docs/public/images/02-data-connection/start-page-connect.png`
- [ ] データソースタブと .hyper の接続例
  - `docs/public/images/02-data-connection/datasource-tab.png`
- [ ] リレーションシップ・結合・ユニオンの違い
  - `docs/public/images/02-data-connection/relationship-join-union.png`
- [ ] 論理レイヤー(外側) と物理レイヤー(内側)
  - `docs/public/images/02-data-connection/logical-physical-layer.png`
- [ ] データインタープリター・ピボット・分割の操作画面
  - `docs/public/images/02-data-connection/data-prep-tools.png`

### 03. 抽出 vs ライブ接続 (2 枚)

- [ ] データソースタブの「ライブ / 抽出」トグル
  - `docs/public/images/03-extract-vs-live/live-extract-toggle.png`
- [ ] 抽出の編集ダイアログ(フィルター / 集計 / サンプリング)
  - `docs/public/images/03-extract-vs-live/extract-dialog.png`

### 04. 基本チャートと VizQL (6 枚)

- [ ] 会社別売上の横棒グラフ(payment_type で積み上げ)
  - `docs/public/images/04-basic-charts/bar-chart.png`
- [ ] 月別 SUM(trip_total) の推移(折れ線)
  - `docs/public/images/04-basic-charts/line-chart.png`
- [ ] 距離 × 料金の散布図にトレンドラインを追加
  - `docs/public/images/04-basic-charts/scatter-plot.png`
- [ ] 曜日 × 時間帯の乗車件数ヒートマップ
  - `docs/public/images/04-basic-charts/heatmap.png`
- [ ] 乗車地の記号マップ(色 = 売上、サイズ = 件数)
  - `docs/public/images/04-basic-charts/map.png`
- [ ] Show Me パネルとマークタイプドロップダウン
  - `docs/public/images/04-basic-charts/show-me.png`

### 05. 集計・フィルター・並べ替え (4 枚)

- [ ] フィルター評価順のレイヤー図(手書きでも可)
  - `docs/public/images/05-filter-sort/filter-order.png`
- [ ] コンテキストに追加されたフィルター(灰色)
  - `docs/public/images/05-filter-sort/context-filter.png`
- [ ] ネスト並べ替え(payment_type の中での company 順)
  - `docs/public/images/05-filter-sort/nested-sort.png`
- [ ] クイックフィルターの各モード
  - `docs/public/images/05-filter-sort/quick-filters.png`

### 06. 計算フィールド基礎 (2 枚)

- [ ] 計算フィールドの作成メニュー
  - `docs/public/images/06-calc-basics/create-calc.png`
- [ ] 計算エディタと右側の関数リファレンス
  - `docs/public/images/06-calc-basics/calc-editor.png`

### 08. 計算関数 (2) 日付 (2 枚)

- [ ] 既定のプロパティ → 会計年度の開始
  - `docs/public/images/08-functions-date/fiscal-year.png`
- [ ] 月別売上と前年同月の並列表示例
  - `docs/public/images/08-functions-date/yoy-compare.png`

### 09. 計算関数 (3) 論理・条件式 (2 枚)

- [ ] 論理演算子の優先順位と括弧の必要性(手書きでも可)
  - `docs/public/images/09-functions-logical/operator-precedence.png`
- [ ] 料金帯バンドを色分けした棒グラフ
  - `docs/public/images/09-functions-logical/fare-band-bar.png`

### 10. 計算関数 (4) 集計関数 (2 枚)

- [ ] ATTR が `*` を返している様子
  - `docs/public/images/10-functions-aggregate/attr-asterisk.png`
- [ ] 会社別の平均値と中央値の比較
  - `docs/public/images/10-functions-aggregate/avg-vs-median.png`

### 11. 計算関数 (5) 表計算関数 (4 枚)

- [ ] 3 種類の計算(行レベル / 集計 / 表計算) の評価フロー
  - `docs/public/images/11-functions-tablecalc/calc-pipeline.png`
- [ ] 右クリック → クイック表計算メニュー
  - `docs/public/images/11-functions-tablecalc/quick-tc-menu.png`
- [ ] INDEX() で TOP 5 に絞った棒グラフ
  - `docs/public/images/11-functions-tablecalc/index-top5.png`
- [ ] 月別売上推移と 3 区間移動平均
  - `docs/public/images/11-functions-tablecalc/moving-average.png`

### 12. LOD 表現 (4 枚)

- [ ] 通常の集計と LOD の粒度の違い
  - `docs/public/images/12-lod/lod-granularity.png`
- [ ] フィルター評価順序の概念図
  - `docs/public/images/12-lod/filter-order.png`
- [ ] コホート × 経過月数のヒートマップ
  - `docs/public/images/12-lod/cohort-heatmap.png`
- [ ] FIXED と通常集計の結果比較
  - `docs/public/images/12-lod/fixed-vs-aggregate.png`

### 13. パラメーター・セット・ビン (4 枚)

- [ ] パラメーター作成ダイアログ(リスト型)
  - `docs/public/images/13-parameters-sets/parameter-dialog.png`
- [ ] 参照線にパラメーターを使った棒グラフ
  - `docs/public/images/13-parameters-sets/parameter-reference-line.png`
- [ ] セット作成ダイアログ(条件タブ)
  - `docs/public/images/13-parameters-sets/set-condition.png`
- [ ] trip_miles の度数分布(ヒストグラム)
  - `docs/public/images/13-parameters-sets/histogram.png`

### 14. ダッシュボード基礎 (4 枚)

- [ ] ダッシュボードビューの左サイドバー(シート/オブジェクト)
  - `docs/public/images/14-dashboard/sidebar.png`
- [ ] ダッシュボードサイズの選択 UI
  - `docs/public/images/14-dashboard/size-options.png`
- [ ] 水平・垂直コンテナを組み合わせた典型レイアウト
  - `docs/public/images/14-dashboard/layout-containers.png`
- [ ] デバイスデザイナーでスマホ用レイアウトを編集する画面
  - `docs/public/images/14-dashboard/device-designer.png`

### 15. アクション (3 枚)

- [ ] アクション追加ダイアログ(種類選択)
  - `docs/public/images/15-actions/action-types.png`
- [ ] フィルターアクションの設定ダイアログ
  - `docs/public/images/15-actions/filter-action.png`
- [ ] URL アクションでフィールド値を埋め込む設定
  - `docs/public/images/15-actions/url-action.png`

### 16. パフォーマンスとベストプラクティス (1 枚)

- [ ] パフォーマンスレコーダーのレポート画面
  - `docs/public/images/16-performance/performance-recorder.png`

### 17. 公開・共有 (2 枚)

- [ ] Tableau Public へのサインインダイアログ
  - `docs/public/images/17-publish/public-sign-in.png`
- [ ] プレゼンテーションモードに切り替えたダッシュボード
  - `docs/public/images/17-publish/presentation-mode.png`

### 18. 総合演習 (4 枚)

- [ ] シート設計のメモ(手描きスケッチでも可)
  - `docs/public/images/18-capstone/sheet-design-sketch.png`
- [ ] 完成イメージのワイヤーフレーム
  - `docs/public/images/18-capstone/dashboard-wireframe.png`
- [ ] 完成ダッシュボードのスクリーンショット
  - `docs/public/images/18-capstone/final-dashboard.png`
- [ ] Tableau Public 公開ページの埋め込みプレビュー
  - `docs/public/images/18-capstone/public-embed.png`

## 撮影のコツ

- **解像度**: ディスプレイ等倍で OK(過剰な高解像度は不要)
- **形式**: PNG(背景透過不要、JPG も可)
- **トリミング**: 画面全体ではなく該当部分のみに絞る。Snipping Tool / ScreenToGif の領域選択で十分
- **テキストの可読性**: ズーム時に文字が読める程度のサイズで撮影(目安: 1200x600 以上)
- **個人情報の混入**: 開いているウィンドウタイトル・ファイルパスなどに自分の名前や社内情報が映っていないか確認

## 進捗の追跡

公開後に少しずつ追加していく場合、GitHub Issues に「画像追加: 〇〇章」のようにチケット化すると進捗が見えやすくなります。
