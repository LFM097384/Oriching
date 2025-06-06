"""
Routers package for the divination API.
Contains all API route definitions.
"""

from .divination import router as divination_router
from .hexagrams import router as hexagrams_router

__all__ = [
    "divination_router",
    "hexagrams_router"
]
