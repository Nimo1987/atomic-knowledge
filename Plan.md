# Atomic Knowledge 优化计划

本文件用于收敛当前 review 结论，并作为后续优化任务列表。

## 1. 项目定位

Atomic Knowledge 的目标，不是做一个泛化的聊天记忆系统，也不是做一个把所有历史对话都存起来的 memory 仓库。

它应该聚焦于：

- 沉淀用户与 agent 在长期研究、比较、判断、探索中的 `work memory`
- 将外部资料和高价值对话火花编译成可复用的知识页
- 在新 session 和新项目中主动复用已有研究上下文
- 让知识以 markdown wiki 的形式持续积累，而不是每次从原始资料重新发现

一句话定义：

> Atomic Knowledge 记录的是 `我们已经一起想明白了什么`，而不是 `这个用户平时喜欢什么`。

## 2. 与 mem0 的边界

本项目需要明确区别于 mem0 一类的记忆库产品。

### 2.1 应记录的内容

- 稳定的研究结论
- 可复用的比较框架
- 项目级决策与取舍理由
- 被验证有效的研究方向
- 被验证无效的研究方向及原因
- 与某个主题相关的高价值 open questions
- 对未来项目仍有帮助的洞见和综合判断

### 2.2 不应记录的内容

- 纯 persona memory
- 单纯的聊天语气偏好
- 一次性任务状态
- 情绪化表达或临时感受
- 没有形成结构的碎片闲聊
- 原样保存整段聊天记录

### 2.3 边界原则

- `mem0` 偏向 `persona memory`
- `Atomic Knowledge` 偏向 `work memory`
- 对话中的精彩瞬间可以沉淀，但必须先被提炼为可复用知识，而不是直接当聊天记忆存档

## 3. 已确认的设计约束

- 继续坚持 markdown 作为主知识载体
- 暂不引入数据库作为主存储
- 暂不为每个页面引入 sidecar JSON，避免用户手改 markdown 后元数据漂移
- 保留最少量、全局性的机器元数据文件，例如 `meta/lint-status.json`
- 知识库最终结构必须保持干净，不允许候选内容无限堆积

## 4. 当前主要问题

### 4.1 当前协议过于 source-first

现有设计已经很好地覆盖了“用户丢一个链接，agent 进行 ingest”的路径，但对“用户与 agent 讨论过程中逐步形成的洞见”支持不足。

这会导致项目更像“资料编译器”，还不像“长期研究协作的 work memory 系统”。

### 4.2 缺少候选沉淀层

当前只有正式 wiki 页面和原始资料层，没有一个中间缓冲层来承接对话中刚形成、但尚未完全稳定的高价值内容。

结果是二选一：

- 要么直接写进正式 wiki，污染知识库
- 要么不写，导致灵感和高质量判断丢失

### 4.3 缺少明确的检索触发协议

目前仓库已经强调“先看 index 再回答”，但仍不够。

需要解决的问题不是“知识是否被存下”，而是：

- 什么时候 agent 应主动参考知识库
- 应先读哪些导航页
- 应读到什么深度
- 什么情况下不该查知识库

### 4.4 Schema 承载能力不足

当前 `concept/entity/project/insight` schema 偏轻，尚不能很好承载：

- 结论的置信度
- 页面之间的推导关系
- 被替代、被修正、被推翻的关系
- 研究中的未决问题
- 当前项目的活跃状态

### 4.5 缺少完整黄金路径示例

仓库现在更像“协议模板 + 初始化脚手架”，但缺少一个最小完整示例来说明：

- 新资料如何进入
- 对话火花如何成为 candidate
- candidate 如何升级为 insight 或 project 更新
- 新 session 如何主动复用这些知识

### 4.6 存在真实实现缺陷

`init-kb.sh` 在处理包含 `&` 的路径时会把生成的 `AGENT.md` 写坏。这是应优先修复的边界问题。

## 5. 目标状态

优化后的项目应达到以下状态：

1. 用户给 agent 一个新链接，agent 不只是总结，还能把它与已有项目和 insight 建立关系。
2. 用户与 agent 讨论中出现高价值火花时，agent 能先沉淀为 candidate，而不是丢失或直接污染正式 wiki。
3. 新 session 遇到研究型问题时，agent 能主动先查知识库，而不是每次重新研究。
4. agent 查知识库时有明确入口，不会因为页面增多而“疯掉”。
5. 正式 wiki 保持干净，candidate 层会被定期清理、合并、提升或丢弃。
6. 用户能清楚感受到：这个项目是一个长期 work memory 系统，而不是另一个聊天记忆工具。

