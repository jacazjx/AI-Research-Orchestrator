# AI Research Orchestrator

`ai-research-orchestrator` 是一个面向 Codex、Claude Code、Openclaw 等环境的科研工作流 Skill。它把一个科研 IDEA 变成一个有状态机、有交付物、有可视化进度、有显式人工 gate 的研究项目。

当前版本已经开始从三阶段骨架升级到更接近 Sibyl 的运行时设计，但保留本项目的核心定位：

- 仍然是 Skill，不是单平台研究操作系统
- 每个阶段固定只有两个 Agent 循环
- 每个阶段切换都要求人类科研人员确认
- 所有关键状态都落盘到 `.autoresearch/state/research-state.yaml` 和 dashboard

## 特性

- 五阶段流程：`Survey/Critic -> Pilot Code/Adviser -> Experiment Code/Adviser -> Paper Writer/Reviewer -> Reflector/Curator`
- 双循环结构：阶段内双 Agent 内循环，主 Agent 控制阶段间外循环
- 五个用户 gate：调研、pilot、小规模验证后 full experiment、论文、reflection/evolution
- 人类拒绝 gate 后可明确选择回退到哪个阶段，主 Agent 会给出建议回退阶段
- 运行时可视化：`.autoresearch/dashboard/`
- 运行时注册表：job、GPU、backend、sentinel 占位文件
- 质量门控脚本：`scripts/quality_gate.py`
- 进度生成脚本：`scripts/generate_dashboard.py`
- 固定角色 prompt 模板 + 主 Agent 动态注入
- 标准化工作区、模板、状态文件、handoff 校验

## 目录结构

初始化后会生成以下目录：

```
my-project/
├── .autoresearch/           # 系统目录（隐藏）
│   ├── state/               # 状态文件
│   │   └── research-state.yaml
│   ├── config/              # 配置文件
│   │   └── orchestrator-config.yaml
│   ├── dashboard/           # 运行时面板
│   ├── runtime/             # 运行时注册表（job、GPU、backend）
│   ├── reference-papers/    # 参考文献
│   ├── templates/           # 模板缓存
│   └── archive/             # 归档
├── agents/                  # Agent 工作目录（按角色组织）
│   ├── survey/
│   ├── critic/
│   ├── coder/
│   ├── adviser/
│   ├── writer/
│   ├── reviewer/
│   ├── reflector/
│   └── curator/
├── paper/                   # 论文相关
│   └── reviewer-report.md
├── code/                    # 代码相关
│   └── configs/
│       └── pilot-experiment-plan.md
├── docs/                    # 文档相关
│   ├── reports/
│   │   ├── survey/
│   │   │   └── research-readiness-report.md
│   │   ├── pilot/
│   │   │   └── pilot-validation-report.md
│   │   └── experiments/
│   │       └── evidence-package-index.md
│   └── ...
└── AGENTS.md 或 CLAUDE.md    # Agent 配置文件
```

## 整体流程

### 阶段名称

项目支持语义化阶段名称：
- `survey` — 文献调研阶段
- `pilot` — Pilot 验证阶段
- `experiments` — 完整实验阶段
- `paper` — 论文写作阶段
- `reflection` — 反思与演化阶段

> **向后兼容**：旧的编号名称（`01-survey`、`02-pilot-analysis`等）仍然支持，但推荐使用新的语义化名称。

### 阶段 1：Survey <-> Critic

- Survey 扩展近 5 年工作、补必要经典工作、拆 atomic academic definitions。
- Critic 对 novelty、feasibility、theory risk、experimental verifiability、resource cost、negative-result risk 做逐项审查。
- 产出 `docs/reports/survey/research-readiness-report.md` 和 `docs/reports/survey/phase-scorecard.md`。
- 用户 Gate 1 决定是否进入 pilot。

### 阶段 2：Pilot Code <-> Pilot Adviser

- Code 先做问题分析和低成本验证设计。
- Adviser 判断 pilot 是否足以支持继续、返工或 pivot。
- 产出 `docs/reports/pilot/pilot-validation-report.md` 和 `docs/reports/pilot/phase-scorecard.md`。
- 用户 Gate 2 决定是否进入 full experiment。

### 阶段 3：Experiment Code <-> Experiment Adviser

- Code 固化 full experiment matrix、run registry、checkpoint index、results summary。
- Adviser 只在证据足够时才建议进入论文阶段。
- 产出 `docs/reports/experiments/evidence-package-index.md` 和 `docs/reports/experiments/phase-scorecard.md`。
- 用户 Gate 3 决定是否进入论文阶段。

### 阶段 4：Paper Writer <-> Reviewer & Editor

