# PDF API

## 概述

PDF处理工具相关接口，支持PDF页面删除、预览和下载。

## 路由配置

- **URL前缀**: `/api/pdf`
- **模块文件**: `backend/api/pdf.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/transformer/delpage` | POST | 删除PDF指定页面 |
| `/transformer/res/preview` | GET | 预览处理后的PDF文件 |
| `/transformer/res/download` | POST | 下载处理后的PDF文件 |

## 接口详细说明

### 1. POST /api/pdf/transformer/delpage

**功能**: 删除PDF指定页面

**请求体参数**:

| 字段 | 类型 | 说明 |
|-----|------|------|
| `operate_type` | string | 操作类型（如 '1' 表示删除页面） |
| `operate_params` | dict | 操作参数，包含 `to_del_pages` |
| `upload_files` | list | 上传的PDF文件名列表 |

**成功响应**:

```json
{
    "code": 200,
    "message": "文件处理成功！",
    "data": {
        "operate_res": {...}
    }
}
```

### 2. GET /api/pdf/transformer/res/preview

**功能**: 预览处理后的PDF文件

**请求参数**:

| 参数 | 类型 | 说明 |
|-----|------|------|
| `oper_type` | string | 操作类型 |
| `prev_file` | string | 预览文件名 |

**成功响应**: 返回PDF文件流

### 3. POST /api/pdf/transformer/res/download

**功能**: 下载处理后的PDF文件

**请求体参数**:

| 字段 | 类型 | 说明 |
|-----|------|------|
| `oper_type` | string | 操作类型 |
| `download_type` | string | 下载类型（如 'zip'） |
| `download_files` | list | 要下载的文件名列表 |

**成功响应**: 返回文件流（PDF或ZIP压缩包）

## 依赖模块

- `flask.Blueprint`, `flask.request`, `flask.send_from_directory`
- `..service.pdf_transformer.PDFTransformer`
- `..utils.web_response.WebResponse`