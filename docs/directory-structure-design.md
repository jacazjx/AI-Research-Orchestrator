# AI-Research-Orchestrator 目录结构设计

**版本**: 2.0.0
**日期**: 2026-03-15
**状态**: 设计完成

---

## 1. 设计原则

### 1.1 与 Superpowers 兼容

- 每个 skill 是独立目录，包含 `SKILL.md`
- `SKILL.md` 使用 YAML frontmatter
- 命令与 skills 分离
- 支持跨平台（Claude Code, Cursor, Codex）

### 1.2 保持向后兼容

- 现有 `scripts/` 目录保持不变
- 现有 17 个子 skills 保持不变
- 新增命令目录不影响现有功能

---

## 2. 新目录结构

```
AI-Research-Orchestrator/
├── SKILL.md                     # 主 skill 定义
│
├── commands/                    # 用户命令（新增）
│   ├── README.md
│   ├── init-research/
│   │   └── SKILL.md
│   ├── run-survey/
│   │   └── SKILL.md
│   ├── run-pilot/
│   │   └── SKILL.md
│   ├── run-experiments/
│   │   └── SKILL.md
│   ├── write-paper/
│   │   └── SKILL.md
│   └── reflect/
│       └── SKILL.md
│
├── skills/                      # 子 skills（现有，保持不变）
│   ├── idea-discovery/
│   │   └── SKILL.md
│   ├── research-lit/
│   │   └── SKILL.md
│   ├── idea-creator/
│   │   └── SKILL.md
│   ├── novelty-check/
│   │   └── SKILL.md
│   ├── research-review/
│   │   └── SKILL.md
│   ├── auto-review-loop/
│   │   └── SKILL.md
│   ├── paper-pipeline/
│   │   └── SKILL.md
│   ├── paper-plan/
│   │   └── SKILL.md
│   ├── paper-figure/
│   │   └── SKILL.md
│   ├── paper-write/
│   │   └── SKILL.md
│   ├── paper-compile/
│   │   └── SKILL.md
│   ├── run-experiment/
│   │   └── SKILL.md
│   ├── monitor-experiment/
│   │   └── SKILL.md
│   ├── analyze-results/
│   │   └── SKILL.md
│   ├── research-pipeline/
│   │   └── SKILL.md
│   ├── feishu-notify/
│   │   └── SKILL.md
│   └── auto-paper-improvement-loop/
│       └── SKILL.md
│
├── scripts/                     # Python 脚本（现有，保持不变）
│   ├── orchestrator_common.py
│   ├── init_research_project.py
│   ├── render_agent_prompt.py
│   ├── quality_gate.py
│   ├── validate_handoff.py
│   ├── generate_dashboard.py
│   ├── generate_statusline.py
│   ├── run_citation_audit.py
│   ├── pivot_manager.py
│   ├── sentinel.py
│   ├── recover_stage.py
│   ├── apply_overlay.py
│   ├── materialize_templates.py
│   ├── verify_system.py
│   ├── analyze_project.py
│   ├── migrate_project.py
│   ├── migrate_structure.py
│   ├── phase_handoff.py
│   ├── run_stage_loop.py
│   ├── run_remote_job.py
│   ├── schedule_jobs.py
│   ├── show_version.py
│   ├── audit_system.py
│   └── exceptions.py
│
├── agents/                      # Agent 配置（现有）
│   ├── codex-mcp.yaml
│   └── openai.yaml
│
├── assets/                      # 模板和资源（现有）
│   ├── prompts/
│   │   ├── orchestrator.md.tmpl
│   │   ├── survey.md.tmpl
│   │   ├── critic.md.tmpl
│   │   ├── code.md.tmpl
│   │   ├── adviser.md.tmpl
│   │   ├── paper-writer.md.tmpl
│   │   ├── reviewer-editor.md.tmpl
│   │   ├── reflector.md.tmpl
│   │   ├── curator.md.tmpl
│   │   ├── system-auditor.md.tmpl
│   │   ├── project-takeover.md.tmpl
│   │   └── survey.md.tmpl
│   └── templates/
│       └── .autoresearch/
│           └── [项目模板]
│
├── references/                  # 参考文档（现有）
│   ├── workflow-protocol.md
│   ├── system-architecture.md
│   ├── gate-rubrics.md
│   ├── orchestrator-protocol.md
│   ├── pivot-policy.md
│   ├── progress-visualization.md
│   ├── remote-execution.md
│   ├── self-healing.md
│   ├── self-evolution.md
│   ├── phase-execution-details.md
│   ├── citation-authenticity.md
│   ├── literature-verification.md
│   ├── experiment-integrity.md
│   ├── paper-quality-assurance.md
│   ├── ai-researcher-agent-mapping.md
│   ├── prompt-customization.md
│   └── role-protocols.md
│
├── docs/                        # 文档（现有）
│   ├── superpowers/
│   │   ├── plans/
│   │   ├── specs/
│   │   └── analysis/
│   └── reports/
│
├── tests/                       # 测试（现有）
│   └── test_*.py
│
├── .github/                     # CI/CD（现有）
│   └── workflows/
│
├── CLAUDE.md                    # Claude Code 配置
├── pyproject.toml               # Python 项目配置
├── requirements.txt             # 依赖
├── README.md                    # 项目说明
├── CHANGELOG.md                 # 变更日志
└── SKILL.md                     # 主 skill 定义
```

