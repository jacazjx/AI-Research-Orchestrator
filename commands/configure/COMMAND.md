---
name: configure
description: "配置系统参数，包括研究Idea、GPU配置、循环次数等"
script: scripts/configure_project.py
triggers:
  - "configure"
  - "配置"
  - "设置参数"
  - "config"
  - "修改配置"
phase: any
agents: []
arguments:
  required:
    - name: project-root
      description: 研究项目根目录的绝对路径
      type: path
  optional:
    - name: action
      description: 配置操作 (show, set, interactive)
      type: enum
      values: [show, set, interactive]
      default: show
    - name: key
      description: 配置键名 (如 idea, max-loops, gpu)
      type: string
    - name: value
      description: 配置值
      type: string
    - name: scope
      description: 配置作用域 (project, user)
      type: enum
      values: [project, user]
      default: project
---

# 配置系统参数

让用户设置系统的各项参数，包括研究Idea、GPU配置、各阶段最大循环次数等。

## 使用场景

- 修改研究Idea
- 调整阶段最大循环次数
- 配置GPU资源
- 修改语言设置
- 更新作者信息

## 用法

```bash
# 显示当前配置
python3 scripts/configure_project.py --project-root /abs/path

# 交互式配置
python3 scripts/configure_project.py --project-root /abs/path --action interactive

# 设置特定配置项
python3 scripts/configure_project.py --project-root /abs/path --action set --key idea --value "新研究想法"
python3 scripts/configure_project.py --project-root /abs/path --action set --key max-loops --value 5

# 配置GPU
python3 scripts/configure_project.py --project-root /abs/path --action set --key gpu --value "gpu-001"
```

## 配置分类

### 项目级配置 (修改 .autoresearch/config/)

| 配置键 | 说明 | 类型 |
|--------|------|------|
| `idea` | 研究Idea | string |
| `research-type` | 研究类型 | enum: ml_experiment, theory, survey, applied |
| `max-loops` | 阶段最大循环次数 | int (1-10) |
| `language` | 语言设置 | string: "process,lang" |
| `starting-phase` | 起始阶段 | enum: survey, pilot, experiments, paper, reflection |
| `gpu` | 计算资源GPU ID | string |

### 用户级配置 (修改 ~/.autoresearch/)

| 配置键 | 说明 | 类型 |
|--------|------|------|
| `author.name` | 作者姓名 | string |
| `author.email` | 作者邮箱 | string |
| `author.institution` | 所属机构 | string |
| `preferences.venue` | 默认投稿期刊/会议 | string |

## 执行流程

1. **解析参数** - 确定操作类型和配置项
2. **加载现有配置** - 读取项目配置和用户配置
3. **执行操作**
   - `show`: 显示当前配置
   - `set`: 更新配置值
   - `interactive`: 启动交互式配置向导
4. **验证配置** - 检查配置值的有效性
5. **保存配置** - 写入配置文件
6. **输出结果** - 显示更新后的配置

## 交互式配置向导

```
⚙️  配置管理
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

当前配置:
┌─────────────────────────────────────────┐
│ 项目配置                                 │
├─────────────────────────────────────────┤
│ Idea: 基于Transformer的时间序列预测      │
│ 类型: ml_experiment                      │
│ 最大循环: 3                              │
│ GPU: RTX 4090 (gpu-001)                 │
│ 语言: 过程/zh-CN, 论文/en-US             │
└─────────────────────────────────────────┘

请选择要修改的配置:
1. 修改研究Idea
2. 修改研究类型
3. 修改最大循环次数
4. 配置GPU资源
5. 修改语言设置
6. 修改作者信息
7. 保存并退出
8. 放弃修改

选择 [1-8]:
```

## 配置优先级

优先级从高到低：
1. 命令行参数 (--max-loops=5)
2. 项目配置 (.autoresearch/config/)
3. 用户配置 (~/.autoresearch/)
4. 系统默认值

## 错误处理

- **配置键不存在**: 提示可用的配置键
- **配置值无效**: 显示期望的类型和范围
- **权限不足**: 提示需要的权限
- **配置文件损坏**: 提供修复建议