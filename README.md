# Tableau 学習ツール (tableau_study_app)

新人向けの Tableau Desktop 学習サイトです。VitePress 製の静的サイトで、GitHub Pages 上で公開する想定です。

## 構成

- フレームワーク: [VitePress](https://vitepress.dev/) 1.x
- ホスティング: GitHub Pages（GitHub Actions により自動デプロイ）
- 演習データ: [City of Chicago Open Data Portal](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew) の Taxi Trips を抽出した `.hyper` ファイル

## ディレクトリ構成

```
.
├─ docs/
│  ├─ .vitepress/
│  │  ├─ config.ts                # サイト設定 (ナビ・サイドバー・検索 等)
│  │  └─ theme/
│  │     ├─ index.ts              # 拡張テーマ登録
│  │     ├─ QuizTrueFalse.vue     # 章末クイズ (○× 形式)
│  │     ├─ ProgressBadge.vue     # 学習進捗バッジ
│  │     └─ style.css             # カスタムスタイル
│  ├─ public/                     # 静的アセット (画像・配布データ)
│  │  ├─ data/                    # .hyper 等の配布用
│  │  └─ images/                  # スクリーンショット等
│  ├─ 00-intro/                   # 章ごとに 1 ディレクトリ
│  │  ├─ index.md
│  │  └─ quiz.json
│  ├─ 01-basics/ ... 18-capstone/
│  ├─ appendix/                   # ショートカット / よくあるエラー / 関数索引
│  ├─ glossary.md                 # 用語集
│  └─ index.md                    # トップ
├─ .github/workflows/deploy.yml   # GH Pages デプロイ
├─ package.json
└─ README.md
```

## 開発手順

### 1. 依存パッケージのインストール

```bash
npm install
```

### 2. ローカル開発サーバー

```bash
npm run docs:dev
```

ブラウザで `http://localhost:5173/tableau_study_app/` を開いてください（base パス設定により末尾が必要)。

### 3. 本番ビルド

```bash
npm run docs:build
```

ビルド成果物は `docs/.vitepress/dist/` に出力されます。

### 4. ビルド結果のプレビュー

```bash
npm run docs:preview
```

## GitHub Pages へのデプロイ

1. GitHub にリポジトリを作成し、本リポジトリを push します。
2. リポジトリ Settings → Pages → Source を "GitHub Actions" に設定します。
3. `main` ブランチへの push で `.github/workflows/deploy.yml` が走り、自動デプロイされます。
4. リポジトリ名に応じて `docs/.vitepress/config.ts` の `base` を変更してください（例: `/tableau_study_app/`）。

## コンテンツの書き方

### 章ページ

各章は `docs/<番号>-<スラッグ>/index.md` に配置します。先頭の `<div class="goal-list">` ブロックに学習目標、続いて `所要時間目安`、本文、章末クイズの順で記述します。

### クイズの追加

各章ディレクトリに `quiz.json` を作成し、章ページの末尾で `QuizTrueFalse` コンポーネントを呼び出します。

`docs/00-intro/quiz.json` の例を参考にしてください。

```md
<script setup>
import quiz from './quiz.json'
</script>

<QuizTrueFalse chapter-id="01-basics" :questions="quiz" />
```

`chapter-id` は localStorage キーの一部として使われるため、章ディレクトリ名と一致させてください。

### 画像

`docs/public/images/<章ID>/<ファイル名>.png` に配置し、Markdown から `![alt](/images/01-basics/screenshot.png)` のように参照します。

### 演習データ

`.hyper` 等の配布用データは `docs/public/data/` に配置します。100MB を超える場合は Git LFS の利用を検討してください。

## ライセンス

[MIT License](./LICENSE)
