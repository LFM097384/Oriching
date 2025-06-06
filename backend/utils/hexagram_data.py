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
    """
    def __init__(self, data_file: str = "hexagrams_complete_fixed.json"):
        """
        Initialize the data manager.
        
        Args:
            data_file: Path to the hexagram data JSON file
        """
        # 检查是否是相对路径，如果是，则转换为项目根目录的绝对路径
        if not Path(data_file).is_absolute():
            base_dir = Path(__file__).parent.parent  # utils目录的上级目录，即backend目录
            self.data_file = base_dir / data_file
        else:
            self.data_file = Path(data_file)
            
        self._hexagrams_cache: Optional[List[Hexagram]] = None
        self._hexagrams_dict: Optional[Dict[int, Hexagram]] = None
        
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
            }        ]
    
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
                            # 根据卦象生成上下卦（简化版）
                            base_code = bin(hexagram_number)[2:].zfill(6)
                            item["upperTrigram"] = base_code[:3]
                            item["lowerTrigram"] = base_code[3:]
                    
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
            List of matching Hexagram objects
        """
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
    
    def get_hexagrams_by_trigram(self, trigram: str, position: str = "both") -> List[Hexagram]:
        """
        Get hexagrams containing a specific trigram.
        
        Args:
            trigram: Trigram in binary format (e.g., "111")
            position: Where to look - "upper", "lower", or "both"
            
        Returns:
            List of matching Hexagram objects
        """
        self._ensure_data_loaded()
        
        results = []
        
        for hexagram in self._hexagrams_cache:
            if position in ["upper", "both"] and hexagram.upperTrigram == trigram:
                results.append(hexagram)
            elif position in ["lower", "both"] and hexagram.lowerTrigram == trigram:
                if hexagram not in results:  # Avoid duplicates when position="both"
                    results.append(hexagram)
        
        return results
    
    def refresh_data(self) -> None:
        """
        Refresh the cached data by reloading from file.
        """
        self._hexagrams_cache = None
        self._hexagrams_dict = None
        self._ensure_data_loaded()
