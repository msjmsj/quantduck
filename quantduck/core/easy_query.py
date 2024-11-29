from typing import Any, Dict, List, Callable, TypeVar, Optional
from functools import wraps
import pytz
from datetime import datetime
from psycopg2 import pool

T = TypeVar('T')

# 默认数据库配置
DEFAULT_DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "yra154351846",
    "host": "192.168.1.8",
    "port": "5432"
}

def singleton(cls):
    """单例模式装饰器"""
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

class QueryResult:
    """查询结果包装器"""
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
    
    def first(self) -> Optional[Dict[str, Any]]:
        """获取第一条结果"""
        return self.data[0] if self.data else None
    
    def all(self) -> List[Dict[str, Any]]:
        """获取所有结果"""
        return self.data
    
    def count(self) -> int:
        """获取结果数量"""
        return len(self.data)

def query_method(sql_template: str):
    """查询方法装饰器
    
    用法示例:
    @query_method("SELECT * FROM table WHERE id = {id}")
    def get_by_id(self, id: int) -> QueryResult:
        pass
    """
    def decorator(func: Callable[..., QueryResult]) -> Callable[..., QueryResult]:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # 获取函数的参数名
            from inspect import signature
            sig = signature(func)
            bound_args = sig.bind(self, *args, **kwargs)
            bound_args.apply_defaults()
            
            # 移除self参数
            params = dict(bound_args.arguments)
            params.pop('self')
            
            # 格式化SQL
            sql = sql_template.format(**params)
            
            # 执行查询
            results = self.execute_query(sql)
            return QueryResult(results)
        return wrapper
    return decorator

