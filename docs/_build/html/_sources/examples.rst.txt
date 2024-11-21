Examples
========

Basic Usage
----------

.. code-block:: python

    from quantduck.core.database import get_db

    # 获取数据库实例
    db = get_db()

    # 检查特定token
    token = "0xbcdf0ccb39f81c2e40ce696ecd6a5689dd4563b0"
    exists = db.check_token_in_recent_signals(token, hours=24)
    print(f"Token存在: {exists}")

Advanced Usage
-------------

.. code-block:: python

    # 更多高级用法示例...