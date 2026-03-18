<p align="center">
  <img src="assets/images/logo.svg" alt="AI Research Orchestrator" width="200">
</p>

<h1 align="center">AI Research Orchestrator</h1>

<p align="center">
  <strong>把一个科研 IDEA 变成有状态机、有交付物、有显式人工 gate 的研究项目</strong>
</p>

<p align="center">
  简体中文 | <a href="README.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-blue?logo=anthropic" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Version-1.3.0-green" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Python-3.9+-blue" alt="Python">
  <img src="https://img.shields.io/badge/Phase-5-orange" alt="5 阶段">
</p>

---

`AI Research Orchestrator` 把一个科研 IDEA 变成有状态机、有交付物、有可视化进度、有显式人工 gate 的研究项目。专为需要文献调研、Pilot 验证、实验和论文写作的 AI/ML 研究设计。

## 工作流程图

### 整体研究管线

```
    ┌────────────────────────────────────────────────────────────────────────────┐
    │                           研究 IDEA                                          │
    └─────────────────────────────────┬──────────────────────────────────────────┘
                                      │
                                      ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  阶段 1: 文献调研 (SURVEY)                                                   │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │    SURVEY     │ ── 文献综述 ────────────────▶│    CRITIC     │          │
    │  │   (执行者)    │ ── 新颖性检查 ──────────────▶│   (审核者)    │          │
    │  │               │ ◀── 修订请求 ──────────────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   门控 1 ✋   │  ← 需要人工审批                        │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │ 分数 ≥ 3.5
                                 ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  阶段 2: Pilot 验证 (PILOT)                                                 │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │     CODE      │ ── Pilot 实验 ──────────────▶│   ADVISER     │          │
    │  │   (执行者)    │ ── 初步结果 ────────────────▶│   (审核者)    │          │
    │  │               │ ◀── 设计反馈 ──────────────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   门控 2 ✋   │  ← Go/No-Go 决策                       │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │ Go 决策
                                 ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  阶段 3: 完整实验 (EXPERIMENTS)                                             │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │     CODE      │ ── 全量实验 ────────────────▶│   ADVISER     │          │
    │  │   (执行者)    │ ── 证据包 ──────────────────▶│   (审核者)    │          │
    │  │               │ ◀── 验证请求 ──────────────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   门控 3 ✋   │  ← 证据是否充分？                      │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │ 证据获批
                                 ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  阶段 4: 论文写作 (PAPER)                                                   │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │    WRITER     │ ── 论文草稿 ────────────────▶│   REVIEWER    │          │
    │  │   (执行者)    │ ── 证据引用 ────────────────▶│   (审核者)    │          │
    │  │               │ ◀── 修订意见 ──────────────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   门控 4 ✋   │  ← 是否达到投稿标准？                  │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │ 获批
                                 ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  阶段 5: 反思总结 (REFLECTION)                                              │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │  REFLECTOR    │ ── 经验教训 ────────────────▶│    CURATOR    │          │
    │  │   (执行者)    │ ── 改进建议 ────────────────▶│   (审核者)    │          │
    │  │               │ ◀── 可执行项 ──────────────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   门控 5 ✋   │  ← 归档并关闭                          │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌───────────────────────┐
                    │   📁 项目已关闭        │
                    │   经验已归档           │
                    └───────────────────────┘
```

### 阶段内循环详解

