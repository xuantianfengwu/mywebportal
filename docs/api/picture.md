# Picture API

## 概述

图片处理工具相关接口，主要提供图片文字识别（OCR）功能。

## 路由配置

- **URL前缀**: `/api/picture`
- **模块文件**: `backend/api/picture.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/letterrec` | POST | 图片文字识别 |

## 接口详细说明

### 1. POST /api/picture/letterrec

**功能**: 图片文字识别（OCR）

**请求体参数**:

| 字段 | 类型 | 说明 |
|-----|------|------|
| `model_type` | string | 识别模型类型（如 'baidu'） |
| `file_name` | string | 上传的图片文件名 |

**成功响应**:

```json
{
    "code": 200,
    "message": "图片文字识别成功！",
    "data": {
        "rec_text": "识别出的文字内容"
    }
}
```

**实现逻辑**:
1. 解析 `model_type` 和 `file_name` 参数
2. 构建图片文件路径：`backend/static/upload/picture_tools/{file_name}`
3. 调用 `PictureTools.picture_letter_rec()` 进行OCR识别
4. 返回识别结果

## 依赖模块

- `flask.Blueprint`, `flask.request`
- `os`
- `backend.service.picture_tools.PictureTools`
- `backend.utils.web_response.WebResponse`