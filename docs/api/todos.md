# Todos API

## 概述

待办事项管理相关接口，提供任务列表查询功能。

## 路由配置

- **URL前缀**: `/api/todos`
- **模块文件**: `backend/api/todos.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/task` | GET | 获取所有任务列表 |

## 接口详细说明

### 1. GET /api/todos/task

**功能**: 获取所有待办任务列表

**请求参数**: 无

**成功响应**:

```json
{
    "code": 200,
    "message": "get task success!",
    "data": [
        {
            "id": "任务ID",
            "task_name": "任务名称",
            "task_desc": "任务描述",
            "task_owner": "任务所有者",
            "create_date": "创建日期",
            "last_modify_date": "最后修改日期",
            "is_complete": false
        }
    ]
}
```

**实现逻辑**:
- 调用 `TodosService.get_all_tasks()` 获取任务列表

## 依赖模块

- `flask.Blueprint`, `flask.request`
- `..service.todos_service.TodosService`