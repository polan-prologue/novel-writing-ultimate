#!/usr/bin/env python3
"""
novel-writing-skill: gen-character-card.py
生成角色卡片（引用 character-design.md 的完整模板结构）
输出含：表层人设/深层欲望/致命缺陷/人物弧光/关系网络/角色事件线

用法: python3 gen-character-card.py <项目路径> <角色名> [--force]
"""
import sys, json, argparse
from pathlib import Path
from datetime import datetime

CARD_TEMPLATE = """# 角色档案: {name}

## 表层人设

- **身份/职业**:
- **年龄**: （ ）
- **性别**: （男/女）
- **外貌**: （体型、五官、衣着、气质，2-3句话）
- **性格标签**: （2-4个关键词，如 坚毅/腹黑/莽撞/沉默）
- **口头禅/习惯动作**:
- **社交状态**: （话多/寡言/社恐/社牛）

---

## 深层欲望

> **核心动机**:
> （角色最想要什么？为什么？这和主线冲突有什么关系？）

---

## 致命缺陷

> **性格/能力短板**:
> （这个缺陷如何影响剧情走向？何时会成为危机？）

---

## 人物弧光

- **开篇状态**: （起点：弱小/懵懂/偏执/迷失？）
- **经历什么**: （关键转折事件，3-5个节点）
- **结局状态**: （终点：强大/觉醒/牺牲/释然？）

---

## 核心数据

| 维度 | 描述 |
|------|------|
| 擅长 | |
| 短板 | |
| 恐惧 | |
| 执念 | |
| 阴影 | |

---

## 关系网络

| 角色名 | 关系类型 | 对{name}的影响 | 剧情权重 |
|--------|----------|---------------|:--------:|
| | | | % |
| | | | % |

---

## 角色事件线

| 章节 | 事件 | 对角色影响 |
|:----:|:----|:-----------|
| ch001 | | |
| | | |

---

## 角色层级与定位

- **角色层级**: （核心主角/重要配角/阶段性反派/功能角色/路人）
- **预计戏份**: （%）
- **阵营**: （正/邪/中立/亦正亦邪）
- **登场章节**: （chXXX）

---

*卡片生成: {time}*
"""


def main():
    parser = argparse.ArgumentParser(description="生成角色卡片")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("name", help="角色名")
    parser.add_argument("--force", action="store_true", help="覆盖已有卡片")
    args = parser.parse_args()
    project_path = Path(args.project_path)
    meta_file = project_path / "novel.json"
    if not meta_file.exists():
        print(f"[错误] 未找到项目文件: {meta_file}")
        sys.exit(1)
    chars_dir = project_path / "characters"
    chars_dir.mkdir(exist_ok=True)
    out_file = chars_dir / f"{args.name}.md"
    if out_file.exists() and not args.force:
        print(f"[警告] 角色卡片已存在: {out_file}")
        return
    content = CARD_TEMPLATE.format(
        name=args.name,
        time=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    out_file.write_text(content, encoding="utf-8")
    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)
    if args.name not in meta["characters"]:
        meta["characters"].append(args.name)
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"[OK] 角色卡片已生成: {out_file.resolve()}")
    print(f"     内容长度: {len(content)} 字符 | 字段数: 8 (含表层/深层/缺陷/弧光/核心/关系/事件/层级)")


if __name__ == "__main__":
    main()
