# 00. はじめに / 環境準備

<script setup>
import quiz from './quiz.json'
</script>

<div class="goal-list">
<p>学習目標</p>

- [ ] 本ツールの進め方とゴールを説明できる
- [ ] Tableau Desktop の入手・インストールが完了している
- [ ] 本ツール同梱の演習データ (.hyper) を Tableau Desktop で開ける

</div>

**所要時間目安:** 約 30 分

---

## 1. 本ツールについて

本ツールは、Tableau Desktop を初めて触る方が、業務で一通り使いこなせるようになることを目的とした学習サイトです。

- **対象**: Tableau 未経験 〜 3 ヶ月程度の新人
- **対象製品**: Tableau Desktop（Cloud / Server は概要のみ）
- **所要時間**: 合計約 20 時間
- **進め方**: 章順に解説を読み、演習を行い、章末クイズに回答してから次章へ進みます。

## 2. 学習の進め方

各章は次の構成です。

1. **学習目標**: その章を終えたときに何ができるようになるか
2. **解説**: 概念とスクリーンショットによる説明
3. **やってみよう**: 演習データを使った手を動かす練習
4. **クイズ**: 章末の ○× 形式の確認問題（即時採点）

クイズの回答状況はブラウザの localStorage に保存されるため、次回アクセス時に続きから再開できます。

## 3. Tableau Desktop の入手とインストール

以下のいずれかを利用してください。

- **試用版**: [Tableau Desktop 試用版](https://www.tableau.com/products/desktop/download)（14 日間無料）
- **学生版**: 学生・教員向け 1 年間無料ライセンス
- **業務用ライセンス**: 所属組織のライセンスを利用

インストール後、Tableau Desktop を起動して初期画面が表示されることを確認してください。

## 4. 演習データのダウンロード

本ツールでは、City of Chicago Open Data Portal の Taxi Trips データを抽出した `.hyper` を使用します。

- メイン演習データ: `chicago_taxi_trips.hyper`(シカゴ市タクシー走行記録の抽出)
- ダウンロード先: 本サイトの `/data/` 配下(リポジトリ同梱予定)
- 出典: [City of Chicago Open Data Portal](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew)

> 注: 演習データは現時点では未同梱です。後続のセットアップ作業で追加します。

## 5. 用語集・付録の紹介

学習中に分からない用語があれば、サイドバーの「付録」セクションを参照してください。

- 用語集: 主要な Tableau 用語の解説
- ショートカット集: 効率的な操作のためのキーボードショートカット
- よくあるエラー: つまずきやすいエラーと対処法
- 関数リファレンス索引: 07〜11 章で扱う関数の一覧

---

## やってみよう

1. Tableau Desktop を起動してください。
2. スタートページ左側「データに接続」から「Microsoft Excel」「テキストファイル」「その他のファイル」のいずれかが選択できることを確認してください。
3. 起動できれば準備完了です。

---

## 章末クイズ

<QuizTrueFalse chapter-id="00-intro" :questions="quiz" />
