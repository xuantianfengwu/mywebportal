# ForexTradingTools 服务

## 概述

外汇交易工具服务，负责外汇数据的导入、管理和查询。

## 模块文件

`backend/service/forex_trading_tools.py`

## 类结构

### ForexTradingTools

**构造函数**:

```python
def __init__(self):
    """初始化SQLite连接和货币对列表"""
```

**属性**:
| 属性 | 类型 | 说明 |
|-----|------|------|
| `sqlite_name` | string | 数据库名称，默认 'forextrading' |
| `sqlite_db` | SqliteUtils | SQLite工具实例 |
| `symbol_list` | list | 支持的货币对列表 |

## 核心方法

### 数据库操作

| 方法名 | 功能描述 |
|-------|---------|
| `initialize_sqlite_db(replace=False)` | 初始化SQLite数据库表 |
| `import_forex_tester_data(file_path, to_table, row_freq=100000, overwrite=False)` | 导入Forex Tester数据文件 |
| `update_forex_data(data)` | 更新外汇数据 |

### 文件操作

| 方法名 | 功能描述 |
|-------|---------|
| `save_upload_file(f)` | 保存上传的数据文件 |
| `get_symbol_list()` | 获取支持的货币对列表 |

## 支持的货币对

| 货币对 | 说明 |
|-------|------|
| EURUSD | 欧元/美元 |
| GBPUSD | 英镑/美元 |
| AUDUSD | 澳元/美元 |
| USDJPY | 美元/日元 |
| USDCAD | 美元/加元 |
| USDCHF | 美元/瑞郎 |

## 数据格式

### Forex Tester 文件格式

| 字段 | 说明 |
|-----|------|
| TICKER | 货币对代码 |
| DTYYYYMMDD | 日期 |
| TIME | 时间 |
| OPEN | 开盘价 |
| HIGH | 最高价 |
| LOW | 最低价 |
| CLOSE | 收盘价 |
| VOL | 成交量 |

## 依赖模块

- `os`, `numpy`, `pandas`, `time`
- `..utils.sqlite_utils.SqliteUtils`
- `..utils.osfile_utils.OSFileUtils`