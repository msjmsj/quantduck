from quantduck.core.database import DatabaseFactory
from quantduck.core.filter import PriceFilter, VolumeFilter
from quantduck.core.technical import MovingAverage, RSI
from quantduck.core.common import DataProcessor, Logger

def main():
    # 初始化日志
    logger = Logger()
    logger.log("开始测试 quantduck 库")

    try:
        # 创建数据库连接
        db = DatabaseFactory.create_database("sqlite", db_path="example.db")
        if not db.connect():
            logger.log("数据库连接失败", "ERROR")
            return

        # 创建示例数据表和数据
        cursor = db.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                date TEXT,
                symbol TEXT,
                price REAL,
                volume INTEGER
            )
        """)
        
        # 插入示例数据
        sample_data = [
            ("2024-03-01", "AAPL", 150.0, 1000000),
            ("2024-03-02", "AAPL", 152.0, 1200000),
            ("2024-03-03", "AAPL", 151.0, 900000),
            ("2024-03-04", "AAPL", 153.0, 1500000),
            ("2024-03-05", "AAPL", 155.0, 1300000),
        ]
        cursor.executemany(
            "INSERT INTO stocks VALUES (?, ?, ?, ?)",
            sample_data
        )
        db.connection.commit()

        # 查询数据
        data = db.query("SELECT * FROM stocks")
        logger.log(f"获取到 {len(data)} 条数据")

        # 使用数据处理器
        processor = DataProcessor()
        first_day = data[0]["price"]
        last_day = data[-1]["price"]
        change = processor.calculate_percentage_change(first_day, last_day)
        logger.log(f"价格变化百分比: {change:.2f}%")

        # 使用过滤器
        price_filter = PriceFilter(min_price=152.0)
        volume_filter = VolumeFilter(min_volume=1200000)
        
        filtered_by_price = price_filter.filter(data)
        logger.log(f"价格过滤后的数据条数: {len(filtered_by_price)}")
        
        filtered_by_volume = volume_filter.filter(data)
        logger.log(f"成交量过滤后的数据条数: {len(filtered_by_volume)}")

        # 计算技术指标
        ma = MovingAverage(period=3)
        ma_result = ma.calculate(data)
        logger.log("移动平均线计算结果:")
        for i, value in enumerate(ma_result["MA"]):
            if value is not None:
                logger.log(f"日期: {data[i]['date']}, MA3: {value:.2f}")

        rsi = RSI(period=2)
        rsi_result = rsi.calculate(data)
        logger.log("RSI计算结果:")
        for i, value in enumerate(rsi_result["RSI"]):
            if value is not None:
                logger.log(f"日期: {data[i]['date']}, RSI: {value:.2f}")

    except Exception as e:
        logger.log(f"发生错误: {str(e)}", "ERROR")
    
    finally:
        # 清理数据库
        cursor.execute("DROP TABLE IF EXISTS stocks")
        db.connection.commit()
        db.disconnect()
        logger.log("测试完成")

if __name__ == "__main__":
    main() 