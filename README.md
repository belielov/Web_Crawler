# Web_Crawler
# 通过浏览器开发者工具分析百度迁徙网络请求的详细步骤

## 1. 打开百度迁徙网站并启动开发者工具

**步骤：**
1. 使用Chrome浏览器打开 [百度迁徙网站](https://qianxi.baidu.com/)
2. 按 `F12` 键或右键选择"检查"打开开发者工具
3. 切换到 **Network（网络）** 选项卡

## 2. 配置Network面板以便观察

**关键设置：**
- 点击 **"Preserve log"（保留日志）** 复选框，确保页面跳转时请求不会丢失
- 在筛选框中输入 **"jsonp"** 或 **"historycurve"** 过滤请求
- 点击 **"Disable cache"（禁用缓存）** 避免浏览器缓存影响


## 3. 触发数据请求

**操作流程：**
1. 在百度迁徙页面中选择：
   - 选择地区（如：内蒙古自治区）
   - 选择时间范围
   - 选择迁徙类型（迁入/迁出）

2. 观察Network面板中出现的请求

## 4. 分析具体的API请求

**详细步骤：**

### 4.1 找到目标请求
- 在Network面板中滚动查找包含关键词的请求：
  - "historycurve" - 历史曲线数据
  - "jsonp" - JSONP格式的请求
  - "migration" - 迁徙相关

### 4.2 查看请求详情
点击找到的请求，查看以下信息：

**Headers选项卡：**
- **Request URL**: 完整的API地址
- **Request Method**: 通常是GET
- **Query String Parameters**: URL参数

**Preview/Response选项卡：**
- 查看返回的数据格式和内容

## 5. 具体示例分析

假设我们找到了这个请求：
```text
http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id=150000&type=move_in&callback=jsonp_1234567890
```

**参数解析：**
- `dt=province`: 数据级别（省份）
- `id=150000`: 区域代码（内蒙古）
- `type=move_in`: 数据类型（迁入）
- `callback=jsonp_1234567890`: JSONP回调函数名

## 6. 复制和测试API请求

**在开发者工具中直接测试：**
1. 右键点击目标请求
2. 选择 **"Copy" → "Copy as cURL"**
3. 可以在终端或Postman中测试

**或者手动构造URL：**
```bash
# 去掉callback参数，直接访问
curl "http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id=150000&type=move_in"
```
## 7. 验证数据格式
**返回数据示例**
```java
jsonp_1234567890({
    "errmsg": "SUCCESS",
    "data": {
        "list": {
            "20230101": 1.2345,
            "20230102": 1.3456,
            ...
        }
    }
})
```
**数据处理：**
- 去掉JSONP包装：`response.text[4:-1]` 或 `response.text.replace('jsonp_1234567890(', '').replace(')', '')`
- 解析为JSON对象
## 8. 完整实操演示

### 步骤记录：

1. 打开 https://qianxi.baidu.com/
2. F12打开开发者工具 → Network面板
3. 选择"内蒙古自治区" → "迁入"
4. 在Network中搜索"historycurve"请求
5. 找到URL：http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id=150000&type=move_in
6. 复制URL用于代码中

## 9. 注意事项

### 常见问题：

- **请求缓存**：记得勾选"Disable cache"
- **JSONP回调函数**：函数名会变化，需要动态处理
- **请求频率**：注意控制频率，避免被封IP
- **请求头**：某些数据可能需要特定的Referer或User-Agent

### 时间参数说明：

某些接口可能还需要日期参数，如：

- `date=20230101`
- `startDate=20230101&endDate=20230131`

### 关键要点：

- **迁徙规模指数**：全国为总体迁徙规模，不区分迁入或迁出；城市级区分迁入或迁出
- **城市边界**：采用该城市行政区划，包含该城市管辖的区、县、乡、村

通过以上步骤，您可以系统地分析百度迁徙网站的网络请求，找到正确的API接口并理解其参数结构，从而在代码中正确地构造和使用这些接口。
