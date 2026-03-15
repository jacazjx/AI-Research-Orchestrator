# Scripts 目录分组结构设计

**版本**: 1.0.0
**日期**: 2026-03-15
**状态**: 设计阶段（暂不执行迁移）

---

## 1. 当前状态

### 1.1 现有结构

```
scripts/
├── analyze_project.py
├── apply_overlay.py
├── audit_system.py
├── exceptions.py
├── generate_dashboard.py
├── generate_statusline.py
├── init_research_project.py
├── materialize_templates.py
├── migrate_project.py
├── migrate_structure.py
├── orchestrator_common.py
├── phase_handoff.py
├── pivot_manager.py
├── quality_gate.py
├── recover_stage.py
├── render_agent_prompt.py
├── run_citation_audit.py
├── run_remote_job.py
├── run_stage_loop.py
├── schedule_jobs.py
├── sentinel.py
├── show_version.py
├── validate_handoff.py
└── verify_system.py
```

**问题**：
- 24 个脚本平铺，无组织
- 难以快速定位相关脚本
- 不利于新开发者理解

---

## 2. 新目录结构

```
scripts/
├── core/                      # 核心流程脚本 (8 个)
│   ├── __init__.py
│   ├── init_research_project.py
│   ├── run_stage_loop.py
│   ├── quality_gate.py
│   ├── validate_handoff.py
│   ├── phase_handoff.py
│   ├── pivot_manager.py
│   ├── recover_stage.py
│   └── apply_overlay.py
│
├── runtime/                   # 运行时脚本 (6 个)
│   ├── __init__.py
│   ├── generate_dashboard.py
│   ├── generate_statusline.py
│   ├── schedule_jobs.py
│   ├── run_remote_job.py
│   ├── sentinel.py
│   └── run_citation_audit.py
│
├── utils/                     # 工具脚本 (10 个)
│   ├── __init__.py
│   ├── orchestrator_common.py
│   ├── exceptions.py
│   ├── materialize_templates.py
│   ├── render_agent_prompt.py
│   ├── verify_system.py
│   ├── audit_system.py
│   ├── show_version.py
│   ├── analyze_project.py
│   ├── migrate_project.py
│   └── migrate_structure.py
│
└── __init__.py
```

---

## 3. 分组理由

### 3.1 core/ - 核心流程脚本 (8 个)

**定义**: 直接参与五阶段研究流程控制的脚本

| 脚本 | 用途 | 归属理由 |
|------|------|---------|
| `init_research_project.py` | 初始化研究项目 | 入口点，创建项目结构 |
| `run_stage_loop.py` | 运行阶段循环 | 核心流程控制器 |
| `quality_gate.py` | 质量门控评估 | 阶段转换决策 |
| `validate_handoff.py` | 验证阶段切换 | 阶段切换检查 |
| `phase_handoff.py` | 管理阶段交接摘要 | 阶段间数据传递 |
| `pivot_manager.py` | Pivot 提案和审核 | 流程方向控制 |
| `recover_stage.py` | 阶段恢复 | 异常恢复机制 |
| `apply_overlay.py` | 激活演化 overlay | 流程演化控制 |

**特点**:
- 每个脚本都涉及阶段状态转换
- 用户直接调用的主要入口
- 业务逻辑核心

### 3.2 runtime/ - 运行时脚本 (7 个)

**定义**: 支持运行时监控、任务执行和可视化的脚本

| 脚本 | 用途 | 归属理由 |
|------|------|---------|
| `generate_dashboard.py` | 生成仪表盘 | 运行时可视化 |
| `generate_statusline.py` | 生成状态行 | 运行时状态显示 |
| `schedule_jobs.py` | 任务调度 | 运行时任务管理 |
| `run_remote_job.py` | 执行远程任务 | 运行时任务执行 |
| `sentinel.py` | 哨兵监控 | 运行时监控 |
| `run_citation_audit.py` | 引用审计 | 论文阶段运行时任务 |

**特点**:
- 支持运行时操作
- 不直接控制阶段转换
- 可后台运行或异步执行

### 3.3 utils/ - 工具脚本 (10 个)

**定义**: 通用工具、辅助功能和迁移脚本

| 脚本 | 用途 | 归属理由 |
|------|------|---------|
| `orchestrator_common.py` | 公共函数和常量 | 被所有脚本依赖 |
| `exceptions.py` | 异常定义 | 基础设施 |
| `materialize_templates.py` | 实例化模板 | 工具函数 |
| `render_agent_prompt.py` | 渲染 Agent Prompt | 工具函数 |
| `verify_system.py` | 系统完整性验证 | 辅助功能 |
| `audit_system.py` | 系统审计 | 辅助功能 |
| `show_version.py` | 显示版本 | 辅助功能 |
| `analyze_project.py` | 分析现有项目 | 迁移辅助 |
| `migrate_project.py` | 迁移项目 | 迁移工具 |
| `migrate_structure.py` | 迁移目录结构 | 迁移工具 |

**特点**:
- 不涉及主要业务流程
- 被其他脚本调用或独立使用
- 迁移工具单独分组

---

