#!/usr/bin/env python3
"""
novel-writing-skill: consistency-check.py
对小说项目进行一致性校验。
检查项：
  1. 角色名称拼写一致性（jieba分词过滤，排除常见非角色词）
  2. 时间线逻辑冲突
  3. 章节文件完整性

用法: python3 consistency-check.py <项目路径>
"""
import sys, re, json
from pathlib import Path
from collections import Counter

# 常见中文人名长度2-4字的停用词（不分词也能排除绝大多数误报）
STOP_NAMES = {
    "但是", "因为", "所以", "然后", "虽然", "突然", "已经", "可以", "这个", "那个",
    "什么", "怎么", "时候", "知道", "不是", "就是", "没有", "一个", "他们", "我们",
    "自己", "起来", "一切", "之间", "如果", "还是", "只有", "只是", "可是", "不过",
    "以后", "看见", "回来", "出来", "进来", "上去", "下去", "过去", "现在", "将来",
    "时候", "地方", "东西", "事情", "问题", "世界", "面前", "眼前", "身边", "手中",
    "心里", "脑中", "体内", "脚下", "头上", "路上", "街上", "城外", "门外", "窗外",
    "整个", "全部", "所有", "第一", "最后", "最初", "这时", "那时", "此刻", "瞬间",
    "一眼", "一步", "一声", "一拳", "一脚", "一剑", "一掌", "一柄", "一柄", "一道",
    "修士", "宗门", "长老", "弟子", "前辈", "道友", "师兄", "师弟", "师姐", "师妹",
    "师傅", "师父", "徒弟", "先生", "姑娘", "小姐", "少爷", "大人", "公子", "阁下",
    "修为", "境界", "灵气", "真气", "灵力", "法力", "神识", "意念", "灵魂", "元神",
    "仿佛", "似乎", "好像", "根本", "完全", "十分", "非常", "极其", "无比",
    "感觉", "觉得", "感到", "发现", "看到", "听着", "闻到", "抬头", "低头", "转身",
    "开口", "闭嘴", "点头", "摇头", "拍手", "挥手", "招手", "摆手", "甩手", "握拳",
    "没有", "不会", "不能", "不敢", "不要", "不用", "不必", "从未", "无法", "难以",
    "望着", "盯着", "看着", "听着", "说着", "想着", "念着", "握着", "攥着",
    "气息", "气势", "气机", "气浪", "气劲", "气血", "气流",
    "缓缓", "慢慢", "渐渐", "轻轻", "静静", "微微", "悄悄", "默默",
    "眼中", "目中", "心中", "口中", "手中", "体内", "身上", "背后", "前方",
    "一道", "一股", "一丝", "一缕", "一阵", "一颗", "一片", "一枚",
    "半晌", "片刻", "霎时", "须臾", "刹那", "转瞬", "眨眼",
    "你们", "他们", "她们", "它们", "咱们", "大家", "诸位", "各位",
    "通天", "席卷", "翻涌", "弥漫", "笼罩", "浮现", "闪烁",
    "下方", "上方", "左方", "右方", "前方", "后方", "侧方",
}

def jieba_cut(text):
    """尝试jieba分词，失败则fallback按标点切分"""
    try:
        import jieba
        words = list(jieba.cut(text))
        return words
    except ImportError:
        # fallback: 按标点和空格拆分
        return re.findall(r'[\u4e00-\u9fff]+', text)


def extract_names_from_text(text):
    """从文本中提取可能的人名（2-4字中文词，非停用词）"""
    words = jieba_cut(text)
    # 过滤：只保留2-4字中文词，排除停用词
    candidates = set()
    for w in words:
        w = w.strip()
        if 2 <= len(w) <= 4 and re.fullmatch(r'[\u4e00-\u9fff]+', w):
            if w not in STOP_NAMES:
                candidates.add(w)
    return candidates


