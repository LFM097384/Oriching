"""
Hexagram data management and access utilities.
"""

import json
import random
from typing import List, Optional, Dict, Any
from pathlib import Path

from models.schemas import Hexagram


class HexagramDataManager:
    """
    Manages hexagram data loading, caching, and querying.
      This class handles all hexagram data operations including:
    - Loading data from JSON files
    - Caching for performance
    - Searching and filtering hexagrams
    - Providing fallback data
    - Supporting multiple languages
    """
    
    def __init__(self, data_file: str = None):
        """
        Initialize the data manager.
        
        Args:
            data_file: Path to the hexagram data JSON file (optional, will be determined by language)
        """
        self.base_dir = Path(__file__).parent.parent  # utils目录的上级目录，即backend目录
        self.data_file = None  # Will be set based on language
        self._hexagrams_cache: Optional[List[Hexagram]] = None
        self._hexagrams_dict: Optional[Dict[int, Hexagram]] = None
        self._current_language: str = "zh"
        
        # Set initial data file based on default language
        self._update_data_file()
        
    def _update_data_file(self) -> None:
        """
        Update the data file path based on current language.
        """
        if self._current_language == "en":
            filename = "hexagrams_complete_english.json"
        else:
            filename = "hexagrams_complete_fixed.json"
        
        self.data_file = self.base_dir / filename

    def _load_hexagrams_from_file(self) -> List[Dict[str, Any]]:
        """
        Load hexagram data from JSON file.
        
        Returns:
            List of hexagram dictionaries
            
        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Ensure data is a list
            if isinstance(data, dict):
                # If it's a single hexagram, wrap in list
                return [data]
            elif isinstance(data, list):
                return data
            else:
                raise ValueError("Invalid data format in hexagrams file")
                
        except FileNotFoundError:
            # Return default hexagram data if file not found
            return self._get_default_hexagram_data()
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in {self.data_file}: {e.msg}", e.doc, e.pos)
    
    def _get_default_hexagram_data(self) -> List[Dict[str, Any]]:
        """
        Provide default hexagram data as fallback.
        
        Returns:
            List containing default hexagram data
        """
        return [
            {
                "number": 1,
                "name": "Qian",
                "chineseName": "乾",
                "symbol": "☰",
                "upperTrigram": "111",
                "lowerTrigram": "111",
                "description": "纯阳之卦，象征天道刚健，万物之始。代表创造力、领导力和积极进取的精神。",
                "fortune": "大吉大利，诸事顺遂，正是发展的好时机。运势强劲，适合开始新的事业或项目。",
                "love": "感情运势极佳，单身者易遇良缘，有伴者感情升温。真诚待人，感情必有回报。",
                "career": "事业蒸蒸日上，领导能力突出，适合担当重任。把握机会，积极进取，必有所成。",
                "health": "身体健康，精力充沛，但需注意劳逸结合。保持规律作息，适度运动。",
                "advice": "持续努力，保持积极进取的态度，发挥领导才能。时机成熟，大胆行动，必能成就大业。"
            },
            {
                "number": 2,
                "name": "Kun",
                "chineseName": "坤",
                "symbol": "☷",
                "upperTrigram": "000",
                "lowerTrigram": "000",
                "description": "纯阴之卦，象征大地包容万物的品德。代表包容、承载和默默奉献的精神。",
                "fortune": "运势平稳，需要耐心和坚持。虽无大起大落，但稳中有进，厚德载物。",
                "love": "感情需要包容和理解，以柔克刚。真诚相待，细水长流，感情深厚。",
                "career": "事业需要踏实努力，默默耕耘。团队合作，服务他人，终将获得认可。",
                "health": "身体状态稳定，需要调养。注意饮食，保持内心平和，健康自然来。",
                "advice": "保持谦逊包容的态度，以德服人。时机未到不急躁，厚德载物，必有福报。"
            }
        ]
    
    def _get_correct_trigrams(self, hexagram_number: int) -> Dict[str, str]:
        """
        Get the correct traditional I Ching trigram mappings for a hexagram.
        
        Args:
            hexagram_number: The hexagram number (1-64)
            
        Returns:
            Dictionary with 'upper' and 'lower' trigram strings
        """        # 传统易经64卦的正确上下卦组合
        # 使用传统的八卦编码：000=坤(地), 001=震(雷), 010=坎(水), 011=巽(风)
        # 100=艮(山), 101=离(火), 110=兑(泽), 111=乾(天)
        trigram_mappings = {
            1: {"upper": "111", "lower": "111"},   # 乾为天
            2: {"upper": "000", "lower": "000"},   # 坤为地
            3: {"upper": "010", "lower": "001"},   # 水雷屯
            4: {"upper": "100", "lower": "010"},   # 山水蒙
            5: {"upper": "010", "lower": "111"},   # 水天需
            6: {"upper": "111", "lower": "010"},   # 天水讼
            7: {"upper": "000", "lower": "010"},   # 地水师
            8: {"upper": "010", "lower": "000"},   # 水地比
            9: {"upper": "011", "lower": "111"},   # 风天小畜
            10: {"upper": "110", "lower": "111"},  # 泽天履
            11: {"upper": "000", "lower": "111"},  # 地天泰
            12: {"upper": "111", "lower": "000"},  # 天地否
            13: {"upper": "111", "lower": "101"},  # 天火同人
            14: {"upper": "101", "lower": "111"},  # 火天大有
            15: {"upper": "000", "lower": "100"},  # 地山谦
            16: {"upper": "001", "lower": "000"},  # 雷地豫
            17: {"upper": "110", "lower": "001"},  # 泽雷随
            18: {"upper": "100", "lower": "011"},  # 山风蛊
            19: {"upper": "000", "lower": "110"},  # 地泽临
            20: {"upper": "011", "lower": "000"},  # 风地观
            21: {"upper": "101", "lower": "001"},  # 火雷噬嗑
            22: {"upper": "100", "lower": "101"},  # 山火贲
            23: {"upper": "100", "lower": "000"},  # 山地剥
            24: {"upper": "000", "lower": "001"},  # 地雷复
            25: {"upper": "111", "lower": "001"},  # 天雷无妄
            26: {"upper": "100", "lower": "111"},  # 山天大畜
            27: {"upper": "100", "lower": "001"},  # 山雷颐
            28: {"upper": "110", "lower": "011"},  # 泽风大过
            29: {"upper": "010", "lower": "010"},  # 坎为水
            30: {"upper": "101", "lower": "101"},  # 离为火
            31: {"upper": "110", "lower": "100"},  # 泽山咸
            32: {"upper": "001", "lower": "011"},  # 雷风恒
            33: {"upper": "111", "lower": "100"},  # 天山遁
            34: {"upper": "001", "lower": "111"},  # 雷天大壮
            35: {"upper": "101", "lower": "000"},  # 火地晋
            36: {"upper": "000", "lower": "101"},  # 地火明夷
            37: {"upper": "011", "lower": "101"},  # 风火家人
            38: {"upper": "101", "lower": "110"},  # 火泽睽
            39: {"upper": "010", "lower": "100"},  # 水山蹇
            40: {"upper": "001", "lower": "010"},  # 雷水解
            41: {"upper": "100", "lower": "110"},  # 山泽损
            42: {"upper": "011", "lower": "001"},  # 风雷益
            43: {"upper": "110", "lower": "111"},  # 泽天夬
            44: {"upper": "111", "lower": "011"},  # 天风姤
            45: {"upper": "110", "lower": "000"},  # 泽地萃
            46: {"upper": "000", "lower": "011"},  # 地风升
            47: {"upper": "110", "lower": "010"},  # 泽水困
            48: {"upper": "010", "lower": "011"},  # 水风井
            49: {"upper": "110", "lower": "101"},  # 泽火革
            50: {"upper": "101", "lower": "011"},  # 火风鼎
            51: {"upper": "001", "lower": "001"},  # 震为雷
            52: {"upper": "100", "lower": "100"},  # 艮为山
            53: {"upper": "011", "lower": "100"},  # 风山渐
            54: {"upper": "001", "lower": "110"},  # 雷泽归妹
            55: {"upper": "001", "lower": "101"},  # 雷火丰
            56: {"upper": "101", "lower": "100"},  # 火山旅
            57: {"upper": "011", "lower": "011"},  # 巽为风
            58: {"upper": "110", "lower": "110"},  # 兑为泽
            59: {"upper": "011", "lower": "010"},  # 风水涣
            60: {"upper": "010", "lower": "110"},  # 水泽节
            61: {"upper": "011", "lower": "110"},  # 风泽中孚
            62: {"upper": "100", "lower": "001"},  # 山雷小过
            63: {"upper": "010", "lower": "101"},  # 水火既济
            64: {"upper": "101", "lower": "010"}   # 火水未济
        }
        
        return trigram_mappings.get(hexagram_number, {"upper": "000", "lower": "000"})
    
    def _ensure_data_loaded(self) -> None:
        """
        Ensure hexagram data is loaded and cached.
        """
        if self._hexagrams_cache is None:
            raw_data = self._load_hexagrams_from_file()
            
            # Convert to Hexagram objects
            self._hexagrams_cache = []
            self._hexagrams_dict = {}
            
            for item in raw_data:
                try:
                    # 添加兼容处理，处理可能缺失的字段
                    if "upperTrigram" not in item or not item["upperTrigram"]:
                        hexagram_number = item.get("number", 0)
                        # 生成默认的八卦编码
                        if hexagram_number == 1:
                            item["upperTrigram"] = "111"
                            item["lowerTrigram"] = "111"
                        elif hexagram_number == 2:
                            item["upperTrigram"] = "000"
                            item["lowerTrigram"] = "000"
                        else:
                            # 根据传统易经64卦的正确三元组编码
                            trigram_map = self._get_correct_trigrams(hexagram_number)
                            item["upperTrigram"] = trigram_map["upper"]
                            item["lowerTrigram"] = trigram_map["lower"]
                    
                    # 添加描述字段（如果不存在）
                    if "description" not in item and "interpretations" in item and "traditional" in item["interpretations"]:
                        if item["interpretations"]["traditional"] and "description" in item["interpretations"]["traditional"]:
                            item["description"] = item["interpretations"]["traditional"]["description"]
                    elif "description" not in item and "kingWen" in item and "explanation" in item["kingWen"]:
                        item["description"] = item["kingWen"]["explanation"]
                    
                    hexagram = Hexagram(**item)
                    self._hexagrams_cache.append(hexagram)
                    self._hexagrams_dict[hexagram.number] = hexagram
                except Exception as e:
                    print(f"Warning: Skipping invalid hexagram data: {e}")
                    print(f"Problem item: {item}")
                    continue
    
    def get_all_hexagrams(self) -> List[Hexagram]:
        """
        Get all hexagrams.
        
        Returns:
            List of all Hexagram objects
        """
        self._ensure_data_loaded()
        return self._hexagrams_cache.copy()
    
    def get_hexagram_by_number(self, number: int) -> Optional[Hexagram]:
        """
        Get a hexagram by its number.
        
        Args:
            number: Hexagram number (1-64)
            
        Returns:
            Hexagram object if found, None otherwise
        """
        self._ensure_data_loaded()
        return self._hexagrams_dict.get(number)
    
    def get_hexagram_by_trigrams(self, upper_trigram: str, lower_trigram: str) -> Optional[Hexagram]:
        """
        Get hexagram by upper and lower trigram combinations.
        
        Args:
            upper_trigram: Upper trigram in binary format (e.g., "111")
            lower_trigram: Lower trigram in binary format (e.g., "000")
            
        Returns:
            Matching Hexagram object or None
        """
        self._ensure_data_loaded()
        
        for hexagram in self._hexagrams_cache:
            if (hexagram.upperTrigram == upper_trigram and 
                hexagram.lowerTrigram == lower_trigram):
                return hexagram
        
        return None
    
    def search_hexagrams_by_name(self, name: str) -> List[Hexagram]:
        """
        Search hexagrams by Chinese or English name (partial match).
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching Hexagram objects        """
        self._ensure_data_loaded()
        name_lower = name.lower()
        results = []
        
        for hexagram in self._hexagrams_cache:
            if (name_lower in hexagram.name.lower() or 
                name in hexagram.chineseName):
                results.append(hexagram)
        
        return results
    
    def get_random_hexagram(self) -> Hexagram:
        """
        Get a random hexagram.
        
        Returns:
            Random Hexagram object
            
        Raises:
            ValueError: If no hexagrams are available
        """
        self._ensure_data_loaded()
        
        if not self._hexagrams_cache:
            raise ValueError("No hexagrams available")
        
        return random.choice(self._hexagrams_cache)
    
    def set_language(self, language: str) -> None:
        """
        Set the current language for data retrieval.
        
        Args:
            language: Language code ('zh' for Chinese, 'en' for English)
        """
        old_language = self._current_language
        if language in ['zh', 'en']:
            self._current_language = language
        else:
            self._current_language = 'zh'  # Default to Chinese
        
        # If language changed, update data file and clear cache
        if old_language != self._current_language:
            self._update_data_file()
            self._hexagrams_cache = None
            self._hexagrams_dict = None
    
    def get_localized_text(self, text_obj: Dict[str, Any], field: str = "text") -> str:
        """
        Get localized text from a text object.
        
        Args:
            text_obj: Object containing text in multiple languages
            field: Field name to retrieve ('text', 'explanation', etc.)
            
        Returns:
            Localized text string
        """
        if not text_obj:
            return ""
            
        # If current language is English and English version exists
        if self._current_language == "en" and "english" in text_obj:
            english_obj = text_obj["english"]
            if isinstance(english_obj, dict) and field in english_obj:
                return english_obj[field]
        
        # Fall back to Chinese or direct field access
        if isinstance(text_obj, dict) and field in text_obj:
            return text_obj[field]
        elif isinstance(text_obj, str):
            return text_obj
        
        return ""
    
    def get_localized_hexagram_name(self, hexagram_data: Dict[str, Any]) -> str:
        """
        Get localized hexagram name.
        
        Args:
            hexagram_data: Hexagram data dictionary
            
        Returns:
            Localized hexagram name
        """
        if self._current_language == "en" and "english" in hexagram_data:
            english_obj = hexagram_data["english"]
            if "name" in english_obj:
                return english_obj["name"]
        
        # Fall back to Chinese name
        return hexagram_data.get("name", "")
    
    def get_localized_hexagram_meaning(self, hexagram_data: Dict[str, Any]) -> str:
        """
        Get localized hexagram meaning.
        
        Args:
            hexagram_data: Hexagram data dictionary
            
        Returns:
            Localized hexagram meaning
        """
        if self._current_language == "en" and "english" in hexagram_data:
            english_obj = hexagram_data["english"]
            if "chineseName" in english_obj:
                return english_obj["chineseName"]
        
        # Fall back to Chinese meaning
        return hexagram_data.get("chineseName", "")
    
    def refresh_data(self) -> None:
        """
        Refresh the cached data by reloading from file.
        """
        self._hexagrams_cache = None
        self._hexagrams_dict = None
        self._ensure_data_loaded()


# Create default manager instance
hexagram_manager = HexagramDataManager()


def get_hexagram_by_number(number: int) -> Optional[Hexagram]:
    """Convenience function to get hexagram by number."""
    return hexagram_manager.get_hexagram_by_number(number)


def get_hexagram_by_trigrams(upper_trigram: str, lower_trigram: str) -> Optional[Hexagram]:
    """Convenience function to get hexagram by trigrams."""
    return hexagram_manager.get_hexagram_by_trigrams(upper_trigram, lower_trigram)


def get_all_hexagrams() -> List[Hexagram]:
    """Convenience function to get all hexagrams."""
    return hexagram_manager.get_all_hexagrams()
