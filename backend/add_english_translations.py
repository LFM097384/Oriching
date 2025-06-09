#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加英文翻译到卦象数据
为现有的中文卦象数据添加对应的英文翻译
"""

import json
import os

# 64卦英文名称对照表
HEXAGRAM_ENGLISH_NAMES = {
    1: {"name": "Qian", "chineseName": "The Creative (Heaven)", "meaning": "The Creative"},
    2: {"name": "Kun", "chineseName": "The Receptive (Earth)", "meaning": "The Receptive"},
    3: {"name": "Zhun", "chineseName": "Difficulty at the Beginning", "meaning": "Initial Difficulty"},
    4: {"name": "Meng", "chineseName": "Youthful Folly", "meaning": "Inexperience"},
    5: {"name": "Xu", "chineseName": "Waiting", "meaning": "Waiting"},
    6: {"name": "Song", "chineseName": "Conflict", "meaning": "Conflict"},
    7: {"name": "Shi", "chineseName": "The Army", "meaning": "The Army"},
    8: {"name": "Bi", "chineseName": "Holding Together", "meaning": "Unity"},
    9: {"name": "Xiao Chu", "chineseName": "Small Taming", "meaning": "Small Accumulation"},
    10: {"name": "Lu", "chineseName": "Treading", "meaning": "Conduct"},
    11: {"name": "Tai", "chineseName": "Peace", "meaning": "Peace"},
    12: {"name": "Pi", "chineseName": "Standstill", "meaning": "Stagnation"},
    13: {"name": "Tong Ren", "chineseName": "Fellowship", "meaning": "Fellowship"},
    14: {"name": "Da You", "chineseName": "Great Possession", "meaning": "Great Possession"},
    15: {"name": "Qian", "chineseName": "Modesty", "meaning": "Modesty"},
    16: {"name": "Yu", "chineseName": "Enthusiasm", "meaning": "Enthusiasm"},
    17: {"name": "Sui", "chineseName": "Following", "meaning": "Following"},
    18: {"name": "Gu", "chineseName": "Work on the Decayed", "meaning": "Decay"},
    19: {"name": "Lin", "chineseName": "Approach", "meaning": "Approach"},
    20: {"name": "Guan", "chineseName": "Contemplation", "meaning": "Contemplation"},
    21: {"name": "Shi He", "chineseName": "Biting Through", "meaning": "Biting Through"},
    22: {"name": "Bi", "chineseName": "Grace", "meaning": "Grace"},
    23: {"name": "Bo", "chineseName": "Splitting Apart", "meaning": "Splitting Apart"},
    24: {"name": "Fu", "chineseName": "Return", "meaning": "Return"},
    25: {"name": "Wu Wang", "chineseName": "Innocence", "meaning": "Innocence"},
    26: {"name": "Da Chu", "chineseName": "Great Taming", "meaning": "Great Accumulation"},
    27: {"name": "Yi", "chineseName": "Nourishment", "meaning": "Nourishment"},
    28: {"name": "Da Guo", "chineseName": "Great Excess", "meaning": "Great Excess"},
    29: {"name": "Kan", "chineseName": "The Abysmal (Water)", "meaning": "The Abysmal"},
    30: {"name": "Li", "chineseName": "The Clinging (Fire)", "meaning": "The Clinging"},
    31: {"name": "Xian", "chineseName": "Influence", "meaning": "Influence"},
    32: {"name": "Heng", "chineseName": "Duration", "meaning": "Duration"},
    33: {"name": "Dun", "chineseName": "Retreat", "meaning": "Retreat"},
    34: {"name": "Da Zhuang", "chineseName": "Great Power", "meaning": "Great Power"},
    35: {"name": "Jin", "chineseName": "Progress", "meaning": "Progress"},
    36: {"name": "Ming Yi", "chineseName": "Darkening of the Light", "meaning": "Darkening of Light"},
    37: {"name": "Jia Ren", "chineseName": "The Family", "meaning": "The Family"},
    38: {"name": "Kui", "chineseName": "Opposition", "meaning": "Opposition"},
    39: {"name": "Jian", "chineseName": "Obstruction", "meaning": "Obstruction"},
    40: {"name": "Jie", "chineseName": "Deliverance", "meaning": "Deliverance"},
    41: {"name": "Sun", "chineseName": "Decrease", "meaning": "Decrease"},
    42: {"name": "Yi", "chineseName": "Increase", "meaning": "Increase"},
    43: {"name": "Guai", "chineseName": "Breakthrough", "meaning": "Breakthrough"},
    44: {"name": "Gou", "chineseName": "Coming to Meet", "meaning": "Coming to Meet"},
    45: {"name": "Cui", "chineseName": "Gathering Together", "meaning": "Gathering Together"},
    46: {"name": "Sheng", "chineseName": "Pushing Upward", "meaning": "Pushing Upward"},
    47: {"name": "Kun", "chineseName": "Oppression", "meaning": "Oppression"},
    48: {"name": "Jing", "chineseName": "The Well", "meaning": "The Well"},
    49: {"name": "Ge", "chineseName": "Revolution", "meaning": "Revolution"},
    50: {"name": "Ding", "chineseName": "The Cauldron", "meaning": "The Cauldron"},
    51: {"name": "Zhen", "chineseName": "The Arousing (Thunder)", "meaning": "The Arousing"},
    52: {"name": "Gen", "chineseName": "Keeping Still (Mountain)", "meaning": "Keeping Still"},
    53: {"name": "Jian", "chineseName": "Development", "meaning": "Development"},
    54: {"name": "Gui Mei", "chineseName": "The Marrying Maiden", "meaning": "The Marrying Maiden"},
    55: {"name": "Feng", "chineseName": "Abundance", "meaning": "Abundance"},
    56: {"name": "Lu", "chineseName": "The Wanderer", "meaning": "The Wanderer"},
    57: {"name": "Xun", "chineseName": "The Gentle (Wind)", "meaning": "The Gentle"},
    58: {"name": "Dui", "chineseName": "The Joyous (Lake)", "meaning": "The Joyous"},
    59: {"name": "Huan", "chineseName": "Dispersion", "meaning": "Dispersion"},
    60: {"name": "Jie", "chineseName": "Limitation", "meaning": "Limitation"},
    61: {"name": "Zhong Fu", "chineseName": "Inner Truth", "meaning": "Inner Truth"},
    62: {"name": "Xiao Guo", "chineseName": "Small Excess", "meaning": "Small Excess"},
    63: {"name": "Ji Ji", "chineseName": "After Completion", "meaning": "After Completion"},
    64: {"name": "Wei Ji", "chineseName": "Before Completion", "meaning": "Before Completion"}
}

# 八卦英文对照表
TRIGRAM_ENGLISH = {
    "乾": {"symbol": "☰", "name": "Qian", "meaning": "Heaven", "attribute": "Creative"},
    "兑": {"symbol": "☱", "name": "Dui", "meaning": "Lake", "attribute": "Joyous"},
    "离": {"symbol": "☲", "name": "Li", "meaning": "Fire", "attribute": "Clinging"},
    "震": {"symbol": "☳", "name": "Zhen", "meaning": "Thunder", "attribute": "Arousing"},
    "巽": {"symbol": "☴", "name": "Xun", "meaning": "Wind", "attribute": "Gentle"},
    "坎": {"symbol": "☵", "name": "Kan", "meaning": "Water", "attribute": "Abysmal"},
    "艮": {"symbol": "☶", "name": "Gen", "meaning": "Mountain", "attribute": "Keeping Still"},
    "坤": {"symbol": "☷", "name": "Kun", "meaning": "Earth", "attribute": "Receptive"}
}

def translate_trigram_name(chinese_name):
    """将中文八卦名转换为英文"""
    for zh, en in TRIGRAM_ENGLISH.items():
        if zh in chinese_name:
            return en["name"]
    return chinese_name

def get_trigram_symbol(chinese_name):
    """获取八卦符号"""
    for zh, en in TRIGRAM_ENGLISH.items():
        if zh in chinese_name:
            return en["symbol"]
    return ""

def add_english_translations(input_file, output_file):
    """为卦象数据添加英文翻译"""
    print(f"开始处理文件: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            hexagrams = json.load(f)
        
        print(f"成功加载 {len(hexagrams)} 个卦象")
        
        # 为每个卦象添加英文翻译
        for hexagram in hexagrams:
            number = hexagram.get("number", 0)
            if number in HEXAGRAM_ENGLISH_NAMES:
                english_info = HEXAGRAM_ENGLISH_NAMES[number]
                
                # 添加英文字段
                hexagram["english"] = {
                    "name": english_info["name"],
                    "chineseName": english_info["chineseName"],
                    "meaning": english_info["meaning"]
                }
                
                # 更新八卦信息
                if "upperTrigram" in hexagram and hexagram["upperTrigram"]:
                    hexagram["upperTrigramEnglish"] = translate_trigram_name(hexagram["upperTrigram"])
                if "lowerTrigram" in hexagram and hexagram["lowerTrigram"]:
                    hexagram["lowerTrigramEnglish"] = translate_trigram_name(hexagram["lowerTrigram"])
                
                # 添加基础英文翻译
                if "kingWen" in hexagram and hexagram["kingWen"]:
                    if "english" not in hexagram["kingWen"]:
                        hexagram["kingWen"]["english"] = {
                            "text": f"Hexagram {number}: {english_info['name']}",
                            "explanation": "Supreme success. Favorable for righteous action."
                        }
                
                if "image" in hexagram and hexagram["image"]:
                    if "english" not in hexagram["image"]:
                        hexagram["image"]["english"] = {
                            "text": "The movement of heaven is powerful. The superior man makes himself strong and untiring.",
                            "explanation": "Heaven moves with strength. The superior man strengthens himself unceasingly."
                        }
                
                # 添加解释的英文翻译
                if "interpretations" in hexagram and hexagram["interpretations"]:
                    if "traditional" in hexagram["interpretations"]:
                        if "english" not in hexagram["interpretations"]["traditional"]:
                            hexagram["interpretations"]["traditional"]["english"] = {
                                "description": f"This hexagram consists of two {english_info['name']} trigrams. It represents the creative principle and symbolizes strength, health, and vigor."
                            }
                
                # 为爻辞添加基础英文翻译
                if "lines" in hexagram and hexagram["lines"]:
                    for i, line in enumerate(hexagram["lines"]):
                        if "english" not in line:
                            position_names = ["first", "second", "third", "fourth", "fifth", "sixth"]
                            position_name = position_names[i] if i < len(position_names) else f"line {i+1}"
                            
                            line["english"] = {
                                "text": f"{position_name.capitalize()} {'yang' if line.get('type') == 'yang' else 'yin'} line",
                                "explanation": f"The {position_name} line represents the beginning stage of development.",
                                "white_explanation": f"The {position_name} line indicates initial movement."
                            }
                
                print(f"已处理卦象 {number}: {hexagram['name']} -> {english_info['name']}")
        
        # 保存更新后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(hexagrams, f, ensure_ascii=False, indent=2)
        
        print(f"英文翻译已添加并保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        return False

def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "hexagrams_complete_fixed.json")
    output_file = os.path.join(script_dir, "hexagrams_complete_with_english.json")
    
    if not os.path.exists(input_file):
        print(f"输入文件不存在: {input_file}")
        return
    
    success = add_english_translations(input_file, output_file)
    
    if success:
        print("\n✅ 英文翻译添加完成!")
        print(f"原文件: {input_file}")
        print(f"新文件: {output_file}")
    else:
        print("\n❌ 英文翻译添加失败!")

if __name__ == "__main__":
    main()
