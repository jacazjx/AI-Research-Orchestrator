# Work Package 2: Commands 重构

**目标**: 重构 commands 目录结构，补全必需字段，统一命令定义

**预估工作量**: 中 (1-2小时)

---

## 修改文件清单

| 文件 | 操作 |
|------|------|
| `commands/init-research.md` | 移动并重写 |
| `commands/run-survey.md` | 移动并重写 |
| `commands/run-pilot.md` | 移动并重写 |
| `commands/run-experiments.md` | 移动并重写 |
| `commands/write-paper.md` | 移动并重写 |
| `commands/reflect.md` | 移动并重写 |
| `commands/README.md` | 更新 |

---

## 具体任务

### 2.1 重构目录结构

**当前结构** (扁平文件):
```
commands/
├── init-research.md
├── run-survey.md
├── run-pilot.md
├── run-experiments.md
├── write-paper.md
├── reflect.md
└── README.md
```

**目标结构** (子目录):
```
commands/
├── init-research/
│   └── COMMAND.md
├── run-survey/
│   └── COMMAND.md
├── run-pilot/
│   └── COMMAND.md
├── run-experiments/
│   └── COMMAND.md
├── write-paper/
│   └── COMMAND.md
├── reflect/
│   └── COMMAND.md
└── README.md
```

---

### 2.2 补全 COMMAND.md 必需字段

每个 `COMMAND.md` 必须包含以下 frontmatter 字段：

```yaml
---
name: <command-name>
description: "<描述>"
script: scripts/<script-name>.py
triggers:
  - "trigger1"
  - "trigger2"
phase: <phase-name>
agents:
  - <agent1>
  - <agent2>
arguments:
  required:
    - name: <arg-name>
      description: "<描述>"
      type: <string|path|enum>
  optional:
    - name: <arg-name>
      description: "<描述>"
      type: <string|path|enum>
      default: <default-value>
---
```

---

### 2.3 各命令详细定义

#### 2.3.1 init-research/COMMAND.md

```yaml
---
name: init-research
description: "Initialize a new AI research project with proper directory structure and state management"
script: scripts/init_research_project.py
triggers:
  - "init research"
  - "start research project"
  - "初始化研究"
  - "新建研究项目"
phase: init
agents: []
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
    - name: topic
      description: Research topic or idea description
      type: string
  optional:
    - name: client-type
      description: Client type for agent execution
      type: enum
      values: [auto, codex, openai, claude]
      default: auto
---
```

#### 2.3.2 run-survey/COMMAND.md

```yaml
---
name: run-survey
description: "Run the Survey phase for literature review and research gap identification"
script: scripts/run_stage_loop.py
triggers:
  - "run survey"
  - "literature review"
  - "文献调研"
  - "开始调研"
phase: survey
agents:
  - survey
  - critic
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
  optional:
    - name: max-loops
      description: Maximum iteration loops between agents
      type: integer
      default: 3
---
```

#### 2.3.3 run-pilot/COMMAND.md

```yaml
---
name: run-pilot
description: "Run the Pilot phase for preliminary experiment validation"
script: scripts/run_stage_loop.py
triggers:
  - "run pilot"
  - "pilot experiment"
  - "Pilot验证"
  - "小规模实验"
phase: pilot
agents:
  - code
  - adviser
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
  optional:
    - name: max-loops
      description: Maximum iteration loops between agents
      type: integer
      default: 3
---
```

#### 2.3.4 run-experiments/COMMAND.md

```yaml
---
name: run-experiments
description: "Run the full Experiments phase for comprehensive evaluation"
script: scripts/run_stage_loop.py
triggers:
  - "run experiments"
  - "full experiments"
  - "完整实验"
  - "大规模实验"
phase: experiments
agents:
  - code
  - adviser
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
  optional:
    - name: max-loops
      description: Maximum iteration loops between agents
      type: integer
      default: 5
---
```

#### 2.3.5 write-paper/COMMAND.md

```yaml
---
name: write-paper
description: "Run the Paper phase for manuscript writing and review"
script: scripts/run_stage_loop.py
triggers:
  - "write paper"
  - "draft paper"
  - "写论文"
  - "论文写作"
phase: paper
agents:
  - writer
  - reviewer
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
  optional:
    - name: max-loops
      description: Maximum iteration loops between agents
      type: integer
      default: 5
---
```

#### 2.3.6 reflect/COMMAND.md

```yaml
---
name: reflect
description: "Run the Reflection phase for lessons learned and system improvement"
script: scripts/run_stage_loop.py
triggers:
  - "reflect"
  - "lessons learned"
  - "反思"
  - "总结"
phase: reflection
agents:
  - reflector
  - curator
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
  optional:
    - name: max-loops
      description: Maximum iteration loops between agents
      type: integer
      default: 2
---
```

---

### 2.4 更新 README.md

更新 `commands/README.md` 以反映新的目录结构和字段定义。

---

## 验收标准

- [ ] 6 个命令目录都已创建，各包含 `COMMAND.md`
- [ ] 所有 `COMMAND.md` frontmatter 字段完整
- [ ] 触发短语无冲突
- [ ] 脚本路径正确
- [ ] 参数定义完整
- [ ] README.md 已更新

---

## 注意事项

- 删除旧的扁平 `.md` 文件后创建新的子目录结构
- 确保触发短语与 skills/ 中的定义一致
- 此工作包与 WP-3 (Skills) 有逻辑关联但无文件冲突