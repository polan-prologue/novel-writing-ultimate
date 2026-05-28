# novel-writing-ultimate

> **全能小说创作宗师** — 一个基于 Qoder/OpenClaw Agent 的全流程小说创作 Skill

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Qoder-Skill-orange)](#)

融合 RPG 四层架构（装备 / 主动技能 / 被动技能 / 状态栏）+ 双轨创作模式 + 三键全局导航，从灵感火花到完稿发布的全流程覆盖。配备 6 个 Python 自动化脚本、9 份创作参考文档、4 套实用模板，助你高效创作。

---

## 目录

- [核心特色](#核心特色)
- [功能矩阵](#功能矩阵)
- [文件结构](#文件结构)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [脚本工具说明](#脚本工具说明)
- [技术依赖](#技术依赖)
- [许可证](#许可证)

---

## 核心特色

| 特色 | 说明 |
|:----:|------|
| 🛡️ **完整创作体系** | RPG 四层架构覆盖从设定到完稿的每一环节 |
| 🚀 **双轨创作模式** | 灵感发散式（自由创作） / 系统引导式（结构化写作） |
| 🔧 **6 个自动化脚本** | 质检、一致性校验、人物卡片生成、时间线管理等 |
| 📚 **9 份参考文档** | 涵盖人设、剧情、世界观、文风、质检等全方位知识库 |
| 🎯 **主动技能系统** | 钩子、伏笔、反转、爽点等技巧快捷键触发 |
| ⚡ **被动技能链** | 质检 → 结语 → 保存 → 润色 → 连击 → 推送 自动化 |
| 🛡️ **避雷审查系统** | 7 类红线自动检测，规避创作风险 |
| 🔄 **自我升级机制** | 创作数据复盘驱动自身迭代优化 |

---

## 功能矩阵

### 装备层 — 基础框架

| 模块 | 说明 |
|:----:|------|
| **双轨入口 A/B** | 灵感发散式（自由输出）/ 系统引导式（结构化提问） |
| **7步引导** | 类型 → 卖点 → 主角 → 视角 → 篇幅 → 文风 → 金手指 |
| **设计装备组** | 人物设计 / 世界观构建 / 剧情编排 深度补充 |
| **冲突检测** | 4 类设定冲突自动检测，避免逻辑漏洞 |

### 主动技能 — 创作技法

| 类别 | 快捷键 | 技能 | 说明 |
|:----:|:-----:|:----:|------|
| 技巧系 | `Q` | 钩子 | 快速设计章节开篇钩子 |
| 技巧系 | `W` | 伏笔 | 埋设前后呼应的伏笔 |
| 技巧系 | `E` | 反转 | 设计剧情反转桥段 |
| 技巧系 | `R` | 爽点 | 构建高潮爽点段落 |
| 学习系 | `A` | 套路 | 分析经典叙事套路 |
| 学习系 | `S` | 方法 | 传授创作方法论 |
| 学习系 | `D` | 解构 | 深度解构范文结构 |
| 学习系 | `F` | 文风 | 分析目标文风特征 |
| 学习系 | `G` | 仿写 | 仿写指定风格段落 |
| 学习系 | `H` | 文库 | 查询参考文库 |
| 修改系 | `Z` | 续写 | 根据前文续写内容 |
| 修改系 | `X` | 扩写 | 扩充简略段落 |
| 修改系 | `C` | 改写 | 按需求改写段落 |
| 修改系 | `V` | 填补 | 填补剧情逻辑空缺 |

### 被动技能 — 自动执行

```
质检 → 结语 → 保存 → 润色 → COMBO(连击) → 推送
```

每完成一个章节创作，自动链式触发以上流程，确保输出质量。

### 避雷系统

检测以下 7 类红线内容：
政治敏感 · 色情违规 · 暴力血腥 · 宗教争议 · 侵权风险 · 价值观偏离 · 不当影射

---

## 文件结构

```
novel-writing-ultimate/
│
├── SKILL.md                        # 核心技能定义文档（932行）
├── README.md                       # 本文件
├── .gitattributes
├── .gitignore
│
├── scripts/                        # 6 个Python自动化脚本
│   ├── quality-check.py            # 3线17项全面质检
│   ├── consistency-check.py        # 一致性校验（基于jieba分词）
│   ├── punctuation_check.py        # 中文标点符号检查
│   ├── gen-character-card.py       # 人物卡片生成（8字段）
│   ├── gen-timeline.py             # 时间线管理
│   └── manage-project.py           # 项目文件管理
│
├── references/                     # 9 份参考文档
│   ├── character-design.md         # 人物设计指南
│   ├── plot-design.md              # 剧情结构设计
│   ├── worldbuilding.md            # 世界观设计
│   ├── advanced-techniques.md      # 高级写作技巧
│   ├── writing-methods.md          # 创作方法论
│   ├── webnovel-analysis.md        # 网文解构分析
│   ├── quality-check.md            # 质检标准
│   ├── style-learning.md           # 文风学习
│   └── project-management.md       # 项目管理规范
│
└── assets/templates/               # 4 套创作模板
    ├── chapter-template.md         # 章节写作模板
    ├── character-card-template.md  # 人物卡模板
    ├── outline-template.md         # 大纲模板
    └── world-building-template.md  # 世界观设定模板
```

---

## 快速开始

### 方式一：作为 Qoder/OpenClaw Agent Skill 使用

```bash
# 1. 克隆到 skills 目录
git clone https://github.com/polan-prologue/novel-writing-ultimate.git ~/.openclaw/skills/novel-writing-ultimate

# 2. 安装依赖
pip install zhon       # 标点检查（必需）
pip install jieba      # 一致性校验（可选，不装则自动降级）

# 3. 在 Agent 中触发
# 说 "写小说" 或 "帮我创作一个故事" 即可启动
```

### 方式二：独立使用脚本工具

```bash
# 质检当前项目
python scripts/quality-check.py

# 生成人物卡片
python scripts/gen-character-card.py

# 管理项目文件
python scripts/manage-project.py
```

---

## 使用指南

### 启动创作

输入任意以下触发词即可开始：

- 「写小说」
- 「帮我创作一个故事」
- 「构思一个剧情」
- 「设计一个人物」

### 双轨创作模式

| 模式 | 适用场景 | 特点 |
|:----:|:--------:|:----:|
| **A式 · 灵感发散** | 已有初步想法 | 自由表达，AI 帮你梳理扩展 |
| **B式 · 系统引导** | 从零开始 | 7 步引导式提问，逐步构建 |

### 状态查看

随时输入 **`状态`** 查看当前项目概况，包括：
- 已完成章节数 & 总字数
- 当前人物列表
- 最新修改记录
- 待办事项

---

## 脚本工具说明

| 脚本 | 功能 | 依赖 |
|:----:|------|:----:|
| `quality-check.py` | 3 线 17 项全方位质量检测（基础/进阶/风格） | zhon |
| `consistency-check.py` | 基于分词的设定一致性校验 | jieba（可选） |
| `punctuation_check.py` | 中文标点符号使用规范检查 | zhon |
| `gen-character-card.py` | 根据描述自动生成 8 字段标准人物卡片 | 无 |
| `gen-timeline.py` | 管理故事时间线和事件排序 | 无 |
| `manage-project.py` | 项目文件组织、备份和版本管理 | 无 |

---

## 技术依赖

| 依赖 | 版本要求 | 用途 | 是否必需 |
|:----:|:--------:|:----:|:--------:|
| Python | ≥ 3.8 | 脚本运行环境 | ✅ |
| `zhon` | 最新 | 中文标点符号检查 | ✅ |
| `jieba` | 最新 | 中文分词 & 一致性校验 | ❌ 可选 |

---

## 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

---

**Happy Writing! ✍️**
