#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化JSON目录下的文件，去除嵌套结构
每个项只保留：wordRank（序号）、headWord（单词）、usspeech（美音发音）、tranCn（中释）
"""

import json
import os
from pathlib import Path


def is_already_formatted(file_path):
    """检查文件是否已经是目标格式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 检查是否是数组格式
        if not isinstance(data, list):
            return False
        
        # 检查数组是否为空
        if len(data) == 0:
            return True
        
        # 检查第一个元素是否符合目标格式
        first_item = data[0]
        if not isinstance(first_item, dict):
            return False
        
        # 检查是否包含目标字段，且没有嵌套结构
        required_fields = {'wordRank', 'headWord', 'tranCn'}
        has_required = all(field in first_item for field in required_fields)
        
        # 检查是否没有嵌套的 content 结构（说明已经是简化格式）
        has_nested_content = 'content' in first_item
        
        # 如果包含必需字段且没有嵌套结构，说明已经是目标格式
        return has_required and not has_nested_content
        
    except (json.JSONDecodeError, Exception) as e:
        # 如果解析失败，说明需要格式化
        return False


def simplify_item(item):
    """将JSON项简化为扁平结构，只保留wordRank、headWord、usspeech、tranCn"""
    # 如果已经是简化格式，直接返回
    if isinstance(item, dict) and 'headWord' in item and 'tranCn' in item:
        # 检查是否有嵌套结构
        if 'content' not in item:
            # 已经是简化格式，只保留需要的字段
            simplified_item = {}
            if 'wordRank' in item:
                simplified_item['wordRank'] = item['wordRank']
            if 'headWord' in item:
                simplified_item['headWord'] = item['headWord']
            if 'usspeech' in item:
                simplified_item['usspeech'] = item['usspeech']
            if 'tranCn' in item:
                simplified_item['tranCn'] = item['tranCn']
            return simplified_item
    
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
    else:
        # 如果没有嵌套结构，直接获取
        if 'usspeech' in item:
            usspeech = item['usspeech']
        if 'tranCn' in item:
            if isinstance(item['tranCn'], str):
                tranCn_list.append(item['tranCn'])
            elif isinstance(item['tranCn'], list):
                tranCn_list.extend(item['tranCn'])
    
    # 添加usspeech
    if usspeech:
        simplified_item['usspeech'] = usspeech
    
    # 合并多个tranCn为一个字符串（用分号分隔）
    if tranCn_list:
        simplified_item['tranCn'] = '；'.join(tranCn_list)
    
    # 如果没有任何有效字段，返回None
    if not simplified_item:
        return None
    
    return simplified_item


def format_json_file(file_path):
    """格式化单个JSON文件"""
    print(f"正在处理: {file_path.name}")
    
    # 读取文件
    processed_items = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 先尝试作为标准JSON数组读取
            try:
                data = json.load(f)
                if isinstance(data, list):
                    # 已经是数组格式，但可能包含嵌套结构
                    for item in data:
                        processed_item = simplify_item(item)
                        if processed_item:  # 只添加非空项
                            processed_items.append(processed_item)
                else:
                    # 单个对象，转换为数组
                    processed_item = simplify_item(data)
                    if processed_item:
                        processed_items.append(processed_item)
            except json.JSONDecodeError:
                # 如果不是标准JSON，尝试按行读取（JSONL格式）
                f.seek(0)
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:  # 跳过空行
                        continue
                    try:
                        item = json.loads(line)
                        processed_item = simplify_item(item)
                        if processed_item:
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
    # 切换到 public/json 目录
    script_dir = Path(__file__).parent
    json_dir = script_dir / 'public' / 'json'
    
    # 如果 public/json 不存在，尝试 json 目录（向后兼容）
    if not json_dir.exists():
        json_dir = script_dir / 'json'
    
    if not json_dir.exists():
        print(f"错误: 目录 '{json_dir}' 不存在")
        print(f"请确保 'public/json' 或 'json' 目录存在")
        return
    
    # 切换到目标目录
    original_dir = os.getcwd()
    try:
        os.chdir(json_dir)
        print(f"工作目录: {json_dir.absolute()}")
    except Exception as e:
        print(f"错误: 无法切换到目录 '{json_dir}': {e}")
        return
    
    try:
        # 查找所有JSON文件
        json_files = list(Path('.').glob('*.json'))
        
        if not json_files:
            print(f"在 '{json_dir}' 目录下未找到JSON文件")
            return
        
        print(f"找到 {len(json_files)} 个JSON文件")
        print("=" * 50)
        
        success_count = 0
        skipped_count = 0
        for json_file in json_files:
            # 检查是否已经是目标格式
            if is_already_formatted(json_file):
                print(f"跳过: {json_file.name} (已经是目标格式)")
                skipped_count += 1
            elif format_json_file(json_file):
                success_count += 1
            print()
        
        print("=" * 50)
        print(f"处理完成:")
        print(f"  - 成功处理: {success_count} 个文件")
        print(f"  - 跳过(已格式化): {skipped_count} 个文件")
        print(f"  - 总计: {len(json_files)} 个文件")
    finally:
        # 恢复原始目录
        os.chdir(original_dir)


if __name__ == '__main__':
    main()

