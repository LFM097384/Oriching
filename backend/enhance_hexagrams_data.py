#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强卦象数据脚本
从temp_zhouyi/docs中的Markdown文件提取详细信息，更新hexagrams_complete_fixed.json
"""

import json
import os
import re
from typing import Dict, List, Any

def parse_markdown_file(filepath: str) -> Dict[str, Any]:
    """解析单个卦象的Markdown文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {}
    
    # 提取卦象基本信息
    title_match = re.search(r'# 第(\d+)卦：(.+?)（(.+?)）', content)
    if title_match:
        result['number'] = int(title_match.group(1))
        result['name'] = title_match.group(2)
        result['chineseName'] = title_match.group(3)
    
    # 提取卦辞
    kingwen_match = re.search(r'\*\*(.+?)\.\*\* (.+?)(?=\n\n象曰：)', content, re.DOTALL)
    if kingwen_match:
        result['kingWen'] = {
            'text': kingwen_match.group(1) + '。',
            'explanation': kingwen_match.group(2).strip()
        }
    
    # 提取象辞
    image_match = re.search(r'象曰：(.+?)(?=\n\n\*\*白話文解釋\*\*)', content, re.DOTALL)
    if image_match:
        result['image'] = {
            'text': image_match.group(1).strip(),
            'explanation': image_match.group(1).strip()
        }
    
    # 提取传统解卦
    traditional_match = re.search(r'\*\*傳統解卦\*\* \n\n(.+?)(?=\n\n\*\*大象：\*\*)', content, re.DOTALL)
    if traditional_match:
        result['interpretations'] = {
            'traditional': {
                'description': traditional_match.group(1).strip()
            }
        }
    
    # 提取详细解读信息
    detailed_info = {}
    
    # 大象
    daxiang_match = re.search(r'\*\*大象：\*\* (.+?)(?=\n\n)', content)
    if daxiang_match:
        detailed_info['daxiang'] = daxiang_match.group(1).strip()
    
    # 运势
    yunshi_match = re.search(r'\*\*運勢：\*\* (.+?)(?=\n\n)', content)
    if yunshi_match:
        detailed_info['fortune'] = yunshi_match.group(1).strip()
    
    # 事业
    shiye_match = re.search(r'\*\*事業：\*\* (.+?)(?=\n\n)', content)
    if shiye_match:
        detailed_info['career'] = shiye_match.group(1).strip()
    
    # 经商
    jingshang_match = re.search(r'\*\*經商：\*\* (.+?)(?=\n\n)', content)
    if jingshang_match:
        detailed_info['business'] = jingshang_match.group(1).strip()
    
    # 求名
    qiuming_match = re.search(r'\*\*求名：\*\* (.+?)(?=\n\n)', content)
    if qiuming_match:
        detailed_info['fame'] = qiuming_match.group(1).strip()
    
    # 婚恋
    hunlian_match = re.search(r'\*\*婚戀：\*\* (.+?)(?=\n\n)', content)
    if hunlian_match:
        detailed_info['love'] = hunlian_match.group(1).strip()
    
    # 决策
    juece_match = re.search(r'\*\*決策：\*\* (.+?)(?=\n\n)', content)
    if juece_match:
        detailed_info['advice'] = juece_match.group(1).strip()
    
    # 健康
    jiankang_match = re.search(r'\*\*身體：\*\* (.+?)(?=\n\n)', content)
    if jiankang_match:
        detailed_info['health'] = jiankang_match.group(1).strip()
    
    result['detailed_info'] = detailed_info
      # 提取爻辞信息
    lines = []
    
    # 更精确的爻辞解析模式
    # 每种爻的模式：爻名称、爻辞正文、象曰部分
    line_configs = [
        ('初九', '初九', 1, 'yang'), ('九二', '九二', 2, 'yang'), ('九三', '九三', 3, 'yang'),
        ('九四', '九四', 4, 'yang'), ('九五', '九五', 5, 'yang'), ('上九', '上九', 6, 'yang'),
        ('初六', '初六', 1, 'yin'), ('六二', '六二', 2, 'yin'), ('六三', '六三', 3, 'yin'),
        ('六四', '六四', 4, 'yin'), ('六五', '六五', 5, 'yin'), ('上六', '上六', 6, 'yin')
    ]
    
    for line_name, pattern_name, position, line_type in line_configs:
        # 查找爻辞部分
        line_section_pattern = f'周易第\\d+卦{line_name}爻詳解\\n\\n\\*\\*{line_name}爻辭\\*\\* \\n\\n\\*\\*{pattern_name}。\\*\\* (.+?)\\n\\n象曰：(.+?)\\n\\n'
        line_match = re.search(line_section_pattern, content, re.DOTALL)
        
        if line_match:
            line_text = line_match.group(1).strip()
            image_text = line_match.group(2).strip()
            
            line_info = {
                'position': position,
                'type': line_type,
                'changing': False,
                'text': f"{line_name}爻辞",
                'explanation': f"**{pattern_name}。** {line_text}",
                'image': {
                    'text': '',
                    'explanation': image_text
                }
            }
            lines.append(line_info)
    
    # 按位置排序
    lines.sort(key=lambda x: x['position'])
    result['lines'] = lines
    
    return result

