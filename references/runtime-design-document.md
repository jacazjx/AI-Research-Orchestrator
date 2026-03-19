# AI Research Orchestrator Design Document

## 1. 设计目标

本 Skill 的目标是把一个科研 IDEA 组织成一个可控、可追踪、可审计的五阶段科研运行时。

设计约束如下：

- 保持 Skill 形态，而不是演化成只依赖某一个平台的研究操作系统
- 保持每个阶段只有两个 Agent 参与循环，避免多 Agent 并发带来的 Token 浪费
- 保持每个阶段切换都有人工确认，避免黑盒自动推进
- 保持阶段内进度可视化，研究人员能随时看到当前状态、阻塞点和下一步动作
- 保持所有关键状态、交付物路径和 gate 决策都落盘

## 2. 总体架构

系统采用双循环架构：

- `inner_loop`
  阶段内循环。固定由两个 Agent 围绕当前阶段目标迭代。
- `outer_loop`
  阶段间循环。由主 Agent 负责阶段切换、质量门判定、PIVOT 提议、人工确认、恢复和可视化。

主 Agent 是唯一直接和用户对话的 Agent。其余 Agent 都由主 Agent 基于固定模板和当前任务动态渲染 prompt 后启动。

## 3. 核心文件

### 3.1 状态与结构文件

- `.autoresearch/state/research-state.yaml`
  机器可读唯一真相。记录当前阶段、当前 gate、phase review 状态、loop 次数、runtime registry、dashboard 路径、deliverable 索引。
- `.autoresearch/config/orchestrator-config.yaml`
  项目级运行时配置，人类可编辑的配置源。

### 3.2 可视化与运行时文件

- `.autoresearch/dashboard/status.json`
  当前项目机器可读状态快照
- `.autoresearch/dashboard/progress.md`
  人类可读进度板
- `.autoresearch/dashboard/timeline.ndjson`
  事件流
- `.autoresearch/runtime/job-registry.yaml`
  任务登记
- `.autoresearch/runtime/gpu-registry.yaml`
  GPU 占用登记
- `.autoresearch/runtime/backend-registry.yaml`
  执行后端登记
- `.autoresearch/runtime/sentinel-events.ndjson`
  恢复和监测事件流

## 4. 五阶段设计

> **阶段名称**：项目使用语义化阶段名称：`survey`、`pilot`、`experiments`、`paper`、`reflection`。旧的编号名称（`01-survey`等）仍然支持以保持向后兼容。

## 4.1 Phase 1: Literature and IDEA Research

目录：

- `docs/survey/`（Agent工作目录在 `agents/survey/` 和 `agents/critic/`）

角色：

- `Survey`
- `Critic`

阶段目标：

- 从用户 IDEA 和种子参考文献出发，锁定问题边界
- 扩展近 5 年相关工作，并在必要时补充经典工作
- 将 IDEA 拆解成 atomic academic definitions
- 识别 novelty gap、理论风险、候选 baseline、候选数据集和候选代码库
- 判断这个 IDEA 是否值得进入 pilot

### Survey 的具体任务

- 解析用户 IDEA
- 拆分核心概念、变量、假设、机制和目标
- 查找最新相关工作和必要经典工作
- 提取 formal definitions、数学表达、实现线索、可用代码库、可用数据集
- 构建 paper-to-code traceability
- 输出面向 Critic 的综述材料

### Critic 的具体任务

- 对综述结果和 IDEA 做可行性审查
- 对以下维度逐项评分：
  - novelty
  - feasibility
  - theory risk
  - experimental verifiability
  - resource cost
  - negative-result risk
- 给出 failure modes、counterexamples、blocking questions
- 指出最小修订集，而不是泛泛建议

### 阶段交付物

- `docs/survey/survey-round-summary.md`
- `docs/survey/critic-round-review.md`
- `docs/survey/research-readiness-report.md`
- `docs/survey/phase-scorecard.md`

### 质量门

人工 Gate：

- `gate_1`

进入下一阶段前必须满足：

- `phase_reviews.survey_critic = approved`
- `approval_status.gate_1 = approved`
- `research-readiness-report.md` 和 `phase-scorecard.md` 存在

Gate 1 核心标准：

- 问题边界足够明确
- 综述覆盖足够新且足够相关
- 理论和失败模式分析足够清楚
- 至少存在一个可执行的最小验证路径
- 进入 pilot 的理由明确

