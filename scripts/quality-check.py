#!/usr/bin/env python3
"""
novel-writing-skill: quality-check.py
章节质量检测脚本 - 覆盖SKILL.md要求的3线13项中的11项（除标点外）
输出JSON格式，供被动技能①调用。

检测项：
  🧱 质量线（5项）:
    1. 人设一致性 - 统计角色名出现/对话分配比例
    2. 主线一致性 - 检测是否提到已知主线关键词
    3. 逻辑自洽 - 检测时间/空间/因果关系矛盾
    4. 伏笔追踪 - 检测当前章是否使用伏笔关键词
    5. 战力平衡 - 检测战斗/升级相关词密度

  ⚡ 技法线（5项）:
    1. 章末钩子 - 检测末尾100字有无悬念/疑问/未解词
    2. 冲突密度 - 统计冲突相关词出现频次
    3. 展示非讲述 - 检测"感到/觉得/知道"等抽象词
    4. 字数检查 - 检查字数是否在目标区间
    5. 节奏评估 - 检测段落长短是否参差

  🧹 表达线/AI味（2项）:
    1. AI味浓度检测 - 句式标准差/过渡词/副词/主语重复/情感词/段首重复/修饰词
    2. 同词复现 - 检测高频词重复

用法:
  python3 quality-check.py --chapter <章节文件.md> [--reference <项目路径>] [--out <输出文件.json>]
  python3 quality-check.py --chapter <章节文件.md> --thresholds '{"min_words":1500,"max_words":2500}'
"""
import sys, re, json, argparse, math
from pathlib import Path
from collections import Counter


# ========== 通用工具 ==========