```
                    ┌─────────────────────────────────────────┐
                    │            阶段开始                      │
                    └──────────────────┬──────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │   ┌─────────────┐                       │
                    │   │   主要      │                       │
                    │   │   Agent     │                       │
                    │   │  (执行者)   │                       │
                    │   └──────┬──────┘                       │
                    │          │                              │
                    │          │ 产出                         │
                    │          ▼                              │
                    │   ┌─────────────┐                       │
                    │   │   交付物    │                       │
                    │   │   (草稿)    │                       │
                    │   └──────┬──────┘                       │
                    │          │                              │
                    │          │ 提交审核                     │
                    │          ▼                              │
                    │   ┌─────────────┐                       │
                    │   │   审核者    │                       │
                    │   │   Agent     │                       │
                    │   │  (审核者)   │                       │
                    │   └──────┬──────┘                       │
                    │          │                              │
                    │          │ 评分 & 评论                  │
                    │          ▼                              │
              ┌─────┴─────────────────────────────┐           │
              │                                   │           │
              ▼                                   ▼           │
       ┌────────────┐                      ┌────────────┐     │
       │   通过     │                      │   修订     │     │
       │ 分数 ≥3.5  │                      │  分数 <3.5 │     │
       └─────┬──────┘                      └──────┬─────┘     │
             │                                    │           │
             │                                    │           │
             │        ┌───────────────────────────┘           │
             │        │                                       │
             │        │ 反馈循环                               │
             │        └──────────────────────┐                │
             │                               │                │
             │                               ▼                │
             │                    ┌──────────────────┐        │
             │                    │ 达到最大循环次数？│        │
             │                    └────────┬─────────┘        │
             │                             │                  │
             │              ┌──────────────┼──────────────┐    │
             │              │              │              │    │
             │              ▼              ▼              ▼    │
             │         ┌────────┐   ┌────────────┐  ┌────────┐ │
             │         │  是    │   │    否      │  │ 上报   │ │
             │         │退出循环│   │  继续循环  │  │ 给人类 │ │
             │         └────┬───┘   └────────────┘  └───┬────┘ │
             │              │                           │      │
             └──────────────┼───────────────────────────┘      │
                            │                                  │
                            ▼                                  │
                    ┌───────────────┐                          │
                    │   门控检查    │◀─────────────────────────┘
                    │   ✋ 人工      │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │   通过   │  │   修订   │  │   回退   │
       │ 进入下一 │  │ 继续工作 │  │ 返回之前 │
       │   阶段   │  │          │  │   阶段   │
       └────┬─────┘  └──────────┘  └──────────┘
            │
            ▼
    ┌─────────────────┐
    │   下一阶段      │
    └─────────────────┘
```

### 回退与转向流程

```
    当前阶段
         │
         │ 门控未通过 (分数 < 2.5)
         │
         ▼
    ┌─────────────────────────────────────────────────────┐
    │                    回退选项                          │
    │                                                      │
    │   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
    │   │   修订   │   │   回退   │   │   转向   │        │
    │   │  (停留)  │   │  (返回)  │   │  (变更)  │        │
    │   └────┬─────┘   └────┬─────┘   └────┬─────┘        │
    │        │              │              │               │
    │        ▼              ▼              ▼               │
    │   继续当前       返回之前        改变               │
    │   阶段工作       的阶段          研究方向           │
    │                                                      │
    └─────────────────────────────────────────────────────┘
         │
         │ Orchestrator 建议：
         │ "根据发现的问题，建议回退到阶段 X"
         │
         ▼
    ┌─────────────────┐
    │  人类决定       │
    │  选择哪个选项？ │
    └────────┬────────┘
             │
             ▼
    在选择的阶段恢复
    上下文已保留
```

## 五阶段概览

| 阶段 | Agent 组合 | 关键交付物 | 门控 |
|------|-----------|-----------|------|
| **文献调研** | Survey ↔ Critic | `research-readiness-report.md` | 门控 1 |
| **Pilot 验证** | Code ↔ Adviser | `pilot-validation-report.md` | 门控 2 |
| **完整实验** | Code ↔ Adviser | `evidence-package-index.md` | 门控 3 |
| **论文写作** | Writer ↔ Reviewer | `final-acceptance-report.md` | 门控 4 |
| **反思总结** | Reflector ↔ Curator | `runtime-improvement-report.md` | 门控 5 |

## Agent 职责

### 主要 Agent（执行者）

| Agent | 阶段 | 职责 |
|--------|------|------|
| **Survey** | 文献调研 | 使用学术 API 进行文献综述，定义原子化学术概念，识别研究空白 |
| **Code** | Pilot, 实验 | 设计实验，实现代码，运行实验，分析结果 |
| **Writer** | 论文写作 | 基于已批准证据撰写论文，构建论证结构 |
| **Reflector** | 反思总结 | 提炼经验教训，提出系统改进建议 (overlay) |

### 审核 Agent（审计者）

