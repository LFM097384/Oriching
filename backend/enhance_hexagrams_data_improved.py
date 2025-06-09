#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的卦象数据增强脚本
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
    
    result['detailed_info'] = detailed_info
    
    # 提取爻辞信息 - 改进的解析逻辑
    lines = []
    
    # 定义爻的模式
    line_patterns = [
        ('初九', 1, 'yang'), ('九二', 2, 'yang'), ('九三', 3, 'yang'),
        ('九四', 4, 'yang'), ('九五', 5, 'yang'), ('上九', 6, 'yang'),
        ('初六', 1, 'yin'), ('六二', 2, 'yin'), ('六三', 3, 'yin'),
        ('六四', 4, 'yin'), ('六五', 5, 'yin'), ('上六', 6, 'yin')
    ]
    
    for line_name, position, line_type in line_patterns:
        # 查找爻辞详解部分
        line_section_pattern = f'周易第\\d+卦{line_name}爻詳解\\s*\\n\\s*\\*\\*{line_name}爻辭\\*\\*\\s*\\n\\s*\\*\\*{line_name}。\\*\\*\\s*(.+?)\\s*\\n\\s*象曰：(.+?)\\s*\\n\\s*\\*\\*白話文解釋\\*\\*'
        line_match = re.search(line_section_pattern, content, re.DOTALL)
        
        if line_match:
            line_text = line_match.group(1).strip()
            image_text = line_match.group(2).strip()
            
            # 提取白话文解释
            white_text_pattern = f'\\*\\*白話文解釋\\*\\*\\s*\\n\\s*{line_name}：(.+?)\\s*\\n\\s*《象辭》說：(.+?)\\s*\\n\\s*\\*\\*邵雍河洛理數爻辭解釋\\*\\*'
            white_match = re.search(white_text_pattern, content, re.DOTALL)
            
            white_explanation = ""
            symbol_explanation = ""
            if white_match:
                white_explanation = white_match.group(1).strip()
                symbol_explanation = white_match.group(2).strip()
            
            line_info = {
                'position': position,
                'type': line_type,
                'changing': False,
                'text': f"{line_name}爻辞",
                'explanation': line_text,
                'white_explanation': white_explanation,
                'image': {
                    'text': image_text,
                    'explanation': symbol_explanation
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
    
    # 卦名映射
    hexagram_folders = {
        1: "01.乾为天", 2: "02.坤为地", 3: "03.水雷屯", 4: "04.山水蒙", 5: "05.水天需",
        6: "06.天水讼", 7: "07.地水师", 8: "08.水地比", 9: "09.风天小畜", 10: "10.天泽履",
        11: "11.地天泰", 12: "12.天地否", 13: "13.天火同人", 14: "14.火天大有", 15: "15.地山谦",
        16: "16.雷地豫", 17: "17.泽雷随", 18: "18.山风蛊", 19: "19.地泽临", 20: "20.风地观",
        21: "21.火雷噬嗑", 22: "22.山火贲", 23: "23.山地剥", 24: "24.地雷复", 25: "25.天雷无妄",
        26: "26.山天大畜", 27: "27.山雷颐", 28: "28.泽风大过", 29: "29.坎为水", 30: "30.离为火",
        31: "31.泽山咸", 32: "32.雷风恒", 33: "33.天山遁", 34: "34.雷天大壮", 35: "35.火地晋",
        36: "36.地火明夷", 37: "37.风火家人", 38: "38.火泽睽", 39: "39.水山蹇", 40: "40.雷水解",
        41: "41.山泽损", 42: "42.风雷益", 43: "43.泽天夬", 44: "44.天风姤", 45: "45.泽地萃",
        46: "46.地风升", 47: "47.泽水困", 48: "48.水风井", 49: "49.泽火革", 50: "50.火风鼎",
        51: "51.震为雷", 52: "52.艮为山", 53: "53.风山渐", 54: "54.雷泽归妹", 55: "55.雷火丰",
        56: "56.火山旅", 57: "57.巽为风", 58: "58.兑为泽", 59: "59.风水涣", 60: "60.水泽节",
        61: "61.风泽中孚", 62: "62.雷山小过", 63: "63.水火既济", 64: "64.火水未济"
    }
    
    for i in range(1, 65):  # 64卦
        if i in hexagram_folders:
            folder_name = hexagram_folders[i]
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
                                        if 'white_explanation' in md_line:
                                            hexagrams[idx]['lines'][j]['white_explanation'] = md_line['white_explanation']
                                        if 'image' in md_line:
                                            hexagrams[idx]['lines'][j]['image'] = md_line['image']
                                        break
                        
                        print(f"  ✓ 成功更新第{i}卦")
                    else:
                        print(f"  ✗ 未找到第{i}卦的JSON数据")
                        
                except Exception as e:
                    print(f"  ✗ 处理第{i}卦时出错: {e}")
                    import traceback
                    traceback.print_exc()
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
