# Trading API

## 概述

交易相关接口，包含外汇数据管理和云核周报生成功能。

## 路由配置

- **URL前缀**: `/api/trading`
- **模块文件**: `backend/api/trading.py`

## 接口列表

| 接口路径 | HTTP方法 | 功能描述 |
|---------|---------|---------|
| `/forex/data/save` | GET/POST | 保存外汇行情数据 |
| `/forex/file/upload` | POST | 上传Forex Tester文件 |
| `/forex/db/initialize` | GET | 初始化外汇数据库表 |
| `/cloudhands/crawl` | GET | 爬取云核周报数据 |
| `/cloudhands/forex/fund_event` | GET | 获取基本面事件数据 |
| `/cloudhands/forex/trend_summary` | GET | 获取外汇趋势摘要 |
| `/cloudhands/forex/position_data` | GET | 获取持仓数据 |
| `/cloudhands/forex/major_currency_forecast` | GET | 获取主要货币预测 |
| `/cloudhands/forex/future_data_event` | GET | 获取未来数据事件 |
| `/cloudhands/forex/output_report` | POST | 生成周报文件 |
| `/cloudhands/file` | GET | 获取周报文件 |

## 接口详细说明

### 1. POST /api/trading/forex/file/upload

**功能**: 上传Forex Tester数据文件并导入数据库

**请求体参数**:

| 字段 | 类型 | 说明 |
|-----|------|------|
| `file_type` | string | 文件类型（如 'forex_tester'） |
| `file` | File | 上传的文件 |

**成功响应**:

```json
{
    "code": 200,
    "message": "文件导入成功！",
    "data": null
}
```

### 2. GET /api/trading/cloudhands/crawl

**功能**: 爬取云核周报相关数据

**请求参数**:

| 参数 | 类型 | 说明 |
|-----|------|------|
| `data_type` | string | 数据类型 |
| `week_start` | string | 周报起始日期（YYYY-MM-DD） |

**data_type可选值**:
- `fundamental_event_summary` - 基本面事件摘要
- `forex_trend_summary` - 外汇趋势摘要
- `forex_position_data` - 外汇持仓数据
- `major_currency_forecast` - 主要货币预测
- `option_strategy` - 期权策略
- `forex_future_data_event` - 未来数据事件

**成功响应**:

```json
{
    "code": 200,
    "message": "数据爬取成功！",
    "data": null
}
```

### 3. POST /api/trading/cloudhands/forex/output_report

**功能**: 生成周报文件（Word和PDF格式）

**请求体参数**:

| 字段 | 类型 | 说明 |
|-----|------|------|
| `report_title` | string | 报告标题 |
| `report_summary` | string | 报告摘要 |
| `fundamental_events` | json | 基本面事件数据 |
| `trend_image_src` | string | 趋势图片路径 |
| `position_summary_data` | json | 持仓摘要数据 |
| `curr_forecasts` | json | 货币预测数据 |
| `strategy_info` | json | 策略信息 |
| `data_image_src` | string | 数据图片路径 |
| `event_image_src` | string | 事件图片路径 |
| `week_start` | string | 周报起始日期 |

**成功响应**:

```json
{
    "code": 200,
    "message": "获取数据成功！",
    "data": true
}
```

## 依赖模块

- `flask.Blueprint`, `flask.session`, `flask.request`, `flask.send_from_directory`
- `json`, `platform`
- `..utils.web_response.WebResponse`
- `..service.forex_trading_tools.ForexTradingTools`
- `..service.cloudhands_weekly_report.CloudhandsWeeklyReport`