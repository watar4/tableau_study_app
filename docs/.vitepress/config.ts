import { defineConfig } from 'vitepress'

// GitHub Pages 公開時は base をリポジトリ名に合わせて変更してください
// 例: https://<user>.github.io/tableau_study_app/ で公開する場合 → '/tableau_study_app/'
export default defineConfig({
  title: 'Tableau 学習ツール',
  description: '新人向け Tableau Desktop 学習サイト',
  lang: 'ja-JP',
  base: '/tableau_study_app/',
  lastUpdated: true,
  cleanUrls: true,
  head: [
    ['meta', { name: 'theme-color', content: '#1f6feb' }]
  ],

  themeConfig: {
    nav: [
      { text: 'ホーム', link: '/' },
      { text: '学習を始める', link: '/00-intro/' },
      { text: '用語集', link: '/glossary' }
    ],

    sidebar: [
      {
        text: 'はじめに',
        items: [
          { text: '00. はじめに / 環境準備', link: '/00-intro/' }
        ]
      },
      {
        text: '基礎編',
        items: [
          { text: '01. Tableau の基本概念', link: '/01-basics/' },
          { text: '02. データ接続', link: '/02-data-connection/' },
          { text: '03. 抽出 vs ライブ接続', link: '/03-extract-vs-live/' },
          { text: '04. 基本チャートと VizQL', link: '/04-basic-charts/' },
          { text: '05. 集計・フィルター・並べ替え', link: '/05-filter-sort/' }
        ]
      },
      {
        text: '計算フィールド編',
        items: [
          { text: '06. 計算フィールド基礎', link: '/06-calc-basics/' },
          { text: '07. 数値・文字列・型変換', link: '/07-functions-numeric-string/' },
          { text: '08. 日付関数', link: '/08-functions-date/' },
          { text: '09. 論理・条件式', link: '/09-functions-logical/' },
          { text: '10. 集計関数', link: '/10-functions-aggregate/' },
          { text: '11. 表計算関数', link: '/11-functions-tablecalc/' }
        ]
      },
      {
        text: '応用編',
        items: [
          { text: '12. LOD 表現', link: '/12-lod/' },
          { text: '13. パラメーター・セット・ビン', link: '/13-parameters-sets/' },
          { text: '14. ダッシュボード基礎', link: '/14-dashboard/' },
          { text: '15. アクション', link: '/15-actions/' },
          { text: '16. パフォーマンスとベストプラクティス', link: '/16-performance/' },
          { text: '17. 公開・共有', link: '/17-publish/' }
        ]
      },
      {
        text: '総合演習',
        items: [
          { text: '18. ダッシュボード作成', link: '/18-capstone/' }
        ]
      },
      {
        text: '付録',
        items: [
          { text: '用語集', link: '/glossary' },
          { text: 'ショートカット集', link: '/appendix/shortcuts' },
          { text: 'よくあるエラー', link: '/appendix/errors' },
          { text: '関数リファレンス索引', link: '/appendix/functions-index' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/watar4/tableau_study_app' }
    ],

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '検索',
                buttonAriaLabel: '検索'
              },
              modal: {
                noResultsText: '該当する結果が見つかりません',
                resetButtonTitle: '検索条件をリセット',
                displayDetails: '詳細を表示',
                footer: {
                  selectText: '選択',
                  navigateText: '移動',
                  closeText: '閉じる'
                }
              }
            }
          }
        }
      }
    },

    outline: { label: '本ページの目次', level: [2, 3] },
    docFooter: { prev: '前のページへ', next: '次のページへ' },
    lastUpdated: { text: '最終更新' },
    darkModeSwitchLabel: 'カラーテーマ',
    lightModeSwitchTitle: 'ライトモードに切り替え',
    darkModeSwitchTitle: 'ダークモードに切り替え',
    sidebarMenuLabel: 'メニュー',
    returnToTopLabel: 'トップへ戻る',

    editLink: {
      pattern: 'https://github.com/watar4/tableau_study_app/edit/main/docs/:path',
      text: 'このページを GitHub で編集'
    }
  }
})
