"""
学習ツール用の概念図を生成する。

出力先:
    docs/public/images/<章ID>/<file>.png

実行:
    python scripts/generate_diagrams.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "docs" / "public" / "images"

# ---- スタイル ----
COLOR_BG = "#ffffff"
COLOR_BOX = "#f3f4f6"
COLOR_BOX_ACCENT = "#dbeafe"
COLOR_BOX_HIGHLIGHT = "#fde68a"
COLOR_BORDER = "#9ca3af"
COLOR_BORDER_ACCENT = "#3b82f6"
COLOR_TEXT = "#1f2937"
COLOR_TEXT_MUTED = "#6b7280"
COLOR_ARROW = "#6b7280"
COLOR_ACCENT = "#3b82f6"

for name in ["Yu Gothic UI", "Yu Gothic", "Meiryo", "MS Gothic"]:
    if any(f.name == name for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = name
        break

plt.rcParams.update({
    "font.size": 11,
    "axes.edgecolor": COLOR_BORDER,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
    "savefig.facecolor": COLOR_BG,
})


def box(ax, x, y, w, h, text, *, color=COLOR_BOX, edge=COLOR_BORDER,
        fontsize=11, weight="normal", text_color=COLOR_TEXT, lw=1.2,
        pad=0.04, va="center"):
    rect = FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad={pad}",
        facecolor=color, edgecolor=edge, linewidth=lw,
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2,
        y + h / 2 if va == "center" else y + h - 0.15,
        text, ha="center", va=va, fontsize=fontsize, color=text_color,
        weight=weight, wrap=True,
    )


def arrow(ax, x1, y1, x2, y2, color=COLOR_ARROW, style="->", lw=1.5):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, color=color, lw=lw, mutation_scale=14,
    ))


def label(ax, x, y, text, *, fontsize=11, weight="normal", color=COLOR_TEXT,
          ha="center", va="center"):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fontsize, color=color, weight=weight)


def setup(ax, xlim, ylim, title=None):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=13, pad=12, weight="bold", color=COLOR_TEXT)


def save(fig, rel):
    out = IMG / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Wrote {out.relative_to(ROOT)}")


# ============================================================
# 01-basics/workbook-structure.png
# ============================================================
def fig_workbook_structure():
    fig, ax = plt.subplots(figsize=(9, 6))
    setup(ax, (0, 10), (0, 7.5), "Tableau ワークブック構造")

    box(ax, 3, 6.3, 4, 0.8, "データソース", color=COLOR_BOX_ACCENT, weight="bold")
    box(ax, 3, 4.9, 4, 0.8, "ワークブック (.twb / .twbx)", color=COLOR_BOX_ACCENT, weight="bold")

    sheets_y = 3.3
    for i, x in enumerate([0.5, 3.5, 6.5]):
        box(ax, x, sheets_y, 3.0, 0.7, f"ワークシート {i+1}", color=COLOR_BOX)

    box(ax, 1.5, 1.5, 3.5, 0.8, "ダッシュボード", color=COLOR_BOX)
    box(ax, 5.0, 1.5, 3.5, 0.8, "ストーリー", color=COLOR_BOX)

    arrow(ax, 5, 6.25, 5, 5.75)
    arrow(ax, 5, 4.85, 2.0, 4.05)
    arrow(ax, 5, 4.85, 5.0, 4.05)
    arrow(ax, 5, 4.85, 8.0, 4.05)
    arrow(ax, 3.0, 3.25, 3.2, 2.35)
    arrow(ax, 5.0, 3.25, 6.0, 2.35)
    arrow(ax, 6.0, 3.25, 6.5, 2.35)

    label(ax, 5, 0.5, "シート → ダッシュボード → ストーリー の順に組み合わせていく",
          fontsize=10, color=COLOR_TEXT_MUTED)

    save(fig, "01-basics/workbook-structure.png")


# ============================================================
# 02-data-connection/relationship-join-union.png
# ============================================================
def fig_relationship_join_union():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    setup(ax, (0, 12), (0, 7), "リレーションシップ / 結合 / ユニオンの違い")

    # --- リレーションシップ ---
    label(ax, 2.0, 6.0, "リレーションシップ", fontsize=12, weight="bold")
    box(ax, 0.5, 4.2, 1.5, 0.9, "テーブル A", color=COLOR_BOX_ACCENT)
    box(ax, 2.5, 4.2, 1.5, 0.9, "テーブル B", color=COLOR_BOX_ACCENT)
    ax.plot([2.0, 2.5], [4.65, 4.65], color=COLOR_ACCENT, linestyle="--", lw=1.5)
    label(ax, 2.25, 4.9, "リンク", fontsize=9, color=COLOR_ACCENT)
    label(ax, 2.0, 3.4, "粒度を保ったまま関連付ける", fontsize=9, color=COLOR_TEXT_MUTED)
    label(ax, 2.0, 2.9, "ビューで参照されたタイミングで動的に結合", fontsize=9, color=COLOR_TEXT_MUTED)

    # --- 結合 ---
    label(ax, 6.0, 6.0, "結合 (Join)", fontsize=12, weight="bold")
    box(ax, 4.7, 4.2, 2.6, 0.9, "テーブル A + B (一体化)", color=COLOR_BOX)
    label(ax, 6.0, 3.4, "1 つのテーブルに統合", fontsize=9, color=COLOR_TEXT_MUTED)
    label(ax, 6.0, 2.9, "INNER / LEFT / RIGHT / FULL OUTER", fontsize=9, color=COLOR_TEXT_MUTED)

    # --- ユニオン ---
    label(ax, 10.0, 6.0, "ユニオン (Union)", fontsize=12, weight="bold")
    box(ax, 9.0, 4.7, 2.0, 0.6, "テーブル A", color=COLOR_BOX)
    box(ax, 9.0, 4.0, 2.0, 0.6, "テーブル B", color=COLOR_BOX)
    label(ax, 10.0, 3.4, "縦方向に追加 (列構造が同じ)", fontsize=9, color=COLOR_TEXT_MUTED)
    label(ax, 10.0, 2.9, "同じ形式のデータを積み上げ", fontsize=9, color=COLOR_TEXT_MUTED)

    # 比較表
    label(ax, 6.0, 1.6, "Tableau のデフォルトはリレーションシップ。", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 6.0, 1.1, "明示的に結合・ユニオンに切り替えることも可能。", fontsize=10, color=COLOR_TEXT_MUTED)

    save(fig, "02-data-connection/relationship-join-union.png")


# ============================================================
# 02-data-connection/logical-physical-layer.png
# ============================================================
def fig_logical_physical():
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    setup(ax, (0, 10), (0, 7), "論理レイヤー と 物理レイヤー")

    # 外側 (論理)
    outer = FancyBboxPatch(
        (0.5, 0.8), 9.0, 5.5, boxstyle="round,pad=0.05",
        facecolor=COLOR_BOX_ACCENT, edgecolor=COLOR_BORDER_ACCENT, linewidth=2.0,
    )
    ax.add_patch(outer)
    label(ax, 5.0, 5.85, "論理レイヤー", fontsize=13, weight="bold", color=COLOR_ACCENT)
    label(ax, 5.0, 5.45, "(リレーションシップで結びつけ)", fontsize=10, color=COLOR_TEXT_MUTED)

    # 内側 (物理) x2
    box(ax, 1.2, 2.3, 3.6, 2.3, "", color=COLOR_BG, edge=COLOR_BORDER, lw=1.4)
    label(ax, 3.0, 4.3, "物理レイヤー (テーブル 1)", fontsize=11, weight="bold")
    label(ax, 3.0, 3.7, "Join / Union", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 3.0, 3.2, "実際に結合された 1+ テーブル", fontsize=9, color=COLOR_TEXT_MUTED)

    box(ax, 5.2, 2.3, 3.6, 2.3, "", color=COLOR_BG, edge=COLOR_BORDER, lw=1.4)
    label(ax, 7.0, 4.3, "物理レイヤー (テーブル 2)", fontsize=11, weight="bold")
    label(ax, 7.0, 3.7, "Join / Union", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 7.0, 3.2, "実際に結合された 1+ テーブル", fontsize=9, color=COLOR_TEXT_MUTED)

    # 説明
    label(ax, 5.0, 1.3, "論理レイヤー = リレーションシップで論理的に結びつけ",
          fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 5.0, 0.85, "物理レイヤー = ダブルクリックで開く、実テーブルの結合定義",
          fontsize=10, color=COLOR_TEXT_MUTED)

    save(fig, "02-data-connection/logical-physical-layer.png")


# ============================================================
# 05-filter-sort/filter-order.png
# ============================================================
def fig_filter_order_basic():
    fig, ax = plt.subplots(figsize=(9, 8.5))
    setup(ax, (0, 10), (0, 11), "フィルターの評価順序")

    steps = [
        (9.0, "1. 抽出フィルター", ".hyper 生成時に行を絞る", COLOR_BOX),
        (7.8, "2. データソースフィルター", "接続全体に適用 (公開時にも保存)", COLOR_BOX),
        (6.6, "3. コンテキストフィルター", "「コンテキストに追加」で先行評価", COLOR_BOX_HIGHLIGHT),
        (5.4, "4. ディメンションフィルター", "フィルターシェルフ上の通常フィルター", COLOR_BOX),
        (4.2, "5. メジャーフィルター", "集計後の値で絞り込み (SUM > 1000 等)", COLOR_BOX),
        (3.0, "6. 表計算フィルター", "表計算 (RANK, WINDOW_*, LOOKUP 等) の結果", COLOR_BOX),
    ]

    for y, title, desc, color in steps:
        box(ax, 1.2, y, 7.6, 0.85, "", color=color)
        ax.text(1.5, y + 0.55, title, fontsize=11, weight="bold", color=COLOR_TEXT, va="center")
        ax.text(1.5, y + 0.25, desc, fontsize=9, color=COLOR_TEXT_MUTED, va="center")

    label(ax, 5, 10.3, "▲ ソースデータ", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 5, 2.4, "▼ ビュー描画", fontsize=10, color=COLOR_TEXT_MUTED)

    for y in [8.85, 7.65, 6.45, 5.25, 4.05]:
        arrow(ax, 5, y, 5, y - 0.35)

    save(fig, "05-filter-sort/filter-order.png")


# ============================================================
# 09-functions-logical/operator-precedence.png
# ============================================================
def fig_operator_precedence():
    fig, ax = plt.subplots(figsize=(10, 6))
    setup(ax, (0, 12), (0, 7.5), "論理演算子の優先順位と括弧の必要性")

    # Header
    label(ax, 6, 6.7, "優先順位 (高い→低い)", fontsize=12, weight="bold")

    levels = [
        (5.5, "NOT", "否定", "1. 最優先"),
        (4.3, "AND", "論理積", "2. 次に AND"),
        (3.1, "OR", "論理和", "3. 最後に OR"),
    ]
    for y, op, name, rank in levels:
        box(ax, 1, y, 1.5, 0.8, op, color=COLOR_BOX_ACCENT, weight="bold", fontsize=14)
        label(ax, 3.3, y + 0.4, name, fontsize=10, ha="left")
        label(ax, 5.0, y + 0.4, rank, fontsize=10, color=COLOR_TEXT_MUTED, ha="left")

    # Example with parentheses
    label(ax, 6.0, 2.0, "例: 「Cash 以外で 1000 以上」を書くとき", fontsize=10, weight="bold", ha="center")
    label(ax, 6.0, 1.4,
          "NOT [payment_type] = 'Cash' AND [trip_total] >= 1000   ← 意図と違う",
          fontsize=10, color="#dc2626", ha="center")
    label(ax, 6.0, 0.85,
          "NOT ([payment_type] = 'Cash') AND [trip_total] >= 1000   ← 括弧で明示",
          fontsize=10, color="#16a34a", ha="center")

    save(fig, "09-functions-logical/operator-precedence.png")


# ============================================================
# 11-functions-tablecalc/calc-pipeline.png
# ============================================================
def fig_calc_pipeline():
    fig, ax = plt.subplots(figsize=(11, 4.5))
    setup(ax, (0, 14), (0, 5.5), "計算の評価フロー (行レベル → 集計 → 表計算)")

    boxes = [
        (0.3, "ソースデータ", "(行レベルの明細)", COLOR_BOX),
        (3.0, "行レベル計算", "[fare]+[tips] など", COLOR_BOX_ACCENT),
        (5.7, "集計関数", "SUM, AVG, COUNTD 等", COLOR_BOX_ACCENT),
        (8.4, "表計算", "WINDOW_SUM, RANK 等", COLOR_BOX_HIGHLIGHT),
        (11.1, "ビュー描画", "(マーク表示)", COLOR_BOX),
    ]
    for x, title, sub, color in boxes:
        box(ax, x, 2.4, 2.4, 1.3, "", color=color)
        ax.text(x + 1.2, 3.5, title, ha="center", va="center", fontsize=11, weight="bold")
        ax.text(x + 1.2, 2.85, sub, ha="center", va="center", fontsize=9, color=COLOR_TEXT_MUTED)

    for x in [2.7, 5.4, 8.1, 10.8]:
        arrow(ax, x, 3.05, x + 0.3, 3.05)

    label(ax, 7.0, 1.4,
          "行レベル計算と集計関数はデータソース側で処理 / 表計算は Tableau 側で集計後に処理",
          fontsize=10, color=COLOR_TEXT_MUTED)

    save(fig, "11-functions-tablecalc/calc-pipeline.png")


# ============================================================
# 12-lod/lod-granularity.png
# ============================================================
def fig_lod_granularity():
    fig, ax = plt.subplots(figsize=(11, 6))
    setup(ax, (0, 12), (0, 7.5), "通常集計 vs FIXED LOD の粒度比較")

    # --- 通常集計 ---
    label(ax, 3.0, 6.7, "通常の集計", fontsize=12, weight="bold")
    label(ax, 3.0, 6.2, "SUM([trip_total])", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 3.0, 5.7, "→ ビュー上のディメンションに応じて集計", fontsize=10, color=COLOR_TEXT_MUTED)

    rows1 = [
        ("会社", "売上合計"),
        ("Flash Cab", "120,000"),
        ("Taxi Affiliation", "98,000"),
        ("Sun Taxi", "75,000"),
    ]
    for i, (a, b) in enumerate(rows1):
        y = 4.7 - i * 0.6
        color = COLOR_BOX_ACCENT if i == 0 else COLOR_BOX
        weight = "bold" if i == 0 else "normal"
        box(ax, 1.2, y, 1.7, 0.5, "", color=color)
        box(ax, 2.95, y, 1.7, 0.5, "", color=color)
        label(ax, 2.05, y + 0.25, a, fontsize=9, weight=weight)
        label(ax, 3.8, y + 0.25, b, fontsize=9, weight=weight)

    label(ax, 3.0, 1.6, "会社別の合計売上", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 3.0, 1.1, "→ ビュー粒度 = 会社", fontsize=10, color=COLOR_TEXT_MUTED)

    # --- FIXED LOD ---
    label(ax, 9.0, 6.7, "FIXED LOD", fontsize=12, weight="bold", color=COLOR_ACCENT)
    label(ax, 9.0, 6.2, "{ FIXED [company] : SUM([trip_total]) }", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 9.0, 5.7, "→ ビューの粒度に関わらず company 単位で固定集計", fontsize=10, color=COLOR_TEXT_MUTED)

    rows2 = [
        ("会社", "支払方法", "売上 (固定)"),
        ("Flash Cab", "Cash", "120,000"),
        ("Flash Cab", "Credit", "120,000"),
        ("Sun Taxi", "Cash", "75,000"),
    ]
    for i, (a, b, c) in enumerate(rows2):
        y = 4.7 - i * 0.6
        color = COLOR_BOX_ACCENT if i == 0 else COLOR_BOX
        weight = "bold" if i == 0 else "normal"
        box(ax, 6.6, y, 1.5, 0.5, "", color=color)
        box(ax, 8.15, y, 1.5, 0.5, "", color=color)
        box(ax, 9.7, y, 1.7, 0.5, "", color=color)
        label(ax, 7.35, y + 0.25, a, fontsize=9, weight=weight)
        label(ax, 8.9, y + 0.25, b, fontsize=9, weight=weight)
        label(ax, 10.55, y + 0.25, c, fontsize=9, weight=weight, color=COLOR_ACCENT if i > 0 else COLOR_TEXT)

    label(ax, 9.0, 1.6, "ビュー粒度 = 会社 × 支払方法 でも", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 9.0, 1.1, "売上は会社単位で固定された値が返る", fontsize=10, color=COLOR_TEXT_MUTED)

    save(fig, "12-lod/lod-granularity.png")


# ============================================================
# 12-lod/filter-order.png  (LOD を含む全段階)
# ============================================================
def fig_filter_order_lod():
    fig, ax = plt.subplots(figsize=(9, 10.5))
    setup(ax, (0, 10), (0, 13.5), "フィルターと LOD の評価順序 (完全版)")

    steps = [
        (11.0, "1. 抽出フィルター", COLOR_BOX, False),
        (9.9, "2. データソースフィルター", COLOR_BOX, False),
        (8.8, "3. コンテキストフィルター", COLOR_BOX_HIGHLIGHT, False),
        (7.7, "4. FIXED LOD", COLOR_BOX_ACCENT, True),
        (6.6, "5. ディメンションフィルター", COLOR_BOX, False),
        (5.5, "6. INCLUDE / EXCLUDE LOD", COLOR_BOX_ACCENT, True),
        (4.4, "7. メジャーフィルター", COLOR_BOX, False),
        (3.3, "8. 表計算フィルター", COLOR_BOX, False),
    ]
    for y, title, color, is_lod in steps:
        box(ax, 1.2, y, 7.6, 0.85, "", color=color,
            edge=COLOR_BORDER_ACCENT if is_lod else COLOR_BORDER,
            lw=2.0 if is_lod else 1.2)
        ax.text(5.0, y + 0.42, title, ha="center", va="center",
                fontsize=11, weight="bold" if is_lod else "normal",
                color=COLOR_ACCENT if is_lod else COLOR_TEXT)

    label(ax, 5, 12.4, "▲ ソースデータ", fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 5, 2.75, "▼ ビュー描画", fontsize=10, color=COLOR_TEXT_MUTED)

    for y in [10.85, 9.75, 8.65, 7.55, 6.45, 5.35, 4.25]:
        arrow(ax, 5, y, 5, y - 0.25)

    label(ax, 5, 1.8,
          "FIXED は ディメンションフィルター の前 / INCLUDE・EXCLUDE は ディメンションフィルター の後",
          fontsize=10, color=COLOR_TEXT_MUTED)
    label(ax, 5, 1.2,
          "ディメンションフィルターを FIXED に効かせたい場合 → コンテキストフィルターへ昇格",
          fontsize=10, color=COLOR_TEXT_MUTED)

    save(fig, "12-lod/filter-order.png")


# ============================================================
# 18-capstone/sheet-design-sketch.png
# ============================================================
def fig_sheet_design():
    fig, ax = plt.subplots(figsize=(11, 6))
    setup(ax, (0, 12), (0, 7), "シート設計の構成案 (5 種類のビュー)")

    sheets = [
        (0.5, 4.5, 3.0, 1.8, "① KPI カード",
         ["総売上 (USD)", "総乗車回数", "平均距離", "平均料金"]),
        (4.0, 4.5, 3.5, 1.8, "② 月次推移",
         ["折れ線", "月別 SUM(trip_total)", "前年同月線 (任意)"]),
        (8.0, 4.5, 3.5, 1.8, "③ 構成 (会社別シェア)",
         ["横棒グラフ", "company × SUM(trip_total)", "TOP 10 + その他"]),
        (0.5, 1.0, 5.0, 2.5, "④ 地理マップ",
         ["pickup_centroid で記号マップ",
          "色 = SUM(trip_total) / サイズ = 件数",
          "コミュニティエリア単位で集約も可"]),
        (6.0, 1.0, 5.5, 2.5, "⑤ 詳細テーブル",
         ["company × payment_type のクロス集計",
          "SUM(trip_total), AVG(trip_miles)",
          "アクションでフィルター連動"]),
    ]

    for x, y, w, h, title, lines in sheets:
        box(ax, x, y, w, h, "", color=COLOR_BOX_ACCENT, edge=COLOR_BORDER_ACCENT, lw=1.5)
        ax.text(x + 0.2, y + h - 0.3, title, fontsize=12, weight="bold", color=COLOR_ACCENT, va="center")
        for i, line in enumerate(lines):
            ax.text(x + 0.4, y + h - 0.75 - i * 0.32, "・ " + line,
                    fontsize=9, color=COLOR_TEXT, va="center")

    label(ax, 6, 0.4,
          "ダッシュボード上では 上段に KPI/推移/構成 → 下段に地理/詳細 の 2 段構成が定番",
          fontsize=10, color=COLOR_TEXT_MUTED)

    save(fig, "18-capstone/sheet-design-sketch.png")


# ============================================================
# 18-capstone/dashboard-wireframe.png
# ============================================================
def fig_dashboard_wireframe():
    fig, ax = plt.subplots(figsize=(10, 7))
    setup(ax, (0, 12), (0, 9), "ダッシュボード完成イメージ (ワイヤーフレーム)")

    # タイトル帯
    box(ax, 0.5, 7.6, 11.0, 0.8, "", color=COLOR_BOX_ACCENT, edge=COLOR_BORDER_ACCENT, lw=1.5)
    ax.text(6.0, 8.0, "シカゴ タクシー利用 ダッシュボード (2023)",
            ha="center", va="center", fontsize=13, weight="bold", color=COLOR_ACCENT)

    # KPI 行
    kpis = ["総売上", "乗車回数", "平均距離", "平均料金"]
    for i, k in enumerate(kpis):
        x = 0.5 + i * 2.85
        box(ax, x, 6.0, 2.6, 1.2, "", color=COLOR_BOX)
        ax.text(x + 1.3, 6.85, k, fontsize=10, weight="bold", ha="center")
        ax.text(x + 1.3, 6.4, "値", fontsize=14, weight="bold", color=COLOR_ACCENT, ha="center")
        ax.text(x + 1.3, 6.15, "(KPI)", fontsize=8, color=COLOR_TEXT_MUTED, ha="center")

    # 月次推移
    box(ax, 0.5, 3.3, 5.5, 2.3, "", color=COLOR_BOX)
    ax.text(0.7, 5.4, "月次売上推移", fontsize=11, weight="bold")
    ax.text(0.7, 5.1, "(折れ線グラフ)", fontsize=9, color=COLOR_TEXT_MUTED)
    # 折れ線のモック
    pts_x = [1.0, 1.7, 2.4, 3.1, 3.8, 4.5, 5.0]
    pts_y = [3.8, 4.0, 4.3, 4.1, 4.5, 4.7, 4.6]
    ax.plot(pts_x, pts_y, color=COLOR_ACCENT, lw=2.0, marker="o", markersize=4)

    # 構成
    box(ax, 6.5, 3.3, 5.0, 2.3, "", color=COLOR_BOX)
    ax.text(6.7, 5.4, "会社別シェア (上位 10)", fontsize=11, weight="bold")
    ax.text(6.7, 5.1, "(横棒グラフ)", fontsize=9, color=COLOR_TEXT_MUTED)
    for i in range(5):
        bar_len = 4.0 - i * 0.6
        ax.add_patch(patches.Rectangle((6.9, 4.6 - i * 0.3), bar_len, 0.2,
                                       facecolor=COLOR_ACCENT, edgecolor="none", alpha=0.7))

    # マップ
    box(ax, 0.5, 0.5, 5.5, 2.5, "", color=COLOR_BOX)
    ax.text(0.7, 2.75, "乗車地マップ", fontsize=11, weight="bold")
    ax.text(0.7, 2.45, "(記号マップ・色=売上)", fontsize=9, color=COLOR_TEXT_MUTED)
    import numpy as np
    rng = np.random.default_rng(7)
    xs = rng.uniform(1.0, 5.5, 30)
    ys = rng.uniform(0.8, 2.2, 30)
    ax.scatter(xs, ys, s=rng.uniform(20, 100, 30), c=COLOR_ACCENT, alpha=0.5, edgecolors="none")

    # 明細テーブル
    box(ax, 6.5, 0.5, 5.0, 2.5, "", color=COLOR_BOX)
    ax.text(6.7, 2.75, "明細テーブル", fontsize=11, weight="bold")
    ax.text(6.7, 2.45, "(クロス集計)", fontsize=9, color=COLOR_TEXT_MUTED)
    headers = ["会社", "支払方法", "売上", "件数"]
    for i, h in enumerate(headers):
        ax.text(6.9 + i * 1.15, 2.1, h, fontsize=9, weight="bold")
    for r in range(4):
        for c in range(4):
            ax.text(6.9 + c * 1.15, 1.75 - r * 0.3, "—", fontsize=9, color=COLOR_TEXT_MUTED)

    save(fig, "18-capstone/dashboard-wireframe.png")


# ============================================================
# 実行
# ============================================================
def main():
    fig_workbook_structure()
    fig_relationship_join_union()
    fig_logical_physical()
    fig_filter_order_basic()
    fig_operator_precedence()
    fig_calc_pipeline()
    fig_lod_granularity()
    fig_filter_order_lod()
    fig_sheet_design()
    fig_dashboard_wireframe()
    print("\nAll diagrams generated.")


if __name__ == "__main__":
    main()