def update_hexagram_data():
    """更新卦象数据"""
    # 读取现有的JSON文件
    json_path = 'hexagrams_complete_fixed.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        hexagrams = json.load(f)
    
    # 创建一个数字到索引的映射
    hexagram_index = {hex['number']: i for i, hex in enumerate(hexagrams)}
    
    # 遍历所有Markdown文件
    docs_dir = 'temp_zhouyi/docs'
    
    for i in range(1, 65):  # 64卦
        # 构造文件夹名
        folder_names = [
            f"{i:02d}.乾为天", f"{i:02d}.坤为地", f"{i:02d}.水雷屯", f"{i:02d}.山水蒙", f"{i:02d}.水天需",
            f"{i:02d}.天水讼", f"{i:02d}.地水师", f"{i:02d}.水地比", f"{i:02d}.风天小畜", f"{i:02d}.天泽履",
            f"{i:02d}.地天泰", f"{i:02d}.天地否", f"{i:02d}.天火同人", f"{i:02d}.火天大有", f"{i:02d}.地山谦",
            f"{i:02d}.雷地豫", f"{i:02d}.泽雷随", f"{i:02d}.山风蛊", f"{i:02d}.地泽临", f"{i:02d}.风地观",
            f"{i:02d}.火雷噬嗑", f"{i:02d}.山火贲", f"{i:02d}.山地剥", f"{i:02d}.地雷复", f"{i:02d}.天雷无妄",
            f"{i:02d}.山天大畜", f"{i:02d}.山雷颐", f"{i:02d}.泽风大过", f"{i:02d}.坎为水", f"{i:02d}.离为火",
            f"{i:02d}.泽山咸", f"{i:02d}.雷风恒", f"{i:02d}.天山遁", f"{i:02d}.雷天大壮", f"{i:02d}.火地晋",
            f"{i:02d}.地火明夷", f"{i:02d}.风火家人", f"{i:02d}.火泽睽", f"{i:02d}.水山蹇", f"{i:02d}.雷水解",
            f"{i:02d}.山泽损", f"{i:02d}.风雷益", f"{i:02d}.泽天夬", f"{i:02d}.天风姤", f"{i:02d}.泽地萃",
            f"{i:02d}.地风升", f"{i:02d}.泽水困", f"{i:02d}.水风井", f"{i:02d}.泽火革", f"{i:02d}.火风鼎",
            f"{i:02d}.震为雷", f"{i:02d}.艮为山", f"{i:02d}.风山渐", f"{i:02d}.雷泽归妹", f"{i:02d}.雷火丰",
            f"{i:02d}.火山旅", f"{i:02d}.巽为风", f"{i:02d}.兑为泽", f"{i:02d}.风水涣", f"{i:02d}.水泽节",
            f"{i:02d}.风泽中孚", f"{i:02d}.雷山小过", f"{i:02d}.水火既济", f"{i:02d}.火水未济"
        ]
        
        if i <= len(folder_names):
            folder_name = folder_names[i-1]
            md_path = os.path.join(docs_dir, folder_name, 'index.md')
            
            if os.path.exists(md_path):
                print(f"处理第{i}卦: {md_path}")
                try:
                    md_data = parse_markdown_file(md_path)
                    
                    # 更新JSON中对应的卦象
                    if i in hexagram_index:
                        idx = hexagram_index[i]
                        
                        # 更新基本信息
                        if 'kingWen' in md_data:
                            hexagrams[idx]['kingWen'] = md_data['kingWen']
                        
                        if 'image' in md_data:
                            hexagrams[idx]['image'] = md_data['image']
                        
                        if 'interpretations' in md_data:
                            if 'interpretations' not in hexagrams[idx]:
                                hexagrams[idx]['interpretations'] = {}
                            hexagrams[idx]['interpretations'].update(md_data['interpretations'])
                        
                        # 添加详细信息
                        if 'detailed_info' in md_data:
                            for key, value in md_data['detailed_info'].items():
                                hexagrams[idx][key] = value
                        
                        # 更新爻辞信息（保留现有的爻线信息，只增强内容）
                        if 'lines' in md_data and md_data['lines']:
                            for md_line in md_data['lines']:
                                pos = md_line['position']
                                # 找到对应位置的爻
                                for j, existing_line in enumerate(hexagrams[idx]['lines']):
                                    if existing_line['position'] == pos:
                                        # 更新爻辞内容
                                        if 'explanation' in md_line:
                                            hexagrams[idx]['lines'][j]['explanation'] = md_line['explanation']
                                        if 'image' in md_line:
                                            hexagrams[idx]['lines'][j]['image'] = md_line['image']
                                        break
                        
                        print(f"  ✓ 成功更新第{i}卦")
                    else:
                        print(f"  ✗ 未找到第{i}卦的JSON数据")
                        
                except Exception as e:
                    print(f"  ✗ 处理第{i}卦时出错: {e}")
            else:
                print(f"  ✗ 文件不存在: {md_path}")
    
    # 保存更新后的JSON文件
    backup_path = 'hexagrams_complete_fixed_backup.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(hexagrams, f, ensure_ascii=False, indent=2)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(hexagrams, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 数据更新完成！")
    print(f"✓ 原文件已备份为: {backup_path}")
    print(f"✓ 更新后的文件: {json_path}")

if __name__ == "__main__":
    update_hexagram_data()
