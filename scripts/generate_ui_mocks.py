"""
Tableau UI のスキーマ風モックアップを生成する。

写真のような実画面ではなく、教科書の概念図として UI レイアウトを示す。
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "docs" / "public" / "images"

# ---- カラーパレット (Tableau 寄せ) ----
COLOR_BG = "#ffffff"
COLOR_PANEL = "#f7f7f8"
COLOR_PANEL_DARK = "#e8e8eb"
COLOR_TOOLBAR = "#2b3a4d"
COLOR_TOOLBAR_TEXT = "#f0f0f0"
COLOR_BORDER = "#c8ccd1"
COLOR_BORDER_DARK = "#9da3ab"
COLOR_TEXT = "#1f2937"
COLOR_TEXT_MUTED = "#6b7280"

COLOR_DIM_BLUE = "#3b6e8f"      # discrete (ディメンション・不連続)
COLOR_MEAS_GREEN = "#3a8e3a"    # continuous (メジャー・連続)
COLOR_PARAM_PURPLE = "#7d4f9a"
COLOR_ACCENT = "#1f6feb"
COLOR_HIGHLIGHT = "#fde68a"
COLOR_HIGHLIGHT_RED = "#fecaca"
COLOR_GRAY_SHELF = "#dbdcde"

for name in ["Yu Gothic UI", "Yu Gothic", "Meiryo", "MS Gothic"]:
    if any(f.name == name for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = name
        break

plt.rcParams.update({
    "font.size": 10,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
    "savefig.facecolor": COLOR_BG,
})


# ---- ヘルパー ----
def panel(ax, x, y, w, h, *, fill=COLOR_PANEL, edge=COLOR_BORDER, lw=1.0):
    rect = Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, linewidth=lw)
    ax.add_patch(rect)


def rounded(ax, x, y, w, h, *, fill=COLOR_PANEL, edge=COLOR_BORDER, lw=1.0, pad=0.02):
    rect = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={pad}",
                          facecolor=fill, edgecolor=edge, linewidth=lw)
    ax.add_patch(rect)


def pill(ax, x, y, w, h, text, *, color=COLOR_DIM_BLUE, fontsize=9, weight="normal"):
    """ディメンション・メジャー・パラメーターのピル(タグ)を描画。"""
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                          facecolor=color, edgecolor=color, linewidth=0)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            color="white", fontsize=fontsize, weight=weight)


def label(ax, x, y, text, *, fontsize=10, weight="normal", color=COLOR_TEXT,
          ha="center", va="center", style="normal"):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fontsize, weight=weight,
            color=color, style=style)


def setup(ax, xlim, ylim, title=None, subtitle=None):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=12, weight="bold", color=COLOR_TEXT, pad=10)
    if subtitle:
        ax.text(0.5, 1.01, subtitle, transform=ax.transAxes,
                ha="center", fontsize=9, color=COLOR_TEXT_MUTED)


def save(fig, rel):
    out = IMG / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Wrote {out.relative_to(ROOT)}")


# ============================================================
# 01-basics
# ============================================================
def ui_dim_measure_pane():
    fig, ax = plt.subplots(figsize=(6, 8))
    setup(ax, (0, 6), (0, 11), "データペイン (ディメンション / メジャー)")

    # 外枠
    panel(ax, 0.5, 0.5, 5, 10, fill="white", edge=COLOR_BORDER_DARK, lw=1.2)
    # ヘッダー
    panel(ax, 0.5, 9.6, 5, 0.9, fill=COLOR_PANEL_DARK, edge=COLOR_BORDER)
    label(ax, 3, 10.05, "Chicago Taxi Trips", fontsize=11, weight="bold")

    # 検索欄
    rounded(ax, 0.8, 9.0, 4.4, 0.4, fill="white", edge=COLOR_BORDER_DARK)
    label(ax, 1.0, 9.2, "🔍 検索", fontsize=9, color=COLOR_TEXT_MUTED, ha="left")

    # ディメンション
    panel(ax, 0.7, 7.6, 4.6, 1.2, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 3, 8.55, "ディメンション", fontsize=10, weight="bold")
    dim_fields = ["Abc  trip_id", "Abc  taxi_id", "Abc  company", "Abc  payment_type"]
    for i, f in enumerate(dim_fields):
        label(ax, 0.95, 8.25 - i * 0.18, f, fontsize=9, color=COLOR_DIM_BLUE, ha="left")

    # 日付
    panel(ax, 0.7, 6.0, 4.6, 1.4, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 3, 7.15, "日付 / 日時", fontsize=10, weight="bold")
    date_fields = ["📅  trip_start_timestamp", "📅  trip_end_timestamp"]
    for i, f in enumerate(date_fields):
        label(ax, 0.95, 6.85 - i * 0.22, f, fontsize=9, color=COLOR_DIM_BLUE, ha="left")
    # 地理
    label(ax, 0.95, 6.3, "🌐  pickup_centroid_location", fontsize=9, color=COLOR_DIM_BLUE, ha="left")

    # 区切り
    ax.plot([0.5, 5.5], [5.8, 5.8], color=COLOR_BORDER_DARK, lw=0.8, linestyle="--")

    # メジャー
    panel(ax, 0.7, 3.4, 4.6, 2.2, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 3, 5.35, "メジャー", fontsize=10, weight="bold")
    meas_fields = ["#  trip_seconds", "#  trip_miles", "#  fare", "#  tips",
                   "#  tolls", "#  extras", "#  trip_total"]
    for i, f in enumerate(meas_fields):
        label(ax, 0.95, 5.05 - i * 0.22, f, fontsize=9, color=COLOR_MEAS_GREEN, ha="left")

    # 説明 (右の吹き出し風)
    ax.annotate("← 上半分:\nディメンション\n(青)",
                xy=(5.4, 7.8), xytext=(5.5, 8.2),
                fontsize=9, color=COLOR_DIM_BLUE,
                ha="left", va="center")
    ax.annotate("← 下半分:\nメジャー\n(緑)",
                xy=(5.4, 4.5), xytext=(5.5, 4.5),
                fontsize=9, color=COLOR_MEAS_GREEN,
                ha="left", va="center")

    # 注記
    label(ax, 3, 2.7, "計算フィールド・パラメーター・セットも", fontsize=8, color=COLOR_TEXT_MUTED)
    label(ax, 3, 2.4, "このペインに追加されます", fontsize=8, color=COLOR_TEXT_MUTED)

    save(fig, "01-basics/dim-measure-pane.png")


def ui_green_vs_blue():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    setup(ax, (0, 12), (0, 6), "青 (不連続) と 緑 (連続) の見た目と挙動")

    # 青ピル
    label(ax, 3, 5.0, "青 = 不連続 (Discrete)", fontsize=11, weight="bold", color=COLOR_DIM_BLUE)
    pill(ax, 1.5, 4.0, 3.0, 0.6, "company", color=COLOR_DIM_BLUE)
    label(ax, 3, 3.4, "→ ヘッダー (カテゴリ別の枠) として表示", fontsize=9, color=COLOR_TEXT_MUTED)
    # ヘッダーのモック
    for i, n in enumerate(["Flash Cab", "Sun Taxi", "City Service"]):
        panel(ax, 0.7 + i * 1.4, 2.2, 1.4, 0.5, fill=COLOR_PANEL_DARK, edge=COLOR_BORDER)
        label(ax, 1.4 + i * 1.4, 2.45, n, fontsize=8)
    label(ax, 3, 1.6, "(個別の値ごとにブロックが並ぶ)", fontsize=8, color=COLOR_TEXT_MUTED)

    # 緑ピル
    label(ax, 9, 5.0, "緑 = 連続 (Continuous)", fontsize=11, weight="bold", color=COLOR_MEAS_GREEN)
    pill(ax, 7.5, 4.0, 3.0, 0.6, "SUM(trip_total)", color=COLOR_MEAS_GREEN)
    label(ax, 9, 3.4, "→ 連続軸 (数直線) として表示", fontsize=9, color=COLOR_TEXT_MUTED)
    # 軸のモック
    ax.plot([6.8, 11.2], [2.5, 2.5], color=COLOR_BORDER_DARK, lw=1.5)
    for x in [6.8, 7.9, 9.0, 10.1, 11.2]:
        ax.plot([x, x], [2.45, 2.55], color=COLOR_BORDER_DARK, lw=1.5)
    for x, v in zip([6.8, 7.9, 9.0, 10.1, 11.2], ["0", "1M", "2M", "3M", "4M"]):
        label(ax, x, 2.2, v, fontsize=8, color=COLOR_TEXT_MUTED)
    label(ax, 9, 1.6, "(連続した目盛りを持つ軸が引かれる)", fontsize=8, color=COLOR_TEXT_MUTED)

    label(ax, 6, 0.7, "ディメンション/メジャーとは独立した属性。フィールド右クリックで切り替え可能。",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "01-basics/green-vs-blue.png")


def ui_shelves():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    setup(ax, (0, 14), (0, 8), "シェルフ: 列・行・フィルター・ページ")

    # ページ
    label(ax, 1.5, 7.3, "ページ", fontsize=9, color=COLOR_TEXT_MUTED)
    panel(ax, 0.5, 6.7, 2.0, 0.5, fill=COLOR_GRAY_SHELF, edge=COLOR_BORDER)

    # フィルター
    label(ax, 1.5, 6.3, "フィルター", fontsize=9, color=COLOR_TEXT_MUTED)
    panel(ax, 0.5, 5.7, 2.0, 0.5, fill=COLOR_GRAY_SHELF, edge=COLOR_BORDER)
    pill(ax, 0.6, 5.75, 1.8, 0.4, "payment_type", color=COLOR_DIM_BLUE, fontsize=8)

    # マーク (略)
    label(ax, 1.5, 5.3, "マーク", fontsize=9, color=COLOR_TEXT_MUTED)
    panel(ax, 0.5, 0.8, 2.0, 4.3, fill=COLOR_PANEL, edge=COLOR_BORDER)
    items = ["▼ 自動", "■ 色", "□ サイズ", "T ラベル", "i 詳細", "💡 ツールヒント"]
    for i, t in enumerate(items):
        label(ax, 1.5, 4.7 - i * 0.55, t, fontsize=9)

    # 列 (Columns)
    label(ax, 3.0, 7.3, "列", fontsize=10, weight="bold", color=COLOR_TEXT)
    panel(ax, 2.8, 6.7, 10.7, 0.5, fill=COLOR_GRAY_SHELF, edge=COLOR_BORDER)
    pill(ax, 3.0, 6.78, 1.8, 0.4, "company", color=COLOR_DIM_BLUE, fontsize=8)

    # 行 (Rows)
    label(ax, 3.0, 6.3, "行", fontsize=10, weight="bold", color=COLOR_TEXT)
    panel(ax, 2.8, 5.7, 10.7, 0.5, fill=COLOR_GRAY_SHELF, edge=COLOR_BORDER)
    pill(ax, 3.0, 5.78, 1.8, 0.4, "SUM(trip_total)", color=COLOR_MEAS_GREEN, fontsize=8)

    # ビュー領域 (棒グラフのモック)
    panel(ax, 2.8, 0.8, 10.7, 4.6, fill="white", edge=COLOR_BORDER)
    label(ax, 8.0, 5.05, "ビュー", fontsize=9, color=COLOR_TEXT_MUTED)
    # シンプルな棒グラフ
    for i, h in enumerate([3.5, 3.0, 2.4, 2.0, 1.6, 1.3, 1.0, 0.8, 0.6, 0.5]):
        x = 3.2 + i * 1.0
        ax.add_patch(Rectangle((x, 1.2), 0.7, h, facecolor=COLOR_DIM_BLUE, edgecolor="none"))

    save(fig, "01-basics/shelves.png")


def ui_mark_card():
    fig, ax = plt.subplots(figsize=(5.5, 7.5))
    setup(ax, (0, 5), (0, 10), "マークカード (6 シェルフ)")

    panel(ax, 0.3, 0.5, 4.4, 9, fill=COLOR_PANEL, edge=COLOR_BORDER, lw=1.2)
    label(ax, 2.5, 9.05, "マーク", fontsize=11, weight="bold")

    # マークタイプ
    rounded(ax, 0.6, 8.0, 3.8, 0.7, fill="white", edge=COLOR_BORDER)
    label(ax, 1.4, 8.35, "▼", fontsize=11, ha="left", color=COLOR_ACCENT)
    label(ax, 2.5, 8.35, "自動 (棒)", fontsize=10, color=COLOR_TEXT)

    shelves = [
        ("色 (Color)", "■", "ディメンション → 系列色 / メジャー → グラデーション"),
        ("サイズ (Size)", "□", "バブル等で件数を表現"),
        ("ラベル (Label)", "T", "マーク上に値を表示"),
        ("詳細 (Detail)", "i", "粒度を細かくする (ビューに表示しない)"),
        ("ツールヒント", "💡", "マウスオーバー時の補足表示"),
        ("形状 (Shape)", "▲", "マークタイプ=形状 のときのみ有効"),
    ]
    for i, (name, icon, desc) in enumerate(shelves):
        y = 7.2 - i * 1.05
        rounded(ax, 0.6, y, 3.8, 0.85, fill="white", edge=COLOR_BORDER)
        # アイコン
        ax.add_patch(Rectangle((0.75, y + 0.2), 0.45, 0.45, facecolor=COLOR_PANEL_DARK, edgecolor=COLOR_BORDER))
        label(ax, 0.98, y + 0.42, icon, fontsize=11)
        label(ax, 1.4, y + 0.6, name, fontsize=9, weight="bold", ha="left")
        label(ax, 1.4, y + 0.25, desc, fontsize=7, color=COLOR_TEXT_MUTED, ha="left")

    save(fig, "01-basics/mark-card.png")


def ui_analytics_pane():
    fig, ax = plt.subplots(figsize=(6, 7.5))
    setup(ax, (0, 6), (0, 11), "アナリティクスペイン")

    panel(ax, 0.5, 0.5, 5, 10, fill="white", edge=COLOR_BORDER_DARK, lw=1.2)
    panel(ax, 0.5, 9.6, 5, 0.9, fill=COLOR_PANEL_DARK)
    label(ax, 3, 10.05, "アナリティクス", fontsize=11, weight="bold")

    sections = [
        ("サマリー", ["定数線", "平均線", "中央値とトリプル分位"]),
        ("モデル", ["平均と 95% 信頼区間", "中央値と四分位範囲", "ボックスプロット", "合計", "分布バンド", "予測"]),
        ("カスタム", ["リファレンス線", "リファレンスバンド", "分布バンド", "ボックスプロット", "トレンドライン", "予測", "クラスター"]),
    ]
    y = 9.3
    for name, items in sections:
        y -= 0.2
        label(ax, 0.7, y, name, fontsize=10, weight="bold", ha="left", color=COLOR_ACCENT)
        for it in items:
            y -= 0.35
            # アイコン
            ax.add_patch(Rectangle((0.85, y - 0.1), 0.25, 0.25, facecolor=COLOR_PANEL_DARK, edgecolor=COLOR_BORDER))
            label(ax, 1.25, y, it, fontsize=9, ha="left")
        y -= 0.2

    label(ax, 3, 0.85, "ドラッグでビューに分析オブジェクトを追加",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "01-basics/analytics-pane.png")


# ============================================================
# 02-data-connection
# ============================================================
def ui_start_page_connect():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    setup(ax, (0, 12), (0, 8), "スタート画面 - データに接続")

    # 左ペイン
    panel(ax, 0.3, 0.5, 4.0, 7.0, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 2.3, 7.2, "データに接続", fontsize=11, weight="bold")

    label(ax, 0.5, 6.6, "ファイル", fontsize=10, weight="bold", ha="left", color=COLOR_ACCENT)
    files = ["Microsoft Excel", "テキストファイル", "Microsoft Access",
             "JSON ファイル", "PDF ファイル", "空間ファイル", "統計ファイル",
             "その他のファイル (.hyper など)"]
    for i, f in enumerate(files):
        label(ax, 0.7, 6.2 - i * 0.30, f, fontsize=9, ha="left")

    label(ax, 0.5, 3.6, "サーバー", fontsize=10, weight="bold", ha="left", color=COLOR_ACCENT)
    servers = ["Tableau Server", "Microsoft SQL Server", "MySQL",
               "PostgreSQL", "Google BigQuery", "Snowflake",
               "Amazon Redshift", "その他..."]
    for i, s in enumerate(servers):
        label(ax, 0.7, 3.2 - i * 0.30, s, fontsize=9, ha="left")

    # 右側 (最近開いたファイル)
    panel(ax, 4.5, 0.5, 7.2, 7.0, fill="white", edge=COLOR_BORDER)
    label(ax, 8.1, 7.2, "最近開いたファイル", fontsize=11, weight="bold")
    for i, name in enumerate(["chicago_taxi_trips.hyper", "売上分析.twbx", "顧客マスタ.twbx"]):
        y = 6.5 - i * 0.7
        rounded(ax, 4.8, y - 0.2, 6.6, 0.55, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, 5.0, y + 0.05, "📊", fontsize=12, ha="left")
        label(ax, 5.4, y + 0.05, name, fontsize=10, ha="left")

    # 矢印で「クリック箇所」をハイライト
    ax.add_patch(FancyArrowPatch((0.5, 5.6), (3.5, 5.6),
                                 arrowstyle="<-", color=COLOR_ACCENT, lw=2, mutation_scale=14))
    label(ax, 1.9, 5.85, "★ .hyper はここから", fontsize=9, color=COLOR_ACCENT, weight="bold")

    save(fig, "02-data-connection/start-page-connect.png")


def ui_datasource_tab():
    fig, ax = plt.subplots(figsize=(12, 7))
    setup(ax, (0, 14), (0, 8), "データソースタブ")

    # 上部タイトルバー
    panel(ax, 0.3, 7.0, 13.4, 0.8, fill=COLOR_TOOLBAR, edge=COLOR_TOOLBAR)
    label(ax, 0.5, 7.4, "📁  chicago_taxi_trips", fontsize=11, color=COLOR_TOOLBAR_TEXT, ha="left", weight="bold")
    rounded(ax, 11.8, 7.15, 1.8, 0.5, fill="white", edge=COLOR_BORDER)
    label(ax, 12.0, 7.4, "接続:", fontsize=8, color=COLOR_TEXT, ha="left")
    label(ax, 12.55, 7.4, "● 抽出", fontsize=8, color=COLOR_MEAS_GREEN, ha="left", weight="bold")

    # 左サイドバー
    panel(ax, 0.3, 0.4, 2.5, 6.5, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 1.55, 6.6, "接続", fontsize=10, weight="bold")
    rounded(ax, 0.5, 6.0, 2.1, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 0.65, 6.2, "chicago_taxi_trips.hyper", fontsize=8, ha="left")
    label(ax, 1.55, 5.4, "シート", fontsize=10, weight="bold")
    for i, t in enumerate(["Extract"]):
        rounded(ax, 0.5, 5.0 - i * 0.5, 2.1, 0.35, fill="white", edge=COLOR_BORDER)
        label(ax, 0.65, 5.17 - i * 0.5, "▫  " + t, fontsize=8, ha="left")

    # 中央: キャンバス (テーブル)
    panel(ax, 3.0, 5.5, 10.7, 1.4, fill="white", edge=COLOR_BORDER)
    label(ax, 8.3, 6.6, "論理レイヤー (リレーションシップ キャンバス)", fontsize=9, color=COLOR_TEXT_MUTED)
    rounded(ax, 7.3, 5.8, 2.4, 0.6, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 8.5, 6.1, "Extract", fontsize=10, color="white", weight="bold")

    # 下部: フィールド表
    panel(ax, 3.0, 0.4, 10.7, 4.9, fill="white", edge=COLOR_BORDER)
    label(ax, 3.2, 5.05, "データのプレビュー (最初の 1000 行)", fontsize=9,
          ha="left", color=COLOR_TEXT_MUTED)
    # ヘッダー行
    panel(ax, 3.0, 4.5, 10.7, 0.4, fill=COLOR_PANEL_DARK, edge=COLOR_BORDER)
    headers = ["#  trip_seconds", "Abc  trip_id", "Abc  company", "📅  trip_start", "#  trip_total", "Abc  payment_type"]
    col_w = 10.7 / len(headers)
    for i, h in enumerate(headers):
        label(ax, 3.0 + i * col_w + 0.1, 4.7, h, fontsize=8, ha="left", color=COLOR_TEXT)
    # データ行 (ダミー)
    sample_rows = [
        ["857", "37a210...", "City Service", "2023-01-10 09:15", "11.83", "Mobile"],
        ["691", "842eef...", "City Service", "2023-01-05 18:15", "12.30", "Mobile"],
        ["1560", "ad3c29...", "U Taxicab", "2023-01-08 20:15", "52.50", "Credit Card"],
        ["780", "d261da...", "Sun Taxi", "2023-01-12 13:30", "16.75", "Cash"],
    ]
    for j, row in enumerate(sample_rows):
        for i, v in enumerate(row):
            label(ax, 3.0 + i * col_w + 0.1, 4.2 - j * 0.4, v, fontsize=8, ha="left")

    save(fig, "02-data-connection/datasource-tab.png")


def ui_data_prep_tools():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    setup(ax, (0, 12), (0, 7), "データの前処理: インタープリター / ピボット / 分割")

    # 3 つの機能を並べる
    items = [
        (1.0, "データインタープリター",
         ["Excel/PDF/HTML の", "結合セル・タイトル行を", "自動で解釈・整形"],
         "Before: バラバラ → After: 表形式"),
        (5.0, "ピボット (Pivot)",
         ["横持ち (列が並ぶ) を", "縦持ち (1 列 + 値) に", "変換"],
         "[Q1][Q2][Q3] → [Quarter][Value]"),
        (9.0, "分割 (Split)",
         ["1 つの列を区切り文字で", "分割し、新しい列を作る", "(自動分割もあり)"],
         "Full Name → 姓 / 名"),
    ]
    for x, title, lines, before_after in items:
        rounded(ax, x - 1.3, 1.5, 2.6, 4.5, fill=COLOR_PANEL, edge=COLOR_BORDER, lw=1.2)
        label(ax, x, 5.5, title, fontsize=11, weight="bold", color=COLOR_ACCENT)
        for i, line in enumerate(lines):
            label(ax, x, 4.8 - i * 0.4, line, fontsize=9)
        rounded(ax, x - 1.15, 1.7, 2.3, 0.7, fill="white", edge=COLOR_BORDER)
        label(ax, x, 2.05, before_after, fontsize=8, color=COLOR_TEXT_MUTED)

    label(ax, 6, 0.8,
          "いずれもデータソース画面 (右クリックメニューや上部ツールバー) から利用可能",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "02-data-connection/data-prep-tools.png")


# ============================================================
# 03-extract-vs-live
# ============================================================
def ui_live_extract_toggle():
    fig, ax = plt.subplots(figsize=(8, 4))
    setup(ax, (0, 10), (0, 5), "接続の「ライブ / 抽出」トグル")

    panel(ax, 0.5, 0.5, 9, 4, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 5, 4.0, "接続", fontsize=11, weight="bold")

    # ライブ
    rounded(ax, 1.0, 2.3, 3.6, 1.2, fill="white", edge=COLOR_BORDER)
    label(ax, 1.6, 3.1, "○", fontsize=14, color=COLOR_BORDER_DARK, ha="left")
    label(ax, 2.1, 3.1, "ライブ", fontsize=11, weight="bold", ha="left", color=COLOR_TEXT)
    label(ax, 2.0, 2.7, "都度クエリ・最新データ", fontsize=8, color=COLOR_TEXT_MUTED, ha="left")

    # 抽出 (selected)
    rounded(ax, 5.2, 2.3, 3.6, 1.2, fill=COLOR_HIGHLIGHT, edge=COLOR_ACCENT, lw=2)
    label(ax, 5.8, 3.1, "●", fontsize=14, color=COLOR_ACCENT, ha="left")
    label(ax, 6.3, 3.1, "抽出", fontsize=11, weight="bold", ha="left", color=COLOR_ACCENT)
    label(ax, 6.2, 2.7, ".hyper に取り込み・高速", fontsize=8, color=COLOR_TEXT_MUTED, ha="left")

    label(ax, 8.5, 2.0, "編集...", fontsize=9, color=COLOR_ACCENT, ha="right",
          weight="bold")

    label(ax, 5, 1.3, "右上の「接続」セクションで切替。「編集」リンクで抽出設定が開く。",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "03-extract-vs-live/live-extract-toggle.png")


def ui_extract_dialog():
    fig, ax = plt.subplots(figsize=(9, 7))
    setup(ax, (0, 10), (0, 8.5), "抽出データの編集ダイアログ")

    # ダイアログ枠
    panel(ax, 0.5, 0.5, 9, 7.8, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 7.6, 9, 0.7, fill=COLOR_PANEL_DARK)
    label(ax, 5, 7.95, "抽出データ", fontsize=11, weight="bold")

    # データの保存形式
    label(ax, 0.8, 7.2, "データの保存形式", fontsize=10, weight="bold", ha="left")
    label(ax, 1.0, 6.9, "● 論理テーブル (推奨)", fontsize=9, ha="left")
    label(ax, 1.0, 6.65, "○ 複数のテーブル", fontsize=9, ha="left", color=COLOR_TEXT_MUTED)

    # フィルター
    label(ax, 0.8, 6.2, "フィルター", fontsize=10, weight="bold", ha="left")
    panel(ax, 0.8, 4.7, 8.4, 1.3, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 1.0, 5.6, "(なし)", fontsize=9, ha="left", color=COLOR_TEXT_MUTED)
    rounded(ax, 0.95, 4.85, 0.9, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 1.4, 5.05, "追加...", fontsize=8)

    # 集計
    label(ax, 0.8, 4.3, "集計", fontsize=10, weight="bold", ha="left")
    label(ax, 1.0, 4.0, "□ 可視ディメンションのデータを集計", fontsize=9, ha="left")

    # 行数
    label(ax, 0.8, 3.5, "行数", fontsize=10, weight="bold", ha="left")
    label(ax, 1.0, 3.2, "○ すべての行", fontsize=9, ha="left", color=COLOR_TEXT_MUTED)
    label(ax, 1.0, 2.95, "● サンプル", fontsize=9, ha="left")
    label(ax, 1.5, 2.7, "○ 最初の", fontsize=9, ha="left", color=COLOR_TEXT_MUTED)
    rounded(ax, 2.6, 2.55, 1.0, 0.35, fill=COLOR_HIGHLIGHT, edge=COLOR_ACCENT)
    label(ax, 3.1, 2.72, "1,000,000", fontsize=9, weight="bold")
    label(ax, 3.7, 2.7, "行", fontsize=9, ha="left")

    # 抽出のオプション
    label(ax, 0.8, 2.1, "オプション", fontsize=10, weight="bold", ha="left")
    label(ax, 1.0, 1.8, "□ 増分更新を有効化", fontsize=9, ha="left")

    # ボタン
    rounded(ax, 6.0, 0.8, 1.3, 0.5, fill="white", edge=COLOR_BORDER)
    label(ax, 6.65, 1.05, "キャンセル", fontsize=9)
    rounded(ax, 7.5, 0.8, 1.5, 0.5, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 8.25, 1.05, "OK", fontsize=10, color="white", weight="bold")

    save(fig, "03-extract-vs-live/extract-dialog.png")


# ============================================================
# 04-basic-charts
# ============================================================
def ui_show_me():
    fig, ax = plt.subplots(figsize=(6.5, 7.5))
    setup(ax, (0, 6), (0, 10), "Show Me パネル")

    panel(ax, 0.3, 0.5, 5.4, 9.5, fill="white", edge=COLOR_BORDER_DARK, lw=1.2)
    label(ax, 3, 9.4, "Show Me", fontsize=11, weight="bold")

    # 4 列 × 6 行 のチャートサムネ
    chart_names = [
        "▫ テキスト", "| 棒", "≡ 棒(積上)", "Ⅲ 棒(並列)",
        "/  折れ線", "//  折れ線(個別)", "▪ 散布図", "≣ ヒートマップ",
        "● 円", "▥ ツリーマップ", "🌐 シンボルマップ", "🌐 塗り分けマップ",
        "∿ 面グラフ", "≣ ハイライト表", "📊 二重軸", "○ パッキングバブル",
    ]
    for i, name in enumerate(chart_names):
        col = i % 4
        row = i // 4
        x = 0.5 + col * 1.30
        y = 8.3 - row * 1.30
        # selected (棒は条件を満たすので青枠ハイライト)
        if name == "| 棒":
            rounded(ax, x, y, 1.20, 1.1, fill=COLOR_HIGHLIGHT, edge=COLOR_ACCENT, lw=2)
        else:
            rounded(ax, x, y, 1.20, 1.1, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, x + 0.6, y + 0.7, name.split()[0], fontsize=16)
        label(ax, x + 0.6, y + 0.25, name.split()[1] if len(name.split()) > 1 else "",
              fontsize=8)

    # 説明欄
    panel(ax, 0.5, 1.3, 5.0, 1.8, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 3, 2.85, "現在の選択フィールド", fontsize=9, weight="bold")
    label(ax, 3, 2.55, "1 ディメンション + 1 メジャー", fontsize=8, color=COLOR_TEXT_MUTED)
    label(ax, 3, 2.15, "→ 棒・並列棒・積み上げ棒・", fontsize=8, color=COLOR_ACCENT)
    label(ax, 3, 1.90, "テキスト表 が利用可能", fontsize=8, color=COLOR_ACCENT)
    label(ax, 3, 1.55, "条件を満たさないチャートは灰色", fontsize=8, color=COLOR_TEXT_MUTED)

    save(fig, "04-basic-charts/show-me.png")


# ============================================================
# 05-filter-sort
# ============================================================
def ui_context_filter():
    fig, ax = plt.subplots(figsize=(7, 5))
    setup(ax, (0, 10), (0, 7), "コンテキストに追加されたフィルター")

    label(ax, 5, 6.5, "フィルター シェルフ", fontsize=10, weight="bold", color=COLOR_TEXT)

    # 通常フィルター
    pill(ax, 1.0, 5.4, 3.0, 0.7, "company", color=COLOR_DIM_BLUE)
    label(ax, 2.5, 5.0, "通常のディメンションフィルター", fontsize=8, color=COLOR_TEXT_MUTED)

    # コンテキストフィルター (灰色)
    pill(ax, 1.0, 4.0, 3.0, 0.7, "payment_type", color="#737373")
    label(ax, 2.5, 3.6, "コンテキストフィルター (灰色)", fontsize=8, color="#737373", weight="bold")

    # 矢印で説明
    ax.add_patch(FancyArrowPatch((4.2, 4.35), (5.5, 4.35),
                                 arrowstyle="->", color=COLOR_ACCENT, lw=2, mutation_scale=14))

    panel(ax, 5.7, 3.5, 3.8, 2.0, fill=COLOR_HIGHLIGHT, edge=COLOR_ACCENT)
    label(ax, 7.6, 5.0, "コンテキストの効果", fontsize=10, weight="bold", color=COLOR_ACCENT)
    label(ax, 7.6, 4.5, "・他のディメンションフィルターより", fontsize=8)
    label(ax, 7.6, 4.2, "  先に評価される", fontsize=8)
    label(ax, 7.6, 3.9, "・上位 N フィルターの母集合になる", fontsize=8)
    label(ax, 7.6, 3.6, "・パフォーマンス改善になる場合あり", fontsize=8)

    label(ax, 5, 2.5, "右クリック → 「コンテキストに追加」 で昇格", fontsize=9, color=COLOR_TEXT_MUTED)
    label(ax, 5, 1.7, "ピルが青→灰色に変わる", fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "05-filter-sort/context-filter.png")


def ui_nested_sort():
    fig, ax = plt.subplots(figsize=(10, 6))
    setup(ax, (0, 12), (0, 8), "ネスト並べ替え: payment_type の中での company 順")

    # 行シェルフ
    label(ax, 1, 7.3, "行 シェルフ:", fontsize=10, ha="left", color=COLOR_TEXT_MUTED)
    pill(ax, 2.6, 7.15, 2.5, 0.5, "payment_type", color=COLOR_DIM_BLUE)
    label(ax, 5.3, 7.4, "+", fontsize=14, color=COLOR_TEXT_MUTED)
    pill(ax, 5.7, 7.15, 2.0, 0.5, "company", color=COLOR_DIM_BLUE)
    label(ax, 8.0, 7.4, "←  SUM(trip_total) で並べ替え", fontsize=9, color=COLOR_TEXT_MUTED, ha="left")

    # 結果の表
    panel(ax, 0.5, 0.8, 11, 5.5, fill="white", edge=COLOR_BORDER)
    pays = [("Cash", ["Flash Cab (45k)", "Sun Taxi (38k)", "City Service (21k)"]),
            ("Credit Card", ["Taxi Affiliation (62k)", "Globe Taxi (40k)", "5 Star Taxi (15k)"]),
            ("Mobile", ["Sun Taxi (29k)", "Flash Cab (24k)", "City Service (12k)"])]

    y = 5.7
    for pay, items in pays:
        # payment_type ヘッダー
        panel(ax, 0.6, y - 0.4, 10.8, 0.5, fill=COLOR_PANEL_DARK)
        label(ax, 0.8, y - 0.15, pay, fontsize=10, weight="bold", ha="left", color=COLOR_DIM_BLUE)
        y -= 0.55
        # 棒グラフ
        for i, txt in enumerate(items):
            name, val = txt.rsplit(" (", 1)
            val = int(val.rstrip(")k"))
            width = val / 70 * 9
            ax.add_patch(Rectangle((2.5, y - 0.18), width, 0.3, facecolor=COLOR_TABLEAU_BLUE if False else "#4e79a7"))
            label(ax, 2.4, y - 0.03, name, fontsize=8, ha="right")
            label(ax, 2.55 + width, y - 0.03, f"{val}k", fontsize=8, ha="left", color=COLOR_TEXT_MUTED)
            y -= 0.4
        y -= 0.2

    label(ax, 6, 0.3,
          "「会社の売上順」は payment_type の中での順序であって、全体の順序ではない",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "05-filter-sort/nested-sort.png")


def ui_quick_filters():
    fig, ax = plt.subplots(figsize=(11, 7))
    setup(ax, (0, 13), (0, 8.5), "クイックフィルター: モードの一覧")

    modes = [
        (0.5, 6.0, "単一値 (リスト)",
         ["○ All", "● Cash", "○ Credit Card", "○ Mobile"]),
        (4.5, 6.0, "単一値 (ドロップダウン)",
         ["[ Cash               ▼ ]", "", "", ""]),
        (8.5, 6.0, "単一値 (スライダー)",
         ["━━━━●━━━━━━━━", "  Cash", "", ""]),
        (0.5, 3.0, "複数値 (リスト)",
         ["■ Cash", "■ Credit Card", "□ Mobile", "□ Prcard"]),
        (4.5, 3.0, "複数値 (ドロップダウン)",
         ["[ Cash, Credit Card  ▼ ]", "", "", ""]),
        (8.5, 3.0, "範囲スライダー (連続値)",
         ["━━━━━●━━━━━━━●━", "  $5         $100", "", ""]),
    ]

    for x, y, name, lines in modes:
        panel(ax, x, y - 2.3, 3.8, 2.5, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, x + 1.9, y + 0.05, name, fontsize=10, weight="bold")
        for i, line in enumerate(lines):
            label(ax, x + 0.2, y - 0.3 - i * 0.35, line, fontsize=9, ha="left")

    label(ax, 6.5, 0.5,
          "フィルター右上の ▼ から各モードを切り替え。値が多いときはドロップダウン、選ばせたいときはリスト等。",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "05-filter-sort/quick-filters.png")


# ============================================================
# 06-calc-basics
# ============================================================
def ui_create_calc():
    fig, ax = plt.subplots(figsize=(6, 5))
    setup(ax, (0, 8), (0, 7), "計算フィールドの作成 (右クリックメニュー)")

    # データペイン背景
    panel(ax, 0.5, 0.5, 4, 6, fill="white", edge=COLOR_BORDER)
    label(ax, 2.5, 6.0, "データペイン", fontsize=10, weight="bold")
    fields = ["Abc  company", "Abc  payment_type", "#  trip_total", "#  trip_miles"]
    for i, f in enumerate(fields):
        c = COLOR_DIM_BLUE if "Abc" in f else COLOR_MEAS_GREEN
        label(ax, 0.7, 5.5 - i * 0.4, f, fontsize=9, ha="left", color=c)

    # 右クリックメニュー
    panel(ax, 4.8, 1.2, 3.0, 4.0, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    menu_items = [
        ("作成", True),
        ("  計算フィールド...", True),
        ("  パラメーター...", False),
        ("  グループ...", False),
        ("  セット...", False),
        ("  ビン...", False),
        ("変換", False),
        ("  ディメンションに変換", False),
        ("  メジャーに変換", False),
    ]
    for i, (item, highlight) in enumerate(menu_items):
        y = 5.0 - i * 0.4
        if highlight:
            panel(ax, 4.85, y - 0.16, 2.9, 0.32, fill=COLOR_HIGHLIGHT, edge=COLOR_HIGHLIGHT)
            color = COLOR_ACCENT
            weight = "bold"
        else:
            color = COLOR_TEXT
            weight = "normal"
        label(ax, 5.0, y, item, fontsize=9, ha="left", color=color, weight=weight)

    # 矢印
    ax.add_patch(FancyArrowPatch((4.5, 4.0), (4.7, 4.6),
                                 arrowstyle="->", color=COLOR_ACCENT, lw=2, mutation_scale=14))

    label(ax, 4, 0.8, "フィールドを右クリック → 「作成」 → 「計算フィールド...」",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "06-calc-basics/create-calc.png")


def ui_calc_editor():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    setup(ax, (0, 12), (0, 8), "計算エディタ")

    # ダイアログ枠
    panel(ax, 0.5, 0.5, 11, 7.3, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 7.1, 11, 0.7, fill=COLOR_PANEL_DARK)
    label(ax, 6, 7.45, "計算フィールド", fontsize=11, weight="bold")

    # 名前
    label(ax, 0.8, 6.7, "名前:", fontsize=10, ha="left")
    rounded(ax, 1.6, 6.55, 5, 0.45, fill="white", edge=COLOR_BORDER)
    label(ax, 1.8, 6.78, "チップ率", fontsize=10, ha="left")

    # 式エリア
    panel(ax, 0.8, 2.3, 7.5, 4.0, fill="white", edge=COLOR_BORDER)
    expr_lines = [
        ("// チップ率 = チップ ÷ 基本料金", COLOR_TEXT_MUTED, "italic"),
        ("IF [fare] > 0 THEN", COLOR_TEXT, "normal"),
        ("    [tips] / [fare]", COLOR_TEXT, "normal"),
        ("ELSE 0", COLOR_TEXT, "normal"),
        ("END", COLOR_TEXT, "normal"),
    ]
    for i, (line, c, st) in enumerate(expr_lines):
        label(ax, 1.0, 5.8 - i * 0.55, line, fontsize=10, ha="left",
              color=c, style=st)

    # ステータス
    label(ax, 0.8, 1.95, "✓ 計算は有効です。", fontsize=9, ha="left", color=COLOR_MEAS_GREEN)

    # 関数リファレンス (右側)
    panel(ax, 8.4, 2.3, 3.1, 4.6, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 9.95, 6.65, "関数", fontsize=10, weight="bold")
    rounded(ax, 8.55, 6.0, 2.8, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 8.7, 6.2, "🔍 関数を検索", fontsize=8, color=COLOR_TEXT_MUTED, ha="left")
    funcs = ["ABS", "AVG", "CONTAINS", "DATEDIFF", "DATEPART",
             "IF", "IFNULL", "INDEX", "LEN", "MAX", "ROUND"]
    for i, f in enumerate(funcs):
        label(ax, 8.6, 5.6 - i * 0.32, f, fontsize=9, ha="left",
              color=COLOR_ACCENT if f == "IF" else COLOR_TEXT)

    # ボタン
    rounded(ax, 9.0, 0.8, 1.1, 0.45, fill="white", edge=COLOR_BORDER)
    label(ax, 9.55, 1.02, "キャンセル", fontsize=9)
    rounded(ax, 10.3, 0.8, 1.0, 0.45, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 10.8, 1.02, "OK", fontsize=10, color="white", weight="bold")

    save(fig, "06-calc-basics/calc-editor.png")


# ============================================================
# 08-functions-date
# ============================================================
def ui_fiscal_year():
    fig, ax = plt.subplots(figsize=(8, 5.5))
    setup(ax, (0, 10), (0, 7), "日付プロパティ: 会計年度の開始")

    panel(ax, 0.5, 0.5, 9, 6, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 5.9, 9, 0.6, fill=COLOR_PANEL_DARK)
    label(ax, 5, 6.2, "日付プロパティ", fontsize=11, weight="bold")

    # 既定の日付形式
    label(ax, 0.8, 5.3, "既定の日付形式:", fontsize=10, ha="left")
    rounded(ax, 3.5, 5.15, 4.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 3.7, 5.35, "自動 (yyyy/mm/dd hh:mm)  ▼", fontsize=9, ha="left")

    # 既定のカレンダー
    label(ax, 0.8, 4.5, "既定のカレンダー:", fontsize=10, ha="left")
    label(ax, 3.7, 4.35, "● 標準のカレンダー", fontsize=9, ha="left")
    label(ax, 3.7, 4.1, "○ ISO 8601 週ベースのカレンダー", fontsize=9, ha="left", color=COLOR_TEXT_MUTED)

    # 週の開始
    label(ax, 0.8, 3.5, "週の開始:", fontsize=10, ha="left")
    rounded(ax, 3.5, 3.35, 3.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 3.7, 3.55, "月曜日  ▼", fontsize=9, ha="left")

    # 会計年度の開始 (highlighted)
    panel(ax, 0.6, 1.6, 8.8, 1.4, fill=COLOR_HIGHLIGHT, edge=COLOR_ACCENT, lw=1.5)
    label(ax, 0.8, 2.7, "会計年度の開始:", fontsize=10, weight="bold", ha="left", color=COLOR_ACCENT)
    rounded(ax, 3.5, 2.55, 3.0, 0.4, fill="white", edge=COLOR_ACCENT)
    label(ax, 3.7, 2.75, "4月  ▼", fontsize=9, ha="left", weight="bold")
    label(ax, 0.8, 2.1, "↑ 4 月を会計年度の開始月に設定すると、", fontsize=8, ha="left", color=COLOR_TEXT_MUTED)
    label(ax, 0.8, 1.85, "  YEAR / QUARTER / DATEPART('year', ...) が会計年度ベースで動く", fontsize=8, ha="left", color=COLOR_TEXT_MUTED)

    # ボタン
    rounded(ax, 8.0, 0.7, 1.2, 0.45, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 8.6, 0.93, "OK", fontsize=10, color="white", weight="bold")

    save(fig, "08-functions-date/fiscal-year.png")


# ============================================================
# 10-functions-aggregate
# ============================================================
def ui_attr_asterisk():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    setup(ax, (0, 12), (0, 7), "ATTR で `*` が返るケース")

    # テーブル
    label(ax, 6, 6.2, "ビュー: company 別の ATTR([payment_type])", fontsize=11, weight="bold")
    headers = ["company", "件数", "ATTR([payment_type])"]
    rows = [
        ("Flash Cab", "12,345", "*", True),
        ("Sun Taxi", "8,901", "*", True),
        ("City Service", "5,678", "Cash", False),
        ("Globe Taxi", "3,210", "Credit Card", False),
        ("U Taxicab", "1,098", "*", True),
    ]

    # ヘッダー
    panel(ax, 0.8, 4.6, 10.4, 0.5, fill=COLOR_PANEL_DARK, edge=COLOR_BORDER)
    col_widths = [4.0, 2.5, 3.9]
    cx = 0.8
    for h, w in zip(headers, col_widths):
        label(ax, cx + w / 2, 4.85, h, fontsize=10, weight="bold")
        cx += w

    # データ行
    y = 4.1
    for company, cnt, val, ast in rows:
        cx = 0.8
        for txt, w in zip([company, cnt, val], col_widths):
            panel(ax, cx, y - 0.25, w, 0.5, fill="white" if not ast else "white", edge=COLOR_BORDER)
            color = "#dc2626" if txt == "*" else COLOR_TEXT
            weight = "bold" if txt == "*" else "normal"
            label(ax, cx + w / 2, y, txt, fontsize=10, color=color, weight=weight)
            cx += w
        y -= 0.5

    # 説明
    panel(ax, 0.8, 0.7, 10.4, 1.2, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 6, 1.55, "ATTR は「集計後のディメンション粒度で値が一意なら値、複数あれば *」を返す",
          fontsize=10, weight="bold")
    label(ax, 6, 1.15, "Flash Cab は Cash / Credit Card など複数の payment_type があるため * になる",
          fontsize=9, color=COLOR_TEXT_MUTED)
    label(ax, 6, 0.85, "City Service は (例として) すべて Cash だったため値 'Cash' が返る",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "10-functions-aggregate/attr-asterisk.png")


# ============================================================
# 11-functions-tablecalc
# ============================================================
def ui_quick_tc_menu():
    fig, ax = plt.subplots(figsize=(7, 5.5))
    setup(ax, (0, 10), (0, 8), "クイック表計算メニュー (右クリック)")

    # ピル
    pill(ax, 1.0, 6.7, 3.0, 0.7, "SUM(trip_total)", color=COLOR_MEAS_GREEN)

    # 右クリックメニュー (簡易)
    panel(ax, 4.5, 1.5, 5.0, 5.8, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    menu = [
        ("メジャー (合計)", False),
        ("ディメンション", False),
        ("属性", False),
        ("不連続", False),
        ("─ 区切り ─", None),
        ("クイック表計算  ▶", True),
        ("─ 区切り ─", None),
        ("ラベルの編集...", False),
        ("計算を編集...", False),
        ("削除", False),
    ]
    y = 6.9
    for item, highlight in menu:
        if item.startswith("─"):
            ax.plot([4.6, 9.4], [y, y], color=COLOR_BORDER, lw=0.5)
            y -= 0.25
            continue
        if highlight:
            panel(ax, 4.55, y - 0.18, 4.9, 0.34, fill=COLOR_HIGHLIGHT, edge=COLOR_HIGHLIGHT)
            color = COLOR_ACCENT
            weight = "bold"
        else:
            color = COLOR_TEXT
            weight = "normal"
        label(ax, 4.7, y, item, fontsize=9, ha="left", color=color, weight=weight)
        y -= 0.42

    # サブメニュー
    panel(ax, 8.7, 0.6, 4.0, 4.5, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    label(ax, 8.85, 4.7, "クイック表計算:", fontsize=8, ha="left", color=COLOR_TEXT_MUTED)
    submenu = ["累計", "差", "差(変化率)", "前年比", "順位", "パーセンタイル", "移動平均", "YTD 合計", "YoY 成長"]
    for i, s in enumerate(submenu):
        label(ax, 8.95, 4.4 - i * 0.42, s, fontsize=9, ha="left")

    save(fig, "11-functions-tablecalc/quick-tc-menu.png")


# ============================================================
# 13-parameters-sets
# ============================================================
def ui_parameter_dialog():
    fig, ax = plt.subplots(figsize=(8, 7))
    setup(ax, (0, 10), (0, 8.5), "パラメーターの作成 (リスト型)")

    panel(ax, 0.5, 0.5, 9, 7.8, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 7.6, 9, 0.7, fill=COLOR_PANEL_DARK)
    label(ax, 5, 7.95, "パラメーターの作成", fontsize=11, weight="bold")

    # 名前
    label(ax, 0.8, 7.2, "名前:", fontsize=10, ha="left")
    rounded(ax, 2.0, 7.05, 5.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.2, 7.25, "上位 N", fontsize=10, ha="left")

    # データ型
    label(ax, 0.8, 6.45, "データ型:", fontsize=10, ha="left")
    rounded(ax, 2.0, 6.30, 3.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.2, 6.50, "整数  ▼", fontsize=10, ha="left")

    # 現在値
    label(ax, 0.8, 5.70, "現在値:", fontsize=10, ha="left")
    rounded(ax, 2.0, 5.55, 2.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.2, 5.75, "5", fontsize=10, ha="left")

    # 表示形式
    label(ax, 0.8, 4.95, "表示形式:", fontsize=10, ha="left")
    rounded(ax, 2.0, 4.80, 3.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.2, 5.0, "自動", fontsize=10, ha="left")

    # 許容値
    label(ax, 0.8, 4.20, "許容値:", fontsize=10, ha="left")
    label(ax, 2.0, 4.05, "○ すべて   ● リスト   ○ 範囲", fontsize=10, ha="left")

    # リスト
    panel(ax, 2.0, 1.3, 6.4, 2.5, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 2.2, 3.55, "値", fontsize=9, ha="left", weight="bold")
    label(ax, 5.0, 3.55, "表示テキスト", fontsize=9, ha="left", weight="bold")
    values = [("3", "上位 3 社"), ("5", "上位 5 社"), ("10", "上位 10 社"), ("20", "上位 20 社")]
    for i, (v, t) in enumerate(values):
        label(ax, 2.2, 3.20 - i * 0.4, v, fontsize=9, ha="left")
        label(ax, 5.0, 3.20 - i * 0.4, t, fontsize=9, ha="left")

    rounded(ax, 7.5, 0.8, 1.5, 0.45, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 8.25, 1.025, "OK", fontsize=10, color="white", weight="bold")

    save(fig, "13-parameters-sets/parameter-dialog.png")


def ui_parameter_reference_line():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    setup(ax, (0, 12), (0, 7), "パラメーターを参照線に使う")

    # ビューエリア
    panel(ax, 0.5, 0.5, 9, 6, fill="white", edge=COLOR_BORDER)

    # 棒グラフ
    companies = ["Flash Cab", "Taxi Aff.", "Sun Taxi", "City Svc", "Globe T."]
    values = [5.2, 4.8, 3.2, 2.8, 1.0]  # millions
    threshold = 3.5

    for i, (c, v) in enumerate(zip(companies, values)):
        color = COLOR_MEAS_GREEN if v >= threshold else "#4e79a7"
        ax.add_patch(Rectangle((1.0 + i * 1.6, 0.8), 1.3, v * 0.8,
                               facecolor=color, edgecolor="none"))
        label(ax, 1.65 + i * 1.6, 0.6, c, fontsize=8)

    # 参照線 (パラメーター値)
    y_ref = 0.8 + threshold * 0.8
    ax.plot([0.7, 9.3], [y_ref, y_ref], color="#e15759", lw=2, linestyle="--")
    label(ax, 9.3, y_ref + 0.15, "目標値 = $3.5M", fontsize=9, color="#e15759",
          ha="right", weight="bold")

    # パラメーターコントロール (右側)
    panel(ax, 10.0, 2.5, 1.8, 3.5, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 10.9, 5.7, "目標値", fontsize=10, weight="bold", color=COLOR_PARAM_PURPLE)
    label(ax, 10.9, 5.4, "(パラメーター)", fontsize=8, color=COLOR_TEXT_MUTED)
    # スライダー
    ax.plot([10.2, 11.6], [4.5, 4.5], color=COLOR_BORDER, lw=2)
    ax.add_patch(patches.Circle((11.0, 4.5), 0.1, facecolor=COLOR_PARAM_PURPLE))
    label(ax, 10.9, 4.1, "$3.5M", fontsize=10, weight="bold", color=COLOR_PARAM_PURPLE)
    label(ax, 10.9, 3.7, "↕ ドラッグで変更", fontsize=7, color=COLOR_TEXT_MUTED)

    label(ax, 5, 6.5, "パラメーターの値を参照線にバインド → 動的なしきい値ビュー",
          fontsize=11, weight="bold")

    save(fig, "13-parameters-sets/parameter-reference-line.png")


def ui_set_condition():
    fig, ax = plt.subplots(figsize=(8, 7))
    setup(ax, (0, 10), (0, 8.5), "セットの作成 (条件タブ)")

    panel(ax, 0.5, 0.5, 9, 7.8, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 7.6, 9, 0.7, fill=COLOR_PANEL_DARK)
    label(ax, 5, 7.95, "セットの作成 ─ company", fontsize=11, weight="bold")

    # タブ
    tabs = ["全般", "条件", "上位"]
    for i, t in enumerate(tabs):
        x = 0.8 + i * 1.5
        if t == "条件":
            panel(ax, x, 6.75, 1.4, 0.45, fill="white", edge=COLOR_ACCENT, lw=2)
            label(ax, x + 0.7, 6.97, t, fontsize=10, weight="bold", color=COLOR_ACCENT)
        else:
            panel(ax, x, 6.75, 1.4, 0.45, fill=COLOR_PANEL_DARK, edge=COLOR_BORDER)
            label(ax, x + 0.7, 6.97, t, fontsize=10, color=COLOR_TEXT_MUTED)

    # 条件タブの内容
    label(ax, 0.8, 6.20, "● フィールド指定", fontsize=10, ha="left", weight="bold")

    label(ax, 1.0, 5.65, "フィールド:", fontsize=9, ha="left")
    rounded(ax, 2.5, 5.50, 3.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.7, 5.70, "trip_total", fontsize=9, ha="left", color=COLOR_MEAS_GREEN)

    label(ax, 1.0, 5.10, "集計:", fontsize=9, ha="left")
    rounded(ax, 2.5, 4.95, 1.8, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.7, 5.15, "合計", fontsize=9, ha="left")

    label(ax, 1.0, 4.55, "演算子:", fontsize=9, ha="left")
    rounded(ax, 2.5, 4.40, 1.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.7, 4.60, ">=", fontsize=9, ha="left")

    label(ax, 1.0, 4.0, "値:", fontsize=9, ha="left")
    rounded(ax, 2.5, 3.85, 2.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.7, 4.05, "100,000", fontsize=9, ha="left")

    # 説明
    panel(ax, 0.8, 1.6, 8.4, 1.5, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 5, 2.75, "条件: SUM(trip_total) >= 100,000 となる company が IN", fontsize=10, weight="bold")
    label(ax, 5, 2.35, "→ TOP セールス会社のセットを動的に維持", fontsize=9, color=COLOR_TEXT_MUTED)
    label(ax, 5, 1.95, "→ IN / OUT のブール値として計算フィールドや色で利用可能", fontsize=9, color=COLOR_TEXT_MUTED)

    rounded(ax, 7.5, 0.7, 1.5, 0.45, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 8.25, 0.925, "OK", fontsize=10, color="white", weight="bold")

    save(fig, "13-parameters-sets/set-condition.png")


# ============================================================
# 14-dashboard
# ============================================================
def ui_dashboard_sidebar():
    fig, ax = plt.subplots(figsize=(5.5, 7.5))
    setup(ax, (0, 5), (0, 10), "ダッシュボードの左サイドバー")

    panel(ax, 0.3, 0.5, 4.4, 9.2, fill="white", edge=COLOR_BORDER_DARK, lw=1.2)

    # サイズセクション
    label(ax, 2.5, 9.4, "サイズ", fontsize=10, weight="bold")
    rounded(ax, 0.55, 8.7, 3.95, 0.55, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 0.7, 8.95, "自動 (デスクトップ)  ▼", fontsize=9, ha="left")

    # シート一覧
    label(ax, 2.5, 8.2, "シート", fontsize=10, weight="bold")
    sheets = ["KPI ボード", "月次推移", "会社別シェア", "乗車地マップ", "明細テーブル"]
    for i, s in enumerate(sheets):
        rounded(ax, 0.55, 7.6 - i * 0.5, 3.95, 0.42, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, 0.75, 7.81 - i * 0.5, f"▫  {s}", fontsize=9, ha="left")

    # 区切り
    ax.plot([0.55, 4.55], [4.85, 4.85], color=COLOR_BORDER, lw=0.8)

    # オブジェクト
    label(ax, 2.5, 4.5, "オブジェクト", fontsize=10, weight="bold")
    objects = ["▫  水平", "▭  垂直", "T  テキスト", "🖼️  画像", "🌐  Web ページ",
               "≣  空白", "🔘  ナビゲーション", "⬇️  ダウンロード"]
    for i, o in enumerate(objects):
        rounded(ax, 0.55, 3.95 - i * 0.42, 3.95, 0.36, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, 0.75, 4.13 - i * 0.42, o, fontsize=9, ha="left")

    save(fig, "14-dashboard/sidebar.png")


def ui_size_options():
    fig, ax = plt.subplots(figsize=(7, 5))
    setup(ax, (0, 10), (0, 7), "ダッシュボードのサイズ設定")

    panel(ax, 0.5, 0.5, 9, 6, fill="white", edge=COLOR_BORDER_DARK, lw=1.2)
    label(ax, 5, 6.2, "サイズ", fontsize=11, weight="bold")

    # オプション
    options = [
        ("● 固定サイズ", "1000 × 800 px", "画面サイズに依らず常に同じサイズ", True),
        ("○ 自動", "ウィンドウに合わせて", "閲覧者の画面サイズで自動調整", False),
        ("○ レンジ", "幅 800〜1200 px", "最小・最大の範囲を指定", False),
    ]
    for i, (label_text, dim, desc, sel) in enumerate(options):
        y = 5.0 - i * 1.5
        if sel:
            panel(ax, 0.7, y - 0.5, 8.6, 1.2, fill=COLOR_HIGHLIGHT, edge=COLOR_ACCENT, lw=1.5)
        label(ax, 0.9, y + 0.4, label_text, fontsize=11, ha="left", weight="bold" if sel else "normal",
              color=COLOR_ACCENT if sel else COLOR_TEXT)
        label(ax, 4.5, y + 0.4, dim, fontsize=10, ha="left", color=COLOR_TEXT)
        label(ax, 0.9, y - 0.1, desc, fontsize=9, ha="left", color=COLOR_TEXT_MUTED)

    save(fig, "14-dashboard/size-options.png")


def ui_layout_containers():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    setup(ax, (0, 14), (0, 8), "レイアウトコンテナ: 水平 + 垂直の組み合わせ")

    # 全体外枠
    panel(ax, 0.5, 0.5, 13, 7.0, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    label(ax, 7.0, 7.2, "ダッシュボード (水平コンテナで左右に分割)",
          fontsize=10, weight="bold", color=COLOR_ACCENT)

    # 左カラム (垂直コンテナ)
    panel(ax, 1.0, 0.8, 6.0, 5.8, fill=COLOR_PANEL, edge=COLOR_ACCENT, lw=1.5)
    label(ax, 4.0, 6.3, "垂直コンテナ", fontsize=9, color=COLOR_ACCENT, weight="bold")
    # 中の 3 シート
    for i, name in enumerate(["KPI ボード", "月次推移", "明細テーブル"]):
        y = 5.5 - i * 1.7
        panel(ax, 1.3, y - 1.2, 5.4, 1.4, fill="white", edge=COLOR_BORDER)
        label(ax, 4.0, y - 0.5, name, fontsize=10, weight="bold")
        label(ax, 4.0, y - 0.85, "(シート)", fontsize=8, color=COLOR_TEXT_MUTED)

    # 右カラム (垂直コンテナ)
    panel(ax, 7.5, 0.8, 5.5, 5.8, fill=COLOR_PANEL, edge=COLOR_ACCENT, lw=1.5)
    label(ax, 10.25, 6.3, "垂直コンテナ", fontsize=9, color=COLOR_ACCENT, weight="bold")
    panel(ax, 7.8, 3.0, 4.9, 3.0, fill="white", edge=COLOR_BORDER)
    label(ax, 10.25, 4.5, "乗車地マップ", fontsize=10, weight="bold")
    panel(ax, 7.8, 1.0, 4.9, 1.7, fill="white", edge=COLOR_BORDER)
    label(ax, 10.25, 1.85, "会社別シェア", fontsize=10, weight="bold")
    label(ax, 10.25, 1.50, "(シート)", fontsize=8, color=COLOR_TEXT_MUTED)

    save(fig, "14-dashboard/layout-containers.png")


def ui_device_designer():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    setup(ax, (0, 14), (0, 8), "デバイスデザイナー")

    # 上部タブ
    devices = [("デスクトップ", True), ("タブレット", False), ("スマホ", False)]
    for i, (d, sel) in enumerate(devices):
        x = 1.0 + i * 2.5
        if sel:
            panel(ax, x, 7.0, 2.3, 0.6, fill="white", edge=COLOR_ACCENT, lw=2)
            label(ax, x + 1.15, 7.30, d, fontsize=10, weight="bold", color=COLOR_ACCENT)
        else:
            panel(ax, x, 7.0, 2.3, 0.6, fill=COLOR_PANEL_DARK, edge=COLOR_BORDER)
            label(ax, x + 1.15, 7.30, d, fontsize=10, color=COLOR_TEXT_MUTED)

    label(ax, 11.5, 7.30, "+ デバイスレイアウトの追加", fontsize=9, color=COLOR_ACCENT, ha="left")

    # デスクトップレイアウト
    panel(ax, 1.0, 0.8, 7.0, 6.0, fill="white", edge=COLOR_BORDER_DARK, lw=1.2)
    label(ax, 4.5, 6.4, "デスクトップ用レイアウト (固定 1200×800)", fontsize=10, weight="bold")
    panel(ax, 1.3, 5.5, 6.4, 0.6, fill=COLOR_ACCENT)
    label(ax, 4.5, 5.8, "タイトル", fontsize=10, color="white", weight="bold")
    # KPI
    for i in range(4):
        panel(ax, 1.3 + i * 1.65, 4.5, 1.5, 0.8, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, 2.05 + i * 1.65, 4.9, "KPI", fontsize=9)
    # 2 charts
    panel(ax, 1.3, 2.5, 3.0, 1.8, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 2.8, 3.4, "推移", fontsize=10)
    panel(ax, 4.5, 2.5, 3.2, 1.8, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 6.1, 3.4, "構成", fontsize=10)
    panel(ax, 1.3, 0.95, 6.4, 1.4, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 4.5, 1.65, "マップ", fontsize=10)

    # スマホレイアウト (右側、縦長)
    panel(ax, 9.0, 0.8, 2.0, 6.0, fill="white", edge=COLOR_BORDER_DARK, lw=1.2)
    label(ax, 10.0, 6.4, "スマホ用 (縦)", fontsize=10, weight="bold")
    panel(ax, 9.2, 5.6, 1.6, 0.5, fill=COLOR_ACCENT)
    label(ax, 10.0, 5.85, "タイトル", fontsize=8, color="white")
    # KPI 縦並び
    for i in range(4):
        panel(ax, 9.2, 5.0 - i * 0.55, 1.6, 0.45, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, 10.0, 5.22 - i * 0.55, f"KPI {i+1}", fontsize=8)
    panel(ax, 9.2, 2.0, 1.6, 0.7, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 10.0, 2.35, "推移", fontsize=9)
    panel(ax, 9.2, 1.0, 1.6, 0.8, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 10.0, 1.4, "マップ", fontsize=9)

    label(ax, 12.5, 4.5, "共通シートを\nデバイスごとに\n再配置 / 取捨選択",
          fontsize=9, color=COLOR_TEXT_MUTED, ha="left", va="center")

    save(fig, "14-dashboard/device-designer.png")


# ============================================================
# 15-actions
# ============================================================
def ui_action_types():
    fig, ax = plt.subplots(figsize=(7, 5))
    setup(ax, (0, 10), (0, 7), "アクション追加ダイアログ (種類選択)")

    panel(ax, 0.5, 0.5, 9, 6, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 5.9, 9, 0.6, fill=COLOR_PANEL_DARK)
    label(ax, 5, 6.2, "アクションの追加", fontsize=11, weight="bold")

    types = [
        ("🔍  フィルター...", "選択値を他シートのフィルターに", True),
        ("✨  ハイライト...", "選択と一致するマークを強調", False),
        ("🔗  URL に移動...", "外部 URL を開く", False),
        ("⚙️  パラメーターの変更...", "ユーザー操作でパラメーター値を更新", False),
        ("📦  セット値の変更...", "セットのメンバーを動的更新", False),
        ("📑  シートに移動...", "別ダッシュボード/シートへ遷移", False),
    ]
    y = 5.2
    for label_text, desc, highlight in types:
        if highlight:
            panel(ax, 0.7, y - 0.32, 8.6, 0.65, fill=COLOR_HIGHLIGHT, edge=COLOR_ACCENT)
        label(ax, 0.9, y, label_text, fontsize=10, ha="left",
              weight="bold" if highlight else "normal",
              color=COLOR_ACCENT if highlight else COLOR_TEXT)
        label(ax, 4.5, y, desc, fontsize=9, ha="left", color=COLOR_TEXT_MUTED)
        y -= 0.75

    save(fig, "15-actions/action-types.png")


def ui_filter_action():
    fig, ax = plt.subplots(figsize=(9, 7))
    setup(ax, (0, 10), (0, 8.5), "フィルターアクションの設定")

    panel(ax, 0.5, 0.5, 9, 7.8, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 7.6, 9, 0.7, fill=COLOR_PANEL_DARK)
    label(ax, 5, 7.95, "フィルターアクションの編集", fontsize=11, weight="bold")

    # 名前
    label(ax, 0.8, 7.2, "名前:", fontsize=10, ha="left")
    rounded(ax, 2.0, 7.05, 5.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.2, 7.25, "会社別 → 月次トレンド", fontsize=10, ha="left")

    # ソースシート
    label(ax, 0.8, 6.4, "ソースシート:", fontsize=10, ha="left")
    rounded(ax, 2.8, 6.25, 4.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 3.0, 6.45, "▫ 会社別シェア", fontsize=10, ha="left")

    # 実行対象
    label(ax, 0.8, 5.65, "実行対象:", fontsize=10, ha="left")
    label(ax, 2.8, 5.65, "○ ホバー   ● 選択   ○ メニュー", fontsize=10, ha="left")

    # ターゲットシート
    label(ax, 0.8, 4.9, "ターゲットシート:", fontsize=10, ha="left")
    panel(ax, 2.8, 4.30, 4.8, 0.95, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 3.0, 5.05, "■ ▫ 月次トレンド", fontsize=9, ha="left")
    label(ax, 3.0, 4.75, "■ ▫ 明細テーブル", fontsize=9, ha="left")
    label(ax, 3.0, 4.45, "□ ▫ KPI ボード", fontsize=9, ha="left", color=COLOR_TEXT_MUTED)

    # 選択をクリアした結果
    label(ax, 0.8, 3.7, "選択をクリア:", fontsize=10, ha="left")
    label(ax, 2.8, 3.7, "○ フィルター結果を保持   ● すべての値を表示   ○ すべて除外",
          fontsize=9, ha="left")

    # 対象フィールド
    label(ax, 0.8, 3.0, "対象フィールド:", fontsize=10, ha="left")
    label(ax, 2.8, 3.0, "● すべてのフィールド   ○ 選択したフィールド",
          fontsize=9, ha="left")

    # 説明
    panel(ax, 0.8, 1.2, 8.4, 1.3, fill=COLOR_HIGHLIGHT, edge=COLOR_ACCENT)
    label(ax, 5, 2.15, "ソースシートでクリックしたマークの値を、",
          fontsize=10)
    label(ax, 5, 1.85, "ターゲットシートのフィルターとして適用する",
          fontsize=10, weight="bold", color=COLOR_ACCENT)
    label(ax, 5, 1.5, "選択解除で全件表示に戻る",
          fontsize=9, color=COLOR_TEXT_MUTED)

    rounded(ax, 7.5, 0.6, 1.5, 0.45, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 8.25, 0.825, "OK", fontsize=10, color="white", weight="bold")

    save(fig, "15-actions/filter-action.png")


def ui_url_action():
    fig, ax = plt.subplots(figsize=(9, 6))
    setup(ax, (0, 10), (0, 7.5), "URL アクション: フィールド値を URL に埋め込み")

    panel(ax, 0.5, 0.5, 9, 6.8, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 6.6, 9, 0.7, fill=COLOR_PANEL_DARK)
    label(ax, 5, 6.95, "URL アクションの編集", fontsize=11, weight="bold")

    label(ax, 0.8, 6.2, "名前:", fontsize=10, ha="left")
    rounded(ax, 2.0, 6.05, 5.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 2.2, 6.25, "会社名で検索", fontsize=10, ha="left")

    label(ax, 0.8, 5.4, "URL:", fontsize=10, ha="left")
    rounded(ax, 0.8, 4.7, 8.4, 0.5, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 1.0, 4.95, "https://www.google.com/search?q=", fontsize=10, ha="left")
    pill(ax, 5.45, 4.75, 1.4, 0.4, "<company>", color=COLOR_DIM_BLUE, fontsize=9)
    label(ax, 6.95, 4.95, "+taxi+chicago", fontsize=10, ha="left")

    # プレースホルダ説明
    panel(ax, 0.8, 2.5, 8.4, 1.9, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 5, 4.0, "プレースホルダ", fontsize=10, weight="bold")
    label(ax, 1.0, 3.55, "<フィールド名>", fontsize=9, ha="left", color=COLOR_ACCENT)
    label(ax, 4.0, 3.55, "クリックされたマークのフィールド値", fontsize=9, ha="left")
    label(ax, 1.0, 3.20, "<パラメーター名>", fontsize=9, ha="left", color=COLOR_ACCENT)
    label(ax, 4.0, 3.20, "パラメーターの現在値", fontsize=9, ha="left")
    label(ax, 1.0, 2.85, "<URL Encoded フィールド名>", fontsize=9, ha="left", color=COLOR_ACCENT)
    label(ax, 4.0, 2.85, "URL エンコード済みの値", fontsize=9, ha="left")

    # トリガー
    label(ax, 0.8, 2.05, "実行対象:", fontsize=10, ha="left")
    label(ax, 2.5, 2.05, "○ ホバー   ○ 選択   ● メニュー",
          fontsize=10, ha="left")
    label(ax, 0.8, 1.7, "(メニューは誤クリック防止に推奨)", fontsize=8, ha="left", color=COLOR_TEXT_MUTED)

    rounded(ax, 7.5, 0.8, 1.5, 0.45, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 8.25, 1.025, "OK", fontsize=10, color="white", weight="bold")

    save(fig, "15-actions/url-action.png")


# ============================================================
# 16-performance
# ============================================================
def ui_performance_recorder():
    fig, ax = plt.subplots(figsize=(11, 6))
    setup(ax, (0, 14), (0, 8), "パフォーマンスレコーダー レポート")

    panel(ax, 0.3, 0.4, 13.4, 7.2, fill="white", edge=COLOR_BORDER_DARK, lw=1.2)
    panel(ax, 0.3, 7.2, 13.4, 0.6, fill=COLOR_PANEL_DARK)
    label(ax, 7, 7.5, "パフォーマンスの概要", fontsize=11, weight="bold")

    # X 軸 (時間)
    label(ax, 7, 6.7, "イベントのタイムライン (秒)", fontsize=10, weight="bold")
    ax.plot([1, 13], [1.0, 1.0], color=COLOR_BORDER, lw=1)
    for s in [0, 1, 2, 3, 4, 5]:
        x = 1 + s * 2.4
        ax.plot([x, x], [0.95, 1.05], color=COLOR_BORDER)
        label(ax, x, 0.7, f"{s}.0", fontsize=8, color=COLOR_TEXT_MUTED)

    # イベント (Gantt-like)
    events = [
        (1.5, 2.0, "クエリの実行 (シート 1)", COLOR_TABLEAU_BLUE := "#4e79a7"),
        (3.5, 0.8, "クエリのコンパイル", "#76b7b2"),
        (4.3, 0.5, "ジオコーディング", "#59a14f"),
        (4.8, 1.2, "クエリの実行 (シート 2)", COLOR_TABLEAU_BLUE),
        (6.0, 0.4, "接続", "#edc948"),
        (6.4, 2.6, "レイアウトのコンピューティング", "#f28e2c"),
    ]
    rows = [5.5, 4.7, 3.9, 3.1, 2.3, 1.5]
    for (start, dur, name, color), y in zip(events, rows):
        x1 = 1 + start * 2.4
        w = dur * 2.4
        ax.add_patch(Rectangle((x1, y - 0.18), w, 0.36, facecolor=color, edgecolor="white"))
        label(ax, x1 - 0.1, y, name, fontsize=8, ha="right")
        label(ax, x1 + w + 0.1, y, f"{dur:.1f}秒", fontsize=8, ha="left", color=COLOR_TEXT_MUTED)

    label(ax, 7, 0.2,
          "棒の長いイベントがボトルネック。クエリが長い → データソース/計算の見直し、レイアウトが長い → シート数/マーク数の削減",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "16-performance/performance-recorder.png")


# ============================================================
# 17-publish
# ============================================================
def ui_public_sign_in():
    fig, ax = plt.subplots(figsize=(6, 5))
    setup(ax, (0, 8), (0, 7), "Tableau Public サインインダイアログ")

    panel(ax, 0.5, 0.5, 7, 6, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    panel(ax, 0.5, 5.7, 7, 0.8, fill=COLOR_ACCENT)
    label(ax, 4, 6.1, "Tableau Public へのサインイン", fontsize=11,
          weight="bold", color="white")

    # メール
    label(ax, 0.8, 5.0, "メールアドレス:", fontsize=10, ha="left")
    rounded(ax, 0.8, 4.4, 6.4, 0.45, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 1.0, 4.62, "watarai.tappei@example.com", fontsize=10, ha="left",
          color=COLOR_TEXT_MUTED)

    # パスワード
    label(ax, 0.8, 3.85, "パスワード:", fontsize=10, ha="left")
    rounded(ax, 0.8, 3.25, 6.4, 0.45, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 1.0, 3.48, "••••••••••••", fontsize=10, ha="left", color=COLOR_TEXT_MUTED)

    # ボタン
    rounded(ax, 0.8, 2.2, 6.4, 0.6, fill=COLOR_ACCENT, edge=COLOR_ACCENT)
    label(ax, 4, 2.5, "サインイン", fontsize=11, color="white", weight="bold")

    # アカウント作成リンク
    label(ax, 4, 1.5, "アカウントがありませんか?  新規作成",
          fontsize=9, color=COLOR_ACCENT)

    # 注記
    label(ax, 4, 0.8, "Tableau Public にサインインしてワークブックを公開",
          fontsize=8, color=COLOR_TEXT_MUTED)

    save(fig, "17-publish/public-sign-in.png")


def ui_presentation_mode():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    setup(ax, (0, 14), (0, 8), "プレゼンテーションモード (F7)")

    # フルスクリーンのダッシュボード(編集 UI なし)
    panel(ax, 0.3, 0.4, 13.4, 7.4, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)

    # タイトル
    panel(ax, 0.5, 6.8, 13.0, 0.8, fill=COLOR_ACCENT)
    label(ax, 7.0, 7.2, "シカゴ タクシー利用 ダッシュボード (2023)",
          fontsize=13, color="white", weight="bold")

    # KPI 行
    for i, k in enumerate(["総売上", "乗車回数", "平均距離", "平均料金"]):
        x = 0.7 + i * 3.3
        panel(ax, x, 5.3, 3.1, 1.2, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, x + 1.55, 6.05, k, fontsize=10, weight="bold")
        label(ax, x + 1.55, 5.65, "$XX,XXX,XXX", fontsize=14, weight="bold", color=COLOR_ACCENT)

    # 2 つのチャート
    panel(ax, 0.7, 2.7, 6.2, 2.3, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 3.8, 4.7, "月次売上推移", fontsize=11, weight="bold")
    pts_x = [1.3, 1.9, 2.6, 3.3, 4.0, 4.7, 5.4, 6.1, 6.8]
    pts_y = [3.2, 3.4, 3.7, 3.5, 3.9, 4.1, 3.8, 4.2, 4.0]
    ax.plot(pts_x, pts_y, color=COLOR_ACCENT, lw=2.5, marker="o", markersize=5)

    panel(ax, 7.4, 2.7, 6.0, 2.3, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 10.4, 4.7, "会社別シェア", fontsize=11, weight="bold")
    for i in range(5):
        ax.add_patch(Rectangle((7.7, 4.3 - i * 0.32), 4.5 - i * 0.6, 0.25,
                               facecolor=COLOR_ACCENT, edgecolor="none"))

    # マップ
    panel(ax, 0.7, 0.6, 13.0, 1.9, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 7.0, 2.1, "乗車地マップ", fontsize=11, weight="bold")
    import numpy as np
    rng = np.random.default_rng(3)
    ax.scatter(rng.uniform(1.0, 13.0, 50), rng.uniform(0.85, 1.7, 50),
               s=rng.uniform(30, 200, 50), c=COLOR_ACCENT, alpha=0.4, edgecolors="none")

    # 注記 (角に小さく)
    label(ax, 13.5, 7.85, "Esc で編集モードに戻る", fontsize=8, color=COLOR_TEXT_MUTED, ha="right")

    save(fig, "17-publish/presentation-mode.png")


# ============================================================
# 18-capstone
# ============================================================
def ui_final_dashboard():
    """完成ダッシュボードのスクリーンショット代替 (より詳細なモック)。"""
    fig, ax = plt.subplots(figsize=(11, 7))
    setup(ax, (0, 14), (0, 9), "完成ダッシュボードイメージ")

    # 全体枠
    panel(ax, 0.3, 0.4, 13.4, 8.2, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)

    # タイトル
    panel(ax, 0.5, 7.9, 13.0, 0.7, fill=COLOR_ACCENT)
    label(ax, 7.0, 8.25, "シカゴ タクシー利用 ダッシュボード (2023 年)",
          fontsize=13, color="white", weight="bold")

    # KPI 4 つ
    kpis = [("総売上", "$28.4M"), ("乗車回数", "1,000,000"),
            ("平均距離", "5.2 mi"), ("平均料金", "$27.77")]
    for i, (k, v) in enumerate(kpis):
        x = 0.7 + i * 3.3
        panel(ax, x, 6.5, 3.1, 1.2, fill=COLOR_PANEL, edge=COLOR_BORDER)
        label(ax, x + 1.55, 7.25, k, fontsize=10, weight="bold")
        label(ax, x + 1.55, 6.75, v, fontsize=15, weight="bold", color=COLOR_ACCENT)

    # 月次推移 (折れ線、ダミー値で曲線)
    panel(ax, 0.7, 3.5, 6.2, 2.8, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 3.8, 6.05, "月次売上推移", fontsize=11, weight="bold")
    import numpy as np
    months = np.arange(12)
    sales = 2.0 + 0.05 * months + 0.3 * np.sin(months * 0.7) + np.array([0, 0.1, 0.2, 0.15, 0.3, 0.25, 0.2, 0.1, 0.2, 0.3, 0.25, 0.15])
    xs = 1.2 + months * 0.46
    ys = 4.0 + sales * 0.35
    ax.plot(xs, ys, color=COLOR_ACCENT, lw=2, marker="o", markersize=4)
    # 軸ラベル
    for i in [0, 3, 6, 9, 11]:
        label(ax, xs[i], 3.7, f"{i+1}月", fontsize=7, color=COLOR_TEXT_MUTED)

    # 会社別 (横棒)
    panel(ax, 7.4, 3.5, 6.0, 2.8, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 10.4, 6.05, "会社別シェア (上位 10)", fontsize=11, weight="bold")
    companies = ["Taxi Affiliation", "Flash Cab", "Sun Taxi", "City Service",
                 "Chicago Indep.", "5 Star Taxi", "Globe Taxi"]
    sales_v = [5.2, 4.8, 3.2, 2.8, 1.7, 1.4, 1.0]
    for i, (c, v) in enumerate(zip(companies, sales_v)):
        y = 5.6 - i * 0.30
        ax.add_patch(Rectangle((9.0, y - 0.10), v * 0.65, 0.20,
                               facecolor=COLOR_ACCENT, edgecolor="none", alpha=0.85))
        label(ax, 8.9, y, c, fontsize=7, ha="right")
        label(ax, 9.05 + v * 0.65, y, f"${v:.1f}M", fontsize=7, ha="left", color=COLOR_TEXT_MUTED)

    # マップ
    panel(ax, 0.7, 0.6, 6.2, 2.7, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 3.8, 3.05, "乗車地マップ", fontsize=11, weight="bold")
    rng = np.random.default_rng(11)
    ax.scatter(rng.uniform(1.0, 6.7, 80), rng.uniform(0.85, 2.6, 80),
               s=rng.uniform(20, 200, 80), c=COLOR_ACCENT, alpha=0.4, edgecolors="none")

    # 明細
    panel(ax, 7.4, 0.6, 6.0, 2.7, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 10.4, 3.05, "明細テーブル", fontsize=11, weight="bold")
    headers = ["会社", "支払方法", "売上", "件数"]
    for i, h in enumerate(headers):
        label(ax, 7.7 + i * 1.45, 2.55, h, fontsize=9, weight="bold")
    sample = [("Flash Cab", "Cash", "$1.2M", "45k"),
              ("Sun Taxi", "Credit", "$0.9M", "32k"),
              ("City Svc", "Mobile", "$0.6M", "21k"),
              ("Globe T.", "Cash", "$0.5M", "18k")]
    for r, row in enumerate(sample):
        for c, v in enumerate(row):
            label(ax, 7.7 + c * 1.45, 2.2 - r * 0.35, v, fontsize=8)

    save(fig, "18-capstone/final-dashboard.png")


def ui_public_embed():
    fig, ax = plt.subplots(figsize=(11, 6))
    setup(ax, (0, 14), (0, 7.5), "Tableau Public 公開ページの埋め込みプレビュー")

    # ブラウザの外枠
    panel(ax, 0.3, 0.4, 13.4, 6.7, fill="white", edge=COLOR_BORDER_DARK, lw=1.4)
    # アドレスバー
    panel(ax, 0.3, 6.5, 13.4, 0.6, fill=COLOR_PANEL_DARK)
    ax.add_patch(patches.Circle((0.55, 6.80), 0.08, facecolor="#ef4444"))
    ax.add_patch(patches.Circle((0.80, 6.80), 0.08, facecolor="#f59e0b"))
    ax.add_patch(patches.Circle((1.05, 6.80), 0.08, facecolor="#10b981"))
    rounded(ax, 1.3, 6.6, 10.0, 0.4, fill="white", edge=COLOR_BORDER)
    label(ax, 1.5, 6.8, "🔒 public.tableau.com/views/your-workbook/Dashboard",
          fontsize=9, ha="left", color=COLOR_TEXT_MUTED)

    # ナビゲーション
    panel(ax, 0.5, 5.7, 13.0, 0.6, fill=COLOR_ACCENT)
    label(ax, 0.7, 6.0, "Tableau Public", fontsize=11, color="white", weight="bold", ha="left")
    label(ax, 11.0, 6.0, "プロフィール | ダウンロード | シェア", fontsize=10, color="white", ha="left")

    # 埋め込みダッシュボード (簡略版)
    panel(ax, 0.5, 0.6, 13.0, 4.8, fill=COLOR_PANEL, edge=COLOR_BORDER)
    label(ax, 7.0, 5.10, "シカゴ タクシー利用 ダッシュボード (2023)",
          fontsize=12, weight="bold")
    # KPI 行
    for i, k in enumerate(["総売上", "乗車回数", "平均距離", "平均料金"]):
        x = 1.0 + i * 3.1
        panel(ax, x, 3.7, 2.8, 1.0, fill="white", edge=COLOR_BORDER)
        label(ax, x + 1.4, 4.3, k, fontsize=9, weight="bold")
        label(ax, x + 1.4, 4.0, "値", fontsize=12, color=COLOR_ACCENT, weight="bold")
    # 折れ線
    panel(ax, 1.0, 1.5, 5.8, 1.9, fill="white", edge=COLOR_BORDER)
    pts_x = [1.4, 2.0, 2.7, 3.4, 4.1, 4.8, 5.5, 6.2, 6.5]
    pts_y = [2.1, 2.3, 2.5, 2.4, 2.7, 2.9, 2.6, 3.0, 2.8]
    ax.plot(pts_x, pts_y, color=COLOR_ACCENT, lw=2)
    # 棒
    panel(ax, 7.2, 1.5, 5.8, 1.9, fill="white", edge=COLOR_BORDER)
    for i in range(5):
        ax.add_patch(Rectangle((7.4, 3.1 - i * 0.32), 4.0 - i * 0.5, 0.22,
                               facecolor=COLOR_ACCENT, edgecolor="none", alpha=0.8))

    # フッター
    label(ax, 7, 1.0, "🔗 シェア   ⬇️ ダウンロード   ⛶ 全画面",
          fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "18-capstone/public-embed.png")


# ============================================================
# main
# ============================================================
def main():
    # 01
    ui_dim_measure_pane()
    ui_green_vs_blue()
    ui_shelves()
    ui_mark_card()
    ui_analytics_pane()
    # 02
    ui_start_page_connect()
    ui_datasource_tab()
    ui_data_prep_tools()
    # 03
    ui_live_extract_toggle()
    ui_extract_dialog()
    # 04
    ui_show_me()
    # 05
    ui_context_filter()
    ui_nested_sort()
    ui_quick_filters()
    # 06
    ui_create_calc()
    ui_calc_editor()
    # 08
    ui_fiscal_year()
    # 10
    ui_attr_asterisk()
    # 11
    ui_quick_tc_menu()
    # 13
    ui_parameter_dialog()
    ui_parameter_reference_line()
    ui_set_condition()
    # 14
    ui_dashboard_sidebar()
    ui_size_options()
    ui_layout_containers()
    ui_device_designer()
    # 15
    ui_action_types()
    ui_filter_action()
    ui_url_action()
    # 16
    ui_performance_recorder()
    # 17
    ui_public_sign_in()
    ui_presentation_mode()
    # 18
    ui_final_dashboard()
    ui_public_embed()

    print("\nAll UI mocks generated.")


if __name__ == "__main__":
    main()