- Writer 只能基于已批准证据写稿。
- Reviewer & Editor 按顶刊顶会可投稿标准给出结构化评审。
- 双方循环直到 `paper/final-acceptance-report.md` 达到投稿级标准。
- 用户 Gate 4 决定是否进入 reflection 或直接交付。

### 阶段 5：Reflector <-> Curator

- Reflector 提炼 lessons learned、overlay draft、runtime 改进建议。
- Curator 判断哪些建议可复用、哪些只能保留为草案。
- 用户 Gate 5 决定是否激活 overlay 或仅保留记录。

## 安装

### 方式一：从 GitHub Marketplace 安装（推荐）

```bash
# 1. 添加 marketplace
/plugin marketplace add jacazjx/AI-Research-Orchestrator

# 2. 安装插件
/plugin install autoresearch@autoresearch
```

安装后重启 Claude Code 即可使用。

### 方式二：配置 settings.json

在 `~/.claude/settings.json` 中添加：

```json
{
  "extraKnownMarketplaces": {
    "autoresearch": {
      "source": {
        "source": "github",
        "repo": "jacazjx/AI-Research-Orchestrator"
      }
    }
  },
  "enabledPlugins": {
    "autoresearch@autoresearch": true
  }
}
```

### 方式三：本地开发安装

```bash
# 指定本地目录
cc --plugin-dir /path/to/AI-Research-Orchestrator
```

### 安装到 Codex

```bash
cp -a ai-research-orchestrator "$CODEX_HOME/skills/ai-research-orchestrator"
```

安装后重启 Codex。

## 快速开始

### 1. 初始化项目

```bash
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --topic "Your research idea" \
  --client-type auto
```

### 2. 重新展开模板

```bash
python3 scripts/materialize_templates.py --project-root /abs/path/to/my-project
```

### 3. 渲染一个角色 prompt

```bash
python3 scripts/render_agent_prompt.py \
  --project-root /abs/path/to/my-project \
  --role survey \
  --task-summary "Expand the idea into atomic academic definitions and recent literature" \
  --current-objective "Prepare the first survey round before critic review"
```

### 4. 校验阶段切换

```bash
python3 scripts/validate_handoff.py \
  --project-root /abs/path/to/my-project \
  --target survey-to-pilot
```

### 5. 生成进度面板

```bash
python3 scripts/generate_dashboard.py --project-root /abs/path/to/my-project
```

### 6. 执行质量门控

```bash
python3 scripts/quality_gate.py \
  --project-root /abs/path/to/my-project \
  --phase survey
```

## 关键脚本

- `scripts/init_research_project.py`：初始化五阶段工作区
- `scripts/materialize_templates.py`：补齐缺失模板
- `scripts/render_agent_prompt.py`：基于固定模板渲染角色 prompt
- `scripts/validate_handoff.py`：校验阶段切换和 loop 升级
- `scripts/quality_gate.py`：输出 `advance / revise / pivot / escalate_to_user`
- `scripts/generate_dashboard.py`：生成 `.autoresearch/dashboard/` 和基础 runtime registry
- `.autoresearch/config/orchestrator-config.yaml`：loop limit、sentinel 阈值、backend 开关、GPU 发现策略
- `scripts/run_stage_loop.py`：推进阶段内循环并在满足条件时转移阶段
- `scripts/pivot_manager.py`：提出和审核 pivot
- `scripts/schedule_jobs.py`：登记任务并分配 backend/GPU 元数据
- `scripts/run_remote_job.py`：执行本地或 SSH 任务并落盘日志
- `scripts/sentinel.py`：检测 stale job、缺失工件和运行时异常
- `scripts/recover_stage.py`：执行 retry、resume 和 dashboard 恢复
- `scripts/apply_overlay.py`：在 Gate 5 批准后激活 overlay
- `scripts/run_citation_audit.py`：调用 `latex-citation-curator` 做论文引用真实性审查

## 参考文档

- `SKILL.md`：运行时说明
- `references/workflow-protocol.md`：五阶段流程
- `references/gate-rubrics.md`：门控规则
- `references/system-architecture.md`：双循环与状态模型
- `references/pivot-policy.md`：PIVOT 规则
- `references/progress-visualization.md`：进度可视化约定
- `references/remote-execution.md`：远程执行和 job/GPU registry
- `references/self-healing.md`：sentinel 和恢复机制
- `references/self-evolution.md`：overlay 和受控演化
- `references/phase-execution-details.md`：每阶段内的具体推进步骤
- `references/citation-authenticity.md`：paper phase 的引用真实性规则

## 验证

```bash
python3 -m unittest discover -s tests
python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/ai-research-orchestrator
```
