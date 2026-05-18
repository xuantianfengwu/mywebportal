# Video API

## 概述

视频相关接口，提供视频文件获取和视频列表查询功能。

## 路由配置

- **URL前缀**: `/api/video`
- **模块文件**: `backend/api/video.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/get/<videoname>` | GET | 获取指定视频文件 |
| `/videolist/get` | GET | 获取视频列表 |

## 接口详细说明

### 1. GET /api/video/get/<videoname>

**功能**: 获取指定视频文件

**路径参数**:

| 参数 | 类型 | 说明 |
|-----|------|------|
| `videoname` | string | 视频文件名 |

**成功响应**: 返回视频文件流

**实现逻辑**:
- 从 `backend/static/videos/` 目录读取视频文件
- 返回文件流（附件形式）

### 2. GET /api/video/videolist/get

**功能**: 获取前后端视频列表

**请求参数**: 无

**成功响应**:

```json
{
    "frontend": {
        "videolist": ["F_视频1.mp4", "F_视频2.mp4", ...]
    },
    "backend": {
        "videolist": ["B_视频1.mp4", "B_视频2.mp4", ...]
    }
}
```

**实现逻辑**:
1. 检查并创建视频目录（如不存在）
2. 分别读取 `backend/static/videos/` 和 `frontend/src/static/videos/` 目录
3. 为前端视频添加 `F_` 前缀，后端视频添加 `B_` 前缀
4. 返回视频列表

## 依赖模块

- `flask.Blueprint`, `flask.send_from_directory`
- `os`