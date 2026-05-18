# TodosService 服务

## 概述

待办事项服务，提供任务数据的查询功能。

## 模块文件

`backend/service/todos_service.py`

## 类结构

### TodosService

**构造函数**:

```python
def __init__(self):
    """初始化SQLite连接和任务列表"""
```

**属性**:
| 属性 | 类型 | 说明 |
|-----|------|------|
| `sqlite_name` | string | 数据库名称，默认 'todos' |
| `sqlite_db` | SqliteConnection | SQLite连接实例 |
| `task_lst` | list | 任务列表 |

## 核心方法

| 方法名 | 功能描述 |
|-------|---------|
| `_generate_task_lst()` | 生成任务列表（内部方法） |
| `get_all_tasks()` | 获取所有任务 |

## 任务数据结构

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | string | 任务ID |
| task_name | string | 任务名称 |
| task_desc | string | 任务描述 |
| task_owner | string | 任务所有者 |
| create_date | string | 创建日期 |
| last_modify_date | string | 最后修改日期 |
| is_complete | bool | 是否完成 |

## 数据库表结构

### task 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | TEXT | 任务ID |
| task_name | TEXT | 任务名称 |
| task_desc | TEXT | 任务描述 |
| task_owner | TEXT | 任务所有者 |
| create_date | TEXT | 创建日期 |
| last_modify_date | TEXT | 最后修改日期 |
| is_complete | INTEGER | 是否完成（0/1） |

## 依赖模块

- `os`
- `..utils.sqlite_utils`