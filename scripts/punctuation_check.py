#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说文本标点符号检查工具
检查引号配对、全角半角、标点规范等问题
"""

import argparse
import json
import re
from pathlib import Path


def check_punctuation(text):
    """检查文本中的标点符号问题"""
    issues = []
    lines = text.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # 检查引号配对
        issues.extend(check_quote_pairs(line, line_num))
        
        # 检查书名号配对
        issues.extend(check_book_title_pairs(line, line_num))
        
        # 检查全角半角混用
        issues.extend(check_mixed_width(line, line_num))
        
        # 检查连续标点
        issues.extend(check_consecutive_punctuation(line, line_num))
        
        # 检查句尾标点
        issues.extend(check_line_ending(line, line_num))
        
        # 检查引号前空格
        issues.extend(check_space_before_quote(line, line_num))
    
    return {
        "status": "success",
        "total_lines": len(lines),
        "issues_count": len(issues),
        "issues": issues
    }


def check_quote_pairs(line, line_num):
    """检查引号配对"""
    issues = []
    
    # 英文双引号计数
    en_quote_open = line.count('"')
    en_quote_close = line.count('"')
    
    # 中文双引号计数
    cn_quote_open = line.count('\u201c')  # "
    cn_quote_close = line.count('\u201d')  # "
    
    # 中文单引号计数
    cn_single_open = line.count('\u2018')  # '
    cn_single_close = line.count('\u2019')  # '
    
    if (en_quote_open + en_quote_close) % 2 != 0:
        issues.append({
            "line": line_num,
            "type": "quote_mismatch",
            "severity": "error",
            "message": "英文双引号 \" 数量为奇数，可能未配对",
            "content": line.strip()[:50]
        })
    
    if (cn_quote_open + cn_quote_close) % 2 != 0:
        issues.append({
            "line": line_num,
            "type": "quote_mismatch",
            "severity": "error",
            "message": "中文引号 \"\" 数量为奇数，可能未配对",
            "content": line.strip()[:50]
        })
    
    if (cn_single_open + cn_single_close) % 2 != 0:
        issues.append({
            "line": line_num,
            "type": "quote_mismatch",
            "severity": "error",
            "message": "中文单引号 '' 数量为奇数，可能未配对",
            "content": line.strip()[:50]
        })
    
    return issues


def check_book_title_pairs(line, line_num):
    """检查书名号配对"""
    issues = []
    angle_open = line.count('\u300a')  # 《
    angle_close = line.count('\u300b')  # 》
    
    if angle_open != angle_close:
        issues.append({
            "line": line_num,
            "type": "book_title_mismatch",
            "severity": "error",
            "message": f"书名号《》不配对：{angle_open}个《，{angle_close}个》",
            "content": line.strip()[:50]
        })
    
    return issues


def check_mixed_width(line, line_num):
    """检查全角半角混用"""
    issues = []
    
    # 中文引号后不应直接跟英文逗号/句号
    if re.search(r'["\u201c\u201d\u2018\u2019]\s*[,\.]', line):
        issues.append({
            "line": line_num,
            "type": "mixed_width",
            "severity": "warning",
            "message": "引号后使用了英文标点，建议使用中文标点",
            "content": line.strip()[:50]
        })
    
    return issues


def check_consecutive_punctuation(line, line_num):
    """检查连续标点"""
    issues = []
    
    # 连续三个以上相同中文标点
    consecutive_patterns = [
        r'[，。！？；：]{3,}',  # 连续标点
        r'[、，]{2,}',         # 连续顿号或逗号
    ]
    
    for pattern in consecutive_patterns:
        if re.search(pattern, line):
            issues.append({
                "line": line_num,
                "type": "consecutive_punctuation",
                "severity": "warning",
                "message": "存在连续标点符号",
                "content": line.strip()[:50]
            })
            break
    
    return issues


def check_line_ending(line, line_num):
    """检查行尾标点"""
    issues = []
    stripped = line.strip()
    
    if not stripped:
        return issues
    
    # 非空行且非标题行应有一定标点
    if len(stripped) > 10:
        # 检查是否是章节标题（短行或特定格式）
        is_title = len(stripped) < 20 and re.match(r'^第[一二三四五六七八九十百千\\d]+[章节卷部]', stripped)
        is_short_title = len(stripped) < 15 and re.match(r'^[\u4e00-\u9fa5a-zA-Z]+$', stripped)
        
        if not (is_title or is_short_title):
            if not re.search(r'[，。！？；：、""''\u201c\u201d\u2018\u2019\u300b\u300a]$', stripped):
                issues.append({
                    "line": line_num,
                    "type": "missing_ending_punct",
                    "severity": "info",
                    "message": "段落行尾缺少标点符号",
                    "content": stripped[:50]
                })
    
    return issues


def check_space_before_quote(line, line_num):
    """检查引号前空格"""
    issues = []
    
    # 引号前有空格但引号后无空格（中文排版习惯）
    if re.search(r'\s[""\u201c\u201d]', line):
        issues.append({
            "line": line_num,
            "type": "space_before_quote",
            "severity": "warning",
            "message": "引号前有空格，排版不统一",
            "content": line.strip()[:50]
        })
    
    return issues


def main():
    parser = argparse.ArgumentParser(description='小说文本标点符号检查工具')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--output', '-o', help='输出JSON文件路径（可选）')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        result = {
            "status": "error",
            "message": f"文件不存在: {args.input}"
        }
    else:
        text = input_path.read_text(encoding='utf-8')
        result = check_punctuation(text)
    
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        Path(args.output).write_text(output_json, encoding='utf-8')
    else:
        print(output_json)


if __name__ == "__main__":
    main()
