# Atomic Knowledge

[English](README.md)

Atomic Knowledge 是一个平台中立、基于 Markdown 的 agent 维护型 `work memory` 协议。

它受 Andrej Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 启发：不是每次提问都从原始资料重新检索和综合，而是让 agent 持续维护一套可复用、可链接、可演进的 Markdown wiki。

## 它是什么

Atomic Knowledge 面向已经在日常使用 agent 的人，尤其是这些场景：

- 持续把链接、笔记、资料交给 agent
- 在多个 session 之间延续讨论
- 比较工具、想法、项目和方向
- 逐步积累一个长期研究上下文

真正重要的不只是 source 本身，而是 source 和讨论共同形成的 insight。

它的目标不是记住所有聊天，也不是存用户画像；它的目标是保留可复用的 `work memory`，例如稳定结论、比较结果、项目上下文和决策理由，让未来 session 可以继续往前推进。

## 它不是什么

Atomic Knowledge 不是：

- 像 mem0 那样的 persona memory 层
- 聊天记录归档器
- 向量数据库
- 泛化 RAG 框架
- 某个平台专属的 prompt 包

它更像一个基于文件系统的协议和工作流，用来让用户与 agent 共同维护长期 work memory。

相比 mem0，它关注的是 work memory，而不是偏好、语气或 persona memory。

相比普通 RAG，它维护的是一层持续整理过的知识层，而不是只在回答时临时取回原始 chunk。

## 主线

`universal/` 是这个仓库的主线产品面。

它包含适合 GitHub 分发和跨 agent 接入的、平台中立版本。

## 自主边界

Atomic Knowledge 运行在普通 agent 对话里，但自主边界保持保守：

- 读取：agent 应主动做，用于 continuation、上下文恢复、检索和 lint 新鲜度检查
- 建议：agent 可以主动建议 ingest、candidate capture、promotion/merge、stale cleanup 或 lint，但默认不落盘
- 写入：只有当用户自然语言里已经明确表达记录意图时，才视为获得授权
- 高影响操作：删除、归档、批量整理、大规模重构、目录结构修改，都需要明确确认

“总结/分析一个链接”不等于自动 ingest。

## 快速开始

### 本地安装

```bash
bash init.sh "$HOME/Desktop/My-Knowledge"
```

`init.sh` 是 `universal/scripts/init-kb.sh` 的轻量封装。

它会创建一个新的知识库，并生成：

```text
$HOME/Desktop/My-Knowledge/AGENT.md
```

然后二选一：

1. 放进你的 agent 平台支持的持久指令区
2. 如果平台不支持持久指令，就让 agent 在每次 session 开始时读取这个文件

Atomic Knowledge 是接入你现有 agent 工作流的，不会再引入一个新的 app、dashboard 或 command surface。

更多用法见 [Agent-Native Usage](universal/docs/AGENT_NATIVE_USAGE.md)。

### 一句 bootstrap prompt

把 `universal/BOOTSTRAP_PROMPT.md` 里的内容粘贴给一个支持本地文件读写和 shell 执行的 agent。

## 从这里开始

- [Universal Kit Guide](universal/README.md)：安装方式和通用目录结构
- [Agent-Native Usage](universal/docs/AGENT_NATIVE_USAGE.md)：如何在现有 agent 对话里使用
- [Example Knowledge Base](universal/example-kb/) 与 [Walkthrough](universal/example-kb/WALKTHROUGH.md)：一个可读、可参照的小型示例知识库
- [Eval Scenarios](universal/evals/README.md)：如何验证一个现有 agent 是否真的接入了协议
- [Optional Local Health Check](universal/scripts/check-kb.sh)：只读的知识库结构和新鲜度检查
- [Candidate Lifecycle](universal/docs/CANDIDATE_LIFECYCLE.md)：`meta/candidates/` 如何经历 `open -> promoted | merged | dropped`
- [Lint Workflow](universal/docs/LINT_WORKFLOW.md)：维护循环如何保持知识库干净和可用

## 核心思想

传统 RAG 往往是：

1. 存原始文件
2. 查询时取 chunk
3. 当场重新综合答案

Atomic Knowledge 在原始资料和最终答案之间加入一层“被维护的 wiki”：

1. 原始 source 只捕获一次
2. agent 把 source 和围绕它产生的 durable insight 编译成 wiki 页面
3. 未来的回答优先建立在这层被维护的知识层上
4. 当用户明确要求保留时，好的回答和讨论 insight 也可以被写回

