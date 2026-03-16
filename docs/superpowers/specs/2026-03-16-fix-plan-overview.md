# AI-Research-Orchestrator 项目修复计划

**创建日期**: 2026-03-16

**修复范围**: 全面修复 36 个问题（6 CRITICAL + 10 HIGH + 12 MEDIUM + 8 LOW）

**执行策略**: 5 个并行 session，每个 session 使用独立 worktree

---

## 工作包总览

| WP | 名称 | 工作量 | 文件数 | 冲突风险 | 规格文件 |
|----|------|--------|--------|---------|---------|
| WP-1 | 项目配置修复 | 小 (30分钟) | 4 | 低 | `2026-03-16-WP1-project-config.md` |
| WP-2 | Commands 重构 | 中 (1-2小时) | 7 | 低 | `2026-03-16-WP2-commands-refactor.md` |
| WP-3 | Skills 标准化 | 大 (2-3小时) | 41 | 低 | `2026-03-16-WP3-skills-standardization.md` |
| WP-4 | Python 脚本修复 | 大 (2-3小时) | 24 | 低 | `2026-03-16-WP4-scripts-fix.md` |
| WP-5 | 文档更新 | 中 (1-2小时) | 6 | 低 | `2026-03-16-WP5-documentation-update.md` |

---

## 文件修改矩阵

显示每个工作包修改的文件，便于识别潜在冲突：

```
文件/目录                      WP-1  WP-2  WP-3  WP-4  WP-5
─────────────────────────────────────────────────────────────
pyproject.toml                  ✓
requirements.txt                ✓
scripts/__init__.py             ✓   (新建)
.gitignore                      ✓
scripts/run_stage_loop.py                   ✓
scripts/pivot_manager.py                   ✓
scripts/orchestrator_common.py              ✓
scripts/run_remote_job.py                  ✓
scripts/sentinel.py                        ✓
scripts/quality_gate.py                    ✓
scripts/generate_statusline.py             ✓
scripts/*.py (其他)                         ✓
commands/ (重构)                      ✓
skills/orchestrator/SKILL.md                 ✓
skills/paper-writing/ → paper-pipeline/      ✓   (重命名)
skills/*/SKILL.md (41个)                     ✓
docs/directory-structure-design.md                        ✓
README.md                                                 ✓
README.zh-CN.md                                           ✓
CHANGELOG.md                                              ✓
```

**结论**: 文件重叠极少，可以安全并行。

---

## 执行顺序建议

虽然可以完全并行，但建议以下顺序以减少合并时的调整：

```
┌─────────────────────────────────────────────────────────────┐
│                    并行执行 (Phase 1)                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │  WP-1   │  │  WP-2   │  │  WP-3   │  │  WP-4   │        │
│  │ 项目配置 │  │Commands │  │ Skills  │  │ 脚本   │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
└───────┼────────────┼────────────┼────────────┼──────────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│                    合并到主线 (我来处理)                      │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                    后续执行 (Phase 2)                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                       WP-5                           │   │
│  │                     文档更新                          │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**建议**: WP-5 在 WP-2 和 WP-3 完成后执行，确保文档与实现一致。

---

## Session 指令模板

### Session 1 (WP-1: 项目配置)

```
阅读 docs/superpowers/specs/2026-03-16-WP1-project-config.md，
完成所有任务并通过验收标准。
修改完成后运行 python -m pytest tests/ -v 确保测试通过。
```

### Session 2 (WP-2: Commands 重构)

```
阅读 docs/superpowers/specs/2026-03-16-WP2-commands-refactor.md，
完成所有任务并通过验收标准。
主要工作：将 commands/ 从扁平文件重构为子目录结构。
```

### Session 3 (WP-3: Skills 标准化)

```
阅读 docs/superpowers/specs/2026-03-16-WP3-skills-standardization.md，
完成所有任务并通过验收标准。
主要工作：补全 agent 字段、解决触发短语冲突、重命名 paper-writing 为 paper-pipeline。
```

### Session 4 (WP-4: Python 脚本修复)

```
阅读 docs/superpowers/specs/2026-03-16-WP4-scripts-fix.md，
完成所有任务并通过验收标准。
主要工作：修复 KeyError 风险、统一阶段名称、提取公共函数到 orchestrator_common.py。
```

### Session 5 (WP-5: 文档更新)

```
等待 WP-2 和 WP-3 完成后执行。
阅读 docs/superpowers/specs/2026-03-16-WP5-documentation-update.md，
完成所有任务并通过验收标准。
主要工作：同步文档与实现、更新统计数字、记录变更日志。
```

---

## 合并策略

作为 Reviewer，我将按以下顺序合并：

1. **WP-1** (项目配置) - 基础配置，先合并
2. **WP-4** (脚本修复) - 核心逻辑修复
3. **WP-2** (Commands) - 结构重构
4. **WP-3** (Skills) - 标准化
5. **WP-5** (文档) - 最后更新文档

每个 WP 合并前我会：
- 检查测试是否通过
- 验证验收标准是否达成
- 处理任何冲突（预计极少）

---

## 验收检查清单

全部工作包完成后，我会验证：

- [ ] `pip install -e .` 成功
- [ ] `python -m pytest tests/ -v` 全部通过
- [ ] `python -m mypy scripts/ --ignore-missing-imports` 无错误
- [ ] 6 个命令目录结构正确
- [ ] 41 个技能格式一致
- [ ] 无触发短语冲突
- [ ] 文档统计数字正确
- [ ] CHANGELOG.md 已更新

---

## 规格文件列表

所有规格文件位于 `docs/superpowers/specs/`:

- `2026-03-16-WP1-project-config.md`
- `2026-03-16-WP2-commands-refactor.md`
- `2026-03-16-WP3-skills-standardization.md`
- `2026-03-16-WP4-scripts-fix.md`
- `2026-03-16-WP5-documentation-update.md`