---

## 3. 目录职责

### 3.1 commands/ 目录

**用途**: 用户入口命令，映射到五阶段流程

| 命令 | 阶段 | 调用的 skill/script |
|------|------|---------------------|
| `/init-research` | 初始化 | `scripts/init_research_project.py` |
| `/run-survey` | Phase 1 | `scripts/run_stage_loop.py --phase survey` |
| `/run-pilot` | Phase 2 | `scripts/run_stage_loop.py --phase pilot` |
| `/run-experiments` | Phase 3 | `scripts/run_stage_loop.py --phase experiments` |
| `/write-paper` | Phase 4 | `scripts/run_stage_loop.py --phase paper` |
| `/reflect` | Phase 5 | `scripts/run_stage_loop.py --phase reflection` |

### 3.2 skills/ 目录

**用途**: 可复用的子功能模块

现有 17 个 skills 分为三类：

**Workflow Skills（工作流）**:
- `idea-discovery` - 创意发现流程
- `research-pipeline` - 端到端研究流程
- `auto-review-loop` - 自主评审循环

**Task Skills（任务）**:
- `research-lit` - 文献调研
- `idea-creator` - 创意生成
- `novelty-check` - 新颖性验证
- `research-review` - 研究评审
- `run-experiment` - 运行实验
- `monitor-experiment` - 监控实验
- `analyze-results` - 分析结果

**Paper Skills（论文）**:
- `paper-pipeline` - 论文写作流程
- `paper-plan` - 论文规划
- `paper-figure` - 图表生成
- `paper-write` - 论文撰写
- `paper-compile` - 论文编译
- `auto-paper-improvement-loop` - 论文自动改进

**Utility Skills（工具）**:
- `feishu-notify` - 飞书通知

### 3.3 scripts/ 目录

**用途**: 核心逻辑实现，纯 Python 脚本

保持现有 24 个脚本不变。

### 3.4 agents/ 目录

**用途**: Agent 配置文件

现有文件：
- `codex-mcp.yaml` - Codex MCP 配置
- `openai.yaml` - OpenAI 配置

可扩展为：
```
agents/
├── codex-mcp.yaml
├── openai.yaml
├── cursor.yaml          # 未来：Cursor 支持
└── gemini.yaml          # 未来：Gemini 支持
```

---

## 4. 命令与 Skill 关系

### 4.1 调用关系

```
用户输入: /run-survey
    ↓
commands/run-survey/SKILL.md
    ↓
scripts/run_stage_loop.py --phase survey
    ↓
skills/research-lit/ (文献调研子任务)
    ↓
输出: docs/reports/survey/
```

### 4.2 命令 vs Skill

| 类型 | 触发方式 | 作用 |
|------|---------|------|
| Command | 用户显式调用 | 流程入口，协调多个脚本 |
| Skill | 自动触发或子调用 | 可复用的功能模块 |

---

## 5. 迁移路径

### 5.1 当前状态

- ✅ `commands/` 目录已创建，6 个命令已实现
- ✅ `skills/` 目录已有 17 个子 skills
- ✅ `scripts/` 目录有 24 个脚本
- ✅ 向后兼容现有功能

### 5.2 未来扩展

**Phase 1: 跨平台支持**
```
.cursor/
└── commands/          # Cursor 命令配置

.opencode/
└── commands/          # OpenCode 命令配置
```

**Phase 2: Hooks 支持**
```
hooks/
├── pre-phase/         # 阶段前钩子
├── post-phase/        # 阶段后钩子
└── on-error/          # 错误处理钩子
```

---

## 6. 文件数量统计

| 目录 | 当前文件数 | 说明 |
|------|-----------|------|
| commands/ | 7 (6 SKILL.md + README) | 新增 |
| skills/ | 17 | 保持不变 |
| scripts/ | 24 | 保持不变 |
| agents/ | 2 | 保持不变 |
| assets/prompts/ | 12 | 保持不变 |
| assets/templates/ | ~30 | 保持不变 |
| references/ | 17 | 保持不变 |
| tests/ | ~25 | 保持不变 |

**总计**: ~134 个文件

---

## 7. 验收标准

- [x] `commands/` 目录存在
- [x] 6 个命令定义完整
- [x] 每个 command 有 SKILL.md
- [x] SKILL.md 有 YAML frontmatter
- [x] 现有 skills/ 不受影响
- [x] 现有 scripts/ 不受影响
- [x] 测试全部通过

---

## 8. 参考文档

- [Superpowers 项目结构](https://github.com/obra/superpowers)
- `docs/superpowers/analysis/structure-gap-analysis.md` - 差距分析报告
- `docs/superpowers/specs/2026-03-14-folder-restructure-design.md` - 文件夹重构设计