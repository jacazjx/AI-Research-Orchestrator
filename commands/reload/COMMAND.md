---
name: reload
description: "重新加载项目状态和配置，恢复研究上下文"
script: scripts/reload_project.py
triggers:
  - "reload"
  - "重新加载"
  - "恢复状态"
  - "继续研究"
  - "reload project"
phase: any
agents: []
arguments:
  required:
    - name: project-root
      description: 研究项目根目录的绝对路径
      type: path
  optional:
    - name: verbose
      description: 显示详细输出
      type: boolean
      default: false
    - name: json
      description: 输出JSON格式
      type: boolean
      default: false
---

# 重新加载项目状态

当用户重新打开session后，让模型重新理解项目的目的、各项配置以及当前状态。

## 使用场景

- 新会话开始时恢复上下文
- 切换到不同项目时
- 状态文件更新后刷新
- 故障恢复后重建上下文

## 用法

```bash
python3 scripts/reload_project.py --project-root /abs/path/to/project
python3 scripts/reload_project.py --project-root /abs/path/to/project --verbose
python3 scripts/reload_project.py --project-root /abs/path/to/project --json
```

## 执行流程

1. **检测项目根目录** - 查找 `.autoresearch/` 目录
2. **加载项目状态** - 读取 `research-state.yaml`、`orchestrator-config.yaml`、`status.json`
3. **执行状态迁移** - 如需要，调用 `state_migrator.py`
4. **加载用户配置** - 读取 `~/.autoresearch/` 下的用户级配置
5. **检查GitMem历史** - 读取版本跟踪历史
6. **生成上下文摘要** - 汇总项目信息、进度、配置
7. **输出状态报告** - 格式化的状态摘要

## 输出示例

```markdown
## 项目状态重新加载

### 基本信息
- **项目ID**: my-research-project
- **主题**: 基于Transformer的时间序列预测优化
- **研究类型**: ml_experiment
- **创建时间**: 2026-03-15

### 当前进度
- **当前阶段**: pilot (阶段2/5)
- **当前Gate**: gate_2
- **完成度**: 25%

### 已完成工作
- Survey阶段完成 (得分: 4.2)
- Pilot阶段进行中

### 配置信息
- **语言**: 过程文档(zh-CN) / 论文(en-US)
- **GPU**: RTX 4090 (ID: gpu-001)
- **最大循环次数**: 3

### 下一步行动
1. 完成Pilot实验设计
2. 运行Pilot验证
3. 等待Gate 2评审
```

## 错误处理

- **项目不存在**: 提示用户先运行 `/init-research`
- **状态文件损坏**: 尝试从备份恢复或提示重新初始化
- **版本不兼容**: 自动执行状态迁移