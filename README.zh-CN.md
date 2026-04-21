# Atomic Knowledge

[English](README.md)

Atomic Knowledge 是一个平台中立、基于 Markdown 的 agent 维护型 `work memory` 协议。

它是 chat-native 的：正常入口仍然是你和 agent 的普通自然语言对话，背后依托的是 Markdown 知识库，而不是一个额外的命令面板。

它受 Andrej Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 启发：不是每次提问都从原始资料重新检索和综合，而是让 agent 持续维护一套可复用、可链接、可演进的 Markdown wiki。

它不是替代你现有的 agent，而是给你现有的 agent 增加一层可维护、能跨 session 延续的 Markdown work memory。

## 最新更新

这轮 public kit 主要补了三件事：

- 正式把 `wiki/procedures/` 纳入知识模型，用来承接可复用 workflow 和 playbook
- 正式页面现在可以带可选的 `search_anchors` 和 `key_entities` 检索提示
- 模板、example KB、health check 和 runtime 的 `get_context` 都已经认识这一层

## 为什么它存在

- 一换 session，agent 往往很难稳定复用之前研究过的上下文
- 很多高价值判断和综合 insight 出现在讨论里，却又消失在聊天记录中
- 用户经常不得不重复发送旧链接、旧笔记和旧结论，而不是在已有研究上继续推进

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

## 适合谁

如果你符合下面这些情况，Atomic Knowledge 会比较适合你：

- 已经在用 agent 做研究、比较、综合或长期项目推进
- 希望跨 session 延续上下文，但不想把聊天记录本身当成真相源
- 接受本地 markdown / 文件系统工作流
- 想要一个可安装、可检查、可迁移的开源协议，而不是一个托管型 memory 产品

如果你更想要下面这些东西，它可能就不太适合：

- 一个独立的 SaaS app 或 dashboard
- 一个不具备本地文件访问和 shell 执行能力的纯聊天环境
- 一个“什么都记下来”的聊天记忆归档器

## 产品分发面

这个仓库本身就是可安装、平台中立的产品分发面。

仓库根目录就是面向 GitHub 分发和跨 agent 接入的 kit。

## 当前状态

Atomic Knowledge 当前处于较早期的开源发布阶段。

当前仓库基线对应 `v0.2.0`。

现在已经具备：

- 可通过本地 bootstrap 流程安装
- 有 `example-kb/` 作为真实示例
- 有 `evals/` 可用于接入验收
- 包含一个可选的、面向 agent 的 runtime，用于 `init_kb`、`check_kb`、`get_context`、`validate_kb`
- 包含一个最小 MCP adapter，用于 tool-calling 场景下的 agent 集成
- 主要面向支持本地文件读写和 shell 执行的 agent 环境

## 可选 Agent Runtime

Atomic Knowledge 仍然保持平台中立、chat-native、markdown-first。普通用户的主入口仍然是和 agent 的普通对话，而不是 CLI 或 MCP 工作流。

这个仓库现在还包含：

- 一个可选的、面向 agent 的 runtime，用于执行有界的机械型知识库动作
- 一个最小 MCP adapter，用于 agent integration 和 tool calling

它们是给 agent 使用的执行层，不是主要产品入口。普通用户不需要学习 CLI、MCP 或 runtime 细节，也能正常使用 Atomic Knowledge。

当前方向和边界说明见：

- [Agent Runtime Direction](docs/AGENT_RUNTIME_DIRECTION.md)
- [Runtime Boundary](docs/RUNTIME_BOUNDARY.md)
- [Chat-Native Journeys](docs/CHAT_NATIVE_JOURNEYS.md)
- [MCP Tool Contracts](docs/MCP_TOOL_CONTRACTS.md)
- [Runtime README](runtime/README.md)
- [MCP Adapter README](adapters/mcp/README.md)

## 自主边界

Atomic Knowledge 运行在普通 agent 对话里，但自主边界保持保守：

- 读取：agent 应主动做，用于 continuation、上下文恢复、检索和 lint 新鲜度检查
- 建议：agent 可以主动建议 ingest、candidate capture、promotion/merge、stale cleanup 或 lint，但默认不落盘
- 写入：只有当用户自然语言里已经明确表达记录意图时，才视为获得授权
- 高影响操作：删除、归档、批量整理、大规模重构、目录结构修改，都需要明确确认

“总结/分析一个链接”不等于自动 ingest。

用户不应该需要记住 `candidate`、`insight` 这类协议词；系统应优先按当前对话语言理解用户表达，如果当前对话语言不明显，再回退到系统语言或稳定的语言偏好信号。

## 快速开始

大多数用户应该先在聊天里开始，让 agent 帮你完成 bootstrap。正常入口仍然是普通对话，而不是 CLI、runtime 或 MCP 工作流。

