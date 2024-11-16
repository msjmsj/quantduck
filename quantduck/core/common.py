from typing import List, Dict, Any
from datetime import datetime

class DataProcessor:
    """数据处理的基础类"""
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """验证日期格式"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def calculate_percentage_change(old_value: float, new_value: float) -> float:
        """计算百分比变化"""
        if old_value == 0:
            return 0
        return ((new_value - old_value) / old_value) * 100

class Logger:
    """日志记录类"""
    
    @staticmethod
    def log(message: str, level: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{level}] {timestamp}: {message}") 