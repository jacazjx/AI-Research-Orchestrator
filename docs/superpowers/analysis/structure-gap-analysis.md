# Skill 结构差距分析报告

**对比项目**: [superpowers](https://github.com/obra/superpowers) by obra
**分析日期**: 2026-03-15
**分析范围**: AI-Research-Orchestrator vs Superpowers 项目标准

---

## 1. 项目概述对比

### 1.1 Superpowers 项目

| 特性 | 描述 |
|------|------|
| 定位 | 跨平台编码代理工作流自动化 |
| 平台支持 | Claude Code, Cursor, Codex, OpenCode, Gemini CLI |
| Skills 数量 | 14 个核心 skills |
| 核心理念 | 测试先行、系统性优于临时方案、降低复杂度、证据重于声明 |

### 1.2 AI-Research-Orchestrator 项目

| 特性 | 描述 |
|------|------|
| 定位 | AI/ML 研究项目五阶段工作流管理 |
| 平台支持 | Claude Code (Codex MCP 集成) |
| Skills 数量 | 1 个主 skill + 17 个子 skills |
| 核心理念 | 双循环结构、显式门控、状态机驱动 |

---

## 2. 目录结构差异

### 2.1 Superpowers 目录结构

```
superpowers/
├── skills/                      # 14 个核心 skills
│   ├── brainstorming/
│   │   └── SKILL.md
│   ├── test-driven-development/
│   │   └── SKILL.md
│   ├── writing-plans/
│   │   └── SKILL.md
│   ├── writing-skills/
│   │   └── SKILL.md
│   └── ... (10 个更多)
├── agents/                      # 代理配置
├── commands/                    # 命令定义
├── hooks/                       # 钩子
├── docs/                        # 文档
├── tests/                       # 测试
├── .claude-plugin/              # Claude 插件配置
├── .codex/                      # Codex 配置
├── .cursor-plugin/              # Cursor 插件配置
├── GEMINI.md                    # Gemini 配置
└── gemini-extension.json        # Gemini 扩展
```

### 2.2 AI-Research-Orchestrator 目录结构

```
AI-Research-Orchestrator/
├── SKILL.md                     # 主 skill 定义
├── scripts/                     # 24 个 Python 脚本
│   ├── orchestrator_common.py
│   ├── init_research_project.py
│   └── ... (22 个更多)
├── skills/                      # 17 个子 skills
│   ├── idea-discovery/
│   │   └── SKILL.md
│   └── ... (16 个更多)
├── assets/
│   ├── prompts/                 # 12 个 prompt 模板
│   └── templates/               # 项目模板
├── references/                  # 参考文档 (17 个 .md)
├── agents/                      # Agent 配置 (OpenAI, Codex MCP)
└── docs/                        # 文档
```

### 2.3 关键差异

| 方面 | Superpowers | AI-Research-Orchestrator | 差距 |
|------|-------------|--------------------------|------|
| 跨平台配置 | ✅ 多平台 | ⚠️ 仅 Claude Code | **中** |
| scripts/ 目录 | ❌ 无 | ✅ 有（24 个脚本） | 优势 |
| templates/ 目录 | ❌ 无 | ✅ 有 | 优势 |
| hooks/ 目录 | ✅ 有 | ❌ 无 | **低** |
| commands/ 目录 | ✅ 有 | ❌ 无 | **中** |
| references/ 目录 | ❌ 无 | ✅ 有（17 个文档） | 优势 |

---

## 3. SKILL.md 格式差异

### 3.1 Superpowers SKILL.md 格式规范

#### Frontmatter 规范

```yaml
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms]
---
```

**规则:**
- 只有 `name` 和 `description` 两个字段
- 总字符数 ≤ 1024
- `name`: 仅字母、数字、连字符
- `description`: 第三人称，"Use when..." 格式，只写触发条件

#### 章节结构规范

```markdown
# Skill Name

## Overview
## When to Use
## Core Pattern (可选)
## Quick Reference
## Implementation
## Common Mistakes
## Real-World Impact (可选)
```

### 3.2 AI-Research-Orchestrator 主 SKILL.md 格式

#### 当前 Frontmatter

```yaml
---
name: ai-research-orchestrator
description: Initialize and run a gated five-phase AI research project from idea intake through pilot validation, full experiments, paper development, and reflection/evolution. Use when Codex needs to manage a research workspace around an IDEA plus seed references, coordinate sequential dual-agent phases such as Survey/Critic, Code/Adviser, Paper Writer/Reviewer, and Reflector/Curator, maintain machine-readable project state in `research-state.yaml`, generate runtime dashboards, and enforce explicit user approval gates between every major phase.
---
```

#### 当前章节结构

```markdown
# AI Research Orchestrator

## Overview
## Directory Structure
## Phase Names
## Quick Start
## Literature Search (IMPORTANT)
## ARIS Integration
## Workflow
## Hard Rules
## Resource Map
## Cross-Session Feedback Channel
```

### 3.3 格式差异对比

| 方面 | Superpowers 标准 | 当前状态 | 差距 |
|------|-----------------|---------|------|
| Frontmatter 字段数 | 2 个 | 2 个 | ✅ |
| description 长度 | <500 字符 | ~800 字符 | **需精简** |
| 触发条件格式 | "Use when..." | ✅ 符合 | ✅ |
| `argument-hint` 字段 | ❌ 无此字段 | ✅ 有 | 扩展字段 |
| `allowed-tools` 字段 | ❌ 无此字段 | ✅ 有 | 扩展字段 |
| "When to Use" 章节 | ✅ 必需 | ⚠️ 隐含在 Overview | **需明确** |
| "Common Mistakes" 章节 | ✅ 推荐 | ❌ 无 | **需添加** |
| "Quick Reference" 章节 | ✅ 推荐 | ⚠️ 有 Quick Start | ✅ |

---

## 4. 触发条件定义缺失

### 4.1 Superpowers 触发条件示例

```yaml
# test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code

# writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code

# writing-skills
description: Use when creating a new skill, before writing the SKILL.md file
```

**特点:**
- 简洁明确（<500 字符）
- 描述问题场景而非功能
- 使用具体触发词

### 4.2 AI-Research-Orchestrator 主 SKILL.md 触发条件

当前描述包含了触发条件和功能描述的混合，**不够简洁**。

**建议改进:**

```yaml
description: Use when starting a new AI/ML research project, taking over an existing research codebase, or managing a research workflow with literature review, experiments, and paper writing. Triggers: "start research project", "帮我做一个研究", "research workflow", "五阶段研究流程", "take over project".
```

### 4.3 子 Skills 触发条件对比

AI-Research-Orchestrator 的子 skills **已经遵循良好实践**:

```yaml
# idea-discovery
description: "... Use when user says '找idea全流程', 'idea discovery pipeline', '从零开始找方向', or wants the complete idea exploration workflow."

# research-lit
description: "... Use when user says 'literature survey', '文献调研', 'find related work', or needs to map the research landscape."
```

---

## 5. 命令交互模式缺失

### 5.1 Superpowers 命令模式

Superpowers 通过 `commands/` 目录定义独立命令，与 skills 分离。

### 5.2 AI-Research-Orchestrator 命令模式

当前通过 Python 脚本提供命令:

```bash
python3 scripts/init_research_project.py --project-root /path --topic "idea"
python3 scripts/quality_gate.py --project-root /path --phase survey
python3 scripts/generate_dashboard.py --project-root /path
```

**差距:**
- ❌ 无 `commands/` 目录
- ⚠️ 命令与脚本耦合
- ⚠️ 无命令别名或快捷方式

**建议:**
```
commands/
├── init          # -> python3 scripts/init_research_project.py
├── gate          # -> python3 scripts/quality_gate.py
├── dashboard     # -> python3 scripts/generate_dashboard.py
└── handoff       # -> python3 scripts/validate_handoff.py
```

---

## 6. 硬性规则 (Hard Rules) 对比

### 6.1 Superpowers Iron Law 示例

```markdown
## The Iron Law
"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"

If you write code before the test, delete it and start over.

## Red Flags - STOP
Indicators like "Code before test," "Test passes immediately," or rationalizing "just this once" mean you must "Delete code. Start over with TDD."
```

**特点:**
- 强硬语气
- 明确停止条件
- 无例外

### 6.2 AI-Research-Orchestrator Hard Rules

```markdown
## Hard Rules

- Keep every phase as a two-agent loop under the user-facing orchestrator.
- Do NOT spawn explore agents or other helper agents.
- Do NOT use websearch for literature.
- Do not claim plagiarism checks, AI-detection checks, or formal proof verification in v1.
- Do not fabricate experiments, citations, datasets, checkpoints, or reviewer conclusions.
- Do not pivot or advance phases without explicit human approval.
```

**评估:** ✅ 已有清晰的硬性规则，格式符合标准。

---

## 7. 检查清单 (Checklist) 对比

### 7.1 Superpowers Checklist 示例

```markdown
## Verification Checklist
- Every new function/method has a test.
- Watched each test fail before implementing.
- Wrote minimal code to pass.
- All tests pass with pristine output.
```

### 7.2 AI-Research-Orchestrator 检查清单

**当前状态:** ⚠️ 分散在多个文档中，未集中为 Checklist 格式。

**建议添加:**

```markdown
## Phase Gate Checklist

### Gate 1: Survey → Pilot
- [ ] research-readiness-report.md exists
- [ ] phase-scorecard.md score ≥ 3.5
- [ ] User approval recorded

### Gate 2: Pilot → Experiments
- [ ] pilot-validation-report.md exists
- [ ] Pilot experiment results validated
- [ ] User approval recorded

### Gate 3: Experiments → Paper
- [ ] evidence-package-index.md exists
- [ ] All experiments completed
- [ ] User approval recorded

### Gate 4: Paper → Reflection
- [ ] final-acceptance-report.md exists
- [ ] Citation audit passed
- [ ] User approval recorded

### Gate 5: Reflection → Close
- [ ] lessons-learned.md exists
- [ ] runtime-improvement-report.md exists
- [ ] User decision on overlay activation
```

---

## 8. 终端状态定义对比

### 8.1 Superpowers 终端状态

```markdown
## Final Rule
Production code exists only if a test exists and failed first. No exceptions.
```

### 8.2 AI-Research-Orchestrator 终端状态

**当前状态:** ⚠️ 未明确定义项目的终端状态。

**建议添加:**

```markdown
## Terminal States

A research project reaches terminal state when:
1. **Completed**: Gate 5 approved, overlay activated (optional)
2. **Abandoned**: User explicitly terminates, archive created
3. **Escalated**: Unresolvable blocker, human intervention required

State file `research-state.yaml` must record:
- `status: completed | abandoned | escalated`
- `final_phase: <phase_name>`
- `completion_date: <ISO date>`
```

---

## 9. 改进建议汇总

### 9.1 高优先级

| 改进项 | 说明 | 工作量 |
|--------|------|--------|
| 精简 description | <500 字符，聚焦触发条件 | 小 |
| 添加 "When to Use" 章节 | 明确使用场景 | 小 |
| 添加 "Common Mistakes" 章节 | 常见错误和修复 | 中 |
| 添加 Phase Gate Checklist | 集中的检查清单 | 中 |
| 定义终端状态 | completed/abandoned/escalated | 小 |

### 9.2 中优先级

| 改进项 | 说明 | 工作量 |
|--------|------|--------|
| 创建 commands/ 目录 | 命令别名 | 中 |
| 跨平台配置 | Cursor/Gemini 支持 | 大 |
| 添加 hooks/ 目录 | 自动化钩子 | 中 |

### 9.3 低优先级

| 改进项 | 说明 | 工作量 |
|--------|------|--------|
| SKILL.md 国际化 | 中英双语支持 | 中 |
| 子 skill 扩展 | 添加 scripts/templates | 中 |

---

## 10. 总结

AI-Research-Orchestrator 在以下方面**优于** Superpowers:
- 完整的 scripts/ 支持（24 个脚本）
- 丰富的 templates/ 和 prompts/
- 详细的 references/ 文档（17 个）
- 子 skills 的 argument-hint 和 allowed-tools

需要改进的方面:
- 主 SKILL.md description 过长
- 缺少集中的 Checklist
- 缺少终端状态定义
- 缺少 commands/ 目录

**整体评估:** AI-Research-Orchestrator 已具备良好的 skill 结构基础，主要差距在于格式精简和文档组织层面。