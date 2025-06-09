import json
import re

# 64卦的标准中文名称对应关系
hexagram_names = {
    1: {"trigrams": "Heaven over Heaven", "name": "The Creative"},
    2: {"trigrams": "Earth over Earth", "name": "The Receptive"},
    3: {"trigrams": "Water over Thunder", "name": "Difficulty at the Beginning"},
    4: {"trigrams": "Mountain over Water", "name": "Youthful Folly"},
    5: {"trigrams": "Water over Heaven", "name": "Waiting"},
    6: {"trigrams": "Heaven over Water", "name": "Conflict"},
    7: {"trigrams": "Earth over Water", "name": "The Army"},
    8: {"trigrams": "Water over Earth", "name": "Holding Together"},
    9: {"trigrams": "Wind over Heaven", "name": "Small Taming"},
    10: {"trigrams": "Heaven over Lake", "name": "Treading"},
    11: {"trigrams": "Earth over Heaven", "name": "Peace"},
    12: {"trigrams": "Heaven over Earth", "name": "Standstill"},
    13: {"trigrams": "Heaven over Fire", "name": "Fellowship"},
    14: {"trigrams": "Fire over Heaven", "name": "Great Possession"},
    15: {"trigrams": "Earth over Mountain", "name": "Modesty"},
    16: {"trigrams": "Thunder over Earth", "name": "Enthusiasm"},
    17: {"trigrams": "Lake over Thunder", "name": "Following"},
    18: {"trigrams": "Mountain over Wind", "name": "Work on the Decayed"},
    19: {"trigrams": "Earth over Lake", "name": "Approach"},
    20: {"trigrams": "Wind over Earth", "name": "Contemplation"},
    21: {"trigrams": "Fire over Thunder", "name": "Biting Through"},
    22: {"trigrams": "Mountain over Fire", "name": "Grace"},
    23: {"trigrams": "Mountain over Earth", "name": "Splitting Apart"},
    24: {"trigrams": "Earth over Thunder", "name": "Return"},
    25: {"trigrams": "Heaven over Thunder", "name": "Innocence"},
    26: {"trigrams": "Mountain over Heaven", "name": "Great Taming"},
    27: {"trigrams": "Mountain over Thunder", "name": "Nourishment"},
    28: {"trigrams": "Lake over Wind", "name": "Great Exceeding"},
    29: {"trigrams": "Water over Water", "name": "The Abysmal"},
    30: {"trigrams": "Fire over Fire", "name": "The Clinging"},
    31: {"trigrams": "Lake over Mountain", "name": "Influence"},
    32: {"trigrams": "Thunder over Wind", "name": "Duration"},
    33: {"trigrams": "Heaven over Mountain", "name": "Retreat"},
    34: {"trigrams": "Thunder over Heaven", "name": "Great Power"},
    35: {"trigrams": "Fire over Earth", "name": "Progress"},
    36: {"trigrams": "Earth over Fire", "name": "Darkening of the Light"},
    37: {"trigrams": "Wind over Fire", "name": "The Family"},
    38: {"trigrams": "Fire over Lake", "name": "Opposition"},
    39: {"trigrams": "Water over Mountain", "name": "Obstruction"},
    40: {"trigrams": "Thunder over Water", "name": "Deliverance"},
    41: {"trigrams": "Mountain over Lake", "name": "Decrease"},
    42: {"trigrams": "Wind over Thunder", "name": "Increase"},
    43: {"trigrams": "Lake over Heaven", "name": "Breakthrough"},
    44: {"trigrams": "Heaven over Wind", "name": "Coming to Meet"},
    45: {"trigrams": "Lake over Earth", "name": "Gathering Together"},
    46: {"trigrams": "Earth over Wind", "name": "Pushing Upward"},
    47: {"trigrams": "Lake over Water", "name": "Oppression"},
    48: {"trigrams": "Water over Wind", "name": "The Well"},
    49: {"trigrams": "Lake over Fire", "name": "Revolution"},
    50: {"trigrams": "Fire over Wind", "name": "The Cauldron"},
    51: {"trigrams": "Thunder over Thunder", "name": "The Arousing"},
    52: {"trigrams": "Mountain over Mountain", "name": "Keeping Still"},
    53: {"trigrams": "Wind over Mountain", "name": "Development"},
    54: {"trigrams": "Thunder over Lake", "name": "The Marrying Maiden"},
    55: {"trigrams": "Thunder over Fire", "name": "Abundance"},
    56: {"trigrams": "Fire over Mountain", "name": "The Wanderer"},
    57: {"trigrams": "Wind over Wind", "name": "The Gentle"},
    58: {"trigrams": "Lake over Lake", "name": "The Joyous"},
    59: {"trigrams": "Wind over Water", "name": "Dispersion"},
    60: {"trigrams": "Water over Lake", "name": "Limitation"},
    61: {"trigrams": "Wind over Lake", "name": "Inner Truth"},
    62: {"trigrams": "Thunder over Mountain", "name": "Small Exceeding"},
    63: {"trigrams": "Water over Fire", "name": "After Completion"},
    64: {"trigrams": "Fire over Water", "name": "Before Completion"}
}

def fix_line_text(text, position, line_type):
    """修复爻辞的text格式"""
    position_names = {
        1: "Initial",
        2: "Second", 
        3: "Third",
        4: "Fourth",
        5: "Fifth",
        6: "Uppermost"
    }
    
    yang_yin = "Yang" if line_type == "yang" else "Yin"
    return f"The {position_names[position]} {yang_yin}"

def fix_hexagram_data():
    """修复卦象数据"""
    
    # 读取原始数据
    with open('hexagrams_complete_english.json', 'r', encoding='utf-8') as f:
        hexagrams = json.load(f)
    
    print(f"开始修复 {len(hexagrams)} 个卦象...")
    
    for hexagram in hexagrams:
        number = hexagram['number']
        
        # 修复 chineseName 格式
        if number in hexagram_names:
            trigrams = hexagram_names[number]['trigrams']
            name = hexagram_names[number]['name']
            hexagram['chineseName'] = f"{trigrams} - {name}"
            print(f"修复第{number}卦 chineseName: {hexagram['chineseName']}")
        
        # 修复 lines 中的 text 格式
        if 'lines' in hexagram:
            for line in hexagram['lines']:
                if 'position' in line and 'type' in line:
                    old_text = line.get('text', '')
                    new_text = fix_line_text(old_text, line['position'], line['type'])
                    line['text'] = new_text
                    print(f"  修复第{line['position']}爻: {new_text}")
    
    # 保存修复后的数据
    with open('hexagrams_complete_english_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(hexagrams, f, ensure_ascii=False, indent=2)
    
    print("修复完成！已保存到 hexagrams_complete_english_fixed.json")

if __name__ == "__main__":
    fix_hexagram_data()
