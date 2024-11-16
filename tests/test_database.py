import unittest
import pytz
from datetime import datetime
from quantduck.core.database import DatabaseFactory

class TestPostgreSQLDatabase(unittest.TestCase):
    def setUp(self):
        """测试前的设置"""
        self.db = DatabaseFactory.create_database()
        self.assertTrue(self.db.connect())

    def tearDown(self):
        """测试后的清理"""
        self.db.disconnect()

    def test_connection(self):
        """测试数据库连接"""
        # 连接已在setUp中测试
        self.assertIsNotNone(self.db.connection)

    def test_timezone(self):
        """测试时区设置"""
        result = self.db.query("SHOW timezone;")
        # PostgreSQL可能返回大写的列名，我们获取第一个列的值
        timezone_value = list(result[0].values())[0]
        self.assertEqual(timezone_value, 'Asia/Shanghai')

    def test_recent_signals(self):
        """测试获取最近信号"""
        # 获取最近24小时的信号
        signals = self.db.get_recent_signals(hours=24)
        
        # 验证返回的是列表
        self.assertIsInstance(signals, list)
        
        # 如果有数据，验证时间字段
        if signals:
            signal = signals[0]
            self.assertIn('detected_time', signal)
            detected_time = signal['detected_time']
            
            # 验证时间是否为datetime对象
            self.assertIsInstance(detected_time, datetime)
            
            # 验证时区是否为中国时区
            self.assertEqual(
                detected_time.tzinfo.zone,
                'Asia/Shanghai'
            )

if __name__ == '__main__':
    unittest.main() 