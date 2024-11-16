# Quantduck 文档

欢迎使用 Quantduck 量化分析库！

![Version](https://img.shields.io/badge/version-{current_version}-blue)

## 项目简介

Quantduck 是一个专门为加密货币量化分析设计的 Python 库。它提供了一套完整的工具，用于：

- 数据库连接和管理
- 信号分析和处理
- 自动化交易支持

### 主要特性

- **高效的数据库操作**：使用连接池优化的 PostgreSQL 数据库访问
- **实时信号监控**：支持实时获取和分析交易信号
- **自动版本管理**：集成了自动版本控制系统
- **类型提示支持**：完整的类型注解，支持 IDE 智能提示

## 快速开始

### 安装

```bash
pip install git+https://github.com/msjmsj/quantduck.git
```

### 基础用法

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

## 使用指南

### 数据库操作

Quantduck 提供了简单直观的数据库接口：

```python
# 检查特定 token
token = "0xbcdf0ccb39f81c2e40ce696ecd6a5689dd4563b0"
exists = db.check_token_in_recent_signals(token, hours=24)
print(f"Token存在: {exists}")
```

### 信号分析

支持多种信号分析功能：
- 获取最近时间段内的信号
- 检查特定代币的信号情况
- 信号统计和分析

## 项目结构

```
quantduck/
├── core/
│   ├── database.py    # 数据库核心功能
│   └── config.py      # 配置管理
├── utils/             # 工具函数
└── __init__.py        # 版本信息
```

## 更多资源

- [API 文档](api.html)：详细的 API 参考
- [示例代码](examples.html)：常用功能示例
- [GitHub 仓库](https://github.com/msjmsj/quantduck)：源代码和问题反馈

## 贡献指南

我们欢迎社区贡献！如果您想参与项目开发：

1. Fork 项目仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 版本历史

### v0.1.x
- 优化数据库连接池实现
- 简化 API 使用方式
- 添加自动版本管理