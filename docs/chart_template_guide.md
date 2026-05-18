# 图表模版使用指南

## 概述

为了解决 `generate_forex_position_data_new` 样式不符合预期的问题，我们提供了四种方案：

1. **Excel 模版方案** - 在 Excel 中设计图表，Python 填充数据
2. **ECharts JSON 配置方案** - 编辑 JSON 配置文件调整样式
3. **自定义样式方案** - 直接修改 Python 代码
4. **Plotly + Pillow 混合方案** - 专业金融报告图表（推荐）

---

## matplotlib vs Plotly 效果实现对比表

| 层级 | 预期效果 | matplotlib 实现方式 | Plotly 实现方式 | 推荐 |
|------|---------|---------------------|----------------|------|
| **层级1：全局画布** | 外层浅灰底色 | `plt.figure(facecolor=...)` | `layout.paper_bgcolor` | ⚖️ 均可 |
| | 金色粗实线圆角边框 | 需要用 `patches.FancyBboxPatch` 手动绘制 | `layout.shapes` + `type='rect'` + `fillcolor='transparent'` | ✅ Plotly |
| | 整体画布圆角 | matplotlib 不支持，需要手动绘制背景 | Plotly 原生支持 | ✅ Plotly |
| **层级2：绘图区底板** | 双层渐变/分层底色 | 需要用 `matplotlib.colors.LinearSegmentedColormap` + `imshow` | `layout.plot_bgcolor` + `layout.shapes` 渐变背景 | ⚖️ 均可 |
| | 绘图区细微圆角 | 同样需要手动绘制 `FancyBboxPatch` | `layout.xaxis.rangeslider.bordercolor` 等 | ✅ Plotly |
| | 隐形内边距 | `plt.subplots_adjust(left=..., right=..., top=..., bottom=...)` | `layout.margin` + `xaxis.domain` | ✅ 均可 |
| **层级3：坐标轴 & 网格** | Y轴只显示负向刻度 + 0刻度 | `ax.set_ylim(bottom=..., top=0)` + 自定义 `xticks` | `yaxis.autorange` + `yaxis.range` | ⚖️ 均可 |
| | X轴分类文字横向排布 | `plt.xticks(rotation=0)` | `xaxis.tickangle=0` | ⚖️ 均可 |
| | 横向水平网格线 | `ax.grid(axis='y', linestyle='--', alpha=0.3)` | `yaxis.gridwidth` + `yaxis.gridcolor` | ⚖️ 均可 |
| | 0基线加粗 | `ax.axhline(0, linewidth=2)` | `yaxis.zero` + 自定义 shape | ⚖️ 均可 |
| **层级4：3D 柱状主体** | 伪3D立体柱状 | 需要复杂的手动绘制多边形和渐变 | `marker.color` + `marker.gradient` (Plotly Express) | ⚠️ Plotly |
| | 立体侧面光影 | 使用 `patches.Polygon` 手动绘制侧面 | `marker.gradient.type='vertical'` | ✅ Plotly |
| | 两组柱子独立配色 | 两组 `bar` 分别设置 `color` | 两组 trace 分别设置 `marker.color` | ⚖️ 均可 |
| | 金色全包描边 | `edgecolor='gold'` + `linewidth=2` | `marker.line.color` + `marker.line.width` | ⚖️ 均可 |
| | 簇状并列分组 | `width` + `x - width/2` 和 `x + width/2` | `barmode='group'` | ✅ Plotly |
| **层级5：投影阴影** | 后置投影（独立于柱子） | 手动绘制偏移的半透明 `bar` | 自定义 `shapes` + `opacity` | ⚖️ 均可 |
| | 灰色模糊投影 | 使用 `patches.Shadow` 或模糊算法 | Plotly 有限，需要 SVG 处理 | ⚠️ matplotlib |
| | 半透明羽化模糊 | matplotlib 需要额外库（Pillow）处理 | Plotly 原生不支持模糊 | ❌ 困难 |
| **层级6：数据标签** | 顶端/底端悬浮标签 | `ax.annotate(xytext=(0, offset))` | `textposition='outside'` | ✅ Plotly |
| | 白色填充底 + 金色细边框 + 圆角 | `bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='gold')` | `annotations` + `bgcolor` + `bordercolor` | ✅ 均可 |
| **层级7：标题 & 图例** | 顶部居中大标题 | `plt.title(ha='center', fontsize=..., fontweight='bold')` | `title.x=0.5` + `title.font` | ⚖️ 均可 |
| | 右上角图例：白底 + 金色边框 | `ax.legend(facecolor='white', edgecolor='gold', borderpad=...)` | `legend.bgcolor` + `legend.bordercolor` | ✅ 均可 |

---

## SVGChartGenerator 七层实现详解

### 概述

[SVGChartGenerator](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py) 是专业的 SVG 图表生成器，实现了完整的七层视觉效果。

### 七层实现对照表

