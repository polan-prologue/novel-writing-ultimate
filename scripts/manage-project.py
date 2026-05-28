#!/usr/bin/env python3
"""
novel-writing-skill: manage-project.py
初始化/管理小说项目结构。

用法:
  python3 manage-project.py init <项目名> [--author <作者>] [--genre <类型>]
  python3 manage-project.py chapter <项目路径> <章节号> [--title <标题>]
  python3 manage-project.py status <项目路径>
"""
import sys, os, json, argparse
from datetime import datetime
from pathlib import Path

PROJECT_FILE = "novel.json"

def cmd_init(args):
    root = Path(args.name)
    if root.exists():
        print(f"[错误] 目录 '{args.name}' 已存在")
        sys.exit(1)
    root.mkdir(parents=True)
    (root / "chapters").mkdir()
    (root / "characters").mkdir()
    meta = {
        "name": args.name,
        "author": args.author or "",
        "genre": args.genre or "",
        "created": datetime.now().isoformat(),
        "chapters": [],
        "characters": [],
        "world_building": [],
        "timeline": []
    }
    with open(root / PROJECT_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"[OK] 小说项目 '{args.name}' 已创建于 {root.resolve()}")

def cmd_chapter(args):
    root = Path(args.project_path)
    meta_path = root / PROJECT_FILE
    if not meta_path.exists():
        print(f"[错误] 未找到项目文件: {meta_path}")
        sys.exit(1)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    ch_file = root / "chapters" / f"ch{int(args.number):03d}.md"
    if ch_file.exists():
        print(f"[警告] 章节文件已存在: {ch_file}，跳过创建")
        return
    title = args.title or f"第{args.number}章"
    content = f"# {title}\n\n"
    ch_file.write_text(content, encoding="utf-8")
    ch_entry = {"number": int(args.number), "title": title, "file": str(ch_file.relative_to(root))}
    if ch_entry not in meta["chapters"]:
        meta["chapters"].append(ch_entry)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"[OK] 章节已创建: {ch_file.resolve()}")

def cmd_status(args):
    root = Path(args.project_path)
    meta_path = root / PROJECT_FILE
    if not meta_path.exists():
        print(f"[错误] 未找到项目文件: {meta_path}")
        sys.exit(1)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    print(f"项目: {meta['name']}")
    print(f"作者: {meta['author'] or '(未设置)'}")
    print(f"类型: {meta['genre'] or '(未设置)'}")
    print(f"创建时间: {meta['created']}")
    print(f"章节数: {len(meta['chapters'])}")
    print(f"角色数: {len(meta['characters'])}")
    for ch in sorted(meta["chapters"], key=lambda x: x["number"]):
        print(f"  [{ch['number']:03d}] {ch['title']}")

def main():
    parser = argparse.ArgumentParser(description="小说项目管理工具")
    sub = parser.add_subparsers(dest="command")
    p_init = sub.add_parser("init", help="初始化新小说项目")
    p_init.add_argument("name", help="项目名")
    p_init.add_argument("--author", default="", help="作者")
    p_init.add_argument("--genre", default="", help="小说类型")
    p_ch = sub.add_parser("chapter", help="新建章节")
    p_ch.add_argument("project_path", help="项目路径")
    p_ch.add_argument("number", help="章节号")
    p_ch.add_argument("--title", default="", help="章节标题")
    p_st = sub.add_parser("status", help="查看项目状态")
    p_st.add_argument("project_path", help="项目路径")
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    {"init": cmd_init, "chapter": cmd_chapter, "status": cmd_status}[args.command](args)

if __name__ == "__main__":
    main()
