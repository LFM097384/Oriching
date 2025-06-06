"""
Hexagrams router - handles hexagram information queries.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from models.schemas import Hexagram, HexagramResponse
from utils.hexagram_data import HexagramDataManager

router = APIRouter(prefix="/api", tags=["hexagrams"])

# Initialize data manager
data_manager = HexagramDataManager()


@router.get("/hexagrams", response_model=HexagramResponse)
async def get_all_hexagrams(
    limit: Optional[int] = Query(None, ge=1, le=64, description="Maximum number of hexagrams to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of hexagrams to skip")
) -> HexagramResponse:
    """
    Get all hexagrams or a subset with pagination.
    
    Args:
        limit: Maximum number of hexagrams to return (optional)
        offset: Number of hexagrams to skip for pagination
        
    Returns:
        HexagramResponse: List of hexagrams with total count
    """
    try:
        hexagrams = data_manager.get_all_hexagrams()
        total = len(hexagrams)
        
        # Apply pagination if specified
        if limit is not None:
            hexagrams = hexagrams[offset:offset + limit]
        elif offset > 0:
            hexagrams = hexagrams[offset:]
        
        return HexagramResponse(hexagrams=hexagrams, total=total)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取卦象数据失败: {str(e)}")


@router.get("/hexagrams/{hexagram_id}", response_model=Hexagram)
async def get_hexagram(hexagram_id: int) -> Hexagram:
    """
    Get a specific hexagram by its ID (number).
    
    Args:
        hexagram_id: Hexagram number (1-64)
        
    Returns:
        Hexagram: The requested hexagram
        
    Raises:
        HTTPException: If hexagram is not found
    """
    if hexagram_id < 1 or hexagram_id > 64:
        raise HTTPException(status_code=400, detail="卦象编号必须在1-64之间")
    
    try:
        hexagram = data_manager.get_hexagram_by_number(hexagram_id)
        if hexagram is None:
            raise HTTPException(status_code=404, detail=f"未找到编号为 {hexagram_id} 的卦象")
        
        return hexagram
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取卦象失败: {str(e)}")


@router.get("/hexagrams/search/{name}")
async def search_hexagrams_by_name(name: str) -> HexagramResponse:
    """
    Search hexagrams by Chinese or English name.
    
    Args:
        name: Name to search for (partial match supported)
        
    Returns:
        HexagramResponse: List of matching hexagrams
    """
    if not name.strip():
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
    
    try:
        hexagrams = data_manager.search_hexagrams_by_name(name.strip())
        return HexagramResponse(hexagrams=hexagrams, total=len(hexagrams))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索卦象失败: {str(e)}")


@router.get("/hexagrams/trigram/{upper_trigram}/{lower_trigram}")
async def get_hexagram_by_trigrams(upper_trigram: str, lower_trigram: str) -> Hexagram:
    """
    Get hexagram by upper and lower trigram combinations.
    
    Args:
        upper_trigram: Upper trigram in binary format (e.g., "111")
        lower_trigram: Lower trigram in binary format (e.g., "000")
        
    Returns:
        Hexagram: The matching hexagram
        
    Raises:
        HTTPException: If trigrams are invalid or hexagram not found
    """
    # Validate trigram format
    if not (len(upper_trigram) == 3 and all(c in '01' for c in upper_trigram)):
        raise HTTPException(status_code=400, detail="上卦格式错误，应为3位二进制字符串")
    
    if not (len(lower_trigram) == 3 and all(c in '01' for c in lower_trigram)):
        raise HTTPException(status_code=400, detail="下卦格式错误，应为3位二进制字符串")
    
    try:
        hexagram = data_manager.get_hexagram_by_trigrams(upper_trigram, lower_trigram)
        if hexagram is None:
            raise HTTPException(
                status_code=404, 
                detail=f"未找到上卦为{upper_trigram}，下卦为{lower_trigram}的卦象"
            )
        
        return hexagram
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询卦象失败: {str(e)}")


@router.get("/hexagrams/random")
async def get_random_hexagram() -> Hexagram:
    """
    Get a random hexagram for inspiration or study.
    
    Returns:
        Hexagram: A randomly selected hexagram
    """
    try:
        hexagram = data_manager.get_random_hexagram()
        return hexagram
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取随机卦象失败: {str(e)}")
