# Skill 结构差距分析报告

**日期**: 2026-03-15
**分析范围**: AI-Research-Orchestrator vs skills/ 子 skills 格式标准

---

## 1. 目录结构对比

### 当前状态

```
AI-Research-Orchestrator/
├── SKILL.md                    # 主 skill 定义
├── scripts/                    # 24 个 Python 脚本
├── skills/                     # 17 个子 skills
│   ├── idea-discovery/
│   │   └── SKILL.md
│   ├── research-lit/
│   │   └── SKILL.md
│   └── ... (15 个更多)
├── assets/
│   ├── prompts/               # 12 个 prompt 模板
│   └── templates/             # 项目模板
├── references/                 # 参考文档
└── agents/                     # Agent 配置
```

### 差距分析

| 方面 | 当前状态 | 差距 |
|------|---------|------|
| 主目录结构 | ✅ 已按新结构组织 | 无 |
| 子 skills 数量 | 17 个 | 数量充足 |
| scripts/ 组织 | 24 个脚本，无子目录 | 可考虑按功能分组 |

---

## 2. SKILL.md 格式差异

### 2.1 主 SKILL.md frontmatter

```yaml
# 当前格式
---
name: ai-research-orchestrator
description: Initialize and run a gated five-phase...
---
```

### 2.2 子 skill SKILL.md frontmatter (标准格式)

```yaml
# 标准格式
---
name: idea-discovery
description: "Workflow 1: Full idea discovery pipeline..."
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---
```

### 2.3 关键差异

| 字段 | 主 SKILL.md | 子 skills | 差距 |
|------|------------|-----------|------|
| `name` | ✅ 有 | ✅ 有 | 无 |
| `description` | ✅ 有（较长） | ✅ 有（简洁 + 触发条件） | **需优化** |
| `argument-hint` | ❌ 缺失 | ✅ 有 | **需添加** |
| `allowed-tools` | ❌ 缺失 | ✅ 有 | **需添加** |

---

## 3. 触发条件定义缺失

### 3.1 子 skill 触发条件示例

```yaml
# idea-discovery
description: "... Use when user says '找idea全流程', 'idea discovery pipeline', '从零开始找方向', or wants the complete idea exploration workflow."

# research-lit
description: "... Use when user says 'literature survey', '文献调研', 'find related work', or needs to map the research landscape."

# auto-review-loop
description: "... Use when user says 'auto review loop', 'review until it passes', or wants autonomous iterative improvement."
```

### 3.2 主 SKILL.md 触发条件

当前描述中隐含触发条件，但**未明确列出用户可能说的短语**：
- "start a research project"
- "帮我做一个研究项目"
- "research workflow"

**建议**: 添加明确的触发短语列表。

---

## 4. 命令交互模式缺失

### 4.1 子 skill 工具定义

每个子 skill 都定义了 `allowed-tools`：

```yaml
# idea-discovery
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply

# research-lit (更受限)
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch, Agent
```

### 4.2 主 SKILL.md 工具定义

**缺失** `allowed-tools` 字段。需要定义：
- Bash(*): 执行脚本
- Read/Write/Edit: 文件操作
- Grep/Glob: 搜索
- Agent/Skill: 调用子 skills
- MCP tools: Codex 集成

---

## 5. 子 skills 分析

### 5.1 当前子 skills 列表

| Skill | argument-hint | allowed-tools | 触发条件 |
|-------|---------------|---------------|----------|
| idea-discovery | `[research-direction]` | 12 tools | ✅ 明确 |
| research-lit | `[research-topic]` | 8 tools | ✅ 明确 |
| idea-creator | `[research-direction]` | 11 tools | ✅ 明确 |
| novelty-check | `[idea-description]` | 10 tools | ✅ 明确 |
| research-review | `[topic-or-results]` | 11 tools | ✅ 明确 |
| auto-review-loop | `[topic-or-scope]` | 11 tools | ✅ 明确 |
| paper-pipeline | `[narrative-report]` | 12 tools | ✅ 明确 |
| paper-plan | `[results-dir]` | 10 tools | ✅ 明确 |
| paper-figure | `[data-dir]` | 9 tools | ✅ 明确 |
| paper-write | `[paper-plan]` | 10 tools | ✅ 明确 |
| paper-compile | `[paper-dir]` | 9 tools | ✅ 明确 |
| run-experiment | `[command]` | 9 tools | ✅ 明确 |
| monitor-experiment | `[server]` | 8 tools | ✅ 明确 |
| analyze-results | `[results-dir]` | 9 tools | ✅ 明确 |
| research-pipeline | `[research-direction]` | 13 tools | ✅ 明确 |
| feishu-notify | `[message-type]` | 4 tools | ✅ 明确 |
| auto-paper-improvement-loop | `[paper-dir]` | 11 tools | ✅ 明确 |

### 5.2 子 skill 目录结构

每个子 skill 目前只有 `SKILL.md` 一个文件，**缺少**：
- `scripts/` - 支持脚本
- `templates/` - 特定模板
- `prompts/` - 特定 prompts

---

## 6. 改进建议

### 6.1 主 SKILL.md 改进

```yaml
---
name: ai-research-orchestrator
description: "Initialize and run a gated five-phase AI research project. Use when user says 'start research project', '帮我做一个研究', 'research workflow', '五阶段研究流程', or needs structured AI/ML research management."
argument-hint: [research-topic-or-idea]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---
```

### 6.2 建议新增字段

| 字段 | 用途 |
|------|------|
| `version` | Skill 版本号 |
| `requires` | 依赖的其他 skills |
| `produces` | 输出产物列表 |
| `phases` | 阶段定义（五阶段） |

### 6.3 目录结构优化建议

```
AI-Research-Orchestrator/
├── SKILL.md
├── scripts/
│   ├── core/              # 核心流程脚本
│   ├── runtime/           # 运行时脚本
│   └── utils/             # 工具脚本
├── skills/                # 子 skills
│   └── [skill-name]/
│       ├── SKILL.md
│       ├── scripts/       # 可选
│       └── templates/     # 可选
└── tests/
    ├── unit/
    └── integration/
```

---

## 7. 总结

| 类别 | 状态 | 优先级 |
|------|------|--------|
| 目录结构 | ✅ 已完成 | - |
| SKILL.md 格式 | ⚠️ 需补充字段 | **高** |
| 触发条件定义 | ⚠️ 需明确 | **高** |
| 命令交互模式 | ⚠️ 需添加 allowed-tools | **高** |
| 子 skill 扩展 | ❌ 只有 SKILL.md | **中** |
| scripts 分组 | ❌ 无分组 | **低** |

**核心差距**：主 SKILL.md 缺少 `argument-hint` 和 `allowed-tools` 字段，触发条件不够明确。