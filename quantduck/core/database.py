from abc import ABC, abstractmethod
from typing import Any, Dict, List

"""数据库模块设计说明:

设计模式:
1. 抽象工厂模式 (Abstract Factory Pattern)
   - DatabaseFactory 用于创建不同类型的数据库连接
2. 抽象基类模式 (Abstract Base Class Pattern)
   - DatabaseInterface 定义了所有数据库实现必须遵循的接口

扩展方法:
1. 添加新的数据库支持:
   - 创建新的类继承 DatabaseInterface
   - 实现所有抽象方法 (connect, disconnect, query)
   - 在 DatabaseFactory 中添加对应的创建方法

设计原则:
1. 开闭原则 (Open/Closed Principle)
   - 可以添加新的数据库实现而无需修改现有代码
2. 依赖倒置原则 (Dependency Inversion Principle)
   - 高层模块通过抽象接口调用数据库，不依赖具体实现

使用示例:
db = DatabaseFactory.create_database("mysql", host="localhost", port=3306)
"""

class DatabaseInterface(ABC):
    """数据库接口的抽象基类"""
    
    @abstractmethod
    def connect(self) -> bool:
        """连接数据库"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """断开连接"""
        pass
    
    @abstractmethod
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """执行查询"""
        pass

class SQLiteDatabase(DatabaseInterface):
    """SQLite数据库实现"""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def connect(self) -> bool:
        try:
            import sqlite3
            self.connection = sqlite3.connect(self.db_path)
            return True
        except Exception:
            return False
            
    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            
    def query(self, sql: str) -> List[Dict[str, Any]]:
        if not self.connection:
            raise ConnectionError("Database not connected")
        cursor = self.connection.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

class DatabaseFactory:
    """数据库工厂类"""
    
    @staticmethod
    def create_database(db_type: str, **kwargs) -> DatabaseInterface:
        if db_type.lower() == "sqlite":
            return SQLiteDatabase(kwargs.get("db_path", ":memory:"))
        raise ValueError(f"Unsupported database type: {db_type}") 