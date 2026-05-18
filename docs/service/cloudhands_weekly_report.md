# CloudhandsWeeklyReport 服务

## 概述

云核周报生成服务，负责爬取外汇市场数据、生成周报内容并输出报告文件。

## 模块文件

`backend/service/cloudhands_weekly_report.py`

## 类结构

### CloudhandsWeeklyReport

**构造函数**:

```python
def __init__(self, week_start):
    """
    Args:
        week_start: 周报起始日期，格式 'YYYY-MM-DD'
    """
```

**初始化内容**:
- 周报输出目录
- 爬取文件目录
- 元数据目录
- 各数据源URL配置
- 代理配置

## 核心方法

### 数据爬取方法

| 方法名 | 功能描述 |
|-------|---------|
| `crawl_fundamental_event_summary()` | 爬取基本面事件摘要数据 |
| `crawl_forex_trend_summary()` | 爬取外汇行情趋势数据 |
| `crawl_forex_position_data()` | 爬取CFTC持仓数据 |
| `crawl_major_currency_forecast()` | 爬取主要货币预测分析 |
| `crawl_option_strategy()` | 爬取期权策略数据 |
| `crawl_forex_future_data_event()` | 爬取财经数据和事件 |

### 数据生成方法

| 方法名 | 功能描述 |
|-------|---------|
| `generate_fundamental_event_data()` | 生成基本面事件数据 |
| `generate_forex_trend_summary()` | 生成外汇趋势摘要（含图片） |
| `generate_forex_position_data()` | 生成持仓数据（含图片） |
| `generate_major_currency_forecast()` | 生成货币预测数据 |
| `generate_forex_future_data_event(data_type)` | 生成财经数据/事件（含图片） |

#### generate_forex_position_data()

**功能**：生成外汇头寸持仓数据（CFTC持仓报告）

**操作步骤**：
1. 检查爬取的CFTC持仓数据文件是否存在
2. 读取CSV文件并按指定货币顺序合并数据
3. 调用 `get_picture_from_forex_position()` 生成简体图表图片
4. 调用 `add_image_border()` 为图片添加边框
5. 将DataFrame转换为繁体中文
6. 生成繁体图表图片
7. 调用 `get_text_from_forex_position()` 生成数据摘要文本
8. 返回包含数据列表、文件路径、图片名称和摘要文本的字典

**输入**：无（使用类属性中的文件路径）

**输出**：
```python
{
    'data_lst': [],        # 持仓数据列表
    'data_path': '',       # 原始数据文件路径
    'picture_name': '',    # 生成的图表图片文件名
    'text': ''             # 持仓数据摘要文本
}
```

**调用的辅助方法**：
- `get_picture_from_forex_position()` - 生成持仓图表
- `add_image_border()` - 添加图片边框
- `df_to_traditional()` - 简繁转换
- `get_text_from_forex_position()` - 生成摘要文本

---

#### generate_major_currency_forecast()

**功能**：生成重点货币对展望数据

**操作步骤**：
1. 检查爬取的货币预测分析文件是否存在
2. 读取JSON文件内容
3. 返回包含分析字典的结果

**输入**：无（使用类属性中的文件路径）

**输出**：
```python
{
    'analysis_dict': {}    # 各货币对的分析预测数据
}
```

---

#### generate_forex_trend_summary()

**功能**：生成外汇期货合约趋势数据（含图表图片）

**操作步骤**：
1. 读取爬取的外汇趋势数据CSV文件
2. 调用 `reformat_forex_trend_summary_data()` 处理数据格式
3. 调用 `render_forex_trend_table()` 生成简体表格图片
4. 调用 `add_image_border()` 为图片添加边框
5. 将DataFrame转换为繁体中文
6. 生成繁体表格图片
7. 返回包含图片名称的字典

**输入**：无（使用类属性中的文件路径）

**输出**：
```python
{
    'image_name': ''    # 生成的趋势图表图片文件名
}
```

**调用的辅助方法**：
- `reformat_forex_trend_summary_data()` - 重构趋势数据格式
- `render_forex_trend_table()` - 渲染趋势表格图片
- `add_image_border()` - 添加图片边框
- `df_to_traditional()` - 简繁转换

---

#### generate_forex_future_data_event(data_type)

**功能**：生成财经数据或事件日历数据（含表格图片）

**操作步骤**：
1. 读取Excel文件中的指定sheet（DATA或EVENT）
2. 根据data_type筛选和重命名列：
   - **DATA类型**：日期、时间、国家、数据区间、数据类型
   - **EVENT类型**：日期、时间、国家、人物、事件内容
3. 调用 `reformat_long_text()` 处理长文本字段
4. 调用 `render_future_data_event_table()` 生成简体表格图片
5. 调用 `add_image_border()` 为图片添加边框
6. 将DataFrame转换为繁体中文
7. 生成繁体表格图片
8. 返回包含数据列表和图片名称的字典

**输入参数**：
- `data_type` (str): 'DATA' 或 'EVENT'

**输出**：
```python
{
    'data_json_lst': [],   # 数据列表
    'image_name': ''       # 生成的表格图片文件名
}
```

**调用的辅助方法**：
- `reformat_long_text()` - 处理长文本换行
- `render_future_data_event_table()` - 渲染表格图片
- `add_image_border()` - 添加图片边框
- `df_to_traditional()` - 简繁转换

### 报告生成方法

| 方法名 | 功能描述 |
|-------|---------|
| `generate_output_files()` | 生成周报文件（Word/PDF，简繁体） |

### 辅助方法

| 方法名 | 功能描述 |
|-------|---------|
| `df_to_traditional(df)` | 将DataFrame转换为繁体中文 |
| `get_week_dates(week)` | 获取指定周的日期列表 |
| `render_forex_trend_table()` | 渲染外汇趋势表格图片 |
| `render_future_data_event_table()` | 渲染财经数据表格图片 |
| `add_image_border()` | 为图片添加边框 |
| `reformat_forex_trend_summary_data()` | 重构外汇行情数据 |
| `get_contract_symbol()` | 获取期货合约代码 |

## 数据来源

| 数据源 | 用途 |
|-------|------|
| FX678 | 外汇周评文章 |
| TradingView / apilayer | 外汇行情数据 |
| CFTC | 期货持仓报告 |
| FX168 | 货币分析报告 |
| 金十数据 | 财经日历数据 |

## 输出文件

| 文件类型 | 文件名格式 |
|---------|-----------|
| 简体Word | `（简体）CME版本 云核变量策略周报 {日期范围}.docx` |
| 繁体Word | `（繁体）CME版本 云核变量策略周报 {日期范围}.docx` |
| 简体PDF | `（简体）CME版本 云核变量策略周报 {日期范围}.pdf` |
| 繁体PDF | `（繁体）CME版本 云核变量策略周报 {日期范围}.pdf` |

## 依赖模块

- `os`, `datetime`, `pandas`, `numpy`, `json`, `time`
- `requests`, `BeautifulSoup` (数据爬取)
- `docxtpl`, `zhconv` (文档生成)
- `matplotlib`, `PIL` (图表生成)
- `selenium` (动态页面爬取)
- `..utils.osfile_utils`, `..utils.docx_utils`