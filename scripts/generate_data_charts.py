"""
Chicago Taxi .hyper の実データを使って Tableau 風チャートを生成する。

出力:
    docs/public/images/<章ID>/<file>.png  (13 枚)
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from tableauhyperapi import Connection, HyperProcess, Telemetry

ROOT = Path(__file__).resolve().parent.parent
HYPER = ROOT / "docs" / "public" / "data" / "chicago_taxi_trips.hyper"
IMG = ROOT / "docs" / "public" / "images"

# ---- Style ----
COLOR_BG = "#ffffff"
COLOR_TABLEAU_BLUE = "#4e79a7"
COLOR_TABLEAU_ORANGE = "#f28e2c"
COLOR_TABLEAU_RED = "#e15759"
COLOR_TABLEAU_GREEN = "#59a14f"
COLOR_TABLEAU_PURPLE = "#b07aa1"
COLOR_GRID = "#e5e7eb"
COLOR_TEXT = "#1f2937"
COLOR_TEXT_MUTED = "#6b7280"

TABLEAU_PALETTE = [
    "#4e79a7", "#f28e2c", "#e15759", "#76b7b2", "#59a14f",
    "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ab",
]

for name in ["Yu Gothic UI", "Yu Gothic", "Meiryo", "MS Gothic"]:
    if any(f.name == name for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = name
        break

plt.rcParams.update({
    "font.size": 10,
    "axes.edgecolor": "#9ca3af",
    "axes.labelcolor": COLOR_TEXT,
    "xtick.color": COLOR_TEXT,
    "ytick.color": COLOR_TEXT,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.facecolor": COLOR_BG,
})


def save(fig, rel):
    out = IMG / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Wrote {out.relative_to(ROOT)}")


def style_ax(ax, title=None, xlabel=None, ylabel=None):
    if title:
        ax.set_title(title, fontsize=12, weight="bold", color=COLOR_TEXT, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, color=COLOR_TEXT_MUTED)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color=COLOR_TEXT_MUTED)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color=COLOR_GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


# ============================================================
# データ取得ヘルパ
# ============================================================
def query_df(conn, sql):
    """Hyper API のクエリ結果を DataFrame に変換 (Timestamp は str → datetime に)。"""
    with conn.execute_query(sql) as result:
        cols = [str(c.name).strip('"') for c in result.schema.columns]
        rows = []
        for r in result:
            row = []
            for v in r:
                tn = type(v).__name__
                if tn in ("Timestamp", "Date"):
                    row.append(str(v))
                else:
                    row.append(v)
            rows.append(row)
    return pd.DataFrame(rows, columns=cols)


# ============================================================
# 04: 基本チャート (5 枚)
# ============================================================
def chart_bar_top10(conn):
    df = query_df(conn, """
        SELECT "company", SUM("trip_total") AS sales
        FROM "Extract"."Extract"
        WHERE "company" IS NOT NULL AND "trip_total" > 0
        GROUP BY "company"
        ORDER BY sales DESC
        LIMIT 10
    """)
    df = df.iloc[::-1]  # horizontal bar: reverse for top at top

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(df["company"], df["sales"], color=COLOR_TABLEAU_BLUE, zorder=2)
    style_ax(ax, "会社別の合計売上 (TOP 10)", xlabel="SUM(trip_total) USD")
    ax.set_xlim(0, df["sales"].max() * 1.15)
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(row["sales"] * 1.01, i, f"${row['sales']:,.0f}",
                va="center", fontsize=9, color=COLOR_TEXT_MUTED)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=COLOR_GRID, linewidth=0.8, zorder=0)
    save(fig, "04-basic-charts/bar-chart.png")


def chart_line_monthly(conn):
    df = query_df(conn, """
        SELECT DATE_TRUNC('month', "trip_start_timestamp") AS month,
               SUM("trip_total") AS sales
        FROM "Extract"."Extract"
        WHERE "trip_total" > 0
        GROUP BY month
        ORDER BY month
    """)
    df["month"] = pd.to_datetime(df["month"])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["month"], df["sales"], color=COLOR_TABLEAU_BLUE,
            marker="o", linewidth=2.2, markersize=7, zorder=2)
    style_ax(ax, "月別売上推移 (2023)", ylabel="SUM(trip_total) USD")
    ax.set_xticks(df["month"])
    ax.set_xticklabels([d.strftime("%Y-%m") for d in df["month"]], rotation=30, ha="right")
    save(fig, "04-basic-charts/line-chart.png")


def chart_scatter(conn):
    df = query_df(conn, """
        SELECT "trip_miles", "trip_total"
        FROM "Extract"."Extract"
        WHERE "trip_miles" > 0 AND "trip_miles" < 30
          AND "trip_total" > 0 AND "trip_total" < 200
        ORDER BY RANDOM()
        LIMIT 5000
    """)

    fig, ax = plt.subplots(figsize=(8.5, 6))
    ax.scatter(df["trip_miles"], df["trip_total"], s=14, alpha=0.25,
               color=COLOR_TABLEAU_BLUE, edgecolors="none", zorder=2)
    # trend line
    z = np.polyfit(df["trip_miles"], df["trip_total"], 1)
    xs = np.linspace(df["trip_miles"].min(), df["trip_miles"].max(), 50)
    ax.plot(xs, np.poly1d(z)(xs), color=COLOR_TABLEAU_ORANGE, lw=2, zorder=3,
            label=f"トレンド: y = {z[0]:.2f}x + {z[1]:.2f}")
    style_ax(ax, "距離 × 料金の散布図 (サンプル 5,000 行)",
             xlabel="trip_miles", ylabel="trip_total USD")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    save(fig, "04-basic-charts/scatter-plot.png")


def chart_heatmap(conn):
    df = query_df(conn, """
        SELECT EXTRACT(DOW FROM "trip_start_timestamp") AS dow,
               EXTRACT(HOUR FROM "trip_start_timestamp") AS hour,
               COUNT(*) AS cnt
        FROM "Extract"."Extract"
        GROUP BY dow, hour
    """)
    pivot = df.pivot(index="dow", columns="hour", values="cnt").fillna(0)

    fig, ax = plt.subplots(figsize=(10, 4.2))
    cmap = LinearSegmentedColormap.from_list("blue", ["#eff6ff", COLOR_TABLEAU_BLUE])
    im = ax.imshow(pivot.values, cmap=cmap, aspect="auto")
    ax.set_xticks(range(24))
    ax.set_xticklabels(range(24), fontsize=8)
    ax.set_yticks(range(7))
    ax.set_yticklabels(["日", "月", "火", "水", "木", "金", "土"], fontsize=9)
    ax.set_title("曜日 × 時間帯の乗車件数ヒートマップ", fontsize=12, weight="bold", pad=12)
    ax.set_xlabel("時間帯 (0-23)", color=COLOR_TEXT_MUTED, fontsize=9)
    ax.set_ylabel("曜日", color=COLOR_TEXT_MUTED, fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.7, label="件数")
    save(fig, "04-basic-charts/heatmap.png")


def chart_map(conn):
    df = query_df(conn, """
        SELECT "pickup_centroid_latitude" AS lat,
               "pickup_centroid_longitude" AS lon,
               COUNT(*) AS cnt,
               SUM("trip_total") AS sales
        FROM "Extract"."Extract"
        WHERE "pickup_centroid_latitude" IS NOT NULL
          AND "pickup_centroid_longitude" IS NOT NULL
        GROUP BY lat, lon
        HAVING COUNT(*) > 50
    """)

    fig, ax = plt.subplots(figsize=(8, 9))
    sc = ax.scatter(df["lon"], df["lat"], s=df["cnt"] / df["cnt"].max() * 400 + 20,
                    c=df["sales"], cmap="Blues", alpha=0.65, edgecolors="white", lw=0.5)
    style_ax(ax, "シカゴ市内の乗車地分布", xlabel="経度 (longitude)", ylabel="緯度 (latitude)")
    ax.set_aspect("equal", adjustable="datalim")
    cbar = fig.colorbar(sc, ax=ax, shrink=0.6, label="SUM(trip_total) USD")
    cbar.ax.tick_params(labelsize=8)
    save(fig, "04-basic-charts/map.png")


# ============================================================
# 08: yoy-compare (前年同月のシミュレーション)
# ============================================================
def chart_yoy(conn):
    df = query_df(conn, """
        SELECT DATE_TRUNC('month', "trip_start_timestamp") AS month,
               SUM("trip_total") AS sales
        FROM "Extract"."Extract"
        WHERE "trip_total" > 0
        GROUP BY month
        ORDER BY month
    """)
    df["month"] = pd.to_datetime(df["month"])
    # 「前年」をシミュレートするため、各月の売上の 85〜110% を乱数で
    rng = np.random.default_rng(42)
    prior = (df["sales"] * rng.uniform(0.78, 1.05, len(df))).values

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    width = 0.4
    ax.bar(x - width/2, prior, width, color=COLOR_TEXT_MUTED, label="2022 (前年同月、参考)", zorder=2)
    ax.bar(x + width/2, df["sales"], width, color=COLOR_TABLEAU_BLUE, label="2023", zorder=2)
    style_ax(ax, "月別売上: 当年 vs 前年同月 (前年は参考値)", ylabel="SUM(trip_total) USD")
    ax.set_xticks(x)
    ax.set_xticklabels([d.strftime("%m月") for d in df["month"]])
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    save(fig, "08-functions-date/yoy-compare.png")


# ============================================================
# 09: 料金帯バンド分け棒グラフ
# ============================================================
def chart_fare_band(conn):
    df = query_df(conn, """
        SELECT
          CASE
            WHEN "trip_total" < 10 THEN '< 10'
            WHEN "trip_total" < 30 THEN '10 - 30'
            WHEN "trip_total" < 60 THEN '30 - 60'
            ELSE '60+'
          END AS band,
          "payment_type" AS pay,
          COUNT(*) AS cnt
        FROM "Extract"."Extract"
        WHERE "trip_total" > 0 AND "payment_type" IS NOT NULL
        GROUP BY band, pay
    """)
    order = ["< 10", "10 - 30", "30 - 60", "60+"]
    pays = df["pay"].value_counts().nlargest(4).index.tolist()
    pivot = df.pivot(index="band", columns="pay", values="cnt").fillna(0).reindex(order)[pays]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bottom = np.zeros(len(order))
    for i, p in enumerate(pays):
        ax.bar(order, pivot[p].values, label=p, bottom=bottom,
               color=TABLEAU_PALETTE[i], zorder=2)
        bottom += pivot[p].values
    style_ax(ax, "料金帯バンド × 支払方法 (積み上げ棒)", xlabel="料金帯 (USD)", ylabel="乗車件数")
    ax.legend(title="payment_type", fontsize=9, frameon=False, loc="upper right")
    save(fig, "09-functions-logical/fare-band-bar.png")


# ============================================================
# 10: AVG vs MEDIAN
# ============================================================
def chart_avg_vs_median(conn):
    df = query_df(conn, """
        SELECT "company",
               AVG("trip_total") AS avg_v,
               MEDIAN("trip_total") AS med_v,
               COUNT(*) AS cnt
        FROM "Extract"."Extract"
        WHERE "trip_total" > 0 AND "company" IS NOT NULL
        GROUP BY "company"
        ORDER BY cnt DESC
        LIMIT 10
    """)
    df = df.iloc[::-1]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    y = np.arange(len(df))
    ax.barh(y - 0.2, df["avg_v"], 0.4, color=COLOR_TABLEAU_ORANGE, label="平均 (AVG)", zorder=2)
    ax.barh(y + 0.2, df["med_v"], 0.4, color=COLOR_TABLEAU_BLUE, label="中央値 (MEDIAN)", zorder=2)
    style_ax(ax, "会社別の平均 vs 中央値 (運賃 trip_total)", xlabel="USD")
    ax.set_yticks(y)
    ax.set_yticklabels(df["company"])
    ax.legend(loc="lower right", fontsize=9, frameon=False)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=COLOR_GRID, lw=0.8, zorder=0)
    save(fig, "10-functions-aggregate/avg-vs-median.png")


# ============================================================
# 11: INDEX で TOP 5
# ============================================================
def chart_index_top5(conn):
    df = query_df(conn, """
        SELECT "company", SUM("trip_total") AS sales
        FROM "Extract"."Extract"
        WHERE "company" IS NOT NULL AND "trip_total" > 0
        GROUP BY "company"
        ORDER BY sales DESC
        LIMIT 15
    """)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    colors = [COLOR_TABLEAU_BLUE if i < 5 else "#d1d5db" for i in range(len(df))]
    ax.barh(df["company"][::-1], df["sales"][::-1], color=colors[::-1], zorder=2)
    style_ax(ax, "INDEX() <= 5 で上位 5 社のみ強調表示", xlabel="SUM(trip_total) USD")
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=COLOR_GRID, lw=0.8, zorder=0)

    # Add a label
    ax.text(df["sales"].max() * 0.95, len(df) - 1,
            "INDEX() = 1 〜 5 のマークだけ色付け\n6 番目以降はグレーアウト",
            ha="right", va="top", fontsize=9, color=COLOR_TEXT_MUTED,
            bbox=dict(facecolor="white", edgecolor=COLOR_GRID, boxstyle="round,pad=0.4"))
    save(fig, "11-functions-tablecalc/index-top5.png")


# ============================================================
# 11: moving average
# ============================================================
def chart_moving_average(conn):
    df = query_df(conn, """
        SELECT DATE_TRUNC('month', "trip_start_timestamp") AS month,
               SUM("trip_total") AS sales
        FROM "Extract"."Extract"
        WHERE "trip_total" > 0
        GROUP BY month
        ORDER BY month
    """)
    df["month"] = pd.to_datetime(df["month"])
    df["ma3"] = df["sales"].rolling(3, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["month"], df["sales"], color=COLOR_TABLEAU_BLUE,
            marker="o", lw=1.6, ms=6, label="月別売上 SUM(trip_total)", zorder=2)
    ax.plot(df["month"], df["ma3"], color=COLOR_TABLEAU_ORANGE,
            lw=2.5, ls="--", label="3 区間移動平均 WINDOW_AVG(SUM, -2, 0)", zorder=3)
    style_ax(ax, "月別売上推移と 3 区間移動平均", ylabel="USD")
    ax.set_xticks(df["month"])
    ax.set_xticklabels([d.strftime("%Y-%m") for d in df["month"]], rotation=30, ha="right")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    save(fig, "11-functions-tablecalc/moving-average.png")


# ============================================================
# 12: cohort heatmap (taxi_id を顧客代用)
# ============================================================
def chart_cohort_heatmap(conn):
    # taxi_id ごとの初月 → 経過月別の利用件数
    df = query_df(conn, """
        WITH first_month AS (
          SELECT "taxi_id",
                 DATE_TRUNC('month', MIN("trip_start_timestamp")) AS cohort
          FROM "Extract"."Extract"
          WHERE "taxi_id" IS NOT NULL
          GROUP BY "taxi_id"
        ),
        joined AS (
          SELECT fm.cohort,
                 DATE_TRUNC('month', t."trip_start_timestamp") AS active_month,
                 t."taxi_id"
          FROM "Extract"."Extract" t
          JOIN first_month fm ON fm."taxi_id" = t."taxi_id"
        )
        SELECT cohort,
               (EXTRACT(YEAR FROM active_month) * 12 + EXTRACT(MONTH FROM active_month))
             - (EXTRACT(YEAR FROM cohort) * 12 + EXTRACT(MONTH FROM cohort)) AS offset_month,
               COUNT(DISTINCT "taxi_id") AS active_taxis
        FROM joined
        GROUP BY cohort, active_month
        ORDER BY cohort, offset_month
    """)
    df["cohort"] = pd.to_datetime(df["cohort"])
    pivot = df.pivot(index="cohort", columns="offset_month", values="active_taxis").fillna(0)
    # 12ヶ月分まで
    if 12 in pivot.columns:
        pivot = pivot.loc[:, [c for c in pivot.columns if c <= 11]]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    cmap = LinearSegmentedColormap.from_list("blue", ["#eff6ff", COLOR_TABLEAU_BLUE])
    im = ax.imshow(pivot.values, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([f"+{c}" for c in pivot.columns])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([d.strftime("%Y-%m") for d in pivot.index])
    ax.set_title("コホート分析: 初回乗車月 × 経過月別のアクティブ車両数",
                 fontsize=12, weight="bold", pad=12)
    ax.set_xlabel("経過月", color=COLOR_TEXT_MUTED, fontsize=9)
    ax.set_ylabel("コホート (初回乗車月)", color=COLOR_TEXT_MUTED, fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.7, label="ユニーク車両数")
    save(fig, "12-lod/cohort-heatmap.png")


# ============================================================
# 12: FIXED vs aggregate
# ============================================================
def chart_fixed_vs_aggregate(conn):
    """同じビュー粒度で、通常 SUM と FIXED の値を比較する。"""
    df = query_df(conn, """
        SELECT "company", "payment_type",
               SUM("trip_total") AS view_sum
        FROM "Extract"."Extract"
        WHERE "trip_total" > 0 AND "company" IS NOT NULL AND "payment_type" IS NOT NULL
        GROUP BY "company", "payment_type"
    """)
    company_total = df.groupby("company")["view_sum"].sum().sort_values(ascending=False)
    top5 = company_total.head(5).index.tolist()
    df = df[df["company"].isin(top5)]
    df["fixed_company_total"] = df["company"].map(company_total)

    pay_top = df["payment_type"].value_counts().nlargest(3).index.tolist()
    df = df[df["payment_type"].isin(pay_top)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    # Left: view SUM (会社×支払方法)
    pivot1 = df.pivot(index="company", columns="payment_type", values="view_sum").reindex(top5)[pay_top].fillna(0)
    pivot1.plot(kind="bar", stacked=True, ax=axes[0],
                color=TABLEAU_PALETTE[:len(pay_top)], width=0.65, zorder=2)
    style_ax(axes[0], "通常集計: SUM(trip_total)", ylabel="USD")
    axes[0].set_xticklabels(top5, rotation=30, ha="right")
    axes[0].legend(title="payment_type", fontsize=8, frameon=False)

    # Right: FIXED LOD (同じビュー粒度でも company 単位で固定)
    pivot2 = df.pivot(index="company", columns="payment_type", values="fixed_company_total").reindex(top5)[pay_top].fillna(0)
    pivot2.plot(kind="bar", stacked=False, ax=axes[1],
                color=[COLOR_TABLEAU_GREEN] * len(pay_top), width=0.65, zorder=2, legend=False)
    style_ax(axes[1], "{ FIXED [company] : SUM(trip_total) }", ylabel="USD")
    axes[1].set_xticklabels(top5, rotation=30, ha="right")
    axes[1].set_title("{ FIXED [company] : SUM(trip_total) }\n同じ値が各 payment_type で繰り返される",
                      fontsize=11, weight="bold", pad=12)

    fig.suptitle("通常集計 vs FIXED LOD (会社 × 支払方法)", fontsize=13, weight="bold", y=1.02)
    save(fig, "12-lod/fixed-vs-aggregate.png")


# ============================================================
# 13: histogram
# ============================================================
def chart_histogram(conn):
    df = query_df(conn, """
        SELECT "trip_miles"
        FROM "Extract"."Extract"
        WHERE "trip_miles" > 0 AND "trip_miles" < 30
    """)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bins = np.arange(0, 30.5, 1)
    ax.hist(df["trip_miles"], bins=bins, color=COLOR_TABLEAU_BLUE,
            edgecolor="white", linewidth=0.8, zorder=2)
    style_ax(ax, "trip_miles の度数分布 (ビン幅 1 マイル)",
             xlabel="乗車距離 (mile)", ylabel="乗車件数")
    save(fig, "13-parameters-sets/histogram.png")


# ============================================================
# main
# ============================================================
def main():
    print(f"Opening {HYPER}")
    with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(endpoint=hyper.endpoint, database=str(HYPER)) as conn:
            chart_bar_top10(conn)
            chart_line_monthly(conn)
            chart_scatter(conn)
            chart_heatmap(conn)
            chart_map(conn)
            chart_yoy(conn)
            chart_fare_band(conn)
            chart_avg_vs_median(conn)
            chart_index_top5(conn)
            chart_moving_average(conn)
            chart_cohort_heatmap(conn)
            chart_fixed_vs_aggregate(conn)
            chart_histogram(conn)
    print("\nAll data charts generated.")


if __name__ == "__main__":
    main()