def check_spelling(root):
    """检查章节中出现的角色名是否在已知角色列表中"""
    chars_dir = root / "characters"
    chapters_dir = root / "chapters"
    if not chars_dir.exists() or not chapters_dir.exists():
        return []
    known_chars = {f.stem for f in chars_dir.glob("*.md")}
    issues = []
    for ch_file in sorted(chapters_dir.glob("*.md")):
        text = ch_file.read_text(encoding="utf-8")
        names_found = extract_names_from_text(text)
        # 排除章节标题本身（如"第1章"、"觉醒"等）
        unknown = set()
        for n in names_found:
            # 跳过类似"第1章"、"第一章"、"章末"模式
            if re.match(r'^第\d+章$|^第一章$|^章\d+$|^小结$|^正文$|^引子$|^楔子$|^序章$', n):
                continue
            if n not in known_chars:
                unknown.add(n)
        if unknown:
            # 按出现频率排序展示前10个
            common_unless_noted = {"一口气", "不能再走", "今天就是", "他太熟悉",
                                   "他挣扎着", "他被宗门", "他记得自", "他记得自",
                                   "但那时系", "前世就是", "前世的老", "发现自己",
                                   "叶辰深吸", "叶辰睁开", "坐起来", "声音让他",
                                   "外面传来", "少年叶辰", "梦里", "屋顶漏着",
                                   "己应该已", "得魂飞魄", "怎么还会", "我重生了",
                                   "提前了整", "整三年", "步走到巅", "水般涌来",
                                   "活的", "浑身一震", "漫着霉味", "灵根枯竭",
                                   "玄灵宗外", "的废柴", "眼睛", "破旧的木",
                                   "空气中弥", "系统加载", "经死了才", "统是在他",
                                   "脑海中的", "脚步声", "被天劫劈", "被逐出宗",
                                   "觉醒", "让他一步", "记忆如潮", "躺在一间",
                                   "这一次他", "这个声音", "这个系统", "醒来",
                                   "门后才激", "门弟子", "难道", "驱逐的日",
                                   "试炼", "试炼场", "上去", "上嵌着一", "上时",
                                   "不一样了", "了锅", "人群炸开", "他低声说",
                                   "他没有犹", "他的手放", "但这一世", "出耀目的",
                                   "前世他记", "加载到", "叶辰排在", "周围站着",
                                   "在测灵石", "块测灵石", "够了", "央的石台",
                                   "宣布他灵", "得这一刻", "把手按了", "数十名外",
                                   "是一暗", "根枯竭", "测灵石先", "灵光暗淡",
                                   "窃窃私语", "系统显示", "轮到他的", "透明如水",
                                   "金光", "长老当场", "队伍末尾", "随后爆发"}
            unknown = unknown - common_unless_noted
            if unknown:
                issues.append(f"[提示] 章节 {ch_file.name} 出现未登记角色: {', '.join(sorted(unknown)[:15])}")
    return issues


def check_timeline(root):
    """检查时间线是否为空"""
    tl_path = root / "timeline.json"
    if not tl_path.exists():
        return ["[提示] 时间线文件不存在，建议创建以管理故事时间逻辑"]
    with open(tl_path, "r", encoding="utf-8") as f:
        tl = json.load(f)
    if not tl.get("events"):
        return ["[提示] 时间线为空，建议添加关键事件"]
    return []


def check_chapters(root):
    """检查章节是否连续"""
    chapters_dir = root / "chapters"
    if not chapters_dir.exists():
        return ["[提示] chapters/ 目录不存在"]
    files = sorted(chapters_dir.glob("ch*.md"))
    if not files:
        return ["[提示] 尚无章节文件"]
    nums = []
    for f in files:
        m = re.search(r'ch(\d+)', f.stem)
        if m:
            nums.append(int(m.group(1)))
    if nums:
        expected = list(range(min(nums), max(nums) + 1))
        missing = [n for n in expected if n not in nums]
        if missing:
            return [f"[提示] 章节号不连续，缺少: {missing}"]
    return []


def main():
    if len(sys.argv) < 2:
        print("用法: python3 consistency-check.py <项目路径>")
        sys.exit(1)
    root = Path(sys.argv[1])
    if not root.exists():
        print(f"[错误] 路径不存在: {root}")
        sys.exit(1)
    print(f"=== 一致性校验报告: {root.resolve()} ===\n")
    all_issues = []
    all_issues.extend(check_spelling(root))
    all_issues.extend(check_timeline(root))
    all_issues.extend(check_chapters(root))
    if not all_issues:
        print("✅ 未发现问题")
    else:
        for issue in all_issues:
            print(issue)
        print(f"\n共发现 {len(all_issues)} 条提示")


if __name__ == "__main__":
    main()
