"""
按 components.json 重新生成两份 README 里「当前收录的组件」表。

表不手写：别名以 components.json 为准，表从它生成，就不会和 App 实际搜的词对不上。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REGISTRY = Path("components.json")

# (文件, 标题, 表头, 分隔行, 没写别名时显示的内容)
TARGETS = [
    ("README.md", "## 📋 当前收录的组件", "| 组件仓库 | 搜索别名 |", "|---------|---------|", "—"),
    ("README_EN.md", "## 📋 Currently Listed Components", "| Component Repository | Search Aliases |", "|---------------------|----------------|", "—"),
]


def load_entries() -> list[tuple[str, list[str]]]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries: list[tuple[str, list[str]]] = []
    for item in data:
        if isinstance(item, str):
            repo, names = item.strip(), []
        elif isinstance(item, dict):
            repo = str(item.get("repo", "")).strip()
            names = []
            # aliases 和 schools 两个键都认，合并去重
            for key in ("aliases", "schools"):
                for value in item.get(key, []):
                    name = str(value).strip()
                    if name and name not in names:
                        names.append(name)
        else:
            continue
        if repo:
            entries.append((repo, names))
    return entries


def build_table(entries, header: str, separator: str, empty_text: str) -> str:
    rows = [header, separator]
    for repo, names in entries:
        link = f"[{repo}](https://github.com/{repo})"
        listed = " / ".join(names) if names else empty_text
        rows.append(f"| {link} | {listed} |")
    return "\n".join(rows)


def replace_table(text: str, heading: str, table: str) -> str:
    # 从标题后的第一张表吃到表格结束，其余内容原样保留
    pattern = re.compile(
        re.escape(heading) + r"\n\n(?:\|.*\n)+",
        re.MULTILINE,
    )
    if not pattern.search(text):
        raise SystemExit(f"找不到 {heading} 下的表格，README 结构变了？")
    return pattern.sub(f"{heading}\n\n{table}\n", text, count=1)


def main() -> int:
    entries = load_entries()
    changed = False
    for filename, heading, header, separator, empty_text in TARGETS:
        path = Path(filename)
        original = path.read_text(encoding="utf-8")
        updated = replace_table(original, heading, build_table(entries, header, separator, empty_text))
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"updated {filename}")
            changed = True
        else:
            print(f"{filename} already up to date")
    print("changed" if changed else "no changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