| Agent | 阶段 | 职责 |
|--------|------|------|
| **Critic** | 文献调研 | 审核新颖性、可行性、理论风险、引用真实性 |
| **Adviser** | Pilot, 实验 | 审核实验设计，验证结果，判断证据强度 |
| **Reviewer** | 论文写作 | 按顶刊顶会标准审核论文，审计引用 |
| **Curator** | 反思总结 | 判断哪些改进可复用、安全、可执行 |

## 门控机制

### 门控评分

| 分数 | 决定 | 操作 |
|------|------|------|
| 4.5-5.0 | ✅ 通过 | 立即进入下一阶段 |
| 3.5-4.4 | 🔶 推进 | 小修后推进 |
| 2.5-3.4 | 🔄 修订 | 需要大幅修订 |
| 1.5-2.4 | 🔙 重修 | 返回更早阶段 |
| 0.0-1.4 | ⚠️ 转向 | 考虑替代方案或终止 |

### 门控检查清单

**门控 1 (Survey → Pilot)：**
- [ ] 文献综述（至少 10 篇，仅使用学术 API）
- [ ] 有证据支撑的新颖性论证
- [ ] 所有引用已验证真实性
- [ ] 研究问题清晰定义

**门控 2 (Pilot → Experiments)：**
- [ ] Pilot 代码无错误运行
- [ ] 初步结果支持假设
- [ ] 有明确的 go/no-go 建议

**门控 3 (Experiments → Paper)：**
- [ ] 所有实验可追溯（有 run ID）
- [ ] 统计分析完成
- [ ] 无隐藏的负面结果

**门控 4 (Paper → Reflection)：**
- [ ] 论文可编译为 PDF
- [ ] 所有引用已验证（≥90%）
- [ ] 无占位符文本

**门控 5 (Reflection → Close)：**
- [ ] 经验教训已记录
- [ ] Overlay 决策已完成
- [ ] 项目已归档

## 安装

### 方式一：从 GitHub Marketplace 安装（推荐）

```bash
# 1. 添加 marketplace
/plugin marketplace add jacazjx/AI-Research-Orchestrator

# 2. 安装插件
/plugin install airesearchorchestrator@airesearchorchestrator
```

### 方式二：配置 settings.json

在 `~/.claude/settings.json` 中添加：

```json
{
  "extraKnownMarketplaces": {
    "airesearchorchestrator": {
      "source": {
        "source": "github",
        "repo": "jacazjx/AI-Research-Orchestrator"
      }
    }
  },
  "enabledPlugins": {
    "airesearchorchestrator@airesearchorchestrator": true
  }
}
```

### 方式三：本地开发安装

```bash
cc --plugin-dir /path/to/AI-Research-Orchestrator
```

## 快速开始

```bash
# 步骤 0（推荐）：在提交项目前先澄清你的研究想法
/airesearchorchestrator:insight

# 步骤 1：初始化新研究项目
/airesearchorchestrator:init-research

# 步骤 2-6：按顺序运行每个阶段
/airesearchorchestrator:run-survey      # 阶段 1 — 文献调研
/airesearchorchestrator:run-pilot       # 阶段 2 — Pilot 验证
/airesearchorchestrator:run-experiments # 阶段 3 — 完整实验
/airesearchorchestrator:write-paper     # 阶段 4 — 论文撰写
/airesearchorchestrator:reflect         # 阶段 5 — 经验教训总结
```

> **要恢复已存在的项目？** 在每个新的 Claude Code 会话开始时，先运行 `/airesearchorchestrator:reload` 来恢复项目上下文，然后再继续。

## 时间预期

每个研究阶段根据复杂度和范围有不同的时间要求：

| 阶段 | 时长 | 主要活动 |
|------|------|----------|
| **文献调研** | 2-5 天 | 通过学术 API 搜索文献、新颖性分析、引用验证 |
| **Pilot 验证** | 1-3 天 | 代码实现、小规模实验、初步验证 |
| **完整实验** | 3-14 天 | 全量实验运行、统计分析、证据收集（因复杂度而异） |
| **论文写作** | 3-7 天 | 论文撰写、内部评审、修订循环 |
| **反思总结** | 1 天 | 提炼经验教训、提出改进建议 |

**项目总时长：** 通常 10-30 天，取决于实验复杂度和修订循环次数。