def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def chinese_word_count(text):
    """统计中文字数（不含标点空格）"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def sentences(text):
    """按句号/问号/感叹号/省略号分割句子"""
    return [s.strip() for s in re.split(r'[。！？…\n]+', text) if s.strip()]


def last_n_chars(text, n=100):
    """获取文本末尾n个字符"""
    return text[-n:] if len(text) >= n else text


def count_keywords(text, keywords):
    """统计关键词出现次数"""
    count = 0
    for kw in keywords:
        count += text.count(kw)
    return count


# ========== 质量线检测 ==========

class QualityCheck:
    """🧱 质量线"""

    def check_character_consistency(self, text, known_chars=None):
        """
        人设一致性检测
        统计角色名出现频率，检测对话是否集中在某个角色
        """
        # 提取所有中文2-4字词作为候选角色
        all_candidates = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        counter = Counter(all_candidates)
        # 过滤掉常见非角色词，保留出现≥2次且非停用的
        stop_words = {"但是", "因为", "所以", "然后", "虽然", "突然", "已经",
                       "可以", "这个", "那个", "什么", "怎么", "时候", "知道",
                       "不是", "就是", "没有", "一个", "他们", "我们", "自己",
                       "起来", "一切", "之间", "如果", "还是", "只有", "只是",
                       "可是", "不过", "以后", "看见", "回来", "出来", "进来",
                       "现在", "将来", "地方", "东西", "事情", "问题", "世界",
                       "眼前", "心里", "身上", "脚下", "手中", "面前", "整个",
                       "全部", "所有", "最后", "最初", "这时", "那时", "此刻",
                       "一眼", "一步", "一声", "一拳", "一掌", "一道", "一股",
                       "仿佛", "似乎", "好像", "根本", "完全", "十分", "非常",
                       "极其", "无比", "感觉", "觉得", "感到", "发现", "看到",
                       "抬头", "低头", "转身", "开口", "闭嘴", "点头", "摇头",
                       "没有", "不会", "不能", "不敢", "不要", "不用", "从未",
                       "无法", "望着", "盯着", "看着", "听着", "说着", "想着",
                       "气息", "气势", "缓缓", "慢慢", "渐渐", "轻轻", "静静",
                       "眼中", "目中", "心中", "口中", "手中", "背后", "前方",
                       "一道", "一股", "一丝", "一缕", "一阵", "一颗", "一片",
                       "半晌", "片刻", "刹那", "转瞬", "眨眼",
                       "你们", "他们", "她们", "大家", "诸位", "各位",
                       "下方", "上方", "前方", "后方",
                       "修为", "境界", "灵气", "真气", "灵力", "法力", "神识",
                       "意念", "灵魂", "元神"}
        candidates = {}
        for word, freq in counter.most_common(20):
            if len(word) >= 2 and word not in stop_words and freq >= 2:
                candidates[word] = freq
        # 如果有已知角色列表，判断主要角色是否有戏份
        if known_chars:
            char_appearances = {c: candidates.get(c, 0) for c in known_chars}
            active_chars = [c for c, f in char_appearances.items() if f > 0]
            return {
                "score": "pass" if len(active_chars) >= 1 else "warn",
                "active_chars": active_chars,
                "appearances": char_appearances
            }
        return {
            "score": "pass",
            "detected_names": list(candidates.keys())[:10],
            "top_freqs": candidates
        }

    def check_mainline_consistency(self, text, main_keywords=None):
        """
        主线一致性检测
        如果提供了主线关键词，判断当前章节是否偏离
        """
        if main_keywords:
            hits = [kw for kw in main_keywords if kw in text]
            match_rate = len(hits) / len(main_keywords) if main_keywords else 0
            if match_rate >= 0.3:
                return {"score": "pass", "match_rate": round(match_rate, 2), "hits": hits}
            elif match_rate > 0:
                return {"score": "warn", "match_rate": round(match_rate, 2), "hits": hits}
            else:
                return {"score": "fail", "match_rate": 0, "hits": []}
        return {"score": "pass", "match_rate": None, "hits": []}

    def check_logic(self, text):
        """
        逻辑自洽检测
        检查时间矛盾（如"之后"与"之前"在同一段使用）
        """
        # 检测时间矛盾模式
        conflict_patterns = [
            (r'之后.*之前', "时间顺序矛盾"),
            (r'昨天.*前一天', "时间表述矛盾"),
            (r'又重新.*又回到', "重复动作"),
            (r'同时.*之后', "时间表达冲突"),
        ]
        issues = []
        for pattern, desc in conflict_patterns:
            if re.search(pattern, text):
                issues.append(desc)
        return {"score": "pass" if not issues else "warn", "issues": issues}

    def check_foreshadowing(self, text, foreshadow_keywords=None):
        """
        伏笔追踪检测
        检测当前章节是否使用了前文埋伏笔的关键词
        """
        if foreshadow_keywords:
            hits = [kw for kw in foreshadow_keywords if kw in text]
            return {"score": "pass" if hits else "warn", "hits": hits}
        return {"score": "pass", "hits": []}

    def check_power_balance(self, text):
        """
        战力平衡检测
        检测战斗/升级相关词密度
        """
        battle_words = ["突破", "晋级", "晋升", "打败", "击杀", "斩", "战",
                        "丹药", "法宝", "功法", "修炼", "炼体", "筑基",
                        "金丹", "元婴", "化神", "大乘"]  # 升级相关的有依据
        count = sum(text.count(w) for w in battle_words)
        total_words = chinese_word_count(text)
        density = count / max(total_words, 1) * 1000  # 千字密度
        if density > 20:
            return {"score": "warn", "density": round(density, 1), "detail": "战斗/升级词密度过高，注意节奏"}
        if density > 40:
            return {"score": "fail", "density": round(density, 1), "detail": "战斗/升级词密度极高，战力膨胀风险"}
        return {"score": "pass", "density": round(density, 1), "detail": ""}


class TechniqueCheck:
    """⚡ 技法线"""

    def check_twist(self, text):
        """
        章末钩子检测
        检测末尾150字是否有悬念/疑问/转折
        """
        tail = text[-300:] if len(text) >= 300 else text
        suspense_words = ["?", "？", "突然", "却", "但", "然而", "没想到",
                           "发现", "看到", "什么", "是谁", "为什么",
                           "难道", "究竟", "怎么会", "不可能",
                           "...", "……", "不对劲", "诡异", "异样"]
        hits = [w for w in suspense_words if w in tail]
        return {"score": "pass" if len(hits) >= 2 else "warn", "hits": hits[:5]}

    def check_conflict_density(self, text):
        """
        冲突密度检测
        统计冲突相关词密度
        """
        conflict_words = ["怒", "骂", "杀", "打", "战", "斗", "争",
                          "对质", "对峙", "叫板", "冲", "撞", "砸",
                          "骂", "吼", "冷笑", "咬牙", "握拳"]
        count = sum(text.count(w) for w in conflict_words)
        density = count / max(chinese_word_count(text), 1) * 1000
        if density < 3:
            return {"score": "warn", "density": round(density, 1), "detail": "冲突密度偏低"}
        return {"score": "pass", "density": round(density, 1), "detail": ""}

    def check_show_dont_tell(self, text):
        """
        展示非讲述检测
        检测"感到/觉得/知道/意识到"等抽象词的数量
        """
        tell_words = ["感到", "觉得", "知道", "意识", "感觉", "认为",
                       "仿佛", "好像", "似乎", "有些", "有点"]
        count = sum(text.count(w) for w in tell_words)
        density = count / max(chinese_word_count(text), 1) * 1000
        if density > 8:
            return {"score": "warn", "density": round(density, 1), "detail": "讲述词密度高，建议更多用动作/对话展示"}
        return {"score": "pass", "density": round(density, 1), "detail": ""}

    def check_word_count(self, text, min_words=1000, max_words=3000):
        """
        字数检测
        """
        count = chinese_word_count(text)
        if count < min_words:
            return {"score": "warn", "count": count, "target": f"{min_words}-{max_words}"}
        if count > max_words:
            return {"score": "warn", "count": count, "target": f"{min_words}-{max_words}"}
        return {"score": "pass", "count": count, "target": f"{min_words}-{max_words}"}

    def check_rhythm(self, text):
        """
        节奏评估
        段落长短是否有变化
        """
        paras = [p.strip() for p in text.split('\n') if p.strip() and len(p.strip()) > 10]
        if len(paras) < 3:
            return {"score": "warn", "detail": "段落太少，无法评估节奏"}
        para_lens = [len(p) for p in paras]
        avg = sum(para_lens) / len(para_lens)
        max_len = max(para_lens)
        min_len = min(para_lens)
        # 段落长度标准差
        variance = sum((l - avg) ** 2 for l in para_lens) / len(para_lens)
        stddev = math.sqrt(variance) if variance > 0 else 0
        if stddev < 10:
            return {"score": "warn", "stddev": round(stddev, 1), "detail": "段落长度过于均匀，缺少节奏变化"}
        return {"score": "pass", "stddev": round(stddev, 1), "detail": ""}


class AIFlavorCheck:
    """🧹 表达线/AI味检测"""

    def check(self, text):
        """执行全部AI味检测"""
        result = {}
        issues = []

        # 1. 句式长度标准差
        sentences_list = sentences(text)
        if len(sentences_list) >= 3:
            sent_lens = [chinese_word_count(s) for s in sentences_list]
            avg_s = sum(sent_lens) / len(sent_lens)
            var = sum((l - avg_s) ** 2 for l in sent_lens) / len(sent_lens)
            stddev = math.sqrt(var) if var > 0 else 0
            result["sentence_stddev"] = {"value": round(stddev, 1), "threshold": ">=5.0", "pass": stddev >= 5}
            if stddev < 5:
                issues.append("句式长度标准差<5，句式过于整齐")

        # 2. 过渡词密度
        transition_words = ["然后", "于是", "接着", "随后", "接下来", "与此同时",
                            "另一方面", "突然", "忽然", "渐渐的", "慢慢的"]
        trans_count = sum(text.count(w) for w in transition_words)
        total_words = chinese_word_count(text)
        trans_density = trans_count / max(total_words / 500, 1)  # 每500字密度
        result["transition_density"] = {"value": round(trans_density, 1), "threshold": "<=3.0/500字", "pass": trans_density <= 3}
        if trans_density > 3:
            issues.append("过渡词密度>3/500字，连接词过多")

        # 3. 副词密度
        adverb_words = ["很", "非常", "无比", "极其", "十分", "相当", "特别",
                         "太", "极", "格外", "颇为"]
        adverb_count = sum(text.count(w) for w in adverb_words)
        result["adverb_density"] = {"value": adverb_count, "threshold": "<=5次", "pass": adverb_count <= 5}
        if adverb_count > 5:
            issues.append(f"副词'{'/'.join(adverb_words[:3])}...'出现{adverb_count}次>5次")

        # 4. 连续同主语
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        same_subject_count = 0
        for i in range(1, len(lines)):
            if re.match(r'^(他|她|它|我|你)', lines[i]) and re.match(r'^(他|她|它|我|你)', lines[i-1]):
                same_subject_count += 1
        result["same_subject"] = {"value": same_subject_count, "threshold": "<=2次连续", "pass": same_subject_count <= 2}
        if same_subject_count > 2:
            issues.append("连续同主语超过2次")

        # 5. 情感词直说
        emotion_words = ["悲伤", "愤怒", "开心", "高兴", "难过", "痛苦", "恐惧",
                          "害怕", "激动", "兴奋", "委屈", "失落", "无奈", "绝望",
                          "感动", "惊讶", "震惊", "羞愧", "骄傲"]
        emotion_count = sum(text.count(w) for w in emotion_words)
        result["emotion_words"] = {"value": emotion_count, "threshold": "<=3次", "pass": emotion_count <= 3}
        if emotion_count > 3:
            issues.append(f"情感词直说{emotion_count}次>3次，建议改用动作暗示")

        # 6. 段首结构重复
        para_starts = []
        for line in text.split('\n'):
            line = line.strip()
            if len(line) > 5:
                m = re.match(r'^[\u4e00-\u9fff]{2,3}', line)
                if m:
                    para_starts.append(m.group())
        start_counter = Counter(para_starts)
        repeated = {k: v for k, v in start_counter.items() if v >= 3}
        if repeated:
            issues.append(f"段首重复: {', '.join([f'{k}x{v}' for k, v in repeated.items()[:3]])}")
        result["para_start_repeat"] = {"value": len(repeated), "threshold": "<=2组", "pass": len(repeated) <= 2}

        # 7. 修饰词/过度修饰
        modifier_words = ["温柔", "深情", "深邃", "忧郁", "优雅", "华丽", "璀璨",
                           "绚烂", "辉煌", "壮丽", "雄壮", "雄伟", "磅礴", "澎湃",
                           "迷人", "醉人", "动人", "惊人", "逼人", "袭人"]
        mod_count = sum(text.count(w) for w in modifier_words)
        result["modifier_density"] = {"value": mod_count, "threshold": "<=5次", "pass": mod_count <= 5}
        if mod_count > 5:
            issues.append(f"修饰词过多({mod_count}次>5次)")

        # 综合评分
        passed = sum(1 for k, v in result.items() if v.get("pass"))
        total = len(result)
        score = f"{passed}/{total}"
        result["summary"] = {"score": score, "passed": passed, "total": total}
        result["issues"] = issues
        result["overall"] = "pass" if passed / max(total, 1) >= 0.6 else "warn"
        return result


# ========== 主入口 ==========

def main():
    parser = argparse.ArgumentParser(description="章节质量检测")
    parser.add_argument("--chapter", "-c", required=True, help="章节文件路径(.md)")
    parser.add_argument("--reference", "-r", help="项目路径（可选，用于获取已知角色/主线关键词）")
    parser.add_argument("--out", "-o", help="输出JSON文件路径（可选）")
    parser.add_argument("--thresholds", "-t", help="阈值JSON字符串，如'{\"min_words\":1500,\"max_words\":2500}'")
    args = parser.parse_args()

    if not Path(args.chapter).exists():
        print(f"[错误] 文件不存在: {args.chapter}")
        sys.exit(1)

    text = read_text(args.chapter)

    # 解析阈值
    thresholds = {"min_words": 1000, "max_words": 3000}
    if args.thresholds:
        thresholds.update(json.loads(args.thresholds))

    # 加载项目参考信息
    known_chars = None
    main_keywords = None
    foreshadow_keywords = None
    if args.reference:
        ref_path = Path(args.reference)
        chars_dir = ref_path / "characters"
        if chars_dir.exists():
            known_chars = [f.stem for f in chars_dir.glob("*.md")]
        meta_file = ref_path / "novel.json"
        if meta_file.exists():
            # 从项目文件读取主线关键词（如果有）
            pass

    # 执行检测
    qc = QualityCheck()
    tc = TechniqueCheck()
    afc = AIFlavorCheck()

    report = {
        "chapter": args.chapter,
        "word_count": chinese_word_count(text),
        "quality_line": {
            "character_consistency": qc.check_character_consistency(text, known_chars),
            "mainline_consistency": qc.check_mainline_consistency(text, main_keywords),
            "logic": qc.check_logic(text),
            "foreshadowing": qc.check_foreshadowing(text, foreshadow_keywords),
            "power_balance": qc.check_power_balance(text),
        },
        "technique_line": {
            "chapter_twist": tc.check_twist(text),
            "conflict_density": tc.check_conflict_density(text),
            "show_dont_tell": tc.check_show_dont_tell(text),
            "word_count": tc.check_word_count(text, thresholds["min_words"], thresholds["max_words"]),
            "rhythm": tc.check_rhythm(text),
        },
        "ai_flavor": afc.check(text),
    }

    # 输出
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"[OK] 质检报告已写入: {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
