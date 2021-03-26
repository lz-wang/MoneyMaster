# MoneyMaster

**为什么开发这个项目？**

1. 桌面端找不到好看好用的记账软件
2. 找不到可以支持导入微信支付宝账单数据的记账软件
3. 学习SQL语法、PyQt5框架、Python数据分析和爬虫

## 项目预期特性

1. 自动导入微信、支付宝账单等数据 
2. 通过数据库本地持久化 
3. 通过PyQt5框架界面可视化 
4. 统计每日、每月、每年的账单数据
5. 折线图、柱状图、饼状图详细分析账单数据
6. 支持通过农历的视角查看账单数据

## 开发计划

### 开发中

- 界面：重构为侧边栏主选项卡，其余为主要显示区的主窗口UI

### 计划中

- [ ]  界面：支持农历时间过滤数据
- [ ]  数据: 支持支付宝账单数据导入
- [ ]  数据: 支持银行账单数据
- [ ]  数据: 爬虫获取京东账单数据
- [ ]  数据: 智能合并导入的多种类型数据并归一化
- [ ]  数据: 支持导出到其他的记账软件格式
- [ ]  数据库: 支持MySQL数据库交互

### 已完成

1. 数据: 支持微信账单数据导入到数据库
2. 界面：支持数据显示为表格
3. 界面：支持数据表格翻页
4. 界面：支持折线图形式的数据展示
5. 界面：多标签页展示
6. 数据库：支持多种时间类型的SQLite数据库查询
7. 界面：支持柱状图形式的数据展示
8. 界面：支持饼状图形式的数据展示