# Login API

## 概述

用户认证登录相关接口，处理用户登录请求。

## 路由配置

- **URL前缀**: `/api/login`
- **模块文件**: `backend/api/login.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/test` | GET | 测试接口（会触发除零异常） |
| `/login` | POST | 用户登录认证 |

## 接口详细说明

### 1. POST /api/login/login

**功能**: 用户登录认证

**请求体 JSON**:

| 字段 | 类型 | 说明 |
|-----|------|------|
| `userid` | string | 用户ID |
| `password` | string | 用户密码 |

**成功响应**:

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "username": "用户名"
    }
}
```

**失败响应**:

```json
{
    "code": 401,
    "message": "登录失败",
    "data": null
}
```

**实现逻辑**:
1. 解析请求体中的 `userid` 和 `password`
2. 调用 `Auth.Login()` 进行登录验证
3. 若登录成功，将用户名存入 session
4. 返回登录结果

## 依赖模块

- `flask.Blueprint`, `flask.session`, `flask.request`
- `json`
- `..utils.Auth` - 认证工具模块