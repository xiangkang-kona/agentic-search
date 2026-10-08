# Agentic Search — 基于 Qwen 推理决策的智能企业搜索系统

**在线演示**: https://agentic-search-utj2ihtbk7nyd7x66oxa83.streamlit.app

一个用 **LLM Agent 推理决策**取代传统 RAG 固定检索流水线的多源企业搜索系统。用户提出自然语言问题后，由 Qwen 大模型作为 Agent 自主分析意图、规划搜索路径、在多个异构数据源间多轮迭代调用工具，直到收集到足够信息再生成最终回答。

## 项目背景：为什么用 Agentic Search 而不是 RAG

传统 RAG 的检索流程是固定的（切分 -> 嵌入 -> 召回 -> 拼接上下文 -> 生成），面对**多数据源、结构化数据、时间语义**的企业场景效果有限。本项目改用 Agent 模式：

| 维度 | 传统 RAG | 本项目 Agentic Search |
|------|----------|----------------------|
| 检索策略 | 固定流水线，一次召回 | LLM 每轮推理决定下一步查什么、用什么工具 |
| 数据源 | 向量库单源 | 6 类异构数据源、13 个工具按需组合 |
| 时间语义 | 难以处理 | System Prompt 注入当前日期，模型自行解析"本周/本月/最近" |
| 精确查询 | 弱 | Agent 可自主编写并执行 SQL 聚合 |
| 过程可解释 | 黑盒 | 每轮推理、工具调用、API 原始响应全程可视化 |

## 系统架构

```
用户问题
   |
   v
AgenticSearchAgent (core/agent.py)
   |-- System Prompt: 时间感知 + 意图路由规则 + 关键词提取规则
   |-- LLMClient (core/llm.py): OpenAI 兼容接口调用 Qwen (Function Calling)
   |-- 推理循环: 最多 20 轮, 信息充分即停止
   |
   v
13 个搜索工具 (Function Calling)
   |-- database_search / database_sql / database_schema   -> SQLite 结构化数据
   |-- vector_search / vector_info                        -> ChromaDB 向量语义检索
   |-- keyword_search / keyword_info                      -> Whoosh + jieba 中文全文索引
   |-- code_search / code_read / code_list                -> 代码仓库检索
   |-- enterprise_call / enterprise_systems               -> 模拟企业系统 API (HR/财务/项目/Wiki)
   |-- log_search                                         -> 操作日志
   |
   v
Streamlit 可视化界面 (app.py): 推理步骤 / 工具调用 / API 原始响应 / 最终回答全程展示
```

## 核心实现

- **零框架 Agent**: 不依赖 LangChain 等框架，基于 OpenAI SDK 的 Function Calling 原生实现"LLM + 工具调用 + 循环"的完整 Agent 闭环
- **时间语义解析**: System Prompt 动态注入当前日期与时间词换算规则（本周/本月/最近 7 天），使模型能正确查询时间相关数据
- **意图路由**: 通过提示词工程约束工具选择策略（支付流水 -> 财务系统、合同 -> SQL 查询、模糊概念 -> 向量检索），减少无效搜索轮次
- **多源融合**: 结构化查询（SQLite/SQL）、语义检索（Chroma）、关键词检索（Whoosh）、代码检索四类引擎统一封装为工具
- **过程可视化**: 前端完整展示每轮 LLM 推理内容、工具调用参数与结果、最终回答的完整对话上下文

## 技术栈

Python / Streamlit / OpenAI SDK (Qwen, DashScope 兼容模式) / ChromaDB / SQLite / Whoosh / jieba

## 数据源（演示数据）

| 数据源 | 内容 |
|--------|------|
| SQLite 数据库 | 100 员工、15 部门、50 项目、40 合同、40 产品 |
| 向量数据库 | 公司信息、技术文档、会议纪要共 251 篇语义文档 |
| 关键词索引 | 公司政策、技术文章共 110 篇 |
| 代码仓库 | 34 个模拟源码文件 |
| 企业系统 API | HR / 财务 / 项目 / Wiki 四个模拟系统 |

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置密钥
cp .env.example .env
# 编辑 .env, 填入你的 DASHSCOPE_API_KEY (获取地址: https://bailian.console.aliyun.com/)

# 3. 启动 Web 界面
python -m streamlit run app.py

# 或启动命令行交互版 (会自动灌入演示数据)
python main.py
```

## 项目结构

```
├── app.py                 # Streamlit 可视化界面
├── main.py                # 命令行交互入口
├── config.py              # 路径与 LLM 配置
├── core/
│   ├── agent.py           # Agent 核心: System Prompt、工具定义、推理循环
│   ├── llm.py             # OpenAI 兼容客户端 (支持 Function Calling)
│   └── logger.py          # 操作日志
├── engines/
│   ├── database.py        # SQLite 引擎 (关键词搜索 + SQL 执行)
│   ├── vector_db.py       # ChromaDB 向量检索引擎
│   ├── keyword_search.py  # Whoosh + jieba 全文索引引擎
│   ├── code_search.py     # 代码仓库检索引擎
│   └── enterprise_sdk.py  # 模拟企业系统 API
├── seed_data_large.py     # 演示数据生成
└── data/                  # SQLite / 向量库 / 索引 / 代码仓库 / 日志
```
