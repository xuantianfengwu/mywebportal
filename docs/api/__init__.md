# API 模块初始化

## 概述

API模块的初始化入口，负责注册所有Blueprint路由。

## 模块文件

`backend/api/__init__.py`

## 注册的Blueprint

| Blueprint名称 | 模块来源 | URL前缀 | 功能描述 |
|--------------|---------|---------|---------|
| `user_bp` | `user.py` | `/api/user` | 用户信息管理 |
| `upload_bp` | `upload.py` | `/api/upload` | 文件上传 |
| `pdf_bp` | `pdf.py` | `/api/pdf` | PDF处理 |
| `login_bp` | `login.py` | `/api/login` | 用户登录 |
| `video_bp` | `video.py` | `/api/video` | 视频管理 |
| `todos_bp` | `todos.py` | `/api/todos` | 待办事项 |
| `picture_bp` | `picture.py` | `/api/picture` | 图片处理 |
| `trading_bp` | `trading.py` | `/api/trading` | 交易数据 |
| `minip_bp` | `miniprogram.py` | `/api/minip` | 小程序接口 |

## 核心函数

### bind_blueprint(app)

**功能**: 绑定所有Blueprint到Flask应用

**参数**:

| 参数 | 类型 | 说明 |
|-----|------|------|
| `app` | Flask | Flask应用实例 |

**实现逻辑**:
1. 导入所有Blueprint
2. 依次注册到应用，设置对应的URL前缀

## 使用方式

```python
from backend.api import bind_blueprint

app = Flask(__name__)
bind_blueprint(app)
```