# AI-Research-Orchestrator 系统审查报告

**审查时间**: 2026-03-20
**审查目标**: AI-Research-Orchestrator 插件的整体架构、流程设计、逻辑一致性、系统闭环性

---

## 一、整体评分

| 维度 | 分数 | 说明 |
|------|------|------|
| 规范性 | 8/10 | 结构清晰，命名规范，但有少量不一致 |
| 完善性 | 8/10 | 功能完备，覆盖全面，测试充分 |
| 逻辑合理性 | 9/10 | 架构设计合理，职责清晰 |
| 流程科学性 | 9/10 | 五阶段流程符合研究方法论 |
| 系统闭环性 | 9/10 | 状态机完整，回滚机制健全 |

**综合评分: 8.6/10**

---

## 二、优点分析

### 2.1 架构设计优秀

**双循环运行时设计**
```
Outer Loop (Orchestrator): 阶段协调、Gate决策、状态管理
    └── Inner Loop (Per Phase): Primary ↔ Reviewer 直接交互
```

- **职责分离清晰**: Orchestrator 只做协调，不执行研究任务
- **Agent Teams 架构**: 使用 team_name 实现直接通信，避免消息中继
- **Battle 机制**: 3轮辩论后仲裁，保证质量同时允许合理争议

### 2.2 五阶段流程科学

| 阶段 | 目的 | Agent配对 | 符合研究方法论 |
|------|------|-----------|---------------|
| Survey | 文献调研+理论推导 | Survey ↔ Critic | ✅ 符合 |
| Pilot | 问题验证+低成本实验 | Code ↔ Adviser | ✅ 符合 |
| Experiments | 全量实验+证据收集 | Code ↔ Adviser | ✅ 符合 |
| Paper | 论文撰写+引用审核 | Writer ↔ Reviewer | ✅ 符合 |
| Reflection | 经验提取+系统改进 | Reflector ↔ Curator | ✅ 符合 |

**Survey阶段包含理论推导**: 这是关键优势，确保研究有扎实的理论基础

### 2.3 Gate机制完善

**五个Gate的定义清晰**:
- Gate 1: 研究准备度 → 文献覆盖、新意声明、验证路径
- Gate 2: Pilot验证 → 假设可测试、结果可解释
- Gate 3: 实验证据 → 结果可追溯、负结果诚实记录
- Gate 4: 论文质量 → 引用真实性、声明确有证据
- Gate 5: 反思闭环 → 改进建议可追溯、安全可控

**阻塞条件明确**:
- 伪造引用 → 自动阻塞
- 无法验证的假设 → 自动阻塞
- 隐藏负结果 → 自动阻塞

### 2.4 状态管理健壮

**单点真相**:
- `.autoresearch/state/research-state.yaml` 是唯一状态源
- 状态迁移路径明确: `1.0.0 → 1.1.0 → 1.12.0 → 2.0.0`
- 后向兼容: 旧阶段名仍支持

**GitMem版本追踪**:
- 轻量级版本控制，不污染主repo
- 支持检查点、回滚、历史查看

### 2.5 测试覆盖充分

**46个测试文件**，覆盖:
- 核心功能: quality_gate, validate_handoff, run_stage_loop
- 状态管理: state_migrator, state_schema
- 特性功能: gitmem, aris_state, citation_audit
- 集成测试: integration_gate_chain, substep_integration

---

## 三、发现的问题

### 3.1 问题1: Agent名称定义不一致

**问题描述**:
`PHASE_AGENT_PAIRS` 定义与实际 SKILL.md 不完全匹配。

**phases.py 定义**:
```python
PHASE_AGENT_PAIRS = {
    "paper": ("paper-writer", "reviewer-editor"),  # 带连字符
}
```

**实际 SKILL.md 文件**:
```
skills/writer/SKILL.md   → name: airesearchorchestrator:writer
skills/reviewer/SKILL.md → name: airesearchorchestrator:reviewer
```

**影响**: 中等。Agent spawn 时可能使用错误的 subagent_type。

**建议**: 统一使用无连字符命名，或在 spawn 时做名称转换。

### 3.2 问题2: 问题验证子步骤定义不完整

**问题描述**:
`phase-execution-details.md` 提到 Pilot 阶段有 `problem_validation` 子步骤，但 `_build_default_substep_status()` 中 `pilot` 的子步骤是:

```python
"pilot": {
    "problem_analysis": {...},
    "pilot_design": {...},
    "pilot_execution": {...},
}
```

缺少 `problem_validation` 子步骤。

**影响**: 低。功能不受影响，但文档与代码不一致。

**建议**: 在 `_build_default_substep_status()` 中添加 `problem_validation` 子步骤。

### 3.3 问题3: Hooks配置不完整

**问题描述**:
`hooks/hooks.json` 只配置了:
- SessionStart (startup/resume)
- PostToolUse (Write)

缺少：
- `TeammateIdle` hook (Agent Teams idle 通知)
- `TaskCompleted` hook (任务完成验证)

