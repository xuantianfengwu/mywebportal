# TextTools 服务

## 概述

文本处理服务，支持从文本自动生成视频。

## 模块文件

`backend/service/text_tools.py`

## 类结构

### TextTools

**构造函数**:

```python
def __init__(self):
    """初始化爬取和输出目录"""
```

**属性**:
| 属性 | 类型 | 说明 |
|-----|------|------|
| `crawl_dir` | string | 爬取文件目录 |
| `output_dir` | string | 输出文件目录 |

## 核心方法

### 视频生成

| 方法名 | 功能描述 |
|-------|---------|
| `generate_video_from_text(text, video_name)` | 从文本生成视频 |

## 视频生成流程

1. **文本分句**: 将输入文本分割成句子
2. **提取关键词**: 提取每个句子的中心词
3. **翻译关键词**: 将中文关键词翻译成英文
4. **下载图片**: 根据关键词下载相关图片
5. **生成音频**: 将每个句子转换为语音
6. **图片转视频**: 将图片序列转换为视频
7. **合并音视频**: 将音频和视频合并
8. **添加字幕**: 为视频添加字幕

## 视频生成参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| `text` | string | 输入文本内容 |
| `video_name` | string | 输出视频文件名 |

## 输出文件结构

```
backend/static/crawl/text_tools/
├── 0_keyword.jpg      # 图片文件
├── 1_keyword.jpg
├── ...
├── 0_keyword.mp3      # 音频文件
├── 1_keyword.mp3
├── ...
├── video.avi          # 中间视频文件
└── video.wav          # 合并音频文件

backend/static/output/text_tools/
├── video_name.mp4          # 原始视频
└── (subtitled)video_name.mp4  # 带字幕视频
```

## 依赖模块

- `os`, `configparser`, `requests`, `numpy`
- `..utils.text_utils.TextUtils`
- `..utils.audio_utils.AudioUtils`
- `..utils.video_utils.VideoUtils`
- `..utils.osfile_utils.OSFileUtils`