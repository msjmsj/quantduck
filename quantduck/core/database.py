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
    
    def get_recent_signals(self, hours: int = 24) -> List[Dict]:
        """获取最近的信号数据。

        Args:
            hours (int): 获取多少小时内的信号，默认24小时

        Returns:
            List[Dict]: 信号列表，每个信号包含以下字段：
                - token: 代币地址
                - timestamp: 信号时间
                - type: 信号类型
                - ...

        Examples:
            >>> db = get_db()
            >>> signals = db.get_recent_signals(hours=12)
            >>> print(len(signals))
        """
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

    def check_and_insert_signal(self, token_address: str, source: str) -> bool:
        """检查代币是否在最近24小时内出现过，如果没有则插入新的信号记录。

        Args:
            token_address (str): 代币地址
            source (str): 信号来源

        Returns:
            bool: 如果成功插入新记录返回True，如果代币已存在返回False

        Examples:
            >>> db = get_db()
            >>> success = db.check_and_insert_signal("0x123...", "dex_scan")
        """
        # 检查代币是否在最近24小时内出现过
        if self.check_token_in_recent_signals(token_address):
            return False
        
        # 使用当前中国时间
        detected_time = datetime.now(self.CN_TIMEZONE)
            
        sql = """
            INSERT INTO signal_summary (token_address, source, detected_time)
            VALUES (%s, %s, %s)
        """
        
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (token_address, source, detected_time))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)

    def check_token_in_digestchain(self, token_address: str) -> bool:
        """检查代币是否存在于 digestchain 表中

        Args:
            token_address (str): 代币地址

        Returns:
            bool: 如果代币存在返回 True，否则返回 False
        """
        sql = """
            SELECT COUNT(*) as count 
            FROM digestchain 
            WHERE address = %s
        """
        
        result = self.query(sql)
        return bool(result and result[0]['count'] > 0)

    def insert_token_to_digestchain(self, token_address: str, source: str) -> bool:
        """将代币插入到 digestchain 表中

        Args:
            token_address (str): 代币地址
            source (str): 来源

        Returns:
            bool: 插入成功返回 True
        """
        current_time = datetime.now(self.CN_TIMEZONE)
        sql = """
            INSERT INTO digestchain (address, update_time, source)
            VALUES (%s, %s, %s)
        """
        
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (token_address, current_time, source))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)

    def process_new_token(self, token_address: str, source: str) -> dict:
        """综合处理新代币的完整流程
        
        1. 检查并插入到 signal_summary 表
        2. 检查并插入到 digestchain 表
        
        Args:
            token_address (str): 代币地址
            source (str): 信号来源
            
        Returns:
            dict: 处理结果
            {
                'signal_added': bool,  # 是否添加了新信号
                'digest_added': bool,  # 是否添加到 digestchain
                'message': str        # 处理结果描述
            }
        """
        result = {
            'signal_added': False,
            'digest_added': False,
            'message': ''
        }
        
        try:
            # 检查并插入信号
            signal_added = self.check_and_insert_signal(token_address, source)
            result['signal_added'] = signal_added
            
            # 检查并插入 digestchain
            if not self.check_token_in_digestchain(token_address):
                self.insert_token_to_digestchain(token_address, source)
                result['digest_added'] = True
                
            # 生成结果消息
            messages = []
            if signal_added:
                messages.append("新信号已添加")
            else:
                messages.append("代币在最近24小时内已存在")
                
            if result['digest_added']:
                messages.append("代币已添加到 digestchain")
            else:
                messages.append("代币已存在于 digestchain")
                
            result['message'] = '；'.join(messages)
            
        except Exception as e:
            result['message'] = f"处理过程中发生错误: {str(e)}"
            raise
            
        return result

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