### 阶段内关系

- Survey 负责“生成研究地图和定义”
- Critic 负责“攻击和收缩问题”
- 主 Agent 负责决定是否继续循环、是否升级给用户、是否提出 pivot 候选

## 4.2 Phase 2: Problem Analysis and Pilot Validation

目录：

- `docs/pilot/`（代码在 `code/pilot/`，Agent工作目录在 `agents/coder/` 和 `agents/adviser/`）

角色：

- `Code`
- `Adviser`

阶段目标：

- 在 full experiment 之前，先做问题分析和低成本验证
- 用最小代价验证核心假设是否值得继续
- 发现显而易见的理论漏洞、实现漏洞、指标漏洞和实验设计漏洞

### Code 的具体任务

- 将 Phase 1 的研究报告转成 operational problem analysis
- 设计低成本 pilot experiment
- 选择最小必要数据、模型和指标
- 运行小规模验证或快速 sanity check
- 产出 pilot plan 和 pilot results

### Adviser 的具体任务

- 审核 pilot 是否真的能验证或反驳核心主张
- 审核 pilot setup 是否过度简化
- 审核 pilot 结果是否足以支持继续、返工或 pivot
- 给出 full experiment 的进入条件

### 阶段交付物

- `docs/pilot/problem-analysis.md`
- `code/configs/pilot-experiment-plan.md`
- `docs/pilot/pilot-results.md`
- `docs/pilot/pilot-adviser-review.md`
- `docs/pilot/pilot-validation-report.md`
- `docs/pilot/phase-scorecard.md`

### 质量门

人工 Gate：

- `gate_2`

进入下一阶段前必须满足：

- `phase_reviews.pilot_adviser = approved`
- `approval_status.gate_2 = approved`
- pilot 交付物齐全

Gate 2 核心标准：

- pilot setup 能真正检验核心想法
- pilot 结果足以支持继续 full experiment，或清晰支持 revision/pivot
- 风险和失败模式没有被回避
- 资源投入与潜在收益匹配

### 阶段内关系

- Code 负责”把 idea 变成最小验证系统”
- Adviser 负责”判断这个最小验证系统是否真的有辨别力”
- 主 Agent 负责决定是进入 full experiment、继续修订还是提出 pivot
- 如果用户拒绝 Gate 2，主 Agent 必须给出建议回退阶段，并让用户明确选择回到 `survey` 还是 `pilot`

## 4.3 Phase 3: Full Experiment

目录：

- `docs/experiments/`（代码在 `code/experiments/`，Agent工作目录在 `agents/coder/` 和 `agents/adviser/`）

角色：

- `Code`
- `Adviser`

阶段目标：

- 将已通过 pilot 的想法扩展成完整实验矩阵
- 管理实验运行、结果汇总、checkpoint 和 provenance
- 形成可用于论文写作的完整证据包

### Code 的具体任务

- 冻结 experiment spec
- 定义 baseline、dataset、metric、ablation、robustness check
- 维护 run registry、checkpoint index、results summary
- 保持实验可恢复、可追踪、可解释

### Adviser 的具体任务

- 审核实验矩阵是否完整
- 审核结果是否支持或反驳主张
- 审核负结果、空结果是否被正确记录
- 审核 evidence package 是否足够交给论文阶段

### 阶段交付物

- `code/experiments/experiment-spec.md`
- `code/experiments/run-registry.md`
- `code/experiments/results-summary.md`
- `code/experiments/checkpoints/checkpoint-index.md`
- `docs/experiments/experiment-adviser-review.md`
- `docs/experiments/evidence-package-index.md`
- `docs/experiments/phase-scorecard.md`

### 质量门

人工 Gate：

- `gate_3`

进入下一阶段前必须满足：

- `phase_reviews.experiment_adviser = approved`
- `approval_status.gate_3 = approved`
- evidence package 完整

Gate 3 核心标准：

- experiment matrix 已冻结且执行过
- run provenance、checkpoint、结果索引齐全
- 结果与原始主张之间的关系清楚
- baseline / metric / ablation 足够支持论文写作
- 负结果没有被隐藏

### 阶段内关系

- Code 负责“执行实验并沉淀证据”
- Adviser 负责“判断这些证据是否足够支撑论文”
- 主 Agent 负责控制算力消耗、阶段节奏、失败恢复和阶段升级

