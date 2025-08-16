#!/usr/bin/env python3
import os
import re
import sys
import argparse
from collections import defaultdict

def _ensure_utf8_windows():
    try:
        if os.name == "nt":
            if sys.stdout.encoding.lower() != "utf-8":
                sys.stdout.reconfigure(encoding="utf-8")
            if sys.stderr.encoding.lower() != "utf-8":
                sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def naturalsort_key(s: str):
    # 数字を含む名前を自然順に並べる（SCT4.2 < SCT4.10）
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

def label_ext(ext: str) -> str:
    return f".{ext.lstrip('.').lower()}" if ext else "noext"

def print_tree_item(name: str, prefix: str, is_last: bool):
    connector = "└── " if is_last else "├── "
    print(prefix + connector + name)

def smart_tree(root: str, threshold: int = 20, head: int = 3, tail: int = 3,
               show_hidden: bool = True, max_level: int = 0):
    """
    threshold  : この数を超える拡張子グループを中略表示
    head/tail  : 中略時に先頭/末尾に残す件数
    show_hidden: 隠しファイル/ディレクトリも表示 (既定 True)
    max_level  : 表示最大階層 (0 = 無制限) —— ディレクトリ名は出し、再帰だけ制限
    """
    root = os.path.abspath(root)

    def walk(dirpath: str, prefix: str = "", level: int = 1):
        try:
            entries = os.listdir(dirpath)
        except PermissionError:
            print(prefix + "└── <permission denied>")
            return

        if not show_hidden:
            entries = [e for e in entries if not e.startswith('.')]

        # 明示ソート（自然順）
        dirs  = sorted([e for e in entries if os.path.isdir(os.path.join(dirpath, e))], key=naturalsort_key)
        files = sorted([e for e in entries if os.path.isfile(os.path.join(dirpath, e))], key=str.lower)

        # 1) ディレクトリは1つずつ表示して即再帰（深さ優先）
        for i, d in enumerate(dirs):
            # このレベルで後にファイルが残っていれば、最後のディレクトリでも is_last=False
            is_last_dir = (i == len(dirs) - 1) and (len(files) == 0)
            print_tree_item(d + "/", prefix, is_last_dir)

            # 再帰は level 制限に従う
            if not max_level or level < max_level:
                new_prefix = prefix + ("    " if is_last_dir else "│   ")
                walk(os.path.join(dirpath, d), new_prefix, level + 1)

        # 2) 直下のファイル（拡張子ごとに中略）
        if files:
            groups = defaultdict(list)
            for f in files:
                ext = os.path.splitext(f)[1][1:].lower()
                groups[ext].append(f)

            group_keys = sorted(groups.keys(), key=lambda e: (e != "", e))
            for gi, ext in enumerate(group_keys):
                group_files = sorted(groups[ext], key=naturalsort_key)
                count = len(group_files)
                ext_tag = label_ext(ext)

                if count > threshold and head + tail < count:
                    shown = group_files[:head] + [f"... ({count} {ext_tag} files total)"] + group_files[-tail:]
                else:
                    shown = group_files

                for fi, f in enumerate(shown):
                    if isinstance(f, str) and f.startswith("..."):
                        # 省略行は罫線なしで明示
                        print(prefix + "    " + f)
                    else:
                        is_last_file = (gi == len(group_keys) - 1 and fi == len(shown) - 1)
                        print_tree_item(f, prefix, is_last_file)

    root_name = os.path.basename(root.rstrip(os.sep)) or root
    print(root_name + "/")
    walk(root, "", 1)

def main(argv=None):
    _ensure_utf8_windows()
    p = argparse.ArgumentParser(description="tree2: 拡張子ごとに大量ファイルを中略するツリー表示（深さ優先）")
    p.add_argument("root", nargs="?", default=".", help="対象ディレクトリ（既定: .）")
    p.add_argument("--threshold", "-t", type=int, default=10,
                   help="この数を超える拡張子グループは中略（例: 10なら11個以上で省略）")
    p.add_argument("--head", type=int, default=3, help="中略時に先頭に残す件数（既定: 3）")
    p.add_argument("--tail", type=int, default=2, help="中略時に末尾に残す件数（既定: 2）")
    p.add_argument("--level", "-L", type=int, default=0, help="表示最大階層（0=無制限）")
    p.add_argument("--no-hidden", dest="hidden", action="store_false",
                   help="隠しファイル・ディレクトリを非表示にする（既定は表示）")
    args = p.parse_args(argv)
    smart_tree(args.root, args.threshold, args.head, args.tail, args.hidden, args.level)

if __name__ == "__main__":
    main()