**影响**: 低。Agent Teams 功能可能无法自动触发 Orchestrator 检查。

**建议**: 添加 hooks 配置:
```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "matcher": "*",
        "hooks": [
          {"type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/hooks/teammate_idle.py\""}
        ]
      }
    ]
  }
}
```

### 3.4 问题4: 文献搜索工具依赖说明不足

**问题描述**:
`literature-verification.md` 要求使用学术API，但：
- 未说明如何配置API密钥
- 未提供错误处理示例
- Semantic Scholar API 有速率限制，文档未提及

**影响**: 低。高级用户可自行处理，但新手可能困惑。

**建议**: 添加API配置和错误处理指南。

### 3.5 问题5: 回滚阶段的交付物处理

**问题描述**:
当 Gate 拒绝并回滚到早期阶段时，已产生的交付物如何处理？

- 是否删除后续阶段的交付物？
- 是否保留在 `.autoresearch/archive/`？

**当前状态**:
`reset_state_for_phase()` 重置状态，但不处理文件系统。

**影响**: 中等。可能导致交付物与状态不一致。

**建议**: 明确回滚时的文件处理策略，或在文档中说明。

---

## 四、系统闭环性分析

### 4.1 正向闭环 ✅

```
Idea → Survey → Pilot → Experiments → Paper → Reflection → Close
  ↓      ↓        ↓         ↓          ↓         ↓
Gate1  Gate2    Gate3     Gate4      Gate5    (human)
```

### 4.2 反馈闭环 ✅

- **Inner Loop**: Primary ↔ Reviewer 迭代 (max 3 rounds)
- **Battle Phase**: 正式辩论机制
- **Gate Escalation**: 人类介入决策

### 4.3 回滚闭环 ✅

```
                    ┌─────────────────────┐
                    │   任意阶段 Gate N    │
                    └──────────┬──────────┘
                               │ reject
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
         ┌─────────┐     ┌─────────┐      ┌─────────┐
         │ REVISE  │     │ ROLLBACK│      │  PIVOT  │
         │ (同阶段) │     │ (回早期) │      │ (换方向) │
         └────┬────┘     └────┬────┘      └────┬────┘
              │               │                │
              └───────────────┴────────────────┘
                              │
                              ▼
                       返回阶段继续迭代
```

### 4.4 自进化闭环 ✅

Reflection 阶段产生:
- `lessons-learned.md` → 可复用经验
- `overlay-draft.md` → 系统改进提案
- `runtime-improvement-report.md` → 需人工批准后生效

**关键安全机制**: Overlay 修改必须经过 Gate 5 批准，不能静默生效。

---

## 五、与最佳实践对比

### 5.1 相比 AI-Researcher 框架

| 特性 | AI-Research-Orchestrator | AI-Researcher |
|------|--------------------------|---------------|
| 阶段数 | 5 | 3 |
| Agent数量 | 每阶段2个 | 多个专业Agent |
| 人类Gate | 5个强制 | 可选 |
| Battle机制 | ✅ 有 | ❌ 无 |
| 状态持久化 | ✅ YAML | 内存 |
| 回滚支持 | ✅ 有 | ❌ 无 |

### 5.2 相比 Sibyl 框架

| 特性 | AI-Research-Orchestrator | Sibyl |
|------|--------------------------|-------|
| 任务分解 | 子步骤 | Stage |
| 引用验证 | ✅ 强制 | ⚠️ 可选 |
| 负结果处理 | ✅ 强制记录 | 未明确 |

---

## 六、改进建议

### 6.1 短期改进 (优先级高)

1. **统一Agent命名** - 解决 phases.py 与 SKILL.md 不一致
2. **完善Hooks配置** - 添加 TeammateIdle 和 TaskCompleted hooks
3. **补充 problem_validation 子步骤** - 使代码与文档一致

### 6.2 中期改进 (优先级中)

4. **添加回滚文件策略** - 明确 Gate 拒绝时的文件处理
5. **API密钥配置指南** - 在文档中说明学术API使用方法

### 6.3 长期改进 (可选)

6. **实验可复现性增强** - 自动生成 Dockerfile 或 conda env
7. **跨项目知识迁移** - 支持从历史项目复用 lessons

---

## 七、结论

AI-Research-Orchestrator 是一个设计精良的 AI 研究流程编排系统。其五阶段流程设计符合学术研究方法论，双循环架构实现了高效的职责分离，Gate 机制保证了研究质量，状态管理健壮且支持回滚。

主要优势:
- 理论推导环节的引入，使研究有扎实基础
- Battle 机制允许合理争议，避免过早否决
- 引用真实性强制验证，防止学术不端
- 负结果必须记录，保证研究诚信

需要改进的地方:
- Agent命名需要统一
- Hooks配置需要完善
- 回滚时的文件处理策略需要明确

总体而言，该系统已达到生产可用状态，推荐在经过上述短期改进后正式使用。