## 4.4 Phase 4: Paper Development and Submission-Quality Review

目录：

- `paper/`（Agent工作目录在 `agents/writer/` 和 `agents/reviewer/`）

角色：

- `Paper Writer`
- `Reviewer & Editor`

阶段目标：

- 只基于已批准证据写论文
- 通过写作和审稿循环把稿件提升到顶刊顶会可投稿水平

### Paper Writer 的具体任务

- 组织论文结构
- 撰写 methodology、related work、experiments、introduction、conclusion、abstract
- 维护 revision trace 和 rebuttal log
- 避免引入未验证的实验和论断

### Reviewer & Editor 的具体任务

- 按顶刊顶会标准审稿
- 检查 novelty、evidence strength、theoretical foundation、result analysis、writing quality
- 识别 unsupported claims、逻辑跳跃、结果解读不充分、结构性问题
- 返回结构化修改意见

### 阶段交付物

- `paper/paper-draft.md`
- `paper/citation-audit-report.md`
- `paper/reviewer-report.md`
- `paper/rebuttal-log.md`
- `paper/final-acceptance-report.md`
- `paper/phase-scorecard.md`

### 质量门

人工 Gate：

- `gate_4`

进入下一阶段前必须满足：

- `phase_reviews.paper_reviewer = approved`
- `approval_status.gate_4 = approved`
- 论文交付物齐全

Gate 4 核心标准：

- 稿件达到顶刊顶会可投稿水平
- 引用真实性已经审查，关键引用可验证
- 主要 reviewer finding 已被回应或处理
- 稿件不依赖未批准证据
- 理论、实验、写作三者之间一致

### 阶段内关系

- Writer 负责“表达和组织”
- Reviewer & Editor 负责“顶刊顶会标准下的质量筛选”，包括 citation authenticity 审查
- 主 Agent 负责决定继续修稿、停留本阶段还是提交给用户做阶段确认

## 4.5 Phase 5: Reflection and Controlled Evolution

目录：

- `docs/reflection/`（Agent工作目录在 `agents/reflector/` 和 `agents/curator/`）

角色：

- `Reflector`
- `Curator`

阶段目标：

- 将本项目中的经验转化为可复用的系统改进建议
- 形成 overlay 草案、runtime 改进建议和 lessons learned
- 保持闭环能力，但避免系统失控地自修改

### Reflector 的具体任务

- 提取成功路径、失败路径、恢复策略、昂贵错误、有效 prompt 改进点
- 形成 overlay 草案和 runtime 改进建议
- 区分 observation、recommendation、proposed change

### Curator 的具体任务

- 审核 reflection 产物是否可移植、可复用、是否安全
- 阻止不安全 overlay 自动激活
- 阻止平台相关 hack 被写成全局规则

### 阶段交付物

- `docs/reflection/lessons-learned.md`
- `docs/reflection/overlay-draft.md`
- `docs/reflection/runtime-improvement-report.md`
- `docs/reflection/phase-scorecard.md`

### 质量门

人工 Gate：

- `gate_5`

阶段完成前必须满足：

- `phase_reviews.reflection_curator = approved`
- `approval_status.gate_5 = approved`
- overlay 仍然处于 draft 状态，未被自动激活

Gate 5 核心标准：

- lessons learned 真实、可复用
- overlay 只是建议，不是自动生效配置
- runtime 改动建议有安全边界
- 反思结果不破坏 cross-platform Skill 定位

### 阶段内关系

- Reflector 负责“总结和提出演化建议”
- Curator 负责“约束演化边界，避免系统失控”
- 主 Agent 负责决定哪些建议可以进入后续实现计划，哪些仅保留为记录

## 5. Agent 职责总表

| Agent | 所属阶段 | 核心职责 | 核心约束 |
| --- | --- | --- | --- |
| 主 Agent | 全局 | 用户交互、任务分发、prompt 定制、阶段推进、gate 管理、pivot 提议、进度可视化 | 不绕过 gate，不替代子 Agent 直接伪造结论 |
| Survey | Phase 1 | 文献扩展、定义拆解、理论和实现线索整理 | 不做批评，不越界进入实验 |
| Critic | Phase 1 | novelty/feasibility/risk 审查 | 不给空泛建议，必须指出阻塞点 |
| Code | Phase 2/3 | pilot 验证和 full experiment 的设计、实现、运行、证据沉淀 | 不伪造运行，不跳过 provenance |
| Adviser | Phase 2/3 | 审核 pilot 和 full experiment 的设计质量与证据完整性 | 不在证据不足时批准推进 |
| Paper Writer | Phase 4 | 写稿、修稿、维护 rebuttal | 不引入未批准证据 |
| Reviewer & Editor | Phase 4 | 以顶刊顶会标准审稿 | 不降低标准，不把结构性缺陷当润色问题 |
| Reflector | Phase 5 | 提取经验、形成 overlay 草案 | 不自动生效任何改动 |
| Curator | Phase 5 | 审核演化建议是否安全和可复用 | 不允许 uncontrolled prompt drift |

