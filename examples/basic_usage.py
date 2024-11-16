from quantduck.core.database import get_db

def basic_example():
    """基本使用示例"""
    # 获取数据库实例
    db = get_db()
    
    # 示例1: 检查特定token
    token_address = "0xbcdf0ccb39f81c2e40ce696ecd6a5689dd4563b0"
    exists = db.check_token_in_recent_signals(token_address, hours=24)
    print(f"Token {token_address} 在最近24小时内{'存在' if exists else '不存在'}")
    
    # 示例2: 获取最近信号
    signals = db.get_recent_signals(hours=12)  # 获取最近12小时的信号
    print(f"\n最近12小时共有 {len(signals)} 个信号")
    
    # 打印最新的3个信号
    print("\n最新的3个信号:")
    for signal in signals[:3]:
        print(f"\n时间: {signal['detected_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Token地址: {signal['token_address']}")
        # 打印其他可用字段
        for key, value in signal.items():
            if key not in ['detected_time', 'token_address']:
                print(f"{key}: {value}")

if __name__ == "__main__":
    basic_example() 