**加速完成技巧：**
- 初始化时提供清晰、具体的研究想法
- 及时响应门控决策
- 高效利用 GPU 资源进行实验
- 保持文献搜索聚焦于关键论文

## 常见问题 (FAQ)

### Q: 如何恢复中断的研究项目？

在任何新的 Claude Code 会话开始时使用 reload 命令：
```bash
/airesearchorchestrator:reload
```
这将从 `research-state.yaml` 恢复完整的项目上下文，包括：
- 当前阶段和状态
- 门控分数和反馈
- Agent 交接摘要
- 阻塞项和待决策事项

### Q: 门控分数不够怎么办？

分数低于 3.5 需要修订。审核 Agent 会提供具体反馈：

| 分数范围 | 需要的操作 |
|----------|-----------|
| 2.5-3.4 | 需要大幅修订；根据反馈修改后重新提交 |
| 1.5-2.4 | 存在重大问题；可能需要返回更早阶段 |
| 0.0-1.4 | 根本性问题；考虑转向研究方向 |

Orchestrator 会根据审核者的反馈建议具体的补救步骤。

### Q: 如何使用自己的 GPU 服务器？

1. 在 `~/.autoresearch/gpu-registry.yaml` 中注册 GPU：
```yaml
devices:
  - id: "my-gpu-01"
    name: "RTX 4090"
    host: "192.168.1.100"
    ssh_key: "~/.ssh/id_rsa"
```

2. 配置项目使用它：
```bash
/airesearchorchestrator:configure
```

3. 在配置过程中选择你的 GPU。

### Q: 引用验证失败怎么处理？

引用验证失败表示可能存在真实性问题：

1. **检查来源：** 通过 DOI 查询或学术 API 验证论文是否存在
2. **替换伪造引用：** 使用 Semantic Scholar 或 arXiv 查找真实论文
3. **重新验证：** 修正后 Critic Agent 会重新验证

常见原因：
- 论文标题或作者名拼写错误
- 引用了不存在的论文（AI 幻觉）
- 使用网页搜索结果而非学术 API 来源

### Q: 可以跳过某些阶段吗？

**不可以。** 五阶段流程设计用于确保研究质量：

- 每个阶段基于前一阶段的交付物构建
- 门控检查验证进入下一阶段的准备情况
- 跳过阶段会损害研究完整性

**但是，你可以：**
- 如果门控分数为 3.5-4.4，可以申请"小修后推进"
- 使用 `/airesearchorchestrator:configure` 命令调整参数
- 在特殊情况下手动批准提前推进（不推荐）

## 故障排除指南

### 初始化失败

**症状：** `/init-research` 失败或创建不完整的项目结构。

**解决方案：**
1. 确认已安装 Python 3.9+：`python3 --version`
2. 检查目标目录的写入权限
3. 确保有足够的磁盘空间（建议至少 500MB）
4. 尝试使用绝对路径：`--project-root /绝对/路径/到/项目`

### Agent 卡住不动

**症状：** Agent 似乎卡住，长时间没有进展。

**解决方案：**
1. 检查 dashboard 中的阻塞消息
2. 运行 `/airesearchorchestrator:status` 查看当前状态
3. 尝试重新加载项目：`/airesearchorchestrator:reload`
4. 如果确实卡住，可以关闭并重新启动 Agent
5. 检查 `agents/<角色>/` 中的错误日志

### 门控审核失败

**症状：** 尽管多次修订，门控分数仍然很低。

**解决方案：**
1. 仔细阅读审核者反馈 - 它包含具体问题
2. 解决反馈中提到的所有问题
3. 检查交付物是否符合预期格式
4. 验证引用来自学术 API，而非网页搜索
5. 如果问题根本性，考虑请求回退到更早阶段

### 引用问题

**症状：** "引用验证失败" 或 "检测到伪造引用"。

**解决方案：**
1. **验证引用是否存在：**
   ```bash
   # 通过 DOI 检查
   curl "https://api.crossref.org/works?query.title=你的论文标题"

   # 通过 Semantic Scholar 检查
   curl "https://api.semanticscholar.org/graph/v1/paper/search?query=你的查询"
   ```

2. **用来自学术 API 的已验证论文** 替换有问题的引用

3. **重新运行引用审计** 通过审核者 Agent

