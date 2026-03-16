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
  <img src="https://img.shields.io/badge/Version-1.0.0-green" alt="Version">
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
# 初始化新研究项目
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --topic "你的研究想法" \
  --client-type auto

# 运行特定阶段
/airesearchorchestrator:run-survey      # 启动文献调研阶段
/airesearchorchestrator:run-pilot       # 启动 Pilot 阶段
/airesearchorchestrator:run-experiments # 启动完整实验阶段
/airesearchorchestrator:write-paper     # 启动论文写作阶段
/airesearchorchestrator:reflect         # 启动反思总结阶段
```

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
| `/airesearchorchestrator:init-research` | 初始化新项目 | "init research", "初始化研究" |
| `/airesearchorchestrator:run-survey` | 运行文献调研阶段 | "run survey", "文献调研" |
| `/airesearchorchestrator:run-pilot` | 运行 Pilot 阶段 | "run pilot", "Pilot验证" |
| `/airesearchorchestrator:run-experiments` | 运行完整实验 | "run experiments", "完整实验" |
| `/airesearchorchestrator:write-paper` | 撰写论文 | "write paper", "写论文" |
| `/airesearchorchestrator:reflect` | 运行反思总结 | "reflect", "反思总结" |

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