## 4. 依赖关系分析

### 4.1 导入依赖图

```
orchestrator_common.py  ←── 所有脚本
exceptions.py           ←── 多个脚本

core/
├── init_research_project.py ──→ orchestrator_common
├── run_stage_loop.py ──→ orchestrator_common, quality_gate
├── quality_gate.py ──→ orchestrator_common
├── validate_handoff.py ──→ orchestrator_common
├── phase_handoff.py ──→ orchestrator_common
├── pivot_manager.py ──→ orchestrator_common, exceptions, generate_dashboard
├── recover_stage.py ──→ orchestrator_common
└── apply_overlay.py ──→ orchestrator_common, exceptions, generate_dashboard

runtime/
├── generate_dashboard.py ──→ orchestrator_common
├── generate_statusline.py ──→ orchestrator_common
├── schedule_jobs.py ──→ orchestrator_common, exceptions
├── run_remote_job.py ──→ exceptions
├── sentinel.py ──→ orchestrator_common
└── run_citation_audit.py ──→ orchestrator_common, generate_dashboard

utils/
├── orchestrator_common.py ──→ (无内部依赖)
├── exceptions.py ──→ (无依赖)
├── materialize_templates.py ──→ orchestrator_common
├── render_agent_prompt.py ──→ orchestrator_common
├── verify_system.py ──→ orchestrator_common
├── audit_system.py ──→ orchestrator_common
├── show_version.py ──→ orchestrator_common
├── analyze_project.py ──→ orchestrator_common
├── migrate_project.py ──→ orchestrator_common, analyze_project
└── migrate_structure.py ──→ orchestrator_common
```

### 4.2 关键发现

1. `orchestrator_common.py` 是所有脚本的基础依赖
2. `exceptions.py` 被多个脚本依赖
3. `generate_dashboard.py` 被 `pivot_manager.py` 和 `run_citation_audit.py` 依赖
4. 迁移脚本 (`analyze_project.py`, `migrate_project.py`) 有内部依赖

---

## 5. 迁移风险评估

### 5.1 高风险项

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 导入路径变更 | 所有脚本需要更新 import 语句 | 使用 `__init__.py` 重导出 |
| 测试失败 | 现有 230+ 测试可能失败 | 更新测试中的导入路径 |
| CI/CD 失败 | GitHub Actions 工作流可能失败 | 更新工作流中的脚本路径 |

### 5.2 中风险项

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 文档过时 | README/CLAUDE.md 中的路径过时 | 同步更新所有文档 |
| 用户习惯 | 用户可能仍使用旧路径 | 保留顶层兼容脚本（软链接） |
| 调试困难 | 开发者不熟悉新结构 | 添加 README 说明 |

### 5.3 低风险项

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| IDE 配置 | 可能有路径相关的配置 | 更新 .vscode/.idea 配置 |
| 脚本参数 | 脚本参数不变 | 无需修改 |

---

## 6. 迁移步骤（设计）

### 6.1 Phase 1: 准备工作

1. 创建子目录结构
2. 创建 `__init__.py` 文件
3. 更新 `pyproject.toml` 中的包配置

### 6.2 Phase 2: 迁移脚本

1. 移动脚本到对应目录
2. 更新导入语句
3. 添加兼容性导入（可选）

### 6.3 Phase 3: 更新依赖

1. 更新测试文件导入
2. 更新文档中的路径
3. 更新 CI/CD 工作流

### 6.4 Phase 4: 验证

1. 运行完整测试套件
2. 验证 CI/CD 通过
3. 手动测试主要命令

---

## 7. 兼容性方案

### 7.1 方案 A: 软链接兼容

在顶层 `scripts/` 保留软链接指向新位置：

```bash
scripts/init_research_project.py -> core/init_research_project.py
```

### 7.2 方案 B: 导入重导出

在 `scripts/__init__.py` 中重导出：

```python
from scripts.core.init_research_project import main as init_research_main
```

### 7.3 方案 C: 完全迁移

不保留兼容层，直接更新所有引用。

**推荐**: 方案 A + B 混合使用

---

## 8. 建议

### 8.1 暂缓迁移理由

1. 当前结构虽扁平，但功能完整
2. 迁移成本较高，收益相对有限
3. 优先级低于功能开发和测试覆盖率提升

### 8.2 迁移触发条件

建议在以下情况执行迁移：

1. 新增大规模脚本（>10 个）时
2. 需要跨平台支持时
3. 有明确的模块化需求时
4. 团队规模扩大需要更清晰的组织时

### 8.3 替代方案

如果不迁移目录，可以：

1. 在 `scripts/README.md` 中添加分类说明
2. 在 CLAUDE.md 中添加脚本分类表
3. 使用命名前缀区分（如 `core_init.py`）

---

## 9. 总结

| 方面 | 评估 |
|------|------|
| 新结构清晰度 | ✅ 高 |
| 迁移成本 | ⚠️ 中高 |
| 收益 | ⚠️ 中 |
| 风险 | ⚠️ 中 |
| 优先级 | 📋 低 |

**建议**: 暂缓执行迁移，先完成功能开发和测试覆盖率提升。