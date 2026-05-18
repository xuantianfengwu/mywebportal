# 测试新函数说明

## 新增内容

### 新增的函数

1. **`get_picture_from_forex_position_new(data_df)`**
   - 生成专业金融报告风格的持仓图表
   - 包含金色边框、渐变背景、带框数据标签等效果

2. **`generate_forex_position_data_new()`**
   - 调用新图表生成函数并保存图片
   - 同时生成简体和繁体两个版本
   - 输出文件: `cftc_net_position_new.png` 和 `fanti_cftc_net_position_new.png`

## 日期格式注意事项

⚠️ 代码中使用 `datetime.datetime.strptime(self.week_start, '%Y-%m-%d')` 解析日期，**必须使用两位数的月份和日期**，例如：
- ✅ 正确：`'2026-05-18'`
- ❌ 错误：`'2026-5-18'`

## 如何测试运行

### 方法一：使用专门的测试脚本（推荐）

```bash
cd /Users/bytedance/Documents/projects/mywebportal
python test_new_function.py
```

### 方法二：在 Python 交互式环境中测试

```bash
cd /Users/bytedance/Documents/projects/mywebportal
python
```

然后在 Python 环境中执行：

```python
import sys
import os
sys.path.insert(0, os.getcwd())

from backend.service.cloudhands_weekly_report import CloudhandsWeeklyReport

# 使用已有数据目录中的日期（注意格式必须是 YYYY-MM-DD）
str_date = '2026-05-18'
report_generator = CloudhandsWeeklyReport(str_date)

# 测试新函数
result = report_generator.generate_forex_position_data_new()
print(result['picture_name'])
```

## 预期结果

测试成功后，会在以下位置生成新图表：

```
backend/static/output/cloudhands_weely_report/2026-05-18/
├── cftc_net_position_new.png          # 简体版本新图表
└── fanti_cftc_net_position_new.png    # 繁体版本新图表
```

## 新图表样式特点

1. **背景**：灰色渐变 (#e8e8e8)
2. **边框**：金色边框 (#c9a227)
3. **柱形颜色**：深蓝 (#1e4d8c) 和浅蓝 (#4a90d9)
4. **数据标签**：带金色边框的浅灰色背景框
5. **标题**：大号加粗字体
6. **图例**：带金色边框的专业样式

## 数据文件

测试使用的数据文件位于：
```
backend/static/crawl/cloudhands_weely_report/2026-05-18/cftc_net_position.csv
```
