# PictureTools 服务

## 概述

图片处理服务，提供图片文字识别（OCR）功能。

## 模块文件

`backend/service/picture_tools.py`

## 类结构

### PictureTools

**构造函数**:

```python
def __init__(self):
    """初始化图片处理工具"""
```

## 核心方法

### 静态方法

| 方法名 | 功能描述 |
|-------|---------|
| `picture_letter_rec(file_path, model_type)` | 图片文字识别 |
| `get_baidu_access_token()` | 获取百度OCR访问令牌 |

## OCR识别流程

1. 读取图片文件并Base64编码
2. 根据model_type选择识别模型
3. 调用百度OCR API进行识别
4. 解析返回结果，提取文字内容

## 支持的模型类型

| 模型类型 | 说明 |
|---------|------|
| `baidu` | 百度OCR精准识别 |

## 配置文件

OCR服务需要配置第三方工具信息：

```ini
[baidu_ORC]
BAIDU_APP_KEY = your_app_key
BAIDU_SECRET_KEY = your_secret_key
```

配置文件路径: `backend/config/3rd_party_tool.ini`

## 依赖模块

- `base64`, `requests`, `os`, `configparser`