## 6. 建议的信息架构

建议在现有结构上做最小增量调整，而不是推翻重来。

```text
raw/
  sources/

wiki/
  active.md
  recent.md
  index.md
  log.md
  concepts/
  entities/
  projects/
  insights/

meta/
  lint-status.json
  schemas/
  candidates/
    index.md
    <candidate-note>.md
```

### 6.1 `wiki/active.md`

作用：维护当前活跃的研究主题、项目、正在推进的比较和 open questions。

它是 agent 在研究型请求中优先读取的入口页之一。

### 6.2 `wiki/recent.md`

作用：维护最近形成、最近更新、最近被修正的 insight / project。

它解决“最近我们研究到了哪里”的问题。

### 6.3 `meta/candidates/`

作用：承接高价值但尚未完全固化的 work memory。

这里不是正式知识区，也不是永久存档区，而是待整理缓冲区。

## 7. 候选沉淀层设计

### 7.1 设计目的

用于承接对话中的精彩瞬间、高价值判断、初步框架和待继续推进的 open question。

### 7.2 准入门槛

只有满足以下至少一项，才值得进入 candidate：

- 改变了当前项目的理解或方向
- 对未来任务或项目有明显复用价值
- 能与已有 source / concept / project / insight 建立关系
- 构成一个值得追踪的 open question

### 7.3 明确不收录

- 单纯的聊天偏好
- 情绪性表达
- 一次性任务状态
- 没有结构的即兴发散
- 原样聊天记录

### 7.4 生命周期

`对话火花 -> candidate -> promote / merge / drop`

其中：

- `promote`: 提升为正式 insight，或更新某个 project / concept / entity
- `merge`: 合并进已有页面
- `drop`: 明确认定无长期价值，清理掉

### 7.5 清理原则

- candidate 是缓冲区，不是永久知识库
- lint 时应检查长期未处理的 candidate
- 对超过一定时间仍未提升的 candidate 进行提醒和清理
- 默认要保持 candidate 总量可控

## 8. 检索与咨询策略

项目必须同时定义“知识怎么记”和“agent 什么时候必须回头看”。

### 8.1 应触发知识库咨询的场景

- 用户开启一个研究型话题
- 用户让 agent 做比较、判断、路线选择
- 用户给出与既有主题相关的新资料
- 用户明确表达“继续之前那个话题”
- 用户的问题明显属于 ongoing project 的延续
- agent 准备输出综合性结论、方案、路线图之前

### 8.2 不应优先触发知识库咨询的场景

- 简单语法/API 问题
- 当前代码仓库内的即时 debug
- 一次性执行型任务
- 强依赖实时外部信息且与历史研究无关的问题

### 8.3 推荐检索顺序

当触发知识库咨询时，推荐顺序为：

1. `wiki/active.md`
2. `wiki/recent.md`
3. `wiki/index.md`
4. 相关 `project` 页面
5. 相关 `insight` 页面
6. 必要时补充 `concept/entity`
7. 仅在正式 wiki 不足时，再参考相关 `candidate`

### 8.4 Candidate 的使用规则

- candidate 不是一级真相源
- candidate 只能作为补充线索，不应直接当最终结论引用
- 若回答依赖 candidate，应推动后续 promote / merge

## 9. Schema 升级方向

保持轻量，不引入过重的数据模型，但需要让页面能承载更真实的长期研究过程。

### 9.1 `project` 建议新增的最小字段

- `status`: active / paused / archived
- `current_thesis`
- `open_questions`
- `related_insights`
- `last_reviewed`

### 9.2 `insight` 建议新增的最小字段

- `confidence`: low / medium / high
- `derived_from`
- `related_projects`
- `supersedes`
- `superseded_by`

### 9.3 `concept` / `entity` 建议新增的最小字段

- `aliases`
- `related_pages`
- `updated`

### 9.4 `candidate` 需要独立 schema

建议新增 markdown schema，例如：

