from abc import ABC, abstractmethod
from typing import Protocol, List
import pandas as pd
import logging

# 设置日志

logger = logging.getLogger(__name__)

class KlineValidator(Protocol):
    """K线数据验证器协议"""
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """验证并返回处理后的数据"""
        pass

class BaseValidator(ABC):
    """验证器基类"""
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """验证并返回处理后的数据"""
        pass

class DuplicateTimeValidator(BaseValidator):
    """重复时间戳验证器"""
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.index.duplicated().any():
            logger.warning("发现重复的时间戳，保留最后一个值")
            return df[~df.index.duplicated(keep='last')]
        return df

class NegativePriceValidator(BaseValidator):
    """负价格验证器"""
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in ['open', 'high', 'low', 'close']:
            if (df[col] < 0).any():
                logger.warning(f"{col}列存在负值，已被移除")
                df = df[df[col] >= 0]
        return df

class HighLowValidator(BaseValidator):
    """最高最低价验证器"""
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        invalid_hl = df[df['high'] < df['low']].index
        if len(invalid_hl) > 0:
            logger.warning("发现最高价小于最低价的记录，已修正")
            df.loc[invalid_hl, 'high'], df.loc[invalid_hl, 'low'] = (
                df.loc[invalid_hl, 'low'], df.loc[invalid_hl, 'high']
            )
        return df

class TimeSeriesValidator(BaseValidator):
    """完整时间序列验证器
    
    用于确保K线数据在时间序列上的完整性，可以处理不同的时间频率，并对缺失数据进行填充。
    
    支持的时间频率参数(freq):
        秒级：
            'S': 秒
            '2S': 2秒
            ...
        分钟级：
            'T'或'min': 分钟
            '5T'或'5min': 5分钟
            '15T'或'15min': 15分钟
            '30T'或'30min': 30分钟
            ...
        小时级：
            'H': 小时
            '2H': 2小时
            ...
        天级：
            'D': 天
            'B': 工作日
            'W': 周
            ...
        月级：
            'M': 月末
            'BM': 工作日月末
            ...
        季度级：
            'Q': 季度末
            'BQ': 工作日季度末
            ...
        年级：
            'Y': 年末
            'BY': 工作日年末
            ...
            
    使用示例:
        # 创建一个处理小时级数据的验证器
        validator = TimeSeriesValidator(freq='H')
        
        # 创建一个处理15分钟级数据的验证器
        validator = TimeSeriesValidator(freq='15T')
        
        # 在数据处理器中使用
        processor = KlineDataProcessor([
            DuplicateTimeValidator(),
            TimeSeriesValidator(freq='5min')
        ])
        
        # 处理日线数据
        daily_validator = TimeSeriesValidator(freq='D')
        
        # 处理工作日数据（跳过周末）
        business_validator = TimeSeriesValidator(freq='B')
    """
    
    def __init__(self, freq='H'):
        """初始化时间序列验证器
        
        Args:
            freq (str): 时间频率字符串，默认为'H'（小时）
                常用值:
                - 'S': 秒
                - 'T'或'min': 分钟
                - 'H': 小时
                - 'D': 天
                - 'B': 工作日
                - 'W': 周
                - 'M': 月末
                也可以使用数字前缀，如：
                - '5T': 5分钟
                - '4H': 4小时
                
        示例:
            >>> validator = TimeSeriesValidator(freq='15T')  # 15分钟K线
            >>> validator = TimeSeriesValidator(freq='1H')   # 1小时K线
            >>> validator = TimeSeriesValidator(freq='1D')   # 日K线
        """
        self.freq = freq

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """确保时间序列的完整性并填充缺失值
        
        处理步骤：
        1. 检查输入数据是否为空
        2. 创建完整的时间序列（基于给定的频率）
        3. 检测缺失的时间点
        4. 使用前值填充方法处理缺失数据
        
        Args:
            df (pd.DataFrame): 输入的DataFrame，必须包含OHLCV数据，
                             且index为datetime类型
        
        Returns:
            pd.DataFrame: 处理后的DataFrame，包含完整的时间序列和填充后的数据
        
        示例:
            >>> df = validator.validate(df)  # 验证并填充缺失的时间点
        """
        if df.empty:
            logger.warning("输入数据为空")
            return df

        # 创建完整时间序列
        full_range = pd.date_range(start=df.index.min(), 
                                 end=df.index.max(), 
                                 freq=self.freq)
        
        # 检查是否有缺失的时间点
        missing_times = full_range.difference(df.index)
        if len(missing_times) > 0:
            logger.info(f"发现{len(missing_times)}个缺失的时间点，将进行填充")
        
        # 重建索引并填充缺失值
        df = df.reindex(full_range)
        df['close'] = df['close'].fillna(method='ffill')
        df['open'] = df['open'].fillna(df['close'])
        df['high'] = df['high'].fillna(df['close'])
        df['low'] = df['low'].fillna(df['close'])
        df['volume'] = df['volume'].fillna(0)
        
        return df

class KlineDataProcessor:
    """K线数据处理器"""
    def __init__(self, validators: List[BaseValidator] = None):
        self.validators = validators or [
            DuplicateTimeValidator(),
            NegativePriceValidator(),
            HighLowValidator(),
            TimeSeriesValidator(freq='H')
        ]

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理K线数据"""
        # 应用所有验证器
        for validator in self.validators:
            df = validator.validate(df)
        
        # 排序
        df = df.sort_index()
        
        return df
