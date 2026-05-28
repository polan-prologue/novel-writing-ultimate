#!/usr/bin/env python3
"""
novel-writing-skill: gen-timeline.py
管理/生成故事时间线 Markdown 文件。
用法:
  python3 gen-timeline.py init <项目路径>                  # 初始化时间线文件
  python3 gen-timeline.py add <项目路径> <事件> [--time <时间点>]  # 添加事件
  python3 gen-timeline.py render <项目路径>               # 渲染为时间线 Markdown
"""
import sys, os, json, argparse
from pathlib import Path
from datetime import datetime

TIMELINE_FILE = "timeline.json"

def cmd_init(args):
    root = Path(args.project_path)
    tl = {"events": [], "created": datetime.now().isoformat()}
    with open(root / TIMELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(tl, f, ensure_ascii=False, indent=2)
    print(f"[OK] 时间线已初始化: {(root / TIMELINE_FILE).resolve()}")

def cmd_add(args):
    root = Path(args.project_path)
    tl_path = root / TIMELINE_FILE
    if not tl_path.exists():
        print(f"[错误] 未找到时间线文件，请先运行 init")
        sys.exit(1)
    with open(tl_path, "r", encoding="utf-8") as f:
        tl = json.load(f)
    event = {"time": args.time or "(未设定)", "description": args.event, "added": datetime.now().isoformat()}
    tl["events"].append(event)
    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(tl, f, ensure_ascii=False, indent=2)
    print(f"[OK] 事件已添加")

def cmd_render(args):
    root = Path(args.project_path)
    tl_path = root / TIMELINE_FILE
    if not tl_path.exists():
        print(f"[错误] 未找到时间线文件")
        sys.exit(1)
    with open(tl_path, "r", encoding="utf-8") as f:
        tl = json.load(f)
    lines = ["# 故事时间线\n", f"*创建于: {tl['created']}*\n", "---\n"]
    for i, ev in enumerate(tl["events"], 1):
        lines.append(f"### 事件 {i}: {ev['description']}")
        lines.append(f"- **时间点**: {ev['time']}")
        lines.append("")
    out = root / "timeline.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] 时间线已渲染: {out.resolve()}")

def main():
    parser = argparse.ArgumentParser(description="故事时间线管理工具")
    sub = parser.add_subparsers(dest="command")
    p_init = sub.add_parser("init", help="初始化时间线")
    p_init.add_argument("project_path")
    p_add = sub.add_parser("add", help="添加事件")
    p_add.add_argument("project_path")
    p_add.add_argument("event", help="事件描述")
    p_add.add_argument("--time", default="", help="时间点")
    p_rd = sub.add_parser("render", help="渲染时间线 Markdown")
    p_rd.add_argument("project_path")
    args = parser.parse_args()
    if not args.command:
        parser.print_help(); sys.exit(1)
    {"init": cmd_init, "add": cmd_add, "render": cmd_render}[args.command](args)

if __name__ == "__main__":
    main()
