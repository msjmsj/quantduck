from typing import List, Dict, Any
from abc import ABC, abstractmethod

class TechnicalIndicator(ABC):
    """技术指标的抽象基类"""
    
    @abstractmethod
    def calculate(self, data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        """计算技术指标"""
        pass

class MovingAverage(TechnicalIndicator):
    """移动平均线"""
    
    def __init__(self, period: int = 20):
        self.period = period
    
    def calculate(self, data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        prices = [d.get("price", 0) for d in data]
        ma = []
        for i in range(len(prices)):
            if i < self.period - 1:
                ma.append(None)
            else:
                ma.append(sum(prices[i-self.period+1:i+1]) / self.period)
        return {"MA": ma}

class RSI(TechnicalIndicator):
    """相对强弱指标(RSI)"""
    
    def __init__(self, period: int = 14):
        self.period = period
    
    def calculate(self, data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        prices = [d.get("price", 0) for d in data]
        rsi = []
        for i in range(len(prices)):
            if i < self.period:
                rsi.append(None)
                continue
                
            gains = []
            losses = []
            for j in range(i-self.period+1, i+1):
                change = prices[j] - prices[j-1]
                if change >= 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))
            
            avg_gain = sum(gains) / self.period
            avg_loss = sum(losses) / self.period
            
            if avg_loss == 0:
                rsi.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi.append(100 - (100 / (1 + rs)))
                
        return {"RSI": rsi} 