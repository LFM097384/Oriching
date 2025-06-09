#!/usr/bin/env python3
"""
Create a pure English version of hexagrams_complete_fixed.json
This script reads the bilingual version and extracts only the English content.
"""

import json
import os

def extract_english_content(obj):
    """Recursively extract English content from bilingual objects"""
    if isinstance(obj, dict):
        # Handle standard bilingual structure
        if 'english' in obj:
            english_content = obj['english']
            # Keep the structure but use English content
            result = {}
            for key, value in obj.items():
                if key == 'english':
                    continue
                elif key in ['text', 'explanation', 'description', 'white_explanation']:
                    # Replace with English version if available
                    if isinstance(english_content, dict) and key in english_content:
                        result[key] = english_content[key]
                    else:
                        result[key] = translate_key_text(value, key)
                else:
                    result[key] = extract_english_content(value)
            
            # Add any English-only fields
            if isinstance(english_content, dict):
                for key, value in english_content.items():
                    if key not in result:
                        result[key] = value
            
            return result
        else:
            # No English version, process recursively
            result = {}
            for key, value in obj.items():
                if key == 'english':
                    continue
                elif key in ['name', 'chineseName']:
                    result[key] = translate_hexagram_name(value, key)
                elif key in ['daxiang', 'fortune', 'career', 'business', 'fame', 'love', 'advice', 'health']:
                    result[key] = translate_aspect(value, key)
                else:
                    result[key] = extract_english_content(value)
            return result
    elif isinstance(obj, list):
        return [extract_english_content(item) for item in obj]
    else:
        return obj

def translate_hexagram_name(chinese_name, key):
    """Translate hexagram names to English"""
    hexagram_names = {
        "乾卦": "Qian (The Creative)",
        "坤卦": "Kun (The Receptive)", 
        "屯卦": "Zhun (Difficulty at the Beginning)",
        "蒙卦": "Meng (Youthful Folly)",
        "需卦": "Xu (Waiting)",
        "讼卦": "Song (Conflict)",
        "师卦": "Shi (The Army)",
        "比卦": "Pi (Holding Together)",
        "小畜卦": "Xiao Xu (Small Taming)",
        "履卦": "Lu (Treading)",
        "泰卦": "Tai (Peace)",
        "否卦": "Pi (Standstill)",
        # Add more translations as needed
    }
    
    chinese_names = {
        "乾為天": "Heaven over Heaven",
        "坤為地": "Earth over Earth",
        "水雷屯": "Water over Thunder", 
        "山水蒙": "Mountain over Water",
        "水天需": "Water over Heaven",
        "天水讼": "Heaven over Water",
        "地水师": "Earth over Water",
        "水地比": "Water over Earth",
        # Add more translations as needed
    }
    
    if key == "name":
        return hexagram_names.get(chinese_name, chinese_name)
    elif key == "chineseName":
        return chinese_names.get(chinese_name, chinese_name)
    
    return chinese_name

def translate_aspect(text, aspect):
    """Translate fortune aspects to English"""
    # This is a simplified translation - in a real implementation,
    # you would use a proper translation service or predefined translations
    aspect_translations = {
        "daxiang": "Great Symbol: " + text,
        "fortune": "Fortune: " + text,
        "career": "Career: " + text,
        "business": "Business: " + text,
        "fame": "Fame: " + text,
        "love": "Love: " + text,
        "advice": "Advice: " + text,
        "health": "Health: " + text
    }
    
    # For now, return a placeholder or the original text
    # In a real implementation, these would be properly translated
    return f"[{aspect.title()}] " + text

def translate_key_text(text, key):
    """Translate specific key texts"""
    if key == "text":
        if "爻辭" in text:
            position_map = {
                "初九爻辭": "First Yang Line",
                "九二爻辭": "Second Yang Line", 
                "九三爻辭": "Third Yang Line",
                "九四爻辭": "Fourth Yang Line",
                "九五爻辭": "Fifth Yang Line",
                "上九爻辭": "Sixth Yang Line",
                "初六爻辭": "First Yin Line",
                "六二爻辭": "Second Yin Line",
                "六三爻辭": "Third Yin Line", 
                "六四爻辭": "Fourth Yin Line",
                "六五爻辭": "Fifth Yin Line",
                "上六爻辭": "Sixth Yin Line"
            }
            return position_map.get(text, text)
    
    return text

def main():
    input_file = "hexagrams_complete_with_english.json"
    output_file = "hexagrams_complete_english.json"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    # Read the bilingual JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        bilingual_data = json.load(f)
    
    print(f"Processing {len(bilingual_data)} hexagrams...")
    
    # Extract English content
    english_data = extract_english_content(bilingual_data)
    
    # Write the English-only JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(english_data, f, ensure_ascii=False, indent=2)
    
    print(f"English version created: {output_file}")
    print(f"File size: {os.path.getsize(output_file)} bytes")

if __name__ == "__main__":
    main()
