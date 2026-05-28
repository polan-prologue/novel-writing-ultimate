# 项目文件管理

## 项目目录结构

每次启动完整创作项目，自动生成以下结构：

```
项目名/
├── novel.json              # 项目元数据（标题/类型/篇幅/更新时间）
├── concept.md              # 创意概念（核心卖点/一句话简介）
├── outline.md              # 完整大纲（四幕结构+章节简表）
├── timeline.md             # 时间线（重大事件时间轴）
├── characters/
│   ├── 主角.md             # 主角人设卡片
│   ├── 配角.md             # 配角人设卡片
│   └── 反派.md             # 反派人设卡片
└── chapters/
    ├── ch001.md            # 第一章
    ├── ch002.md            # 第二章
    └── ...
```

## 元数据文件 (novel.json)

```json
{
  "title": "书名",
  "genre": "类型",
  "subGenres": ["子类型1", "子类型2"],
  "sellingPoint": "核心卖点",
  "length": "短篇|中篇|长篇|超长篇",
  "perspective": "视角",
  "tone": "文风基调",
  "totalChapters": 10,
  "status": "创作中|已完成",
  "createdAt": "2024-01-01",
  "updatedAt": "2024-01-01"
}
```

## 大纲模板 (outline.md)

按四幕结构组织，每章包含：序号/标题/核心事件/章末钩子/字数

```
# 《书名》- 大纲

## 第一幕：开端（第1-X章）

| 章 | 标题 | 核心事件 | 钩子 | 字数 |
|----|------|---------|------|------|
| 1 | xxx | xxx | xxx | 3000 |

## 第二幕：发展（第X-Y章）

...

## 第三幕：高潮（第Y-Z章）

...

## 第四幕：结局（第Z-结尾）

...
```

## 项目操作

### 初始化项目
```bash
python scripts/manage-project.py init <项目名>
```

### 创建章节
```bash
python scripts/manage-project.py chapter <项目路径> <章节序号>
```

### 校验项目
```bash
python scripts/consistency-check.py --project <项目路径>
python scripts/punctuation_check.py --input <章节文件>
```

## 章节命名规范

- 文件名: ch001.md, ch002.md, ...
- 文件头自动包含：章号、标题、五段结构表
- 每章字数：短篇 2000-3000，中篇 3000-5000，长篇 3000-5000
