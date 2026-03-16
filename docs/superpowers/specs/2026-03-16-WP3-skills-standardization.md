# Work Package 3: Skills 标准化

**目标**: 统一所有技能文件的格式，补全缺失字段，解决触发短语冲突

**预估工作量**: 大 (2-3小时)

---

## 修改文件清单

41 个 `skills/*/SKILL.md` 文件

---

## 具体任务

### 3.1 补全缺失的 `agent` 字段

以下 13 个技能文件需要添加 `agent` 字段：

| 文件 | 建议的 agent 值 | 说明 |
|------|----------------|------|
| `skills/orchestrator/SKILL.md` | `orchestrator` | 主编排器 |
| `skills/idea-discovery/SKILL.md` | `orchestrator` | 流水线编排 |
| `skills/idea-creator/SKILL.md` | `survey` | 子技能 |
| `skills/paper-writing/SKILL.md` | `orchestrator` | 流水线编排 |
| `skills/paper-plan/SKILL.md` | `writer` | 子技能 |
| `skills/paper-figure/SKILL.md` | `writer` | 子技能 |
| `skills/paper-compile/SKILL.md` | `writer` | 子技能 |
| `skills/paper-write/SKILL.md` | `writer` | 子技能 |
| `skills/research-pipeline/SKILL.md` | `orchestrator` | 流水线编排 |
| `skills/research-review/SKILL.md` | `critic` | 子技能 |
| `skills/monitor-experiment/SKILL.md` | `code` | 子技能 |
| `skills/auto-review-loop/SKILL.md` | `orchestrator` | 流水线编排 |
| `skills/auto-paper-improvement-loop/SKILL.md` | `orchestrator` | 流水线编排 |

**对于工具类技能** (无明确 agent):
- `skills/feishu-notify/SKILL.md` - 不需要 agent 字段
- `skills/gitmem/SKILL.md` - 不需要 agent 字段
- `skills/latex-citation-curator/SKILL.md` - 不需要 agent 字段

---

### 3.2 统一 frontmatter 字段顺序

**标准顺序**:
```yaml
---
name: <skill-name>
agent: <agent-name>  # 可选，流水线/工具类不需要
description: "<描述>"
argument-hint: <hint>  # 可选
allowed-tools:  # 可选
  - tool1
  - tool2
---
```

---

### 3.3 解决触发短语冲突

#### 冲突 1: "写论文" 同时匹配 `paper-write` 和 `paper-writing`

**解决方案**: 重命名技能并调整触发短语

| 原技能名 | 新技能名 | 触发短语调整 |
|---------|---------|-------------|
| `paper-write` | `paper-write` (保持) | "write paper section", "生成论文章节" |
| `paper-writing` | `paper-pipeline` | "write paper", "论文写作全流程", "写论文" |

**修改文件**:
- `skills/paper-writing/SKILL.md` → 重命名目录为 `skills/paper-pipeline/`
- 更新 `name` 字段为 `paper-pipeline`
- 调整触发短语

#### 冲突 2: `idea-creator` vs `idea-discovery`

**解决方案**: 明确区分触发短语

| 技能 | 定位 | 触发短语 |
|------|------|---------|
| `idea-creator` | 单步技能 | "create ideas", "生成想法" |
| `idea-discovery` | 流水线 | "discover ideas", "想法发现流程", "idea discovery" |

---

### 3.4 补全缺失的 Key Rules 部分

以下 4 个技能文件需要添加 `## Key Rules` 部分：

| 文件 | 建议的 Key Rules |
|------|-----------------|
| `skills/idea-creator/SKILL.md` | 1. 生成 8-12 个想法 2. 按 novelty/feasibility 筛选 3. 输出 top 3 |
| `skills/monitor-experiment/SKILL.md` | 1. 检查运行状态 2. 报告资源使用 3. 标记异常 |
| `skills/paper-compile/SKILL.md` | 1. 检查 LaTeX 语法 2. 编译 PDF 3. 报告错误 |
| `skills/research-review/SKILL.md` | 1. 验证引用真实性 2. 检查方法论完整性 3. 评分 |

---

### 3.5 统一 "Key Rules" vs "Hard Rules" 命名

**文件**: `skills/latex-citation-curator/SKILL.md`

将 `## Hard Rules` 改为 `## Key Rules` 以保持一致性。

---

### 3.6 补全缺失的 Output 部分

以下 4 个技能文件需要添加 `## Output` 部分：

| 文件 | 建议的 Output |
|------|--------------|
| `skills/idea-creator/SKILL.md` | `docs/reports/survey/idea-candidates.md` |
| `skills/monitor-experiment/SKILL.md` | 控制台输出 + 状态更新 |
| `skills/novelty-check/SKILL.md` | `docs/reports/survey/novelty-report.md` |
| `skills/research-review/SKILL.md` | 审阅意见 |

---

### 3.7 更新 orchestrator/SKILL.md 中的技能统计

**文件**: `skills/orchestrator/SKILL.md`

当前第 217 行声明 "40 skills"，实际有 41 个。

需要：
1. 更新技能数量统计
2. 确保 Primary/Audit/Supporting 分类与实际目录一致
3. 更新 `paper-writing` → `paper-pipeline` 的引用

---

## 验收标准

- [ ] 所有 41 个 SKILL.md 文件格式一致
- [ ] 需要的 `agent` 字段已补全
- [ ] 触发短语无冲突
- [ ] 所有技能有 `## Key Rules` 部分
- [ ] 所有技能有 `## Output` 部分
- [ ] orchestrator/SKILL.md 统计准确
- [ ] 目录重命名完成 (`paper-writing` → `paper-pipeline`)

---

## 注意事项

- 重命名目录后需要更新所有引用该技能的地方
- 触发短语变更需要同步更新 commands/ 中的定义
- 此工作包与 WP-2 (Commands) 有逻辑关联但无文件冲突