- `title`
- `created`
- `status`
- `related_topic`
- `derived_from`
- `why_it_matters`
- `next_action`

## 10. 文档与产品表达优化

需要在 README 和通用协议里更明确地说明：

- 本项目不是 persona memory 系统
- 本项目不是“什么都记”的聊天归档器
- 本项目比普通 RAG 多了“持续编译与维护”的知识层
- 本项目比 mem0 更关注 work memory 和研究复用

同时应补一段更贴近真实场景的说明：

- 用户每天给 agent 链接、资料、问题和讨论
- 真正有价值的，不只是资料本身，还有资料与讨论共同形成的 insight
- Atomic Knowledge 的职责是把这些 insight 编译成未来可复用的结构化知识

## 11. 黄金路径示例

建议新增一个最小但完整的 end-to-end 示例文档，展示以下流程：

1. 用户分享一个新链接
2. agent 进行 ingest，并更新相关 project / insight
3. 用户与 agent 进一步讨论，形成一个高价值判断
4. 该判断先进入 candidate
5. 经过整理后提升为正式 insight
6. 下一个 session 中，agent 在研究同主题时主动先查 `active/recent/index`
7. agent 复用已有 insight，而不是从零开始搜索与总结

这个示例应成为仓库最重要的演示路径之一。

## 12. 分阶段任务列表

### P0：收紧定位并补齐最关键缺口

- [ ] 在 `README.md` 中明确 `work memory` 与 `persona memory` 的边界
- [ ] 在 `README.md` 中明确与 `mem0`、普通 RAG 的差异
- [ ] 在 `universal/AGENT.md` 中加入明确的检索触发规则
- [ ] 在 `universal/AGENT.md` 中加入对 `candidate` 层的说明
- [ ] 在 `universal/knowledge-base-template/` 中新增 `wiki/active.md`
- [ ] 在 `universal/knowledge-base-template/` 中新增 `wiki/recent.md`
- [ ] 在 `universal/knowledge-base-template/` 中新增 `meta/candidates/index.md`
- [ ] 新增 `candidate` markdown schema
- [ ] 修复 `init-kb.sh` 在路径包含 `&` 时的替换问题

### P1：把知识库从“可存”升级为“可用”

- [ ] 为 `project` schema 增加活跃状态与 open question 支持
- [ ] 为 `insight` schema 增加 `confidence`、`derived_from`、`supersedes` 等字段
- [ ] 为 `concept/entity` schema 增加最小关系字段
- [ ] 在 `universal/AGENT.md` 中加入 `active -> recent -> index -> pages` 的检索顺序
- [ ] 明确 candidate 的 promote / merge / drop 流程
- [ ] 明确 candidate 的清理规则与 lint 行为

### P2：补齐可理解性与演示能力

- [ ] 新增一个完整黄金路径示例文档
- [ ] 在 `universal/README.md` 中增加真实使用场景说明
- [ ] 在 `docs/` 中新增“何时查知识库，何时不要查”的独立说明
- [ ] 补一份“项目设计原则”文档，解释为什么不走数据库和 sidecar JSON 路线

### P3：在规模增长后再考虑的方向

- [ ] 评估更好的本地搜索能力，但仍以 markdown 为主
- [ ] 评估更细粒度的反思/决策记录机制
- [ ] 评估更强的 lint 与重复检测能力
- [ ] 评估多 agent 协作时的知识维护约束

## 13. 暂不做的事情

以下内容当前不进入主计划：

- 不做“记录一切”的聊天记忆系统
- 不做 persona-first 的用户画像层
- 不做数据库优先的知识底座
- 不做每页一份 JSON 的 sidecar 元数据体系
- 不做自动保存整段会话的 transcript 仓库

## 14. 完成标准

当以下条件成立时，可以认为当前阶段的优化方向基本正确：

1. 用户能清楚理解项目与 mem0 的边界。
2. 对话中的高价值火花有地方落，但不会污染正式 wiki。
3. agent 在研究型请求中有明确的知识库咨询协议。
4. 知识库规模变大后，agent 仍能通过 `active/recent/index` 快速找到上下文。
5. 新 session 中，agent 的回答能明显体现“基于过去研究继续推进”，而不是重新开始。
6. 正式 wiki 结构依旧干净，没有被 candidate 或闲聊内容侵蚀。
