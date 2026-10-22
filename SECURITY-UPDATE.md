# 2026-10-22 セキュリティ更新

Vue等の互換範囲内の依存を更新し、VitePressが参照するViteを修正済み6.4.4以上へoverrideしています。VitePress 1.6.4の既定指定は古いVite 5系列のため、overrideが必要です。Vue pluginの対応するVite 6系列に留め、VitePress本体のプレビュー版への移行を避けています。

`npm run docs:build` でSSR/クライアントビルドとページの事前レンダリングが成功し、npm監査は全依存で0件でした。

CIはNode.js 24.22.1、公式Actionsの完全SHA参照、最小権限、checkout資格情報の非永続化へ変更しました。
