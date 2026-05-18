# Miniprogram API

## 概述

小程序相关接口，提供量化报告数据查询服务。

## 路由配置

- **URL前缀**: `/api/minip`
- **模块文件**: `backend/api/miniprogram.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/get/q_series_list` | GET | 获取量化系列列表 |
| `/get/q_series_reports` | GET | 获取指定系列的报告列表 |

## 接口详细说明

### 1. GET /api/minip/get/q_series_list

**功能**: 获取量化系列列表

**请求参数**: 无

**成功响应**:

```json
{
    "code": 200,
    "message": "获取数据成功！",
    "data": {
        "q_series_list": [...]
    }
}
```

**实现逻辑**:
- 调用 `MiniProgramTools.generate_q_series_list()` 获取系列列表数据

### 2. GET /api/minip/get/q_series_reports

**功能**: 获取指定券商和系列的报告列表

**请求参数**:

| 参数 | 类型 | 说明 |
|-----|------|------|
| `s_code` | string | 券商代码 |
| `series_code` | string | 系列代码 |

**成功响应**:

```json
{
    "code": 200,
    "message": "获取数据成功！",
    "data": {
        "q_series_info": {...},
        "q_series_reports": [...]
    }
}
```

**实现逻辑**:
1. 解析 `s_code` 和 `series_code` 参数
2. 调用 `MiniProgramTools.generate_q_series_reports()` 获取系列信息和报告列表

## 依赖模块

- `flask.Blueprint`, `flask.request`
- `..service.miniprogram_tools.MiniProgramTools`
- `..utils.web_response.WebResponse`