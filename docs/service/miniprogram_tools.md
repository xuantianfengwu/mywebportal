# MiniProgramTools 服务

## 概述

小程序数据服务，提供量化报告系列数据查询功能。

## 模块文件

`backend/service/miniprogram_tools.py`

## 类结构

### MiniProgramTools

**构造函数**:

```python
def __init__(self):
    """初始化量化报告数据库连接"""
```

**属性**:
| 属性 | 类型 | 说明 |
|-----|------|------|
| `quant_db` | SqliteUtils | 量化报告数据库实例 |

## 核心方法

### 数据查询方法

| 方法名 | 功能描述 |
|-------|---------|
| `get_quant_series_list()` | 获取量化系列列表 |
| `get_quant_series_info(s_code, series_code)` | 获取指定系列信息 |
| `get_quant_series_reports(s_code, series_code)` | 获取指定系列的报告列表 |

### 数据生成方法

| 方法名 | 功能描述 |
|-------|---------|
| `generate_q_series_list()` | 生成系列列表数据（格式化输出） |
| `generate_q_series_reports(s_code, series_code)` | 生成系列报告数据（格式化输出） |

## 数据库表结构

### series_list 表

| 字段 | 说明 |
|-----|------|
| s_code | 券商代码 |
| series_code | 系列代码 |
| ... | 其他字段 |

### report_list 表

| 字段 | 说明 |
|-----|------|
| s_code | 券商代码 |
| series_code | 系列代码 |
| ... | 其他字段 |

## 依赖模块

- `os`, `pandas`
- `..utils.osfile_utils.OSFileUtils`
- `..utils.sqlite_utils.SqliteUtils`