| 层级 | 预期效果 | SVGChartGenerator 实现位置 | 核心代码 |
|------|---------|--------------------------|----------|
| **层级1：全局画布** | 外层浅灰底色 | `_generate_svg()` 方法 | `<rect fill="#e8e8e8"/>` |
| | 金色粗实线圆角边框 | `_generate_svg()` 方法 | `<rect rx="15" stroke="#c9a227" stroke-width="3"/>` |
| | 整体画布圆角 | `_generate_svg()` 方法 | SVG `rect` 元素的 `rx` 和 `ry` 属性 |
| **层级2：绘图区底板** | 双层渐变/分层底色 | `_generate_svg()` 方法 | 内层 `<rect fill="#d8d8d8"/>` |
| | 绘图区细微圆角 | `_generate_svg()` 方法 | `rx="10"` 的内层矩形 |
| | 隐形内边距 | `_generate_svg()` 方法 | `padding=60` 参数控制 |
| **层级3：坐标轴 & 网格** | Y轴刻度 | `_generate_axis()` 方法 | SVG `<text>` 元素绘制刻度值 |
| | X轴分类文字 | `_generate_axis()` 方法 | SVG `<text>` 元素绘制分类标签 |
| | 横向水平网格线 | `_generate_grid()` 方法 | SVG `<line>` 元素，`stroke-dasharray="4,4"` |
| | 0基线加粗 | `_generate_grid()` 方法 | `<line stroke-width="2.5"/>` |
| **层级4：3D 柱状主体** | 伪3D立体柱状 | `_draw_single_3d_bar()` 方法 | 三个 `<polygon>` 组成：前面+右侧面+顶面 |
| | 立体侧面光影 | `_draw_single_3d_bar()` 方法 | 右侧面深色填充，顶面高光填充 |
| | 两组柱子独立配色 | `_generate_3d_bars()` 方法 | `barGradient1` 和 `barGradient2` 渐变 |
| | 金色全包描边 | `_draw_single_3d_bar()` 方法 | `<polygon stroke="#c9a227"/>` |
| | 簇状并列分组 | `_generate_3d_bars()` 方法 | 计算 `group_x + bar_width / 2` 偏移 |
| **层级5：投影阴影** | 后置投影 | `_draw_single_3d_bar()` 方法 | SVG `<rect>` 元素，`filter="url(#shadow)"` |
| | 灰色模糊投影 | `_generate_defs()` 方法 | `<filter id="shadow">` 定义阴影滤镜 |
| | 半透明羽化模糊 | `_generate_defs()` 方法 | `feDropShadow` 滤镜参数控制 |
| **层级6：数据标签** | 顶端/底端悬浮标签 | `_generate_data_labels()` 方法 | SVG `<text>` 元素，动态计算位置 |
| | 白色填充底 + 金色细边框 + 圆角 | `_generate_label()` 方法 | `<rect fill="#f5f5f5" stroke="#c9a227" rx="3"/>` |
| **层级7：标题 & 图例** | 顶部居中大标题 | `_generate_title()` 方法 | `<text text-anchor="middle" font-weight="bold"/>` |
| | 右上角图例：白底 + 金色边框 | `_generate_legend()` 方法 | `<rect fill="#f8f8f8" stroke="#c9a227"/>` |

### 核心方法说明

