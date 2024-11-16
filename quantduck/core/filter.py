from abc import ABC, abstractmethod
from typing import List, Dict, Any

class FilterStrategy(ABC):
    """筛选策略的抽象基类"""
    
    @abstractmethod
    def filter(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """执行筛选"""
        pass

class PriceFilter(FilterStrategy):
    """价格筛选策略"""
    
    def __init__(self, min_price: float = None, max_price: float = None):
        self.min_price = min_price
        self.max_price = max_price
    
    def filter(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = data
        if self.min_price is not None:
            result = [d for d in result if d.get("price", 0) >= self.min_price]
        if self.max_price is not None:
            result = [d for d in result if d.get("price", 0) <= self.max_price]
        return result

class VolumeFilter(FilterStrategy):
    """成交量筛选策略"""
    
    def __init__(self, min_volume: int = None):
        self.min_volume = min_volume
    
    def filter(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self.min_volume is None:
            return data
        return [d for d in data if d.get("volume", 0) >= self.min_volume] 