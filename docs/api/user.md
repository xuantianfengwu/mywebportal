# User API

## 概述

用户信息相关接口，提供用户信息查询功能。

## 路由配置

- **URL前缀**: `/api/user`
- **模块文件**: `backend/api/user.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/test` | GET | 测试接口 |
| `/userinfo/get` | GET | 获取当前用户信息 |

## 接口详细说明

### 1. GET /api/user/test

**功能**: 测试接口

**成功响应**: `test api`

### 2. GET /api/user/userinfo/get

**功能**: 获取当前登录用户信息

**请求参数**: 无（从session获取）

**成功响应**:

```json
{
    "username": "当前用户名"
}
```

**实现逻辑**:
- 从 session 中获取 `username`
- 若未登录，返回 `Not Login!`

## 依赖模块

- `flask.Blueprint`, `flask.session`