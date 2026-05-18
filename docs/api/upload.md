# Upload API

## 概述

文件上传相关接口，支持PDF工具和图片工具的文件上传。

## 路由配置

- **URL前缀**: `/api/upload`
- **模块文件**: `backend/api/upload.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/pdf/transformer` | POST | 上传PDF转换工具的文件 |
| `/picturetools/picture` | POST | 上传图片工具的文件 |

## 接口详细说明

### 1. POST /api/upload/pdf/transformer

**功能**: 上传PDF转换工具的文件

**请求体**:

| 字段 | 类型 | 说明 |
|-----|------|------|
| `file` | File | 要上传的PDF文件 |

**成功响应**: 空字符串（文件保存成功）

**实现逻辑**:
1. 获取上传的文件
2. 保存到 `backend/static/upload/pdf_tools/` 目录
3. 返回空响应

### 2. POST /api/upload/picturetools/picture

**功能**: 上传图片工具的文件

**请求体**:

| 字段 | 类型 | 说明 |
|-----|------|------|
| `file` | File | 要上传的图片文件 |

**请求头**:

| 字段 | 说明 |
|-----|------|
| `FROM` | 来源标识，用于构造文件名 |

**成功响应**:

```json
{
    "code": 200,
    "message": "文件上传成功！",
    "data": null
}
```

**实现逻辑**:
1. 获取上传的文件和请求头中的 `FROM` 字段
2. 构造文件名: `{FROM}_{原始文件名}`
3. 保存到 `backend/static/upload/picture_tools/` 目录

## 依赖模块

- `flask.Blueprint`, `flask.request`
- `os`
- `backend.utils.web_response.WebResponse`
- `backend.utils.osfile_utils.OSFileUtils`