这样得到的是持续积累，而不是重复重发现。

## 仓库结构

```text
atomic-knowledge/
├── init.sh                        # 通用初始化脚本的轻量封装
├── universal/                    # 主线、平台中立版本
│   ├── AGENT.md                  # 可移植的 agent 协议
│   ├── BOOTSTRAP_PROMPT.md       # 面向本地能力 agent 的一句安装 prompt
│   ├── README.md                 # Universal Kit 说明
│   ├── example-kb/               # 可直接阅读的小型示例知识库
│   ├── schemas/                  # 各类知识页面 schema
│   ├── docs/                     # 跨 agent 的说明文档
│   ├── scripts/init-kb.sh        # 标准知识库初始化器
│   └── knowledge-base-template/  # 初始化时复制出去的模板
├── AGENTS.md                     # 仓库维护说明
└── README.md                     # 仓库总览
```

## 知识模型

Atomic Knowledge 使用一个基于 Markdown 的知识库，核心对象包括：

- `raw/sources/`：原始资料捕获
- `wiki/active.md`：当前活跃项目、比较和 open questions
- `wiki/recent.md`：最近新增、更新、修正、替代的知识
- `wiki/index.md`：主题目录
- `wiki/log.md`：ingest、query、writeback、lint 的时间线记录
- `wiki/concepts/`：稳定概念、方法、框架、定义
- `wiki/entities/`：人、工具、公司、项目、命名系统
- `wiki/projects/`：跨 session 的长期研究线程
- `wiki/insights/`：durable takeaway、比较、决策和综合结论
- `meta/candidates/`：仍然是 provisional、但值得保留的 work-memory note
- `meta/lint-status.json`：健康度和新鲜度元数据

其中：

- `active.md` 和 `recent.md` 是主要入口页
- `projects` 和 `insights` 是正式的 durable work-memory 层
- `meta/candidates/` 是补充性缓冲区，不是一等真相源

## 核心工作流

### Ingest

当用户明确要求把 source 保存为未来可复用的知识时，agent 会：

1. 读取 source
2. 提取关键 takeaways
3. 在 `raw/sources/` 中保存 source capture
4. 创建或更新相关 wiki 页面
5. 按需更新 `active.md`、`recent.md`、`index.md`、`log.md` 和元数据

### Query

当用户提出 topic-level 问题时，agent 会：

1. 读取 `wiki/active.md`
2. 读取 `wiki/recent.md`
3. 用 `wiki/index.md` 定位相关主题
4. 读取相关 `wiki/projects/` 和 `wiki/insights/`
5. 仅在必要时再补 `wiki/concepts/` 和 `wiki/entities/`
6. 只有 formal wiki 不足时才看 `meta/candidates/`
7. 带文件引用回答
8. 如果用户请求本身已带记录意图，就直接写回；否则只建议 writeback

### Writeback

只写回 durable knowledge，例如：

- 有复用价值的比较
- 稳定框架
- 项目 thesis
- 决策记录
- 对未来研究仍然有价值的综合结论

### Maintenance

Maintenance 和 ingest、query 一样，是核心工作流的一部分。

它通过以下方式保持知识库长期可用：

- 跑 lint，检查矛盾、过期信息、链接和 index 健康度
- 把 `meta/candidates/` 当成 review queue，而不是永久 backlog
- 通过 `open -> promoted | merged | dropped` 解决 candidate

更多细节见 [Lint Workflow](universal/docs/LINT_WORKFLOW.md) 和 [Candidate Lifecycle](universal/docs/CANDIDATE_LIFECYCLE.md)。

## 跨 agent 设计

Universal Kit 的设计目标就是跨不同 agent 平台工作。

接入模型很简单：

1. 初始化一个知识库
2. 渲染出带真实路径的 `AGENT.md`
3. 把这份协议安装进 agent 平台支持的持久指令面
4. 如果平台没有持久指令面，就把这个文件当成每次 session 的启动协议

## 为什么是 Markdown

因为 Markdown：

- 人可读
- 易 diff
- 适合 git
- 适合 agent 搜索和编辑
- 易于在 Obsidian、编辑器和本地搜索工具之间复用

## 灵感来源

- [Andrej Karpathy - LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Vannevar Bush - As We May Think (1945)](https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/)

## 致谢

Atomic Knowledge 当前这条路径，直接受益于 Andrej Karpathy 的 [LLM Wiki 想法](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。感谢他提供了最初的 framing 和启发。

## License

MIT