4. **避免使用网页搜索** 查找文献 - 始终使用学术 API

### 常见错误信息

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `State file not found` | 项目未初始化 | 运行 `/airesearchorchestrator:init-research` |
| `Invalid phase transition` | 跳过阶段 | 先完成前一阶段 |
| `Gate score insufficient` | 分数 < 3.5 | 根据审核者反馈修改 |
| `Agent timeout` | 长时间运行的任务 | 等待或检查日志 |
| `Citation not found` | 伪造或拼写错误 | 验证并替换引用 |

## 目录结构

```
my-project/
├── .autoresearch/           # 系统目录
│   ├── state/               # research-state.yaml（唯一数据源）
│   ├── config/              # orchestrator-config.yaml
│   ├── dashboard/           # 可视化进度追踪
│   └── runtime/             # Job/GPU/Backend 注册表
├── agents/                  # Agent 工作目录
│   ├── survey/              # Survey agent 工作区
│   ├── critic/              # Critic agent 工作区
│   ├── coder/               # Code agent 工作区
│   ├── adviser/             # Adviser agent 工作区
│   ├── writer/              # Writer agent 工作区
│   ├── reviewer/            # Reviewer agent 工作区
│   ├── reflector/           # Reflector agent 工作区
│   └── curator/             # Curator agent 工作区
├── paper/                   # 论文相关文件
├── code/                    # 代码和实验
└── docs/reports/            # 阶段交付物
    ├── survey/
    ├── pilot/
    ├── experiments/
    └── reflection/
```

## 命令列表

| 命令 | 描述 | 触发词 |
|------|------|--------|
| `/airesearchorchestrator:insight` | 澄清研究意图 | "insight", "澄清意图" |
| `/airesearchorchestrator:init-research` | 初始化新项目 | "init research", "初始化研究" |
| `/airesearchorchestrator:status` | 显示项目状态 | "status", "查看状态", "项目状态" |
| `/airesearchorchestrator:run-survey` | 运行文献调研阶段 | "run survey", "文献调研" |
| `/airesearchorchestrator:run-pilot` | 运行 Pilot 阶段 | "run pilot", "Pilot验证" |
| `/airesearchorchestrator:run-experiments` | 运行完整实验 | "run experiments", "完整实验" |
| `/airesearchorchestrator:write-paper` | 撰写论文 | "write paper", "写论文" |
| `/airesearchorchestrator:reflect` | 运行反思总结 | "reflect", "反思总结" |
| `/airesearchorchestrator:reload` | 恢复会话上下文 | "reload", "重新加载", "恢复项目" |
| `/airesearchorchestrator:configure` | 配置项目设置 | "configure", "配置" |

## 硬规则

1. **每阶段两个 Agent** - 只有主要和审核 Agent 处于活跃状态
2. **文献检索禁止网页搜索** - 使用学术 API（Semantic Scholar、arXiv、CrossRef、DBLP、OpenAlex）
3. **禁止伪造** - 永不伪造引用、实验或结果
4. **人工门控强制** - 未经批准不得自动推进阶段
5. **状态持久化** - 所有状态保存到 `research-state.yaml`

## 文献检索 API

| API | 用途 | 示例 |
|-----|------|------|
| Semantic Scholar | AI/ML 论文 | `api.semanticscholar.org/graph/v1/paper/search?query=transformer` |
| arXiv | 预印本 | `export.arxiv.org/api/query?search_query=all:attention` |
| CrossRef | DOI 验证 | `api.crossref.org/works?query.title=paper+title` |
| DBLP | 计算机科学 | `dblp.org/search/publ/api?q=transformer&format=json` |
| OpenAlex | 综合性 | `api.openalex.org/works?search=vision+transformer` |

## 参考文档

- [工作流协议](references/workflow-protocol.md) - 阶段顺序和要求
- [门控评分细则](references/gate-rubrics.md) - 详细评分标准
- [系统架构](references/system-architecture.md) - 内外循环设计
- [阶段执行细节](references/phase-execution-details.md) - 每阶段子步骤

## 测试

```bash
python3 -m pytest tests/ -v
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE)。

---

<p align="center">
  为 AI 研究者用心打造 ❤️
</p>