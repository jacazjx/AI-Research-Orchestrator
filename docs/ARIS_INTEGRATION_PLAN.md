# ARIS Integration Plan

**Date**: 2026-03-14
**Source**: https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep
**Target Version**: v2.0.0

## Executive Summary

ARIS (Auto-claude-code-research-in-sleep) 是一个跨模型协作的自动化研究系统。本文档规划将其核心特性集成到 AI Research Orchestrator 中。

## Key Features to Integrate

### 1. Cross-Model Collaboration (P0 - Critical)

**ARIS Approach:**
- Claude Code 执行任务
- GPT-5.4 (via Codex MCP) 作为外部审查者
- 使用 `model_reasoning_effort: "xhigh"` 获得深度推理

**Integration Plan:**
- 在 `research-state.yaml` 添加 `reviewer_model` 配置
- 修改 Critic/Reviewer 角色提示，支持选择:
  - 本地 sub-agent (现有模式)
  - 外部 LLM via Codex MCP (新模式)
- 使用 `mcp__codex__codex` 和 `mcp__codex__codex-reply` 维护审查线程

**Code Changes:**
```
scripts/orchestrator_common.py
  - Add REVIEWER_MODEL constant
  - Add function: get_reviewer_config()

assets/prompts/critic.md.tmpl
  - Add section for external review mode
  - Add instructions for using Codex MCP
```

### 2. State Persistence for Long-Running Loops (P0 - Critical)

**ARIS Approach:**
- `REVIEW_STATE.json` 存储循环状态
- 包含: round, threadId, last_score, pending_experiments, timestamp
- 上下文压缩后可恢复

**Integration Plan:**
- 在 `orchestrator_common.py` 添加:
  - `REVIEW_STATE.json` 结构定义
  - `save_review_state()` / `load_review_state()` 函数
- 修改 `run_stage_loop.py` 支持:
  - 每轮后保存状态
  - 启动时检测并恢复中断的循环
- 适用于 auto-review-loop 模式

**State Schema:**
```json
{
  "phase": "02-pilot-analysis",
  "round": 2,
  "max_rounds": 4,
  "threadId": "uuid-for-codex-conversation",
  "status": "in_progress",
  "last_score": 5.5,
  "last_verdict": "almost",
  "pending_experiments": ["exp_20260314_001"],
  "timestamp": "2026-03-14T10:00:00"
}
```

### 3. Feishu Notification System (P1 - High)

**ARIS Approach:**
- 检测 `~/.claude/feishu.json` 配置文件
- 模式: `off`, `push`, `interactive`
- 通知类型: `checkpoint`, `review_scored`, `experiment_done`, `pipeline_done`

**Integration Plan:**
- 新增 `scripts/feishu_notifier.py`
- 配置文件: `~/.claude/feishu.json`
- 在关键节点调用:
  - Phase 完成
  - Gate 通过/失败
  - 审查评分更新
  - 实验完成

**Config Schema:**
```json
{
  "mode": "push",
  "webhook_url": "https://open.feishu.cn/...",
  "user_id": "ou_xxx"
}
```

### 4. Zotero/Obsidian Integration (P1 - High)

**ARIS Approach:**
- 通过 MCP 服务器连接 Zotero
- 通过 MCP 服务器连接 Obsidian vault
- 在 research-lit skill 中使用

**Integration Plan:**
- 修改 `assets/prompts/survey.md.tmpl`:
  - 添加 Zotero MCP 指令
  - 添加 Obsidian MCP 指令
- 检测 MCP 可用性并优雅降级
- 支持从 Zotero 导出 BibTeX

### 5. Experiment Deployment Workflow (P2 - Medium)

**ARIS Approach (run-experiment skill):**
1. 环境检测 (本地/远程)
2. GPU 可用性检查
3. 代码同步 (rsync)
4. Screen/tmux 部署
5. 进程验证

**Integration Plan:**
- 增强 `assets/prompts/code.md.tmpl`:
  - 添加完整的远程部署流程
  - 添加 GPU 资源管理
  - 添加进程监控
- 已在 v1.10.0 添加部分内容，需扩展

### 6. Paper Writing Pipeline (P2 - Medium)

**ARIS Approach (paper-writing workflow):**
```
/paper-plan → /paper-figure → /paper-write → /paper-compile → /auto-paper-improvement-loop
```

**Integration Plan:**
- 在 Phase 04-paper 中集成 ARIS 的 paper-writing workflow
- 修改 `assets/prompts/paper-writer.md.tmpl`:
  - 添加 Claims-Evidence Matrix
  - 添加自动化图表生成
  - 添加 LaTeX 编译流程
- 修改 `assets/prompts/reviewer.md.tmpl`:
  - 添加 improvement-loop 逻辑

## Architecture Comparison

| Dimension | ARIS | AI Research Orchestrator |
|-----------|------|--------------------------|
| Phases | 3 workflows | 5 phases (01-survey ~ 05-reflection) |
| Review Mode | GPT-5.4 cross-model | Local sub-agent |
| State Management | REVIEW_STATE.json | research-state.yaml |
| Paper Writing | Built-in pipeline | Phase 04-paper |
| Experiment Mgmt | run-experiment skill | Phase 02/03 |
| Iteration Control | MAX_ROUNDS + score | ralph-loop + gate |
| External Integration | Feishu, Zotero, Obsidian | None |

## Integration Priorities

| Priority | Feature | Effort | Impact |
|----------|---------|--------|--------|
| P0 | Cross-model review | Medium | High |
| P0 | State persistence | Low | High |
| P1 | Feishu notifications | Low | Medium |
| P1 | Zotero/Obsidian | Medium | Medium |
| P2 | Experiment deployment | Low | Medium |
| P2 | Paper writing pipeline | High | High |

## Version Roadmap

### v1.11.0 - Foundation ✅ COMPLETED
- [x] Add REVIEW_STATE.json structure
- [x] Add `save_review_state()` / `load_review_state()` functions
- [x] Update `orchestrator_common.py` with reviewer_model config
- [x] Add Cross-Model Review Mode section to `critic.md.tmpl`
- [x] Add state persistence guidance for long-running loops

### v1.12.0 - Cross-Model Review (Next)
- [ ] Add Codex MCP integration for Critic role
- [ ] Add `mcp__codex__codex` and `mcp__codex__codex-reply` instructions
- [ ] Test cross-model review workflow

### v1.13.0 - Notifications & Integration
- [ ] Add Feishu notification module
- [ ] Add Zotero MCP integration to survey phase
- [ ] Add Obsidian MCP integration

### v2.0.0 - Full Integration
- [ ] Integrate paper-writing pipeline
- [ ] Full auto-review-loop with state persistence
- [ ] Complete documentation update

## Testing Strategy

1. **Unit Tests**: 新增函数的单元测试
2. **Integration Tests**: 跨模型审查流程测试
3. **E2E Tests**: 完整研究流程测试（使用 mock Codex MCP）

## Rollback Plan

- 所有新特性通过配置开关控制
- 默认使用现有模式
- 可随时关闭新特性回退到稳定版本