| 方法名 | 功能说明 | 代码位置 |
|--------|---------|----------|
| `_generate_svg()` | 主入口，组织所有层级 | [svg_chart_generator.py#L187](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L187) |
| `_generate_defs()` | 定义渐变和滤镜（阴影） | [svg_chart_generator.py#L251](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L251) |
| `_generate_rounded_rect()` | 绘制圆角矩形（背景和边框） | [svg_chart_generator.py#L279](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L279) |
| `_generate_grid()` | 绘制网格线和0基线 | [svg_chart_generator.py#L291](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L291) |
| `_generate_axis()` | 绘制坐标轴和刻度 | [svg_chart_generator.py#L315](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L315) |
| `_generate_3d_bars()` | 遍历绘制所有3D柱子 | [svg_chart_generator.py#L364](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L364) |
| `_draw_single_3d_bar()` | 绘制单个3D柱子（核心） | [svg_chart_generator.py#L396](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L396) |
| `_generate_data_labels()` | 绘制数据标签 | [svg_chart_generator.py#L478](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L478) |
| `_generate_title()` | 绘制标题 | [svg_chart_generator.py#L594](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L594) |
| `_generate_legend()` | 绘制图例 | [svg_chart_generator.py#L597](file:///Users/bytedance/Documents/projects/mywebportal/backend/service/svg_chart_generator.py#L597) |

### 3D柱子绘制原理

`_draw_single_3d_bar()` 方法是核心，它通过组合三个 SVG 元素实现3D效果：

```
┌─────────────────────────────┐
│         顶面（高光）         │  ← 浅蓝渐变
├─────────────────────────────┤
│  前面（主体）  │  右侧面     │
│  深蓝渐变     │  深色阴影    │  ← 立体光影效果
└─────────────────────────────┘
    ↓ 投影阴影
```

每个柱子包含：
1. **阴影层**：使用 SVG 滤镜实现模糊效果
2. **前面**：主颜色渐变填充
3. **右侧面**：深色阴影，营造立体感
4. **顶面**：高光效果，模拟光照
5. **高光条**：左侧白色渐变，增强立体感
6. **金色边框**：全包描边，精致感

### 输出格式

SVGChartGenerator 同时生成两种格式：

| 格式 | 文件名 | 特点 |
|------|--------|------|
| SVG | `cftc_net_position.svg` | 矢量图形，无限缩放 |
| PNG | `cftc_net_position.png` | 位图格式，方便展示 |

---

## 方案对比总结

| 能力维度 | matplotlib | Plotly |
|---------|-----------|--------|
| 基础图表绘制 | ✅ 优秀 | ✅ 优秀 |
| 3D/渐变效果 | ⚠️ 需要手动实现 | ✅ 原生支持 |
| 圆角边框 | ⚠️ 需要手动绘制 | ✅ 原生支持 |
| 阴影模糊效果 | ⚠️ 需要额外库 | ❌ 有限支持 |
| 数据标签样式 | ✅ 支持 | ✅ 支持 |
| 实现复杂度 | 🔥 需要大量自定义代码 | 📊 配置更简洁 |
| 整体接近目标 | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 推荐方案：Plotly + Pillow 混合方案

### 为什么混合方案？

- **Plotly** 处理基础图表框架（80% 的效果）
- **Pillow** 处理高级视觉效果（模糊阴影、精细光影）

### 使用方法

```bash
# 运行测试
python test_new_function.py
```

生成的图片位于：
```
backend/static/output/cloudhands_weely_report/2026-05-18/cftc_net_position_plotly_pillow.png
```

---

## 方案一：ECharts JSON 配置（matplotlib 版）

### 步骤 1：查看当前配置

配置文件位于：
```
backend/config/chart_templates/echarts_config.json
```

### 步骤 2：理解配置结构

```json
{
  "title": {
    "text": "标题文字",
    "textStyle": {
      "fontSize": 24,        // 字体大小
      "fontWeight": "bold",  // 字体粗细
      "color": "#1a1a1a"     // 颜色
    }
  },
  "series": [
    {
      "name": "上周净持仓",
      "type": "bar",
      "itemStyle": {
        "color": "#1e4d8c",  // 柱子颜色
        "borderColor": "#c9a227",  // 边框颜色
        "borderWidth": 2      // 边框宽度
      }
    }
  ]
}
```

### 步骤 3：调整样式

1. 用文本编辑器打开 `echarts_config.json`
2. 修改颜色、字体大小、边框等参数
3. 保存文件

### 步骤 4：测试新配置

```bash
cd /Users/bytedance/Documents/projects/mywebportal
source .venv/bin/activate
python test_new_function.py
```

---

## 方案二：Excel 模版

### 步骤 1：打开 Excel 模版

模版文件位于：
```
backend/config/chart_templates/position_chart_template.xlsx
```

### 步骤 2：设计图表

1. 在 Excel 中打开模版文件
2. 在 "Chart" 工作表中调整图表样式
3. 更改颜色、字体、边框等
4. 保存文件

### 步骤 3：使用模版（开发中）

注意：由于 macOS 系统限制，从 Excel 直接导出图片比较复杂。建议使用 Plotly + Pillow 方案。

---

## 方案三：直接修改 Python 代码

如果您想直接调整当前样式，可以修改 `get_picture_from_forex_position_new` 函数。

文件位置：
```
backend/service/cloudhands_weekly_report.py
```

主要可调整的部分：

```python
# 1. 图表尺寸
fig, ax = plt.subplots(figsize=(14, 8), facecolor='#e8e8e8')

# 2. 背景和边框颜色
fig.patch.set_edgecolor('#c9a227')  # 金色边框

# 3. 柱子颜色
rects1 = ax.bar(..., color='#1e4d8c', ...)
rects2 = ax.bar(..., color='#4a90d9', ...)

# 4. 标题大小
ax.set_title(title, fontsize=24, ...)

# 5. 数据标签样式
bbox_props = dict(boxstyle="square,pad=0.4", 
                  fc="#f5f5f5", 
                  ec="#c9a227", 
                  lw=1)
```

---

## 文件结构

```
mywebportal/
├── backend/
│   ├── config/
│   │   └── chart_templates/
│   │       ├── position_chart_template.xlsx  # Excel 模版
│   │       └── echarts_config.json           # ECharts 配置
│   └── service/
│       ├── cloudhands_weekly_report.py       # 主程序
│       ├── chart_template_utils.py           # 模版工具
│       └── plotly_chart_generator.py         # Plotly + Pillow 生成器
├── docs/
│   └── chart_template_guide.md               # 本文档
└── test_new_function.py                      # 测试脚本
```

---

## 下一步建议

1. 先运行 `test_new_function.py` 查看当前效果
2. 对比生成的图片，选择最合适的方案
3. 如需完全自定义，可以考虑使用专业的图表工具（如 Tableau、D3.js）
