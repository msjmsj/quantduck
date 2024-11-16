# Quantduck 文档

欢迎使用 Quantduck 量化分析库！

![Version](https://img.shields.io/badge/version-{current_version}-blue)

## 快速开始

```python
from quantduck.core.database import get_db
from quantduck import __version__

print(f"当前版本: {__version__}")

# 获取数据库实例
db = get_db()

# 获取最近信号
signals = db.get_recent_signals(hours=12)
print(f"最近12小时共有 {len(signals)} 个信号")
```

## 功能特点

- 数据库连接和管理
- 信号分析功能
- 自动版本管理

更多详细信息请查看 [API 文档](api.html) 和 [示例](examples.html)。 