@singleton
class EasyQuery:
    """简易查询类
    
    用法示例:
    db = EasyQuery()
    signals = db.get_recent_signals(hours=24)
    """
    
    def __init__(self, db_config: Dict[str, str] = None):
        self.CN_TIMEZONE = pytz.timezone('Asia/Shanghai')
        config = db_config or DEFAULT_DB_CONFIG
        self.pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            **config
        )
        
        # 设置时区
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SET timezone='Asia/Shanghai'")
            conn.commit()
        self.pool.putconn(conn)
    
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """执行SQL查询"""
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
    
    @query_method("""
        SELECT *
        FROM signal_summary
        WHERE detected_time > (NOW() AT TIME ZONE 'Asia/Shanghai' - INTERVAL '{hours} hours')
        ORDER BY detected_time DESC
    """)
    def get_recent_signals(self, hours: int = 24) -> QueryResult:
        """获取最近的信号"""
        pass
    
    @query_method("""
        SELECT *
        FROM signal_summary
        WHERE address = '{token_address}'
        AND detected_time > (NOW() AT TIME ZONE 'Asia/Shanghai' - INTERVAL '{hours} hours')
    """)
    def get_token_signals(self, token_address: str, hours: int = 24) -> QueryResult:
        """获取特定代币的信号"""
        pass
    
    @query_method("""
        SELECT *
        FROM digestchain
        WHERE address = '{address}'
    """)
    def get_token_info(self, address: str) -> QueryResult:
        """获取代币信息"""
        pass

    def close(self):
        """关闭数据库连接池"""
        if self.pool:
            self.pool.closeall()

    def execute_update(self, sql: str, params: tuple) -> List[Dict[str, Any]]:
        """执行更新操作并返回结果"""
        if not self.pool:
            raise ConnectionError("Database not connected")
        
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                if cursor.description:  # 如果有返回结果
                    columns = [desc[0] for desc in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    results = []
            conn.commit()
            return results
        finally:
            self.pool.putconn(conn)

    def update_technical_notes(self, id: int, notes: str) -> Optional[Dict[str, Any]]:
        """更新指定ID的technical_notes
        
        Args:
            id (int): 记录ID
            notes (str): 技术分析内容
            
        Returns:
            Optional[Dict[str, Any]]: 更新后的记录，如果更新失败返回None
            
        Example:
            >>> db = EasyQuery()
            >>> result = db.update_technical_notes(4696, "技术分析内容")
            >>> if result:
            ...     print(f"Updated record {result['id']}")
        """
        sql = """
            UPDATE public.signal_summary 
            SET technical_notes = %s
            WHERE id = %s
            RETURNING id, technical_notes;
        """
        results = self.execute_update(sql, (notes, id))
        return results[0] if results else None
    def update_technical_status(self, id: int, status: str) -> Optional[Dict[str, Any]]:
        """更新指定ID的technical_notes
        
        Args:
            id (int): 记录ID
            notes (str): 技术分析内容
            
        Returns:
            Optional[Dict[str, Any]]: 更新后的记录，如果更新失败返回None
            
        Example:
            >>> db = EasyQuery()
            >>> result = db.update_technical_status(4696, "技术分析内容")
            >>> if result:
            ...     print(f"Updated record {result['id']}")
        """
        sql = """
            UPDATE public.signal_summary 
            SET technical_status = %s
            WHERE id = %s
            RETURNING id, technical_status;
        """
        results = self.execute_update(sql, (status, id))
        return results[0] if results else None
    def update_price(self, id: int, price: str) -> Optional[Dict[str, Any]]:
        """更新指定ID的price
        
        Args:
            id (int): 记录ID
            price (str): 价格字符串，支持高精度数值
                
        Returns:
            Optional[Dict[str, Any]]: 更新后的记录，如果更新失败返回None
            
        Example:
            >>> db = EasyQuery()
            >>> result = db.update_price(4696, "123.45678901234567890")
            >>> if result:
            ...     print(f"Updated price for record {result['id']}")
        """
        sql = """
            UPDATE public.signal_summary 
            SET price = %s::numeric
            WHERE id = %s
            RETURNING id, price;
        """
        results = self.execute_update(sql, (price, id))
        return results[0] if results else None
    def update_pair(self, id: int, pair: str) -> Optional[Dict[str, Any]]:
        """更新指定ID的pair
        
        Args:
            id (int): 记录ID
            pair (str): 交易对名称，将以text类型存储
                
        Returns:
            Optional[Dict[str, Any]]: 更新后的记录，如果更新失败返回None
            
        Example:
            >>> db = EasyQuery()
            >>> result = db.update_pair(4696, "WETH/USDT")
            >>> if result:
            ...     print(f"Updated pair for record {result['id']}")
        """
        sql = """
            UPDATE public.signal_summary 
            SET pair = %s::text
            WHERE id = %s
            RETURNING id, pair;
        """
        results = self.execute_update(sql, (pair, id))
        return results[0] if results else None
    def update_field(self, id: int, field: str, value: Any, field_type: str = None) -> Optional[Dict[str, Any]]:
        """通用字段更新方法
        
        Args:
            id (int): 记录ID
            field (str): 要更新的字段名
            value (Any): 新的字段值
            field_type (str, optional): 字段类型（如 'text', 'numeric'），如果不指定则不进行类型转换
                
        Returns:
            Optional[Dict[str, Any]]: 更新后的记录，如果更新失败返回None
            
        Example:
            >>> db = EasyQuery()
            >>> # 更新 pair 字段
            >>> db.update_field(4696, "pair", "WETH/USDT", "text")
            >>> # 更新 price 字段
            >>> db.update_field(4696, "price", "123.456", "numeric")
            >>> # 更新 technical_notes 字段
            >>> db.update_field(4696, "technical_notes", "分析内容")
        """
        type_cast = f"::{field_type}" if field_type else ""
        sql = f"""
            UPDATE public.signal_summary 
            SET {field} = %s{type_cast}
            WHERE id = %s
            RETURNING id, {field};
        """
        results = self.execute_update(sql, (value, id))
        return results[0] if results else None

    def insert_pair_if_not_exists(self, pair: str, **optional_fields) -> Optional[Dict[str, Any]]:
        """检查并插入pair信息，如果24小时内不存在该pair则插入新记录
        
        Args:
            pair (str): 交易对名称（必需）
            **optional_fields: 可选字段，如：
                - address: str
                - price: str
                - technical_notes: str
                - technical_status: str
                - 其他signal_summary表支持的字段
            
        Returns:
            Optional[Dict[str, Any]]: 插入的记录，如果pair已存在返回None
        """
        # 构建字段列表和值列表
        fields = ['pair', 'detected_time']
        placeholders = ['%s', "NOW() AT TIME ZONE 'Asia/Shanghai'"]
        params = [pair]
        
        # 添加可选字段
        for field, value in optional_fields.items():
            fields.append(field)
            placeholders.append('%s')
            params.append(value)
            
        # 构建SQL语句
        fields_str = ', '.join(fields)
        values_str = ', '.join(placeholders)
        
        sql = f"""
            WITH new_record AS (
                INSERT INTO public.signal_summary ({fields_str})
                SELECT {values_str}
                WHERE NOT EXISTS (
                    SELECT 1 FROM signal_summary 
                    WHERE pair = %s 
                    AND detected_time > (NOW() AT TIME ZONE 'Asia/Shanghai' - INTERVAL '24 hours')
                )
                RETURNING id, {fields_str}
            )
            SELECT * FROM new_record;
        """
        
        # 添加WHERE条件的参数
        params.append(pair)
        
        results = self.execute_update(sql, tuple(params))
        return results[0] if results else None

# 使用示例
if __name__ == "__main__":
    db = EasyQuery()
    
    try:
        # 获取最近24小时的信号
        recent_signals = db.get_recent_signals(hours=24)
        print(f"Found {recent_signals.count()} recent signals")
        
        # 使用实际的token地址进行测试
        test_address = "0x2170Ed0880ac9A755fd29B2688956BD959F933F8"  # 例如 ETH 的地址
        
        # 获取特定代币的信号
        token_signals = db.get_token_signals(test_address, hours=48)
        if token_signals.first():
            print("Token has recent signals")
        
        # 获取代币信息
        token_info = db.get_token_info(test_address)
        if token_info.first():
            print("Token exists in digestchain")
            
            
            
        # 测试更新 technical_notes
        test_id = 5883
        test_notes = "技术分析内容2"
        update_result = db.update_technical_notes(test_id, test_notes)
        if update_result:
            print(f"Successfully updated technical notes for ID {update_result['id']}")
            print(f"New notes: {update_result['technical_notes']}")
        else:
            print(f"No record found with ID {test_id}")
        # 测试更新 technical_status
        test_id = 5883
        test_status = "流动性分析"
        update_result = db.update_technical_status(test_id, test_status)
        if update_result:
            print(f"Successfully updated technical status for ID {update_result['id']}")
            print(f"New status: {update_result['technical_status']}")
        else:
            print(f"No record found with ID {test_id}")
        
        # 测试更新 price
        test_id = 5883
        test_price = "123.45678901234567890"
        update_result = db.update_price(test_id, test_price)
        if update_result:
            print(f"Successfully updated price for ID {update_result['id']}")
            print(f"New price: {update_result['price']}")
            
        # 测试插入pair信息
        test_pair = "0x081d5e9116b9052b490a7170a18d87e4b8a84279"
        insert_result = db.insert_pair_if_not_exists(
            test_pair,
            price="0.00234",
            source="uniswap_v2",
            plan="ETH"
        )
        if insert_result:
            print(f"Successfully inserted pair {test_pair}")
            print(f"Price: {insert_result['price']}, Source: {insert_result['source']}")
        else:
            print(f"Pair {test_pair} already exists")
    finally:
        db.close() 