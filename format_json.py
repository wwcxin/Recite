#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化JSON目录下的文件，去除嵌套结构
每个项只保留：wordRank（序号）、headWord（单词）、usspeech（美音发音）、tranCn（中释）
"""

import json
from pathlib import Path


def simplify_item(item):
    """将JSON项简化为扁平结构，只保留wordRank、headWord、usspeech、tranCn"""
    # 创建新的简化项
    simplified_item = {}
    
    # 保留wordRank和headWord
    if 'wordRank' in item:
        simplified_item['wordRank'] = item['wordRank']
    if 'headWord' in item:
        simplified_item['headWord'] = item['headWord']
    
    # 提取usspeech和tranCn
    usspeech = None
    tranCn_list = []
    
    # 从嵌套结构中提取usspeech
    if 'content' in item and 'word' in item['content'] and 'content' in item['content']['word']:
        content_obj = item['content']['word']['content']
        
        # 提取usspeech
        if 'usspeech' in content_obj:
            usspeech = content_obj['usspeech']
        
        # 提取所有tranCn
        if 'trans' in content_obj and isinstance(content_obj['trans'], list):
            for trans_item in content_obj['trans']:
                if isinstance(trans_item, dict) and 'tranCn' in trans_item:
                    tranCn_list.append(trans_item['tranCn'])
    
    # 添加usspeech
    if usspeech:
        simplified_item['usspeech'] = usspeech
    
    # 合并多个tranCn为一个字符串（用分号分隔）
    if tranCn_list:
        simplified_item['tranCn'] = '；'.join(tranCn_list)
    
    return simplified_item


def format_json_file(file_path):
    """格式化单个JSON文件"""
    print(f"正在处理: {file_path}")
    
    # 读取文件
    processed_items = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                try:
                    item = json.loads(line)
                    processed_item = simplify_item(item)
                    processed_items.append(processed_item)
                except json.JSONDecodeError as e:
                    print(f"  警告: 第 {line_num} 行JSON解析失败: {e}")
                    continue
    except Exception as e:
        print(f"  错误: 读取文件失败: {e}")
        return False
    
    # 写回文件（标准JSON数组格式）
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(processed_items, f, ensure_ascii=False, indent=2)
        print(f"  完成: 已处理 {len(processed_items)} 条记录，已转换为标准JSON数组格式")
        return True
    except Exception as e:
        print(f"  错误: 写入文件失败: {e}")
        return False


def main():
    """主函数"""
    json_dir = Path('json')
    
    if not json_dir.exists():
        print(f"错误: 目录 '{json_dir}' 不存在")
        return
    
    # 查找所有JSON文件
    json_files = list(json_dir.glob('*.json'))
    
    if not json_files:
        print(f"在 '{json_dir}' 目录下未找到JSON文件")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件")
    print("=" * 50)
    
    success_count = 0
    for json_file in json_files:
        if format_json_file(json_file):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"处理完成: {success_count}/{len(json_files)} 个文件成功处理")


if __name__ == '__main__':
    main()

