from quantduck.core.db_manager import get_db
from datetime import datetime
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SignalAnalyzer(ABC):
    """信号分析器的抽象基类"""
    @abstractmethod
    def analyze(self, signals: List[Dict[str, Any]]) -> None:
        """分析信号数据的抽象方法"""
        pass

class BasicSignalPrinter(SignalAnalyzer):
    """基础信号打印器"""
    def analyze(self, signals: List[Dict[str, Any]]) -> None:
        print(f"\n找到 {len(signals)} 个信号\n")
        
        if not signals:
            print("没有找到任何信号")
            return
            
        print("=== 最新的5个信号 ===")
        for signal in signals[:5]:
            self._print_signal_summary(signal)
    
    def _print_signal_summary(self, signal: Dict[str, Any]) -> None:
        """打印单个信号的摘要信息"""
        print(f"\n信号时间: {signal['detected_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        for key, value in signal.items():
            if key != 'detected_time':
                print(f"{key}: {value}")

class StatisticalAnalyzer(SignalAnalyzer):
    """统计分析器"""
    def analyze(self, signals: List[Dict[str, Any]]) -> None:
        if not signals:
            return
            
        df = pd.DataFrame(signals)
        
        print("\n=== 数据统计 ===")
        # 按小时统计信号数量
        df['hour'] = df['detected_time'].dt.hour
        hourly_counts = df.groupby('hour').size()
        print("\n每小时信号数量:")
        print(hourly_counts)
        
        # 显示数值型列的基本统计信息
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_columns) > 0:
            print("\n数值统计:")
            print(df[numeric_columns].describe())

class SignalAnalysisManager:
    """信号分析管理器"""
    def __init__(self):
        self.analyzers: List[SignalAnalyzer] = []
    
    def add_analyzer(self, analyzer: SignalAnalyzer) -> None:
        """添加分析器"""
        self.analyzers.append(analyzer)
    
    def analyze_signals(self, hours: int = 24) -> None:
        """执行信号分析"""
        db = get_db()
        try:
            signals = db.get_recent_signals(hours=hours)
            for analyzer in self.analyzers:
                analyzer.analyze(signals)
        except Exception as e:
            print(f"分析过程中发生错误: {e}")

def main():
    """主函数"""
    # 创建分析管理器
    manager = SignalAnalysisManager()
    
    # 添加分析器
    manager.add_analyzer(BasicSignalPrinter())
    manager.add_analyzer(StatisticalAnalyzer())
    
    # 执行分析
    manager.analyze_signals()

if __name__ == "__main__":
    main()