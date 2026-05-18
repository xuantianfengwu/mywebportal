# PDFTransformer 服务

## 概述

PDF转换处理服务，支持PDF页面删除、文件预览和下载。

## 模块文件

`backend/service/pdf_transformer.py`

## 类结构

### PDFTransformer

**构造函数**:

```python
def __init__(self, pdf_files):
    """
    Args:
        pdf_files: PDF文件名或文件名列表
    """
```

**属性**:
| 属性 | 类型 | 说明 |
|-----|------|------|
| `pdf_read_dir` | string | PDF读取目录 |
| `output_dir` | string | 输出目录 |
| `pdf_files` | list | PDF文件名列表 |

## 核心方法

### 操作方法

| 方法名 | 功能描述 |
|-------|---------|
| `operate(operate_type, params)` | 执行PDF操作入口 |
| `del_specific_pages(pdf_files, del_page_lst, output_dir)` | 删除指定页面 |

### 文件处理方法

| 方法名 | 功能描述 |
|-------|---------|
| `_read_in_pdf(pdf_file)` | 读取PDF文件 |
| `get_result_file_path(oper_type)` | 获取单个结果文件路径 |
| `get_result_files_path(oper_type, download_type='zip')` | 获取多个结果文件路径 |

## 支持的操作类型

| 操作类型 | 说明 |
|---------|------|
| `1` | 删除指定页面 |

## 依赖模块

- `os`, `zipfile`
- `PyPDF2.PdfFileReader`, `PyPDF2.PdfFileWriter`
- `..utils.osfile_utils.OSFileUtils`