### Chat-native bootstrap

对大多数用户来说，最简单的起步方式是 `BOOTSTRAP_PROMPT.md`。

把里面的提示词粘贴给一个支持本地文件读写和 shell 执行的 agent，让 agent 帮你完成初始化。

初始化完成后，继续留在同一个聊天里，用自然语言和 agent 协作即可。你不需要自己学习 CLI 命令、MCP 或 runtime 细节。

### 本地 helper

如果你确实想在支持本地能力的环境里直接调用仓库 helper，标准初始化器是：

```bash
bash scripts/init-kb.sh "$HOME/Desktop/My-Knowledge"
```

如果你更喜欢短一点的入口，也可以继续使用 `init.sh` 这个便捷别名。

它会创建一个新的知识库，并生成：

```text
$HOME/Desktop/My-Knowledge/AGENT.md
```

然后二选一：

1. 放进你的 agent 平台支持的持久指令区
2. 如果平台不支持持久指令，就让 agent 在每次 session 开始时读取这个文件

这个命令只是仓库 helper，不是普通用户的主要入口。Atomic Knowledge 仍然是接入你现有 agent 工作流的，不会再引入一个新的 app、dashboard 或 command surface。

更多用法见 [Agent-Native Usage](docs/AGENT_NATIVE_USAGE.md)。

## 从这里开始

- [Kit Guide](docs/KIT_GUIDE.md)：安装方式和通用目录结构
- [Comparison](docs/COMPARISON.md)：它和记忆插件、RAG、聊天记录到底有什么不同
- [Use Cases and FAQ](docs/FAQ.md)：更偏非技术视角的使用场景和常见问题
- [Agent-Native Usage](docs/AGENT_NATIVE_USAGE.md)：如何在现有 agent 对话里使用
- [Example Knowledge Base](example-kb/) 与 [Walkthrough](example-kb/WALKTHROUGH.md)：一个可读、可参照的小型示例知识库
- [Eval Scenarios](evals/README.md)：如何验证一个现有 agent 是否真的接入了协议
- [Optional Local Health Check](scripts/check-kb.sh)：只读的知识库结构和新鲜度检查
- [Candidate Lifecycle](docs/CANDIDATE_LIFECYCLE.md)：`meta/candidates/` 如何经历 `open -> promoted | merged | dropped`
- [Lint Workflow](docs/LINT_WORKFLOW.md)：维护循环如何保持知识库干净和可用

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
├── AGENT.md                  # 可移植的 agent 协议
├── adapters/                 # 可选的 agent 集成适配层
├── BOOTSTRAP_PROMPT.md       # 面向本地能力 agent 的一句安装 prompt
├── README.md                 # 仓库总览
├── README.zh-CN.md           # 中文总览
├── docs/                     # 说明文档与 protocol note
├── evals/                    # agent 接入验收场景
├── example-kb/               # 可直接阅读的小型示例知识库
├── schemas/                  # 各类知识页面 schema
├── scripts/                  # 初始化与健康检查脚本
├── knowledge-base-template/  # 初始化时复制出去的模板
├── init.sh                   # 标准初始化器的可选便捷别名
├── runtime/                  # 可选的内部 runtime，用于有界 KB 动作
├── CONTRIBUTING.md           # 贡献说明
├── AGENTS.md                 # 仓库维护说明
└── LICENSE
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
- `wiki/procedures/`：可重复执行的 workflow、playbook 和稳定操作规则
- `wiki/insights/`：durable takeaway、比较、决策和综合结论
- `meta/candidates/`：仍然是 provisional、但值得保留的 work-memory note
- `meta/lint-status.json`：健康度和新鲜度元数据

其中：

- `active.md` 和 `recent.md` 是主要入口页
- `projects`、`procedures` 和 `insights` 是正式的 durable work-memory 层
- 正式页面可以带可选的 `search_anchors` 和 `key_entities` frontmatter，用作检索提示，但 markdown 页面本身仍然是真相层
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
4. 读取相关 `wiki/projects/` 和 `wiki/procedures/`
5. 读取相关 `wiki/insights/`
6. 仅在必要时再补 `wiki/concepts/` 和 `wiki/entities/`
7. 如果有多个相近正式页，可用可选的 `search_anchors` 和 `key_entities` 缩小读取范围
8. 只有 formal wiki 不足时才看 `meta/candidates/`
9. 带文件引用回答
10. 如果用户请求本身已带记录意图，就直接写回；否则只建议 writeback

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

更多细节见 [Lint Workflow](docs/LINT_WORKFLOW.md) 和 [Candidate Lifecycle](docs/CANDIDATE_LIFECYCLE.md)。

## 跨 agent 设计

根目录 kit 的设计目标就是跨不同 agent 平台工作。

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
