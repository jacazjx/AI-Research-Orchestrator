# Work Package 5: 文档更新

**目标**: 同步文档与实际实现，修复不一致的统计和描述

**预估工作量**: 中 (1-2小时)

---

## 修改文件清单

| 文件 | 修改类型 |
|------|---------|
| `docs/directory-structure-design.md` | 修复统计、移除重复 |
| `docs/superpowers/specs/2026-03-15-commands-directory-design.md` | 同步实际结构 |
| `references/ai-researcher-agent-mapping.md` | 检查一致性 |
| `README.md` | 更新技能统计 |
| `README.zh-CN.md` | 更新技能统计 |
| `CHANGELOG.md` | 记录本次修复 |

---

## 具体任务

### 5.1 修复 directory-structure-design.md

**文件**: `docs/directory-structure-design.md`

#### 5.1.1 移除重复条目

**位置**: 第 116 行和第 126 行

重复列出了 `survey.md.tmpl`，删除其中一个。

#### 5.1.2 更新技能数量统计

**位置**: 第 299-312 行

**当前**: 声明 17 个 skills

**修复**: 更新为实际数量 (41 个) 或分类说明：

```markdown
### Skills Directory (41 skills)

- Primary Skills: 16
- Audit Skills: 12
- Supporting Skills: 12
- Orchestrator: 1
```

#### 5.1.3 更新 Commands 结构描述

**位置**: 第 35-46 行

**当前**: 描述为子目录结构 `commands/<name>/COMMAND.md`

**修复**: 与 WP-2 完成后的结构保持一致（子目录结构）

---

### 5.2 更新 commands-directory-design.md

**文件**: `docs/superpowers/specs/2026-03-15-commands-directory-design.md`

确保设计文档与 WP-2 实施后的结构一致：

- 目录结构示例
- 必需字段定义
- 参数定义格式
- 触发短语列表

---

### 5.3 更新 README.md

**文件**: `README.md`

#### 5.3.1 更新技能数量

搜索 "17 skills" 或类似描述，更新为 41 个。

#### 5.3.2 更新技能列表

如果 README 中列出了具体技能名称，确保与 `skills/` 目录实际内容一致。

特别注意 `paper-writing` 重命名为 `paper-pipeline` 后的更新。

---

### 5.4 更新 README.zh-CN.md

**文件**: `README.zh-CN.md`

同步 README.md 的所有更新。

---

### 5.5 更新 CHANGELOG.md

**文件**: `CHANGELOG.md`

添加本次修复的变更记录：

```markdown
## [Unreleased]

### Fixed

- Project configuration: added `scripts/__init__.py`, fixed pyproject.toml resource paths
- Commands: restructured to subdirectories, added required frontmatter fields
- Skills: standardized format, resolved trigger phrase conflicts, renamed `paper-writing` to `paper-pipeline`
- Scripts: fixed KeyError risk in `_completion_percent()`, unified phase names, extracted common functions
- Documentation: synced skill counts, removed duplicate entries, updated structure descriptions

### Changed

- `paper-writing` skill renamed to `paper-pipeline` to avoid confusion with `paper-write`
- Phase names unified to semantic names (survey, pilot, experiments, paper, reflection)
- Commands directory restructured from flat files to subdirectories with `COMMAND.md`
```

---

### 5.6 检查 references/ 目录一致性

检查以下文件与实际实现的一致性：

| 文件 | 检查内容 |
|------|---------|
| `references/ai-researcher-agent-mapping.md` | 代理与技能的映射关系 |
| `references/workflow-protocol.md` | 阶段名称是否使用语义名称 |
| `references/gate-rubrics.md` | 阶段名称是否使用语义名称 |
| `references/phase-execution-details.md` | 阶段名称是否使用语义名称 |

如果发现 legacy 阶段名称，更新为语义名称。

---

## 验收标准

- [ ] `directory-structure-design.md` 无重复条目
- [ ] `directory-structure-design.md` 技能数量正确
- [ ] `commands-directory-design.md` 与实际结构一致
- [ ] README.md 和 README.zh-CN.md 技能数量正确
- [ ] CHANGELOG.md 记录了本次修复
- [ ] references/ 文档使用语义阶段名称

---

## 注意事项

- 此工作包应在 WP-2 和 WP-3 完成后进行，以确保文档与实现一致
- 如果发现其他文档不一致，一并进行修复
- 中英文 README 需要保持同步