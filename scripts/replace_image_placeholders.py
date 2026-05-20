"""
img-placeholder ブロックを Markdown 画像構文に自動置換する。

使い方:
    python scripts/replace_image_placeholders.py            # 実行
    python scripts/replace_image_placeholders.py --dry-run  # 変更内容を表示するだけ

動作:
    docs/<章ID>/index.md 内の <div class="img-placeholder">...</div> ブロックを走査し、
    指定されたパス (docs/public/images/<章ID>/<file>.png) に画像ファイルが存在すれば、
    そのブロックを ![caption](/images/<章ID>/<file>.png) という Markdown 構文に置き換える。

    画像がまだ無いプレースホルダはそのまま残す。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# img-placeholder ブロックの正規表現
PLACEHOLDER_RE = re.compile(
    r'<div class="img-placeholder">\s*'
    r'<span class="img-placeholder-tag">画像予定</span>\s*'
    r'<span class="img-placeholder-caption">(?P<caption>[^<]+)</span>\s*'
    r'<span class="img-placeholder-path">docs/public/(?P<path>images/[^<]+)</span>\s*'
    r'</div>',
    re.DOTALL,
)

CHAPTER_DIR_RE = re.compile(r"^\d{2}-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Replace img-placeholders with Markdown image syntax.")
    parser.add_argument("--dry-run", action="store_true", help="変更内容を表示するだけで書き込まない")
    args = parser.parse_args()

    replaced_count = 0
    pending_count = 0
    files_changed = 0

    chapter_dirs = sorted(d for d in DOCS.iterdir() if d.is_dir() and CHAPTER_DIR_RE.match(d.name))

    for chapter_dir in chapter_dirs:
        index_path = chapter_dir / "index.md"
        if not index_path.exists():
            continue

        content = index_path.read_text(encoding="utf-8")
        original = content
        local_replaced = 0
        local_pending = 0

        def repl(m: re.Match) -> str:
            nonlocal local_replaced, local_pending
            caption = m.group("caption").strip()
            rel_path = m.group("path").strip()  # e.g., images/01-basics/foo.png
            abs_path = DOCS / "public" / rel_path
            if abs_path.exists():
                local_replaced += 1
                return f"![{caption}](/{rel_path})"
            else:
                local_pending += 1
                return m.group(0)

        new_content = PLACEHOLDER_RE.sub(repl, content)

        replaced_count += local_replaced
        pending_count += local_pending

        if new_content != original:
            files_changed += 1
            marker = "[DRY-RUN]" if args.dry_run else "[WRITE]"
            print(f"{marker} {chapter_dir.name}: {local_replaced} replaced, {local_pending} pending")
            if not args.dry_run:
                index_path.write_text(new_content, encoding="utf-8")
        elif local_pending > 0:
            print(f"[SKIP]  {chapter_dir.name}: 0 replaced, {local_pending} pending (no image files yet)")

    print()
    print("=" * 50)
    print(f"Files changed   : {files_changed}")
    print(f"Placeholders -> images : {replaced_count}")
    print(f"Still pending   : {pending_count}")
    if args.dry_run:
        print("(dry-run, no files were written)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