## 6. Agent 之间的关系

### 6.1 主 Agent 与子 Agent 的关系

- 主 Agent 是 orchestrator，不是执行所有任务的替代者
- 主 Agent 负责：
  - 读 `research-state.yaml`
  - 读当前阶段交付物
  - 选择对应角色模板
  - 注入本轮任务目标、必读文件、附加约束
  - 启动子 Agent
  - 读取子 Agent 产物
  - 决定继续循环、请求人工确认、提出 pivot 或进入下一阶段

### 6.2 同阶段双 Agent 的关系

同一阶段内，两个 Agent 的关系不是对等闲聊，而是“生产者 / 审核者”关系：

- 第一个 Agent 主要产出主工件
- 第二个 Agent 主要做评审、反驳、补强和准入判断
- 主 Agent 决定是否回到第一个 Agent 修订
- 当人类拒绝当前 gate 时，主 Agent 必须呈现可回退阶段列表，并给出建议回退阶段

### 6.3 跨阶段关系

- Phase 1 决定有没有资格进入 pilot
- Phase 2 决定有没有资格花大算力做 full experiment
- Phase 3 决定有没有资格写论文
- Phase 4 决定有没有资格进入 reflection 或交付
- Phase 5 决定哪些经验能进入未来系统改进

也就是说，前一阶段不是简单产出文档，而是后续阶段的准入条件。

## 7. 质量门机制

系统里存在两类质量门：

### 7.1 阶段内质量门

由双 Agent 循环和 `phase_reviews.*` 驱动。

作用：

- 判断当前阶段是否继续 revise
- 判断是否需要 escalate_to_user
- 判断是否需要提出 pivot

### 7.2 阶段间人工 Gate

由 `approval_status.gate_*` 驱动。

作用：

- 只有人工批准后才能进入下一阶段
- 阻断黑盒自动科研

## 8. 决策输出类型

运行时最终会把阶段决策归一成四类：

- `advance`
- `revise`
- `pivot`
- `escalate_to_user`

语义如下：

- `advance`
  当前阶段交付物和质量门都满足，可以进入下一阶段
- `revise`
  当前阶段还需要继续双 Agent 循环
- `pivot`
  当前方向不值得直接继续，需要改变问题定义、理论路线、数据或实验路径
- `escalate_to_user`
  当前阶段在 loop limit 内无法收敛，必须由人来决定

## 9. 为什么要这样设计

这套设计不是追求“完全自动科研”，而是追求“高自动化但不失控的科研协作系统”。

与黑盒自动科研系统相比，这个设计的核心区别是：

- 每个阶段只有两个角色，便于理解和控制
- 每个阶段过渡都有人工参与
- 每个阶段都有落盘交付物和可视化状态
- reflection 能闭环，但 overlay 不能自动生效
- runtime 可以变强，但不会演化成不可控黑盒

## 10. 当前实现状态

当前代码已经落地了以下部分：

- 五阶段目录和状态模型
- handoff 校验
- quality gate 初始脚本
- dashboard 初始脚本
- stage loop 运行器
- pivot proposal / review 管理
- job 调度和本地/SSH 任务执行
- sentinel 检测与恢复脚本
- approved overlay 激活与 prompt 注入
- 固定 prompt 模板和角色映射
- README、SKILL、workflow、gate rubric、deliverable contract、role protocol

还未完全落地的部分包括：

- 更细的 scorecard 内容解析和自动评分细化
- 更完整的 GPU 自动发现和多机资源调度
- 更复杂的远程执行后端，例如 Slurm / RunPod / Kubernetes
- 更丰富的 self-healing 策略和跨项目 overlay 治理

因此，这份文档描述的是当前实现加上已经确定的设计约束，后续实现应以此为基线继续推进。
