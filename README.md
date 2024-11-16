# Quantduck

量化分析库，提供数据库连接和信号分析功能。

## 文档

完整文档请访问：[Quantduck Documentation](https://msjmsj.github.io/quantduck/)

## 基本使用

```python
from quantduck.core.database import get_db

# 获取数据库实例
db = get_db()

# 检查特定token
token = "0xbcdf0ccb39f81c2e40ce696ecd6a5689dd4563b0"
exists = db.check_token_in_recent_signals(token, hours=24)
print(f"Token存在: {exists}")

# 获取最近信号
signals = db.get_recent_signals(hours=12)
print(f"最近12小时共有 {len(signals)} 个信号")
```

## 版本管理

### 版本号格式

版本号采用 `major.minor.patch` 格式：

- major: 重大更新，不兼容的API修改
- minor: 功能更新，向后兼容的功能添加
- patch: 补丁更新，向后兼容的问题修复

### 自动版本更新

项目使用自动版本管理系统：

1. 每次 git commit 时会自动增加 patch 版本号
2. 版本号会同步更新到以下文件：
   - quantduck/__init__.py
   - setup.py
   - pyproject.toml

### 查看当前版本

可以通过以下方式查看当前版本：

```python
from quantduck import __version__
print(__version__)
```
