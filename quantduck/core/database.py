from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import pytz
from datetime import datetime, timedelta
from psycopg2 import pool

"""数据库模块设计说明:

设计模式:
1. 抽象工厂模式 (Abstract Factory Pattern)
   - DatabaseFactory 用于创建不同类型的数据库连接
2. 抽象基类模式 (Abstract Base Class Pattern)
   - DatabaseInterface 定义了所有数据库实现必须遵循的接口
3. 单例模式 (Singleton Pattern)
   - 确保全局只有一个数据库连接实例
"""

# 默认配置
DEFAULT_DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "yra154351846",
    "host": "192.168.1.8",
    "port": "5432"
}

class DatabaseInterface(ABC):
    """数据库接口的抽象基类"""
    
    @abstractmethod
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """执行查询"""
        pass

class PostgreSQLDatabase(DatabaseInterface):
    """PostgreSQL数据库实现"""
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.db_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.CN_TIMEZONE = pytz.timezone('Asia/Shanghai')
        # 初始化时就创建连接池
        self.pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            **self.db_params
        )
        # 设置时区
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SET timezone='Asia/Shanghai'")
            conn.commit()
        self.pool.putconn(conn)
            
    def query(self, sql: str) -> List[Dict[str, Any]]:
        if not self.pool:
            raise ConnectionError("Database not connected")
        
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                columns = [desc[0] for desc in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.commit()
            return results
        finally:
            self.pool.putconn(conn)
    
    def get_recent_signals(self, hours: int = 24) -> List[Dict[str, Any]]:
        """获取最近指定小时数的信号数据，使用中国时区"""
        sql = f"""
            SELECT *
            FROM signal_summary
            WHERE detected_time > (NOW() AT TIME ZONE 'Asia/Shanghai' - INTERVAL '{hours} hours')
            ORDER BY detected_time DESC
        """
        
        results = self.query(sql)
        
        for row in results:
            if 'detected_time' in row and row['detected_time']:
                row['detected_time'] = row['detected_time'].astimezone(self.CN_TIMEZONE)
        
        return results

    def check_token_in_recent_signals(self, token_address: str, hours: int = 24) -> bool:
        """检查指定的 token_address 在最近指定小时数内是否出现在信号数据中
        
        Args:
            token_address: 要检查的 token 地址字符串
            hours: 检查的时间范围,默认24小时
            
        Returns:
            bool: 如果 token_address 在指定时间范围内出现过,返回 True,否则返回 False
        """
        sql = f"""
            SELECT COUNT(*) AS count
            FROM signal_summary
            WHERE token_address = '{token_address}'
              AND detected_time > (NOW() AT TIME ZONE 'Asia/Shanghai' - INTERVAL '{hours} hours')
        """
        
        result = self.query(sql)
        return bool(result and result[0]['count'] > 0)

# 全局数据库实例
_db_instance: Optional[DatabaseInterface] = None

def get_db() -> DatabaseInterface:
    """获取全局数据库实例"""
    global _db_instance
    if _db_instance is None:
        config = DEFAULT_DB_CONFIG.copy()
        _db_instance = PostgreSQLDatabase(
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"]
        )
    return _db_instance 