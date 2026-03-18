---
name: insight
description: "交互式意图澄清，帮助用户明确研究想法"
script: scripts/run_insight.py
triggers:
  - "insight"
  - "澄清意图"
  - "明确想法"
  - "clarify intent"
  - "研究想法"
phase: init
agents: []
arguments:
  required: []
  optional:
    - name: project-root
      description: 研究项目根目录的绝对路径 (可选，如不提供则检测当前目录)
      type: path
    - name: idea
      description: 初始研究想法
      type: string
    - name: interactive
      description: 是否启用交互模式
      type: boolean
      default: true
    - name: max-rounds
      description: 最大澄清轮数
      type: int
      default: 5
    - name: json
      description: 输出JSON格式
      type: boolean
      default: false
---

# 交互式意图澄清

和用户进行反复交互，询问用户问题，搞清楚用户的真实意图。

## 使用场景

- 新研究项目启动前明确研究方向
- 研究想法模糊，需要细化
- 验证研究想法的可行性
- 识别研究约束和目标

## 用法

```bash
# 交互式澄清 (默认)
python3 scripts/run_insight.py

# 带初始想法启动
python3 scripts/run_insight.py --idea "我想研究时间序列预测"

# 指定项目路径
python3 scripts/run_insight.py --project-root /abs/path/to/project

# 非交互模式 (仅评估)
python3 scripts/run_insight.py --idea "研究想法" --interactive false --json
```

## 执行流程

```
/insight
    │
    ├─→ 1. 检测是否有现有项目
    │       ├─→ 有: 基于现有Idea继续澄清
    │       └─→ 无: 从零开始收集Idea
    │
    ├─→ 2. 意图清晰度评估
    │       └─→ 评估五个维度:
    │           ├── Problem (问题定义) - 25%
    │           ├── Solution (解决方案) - 25%
    │           ├── Contribution (贡献类型) - 20%
    │           ├── Constraints (约束条件) - 15%
    │           └── Novelty (新颖性) - 15%
    │
    ├─→ 3. 生成针对性问题
    │       └─→ 基于评分较低的维度生成问题
    │
    ├─→ 4. 交互式问答循环
    │       └─→ 直到清晰度 >= 0.7 或达到最大轮数
    │
    ├─→ 5. 判断是否需要Brainstorming
    │       └─→ 清晰度 < 0.4: 建议触发research-ideation技能
    │
    └─→ 6. 输出澄清结果
            ├── 澄清后的Idea
            ├── 清晰度评分
            ├── 各维度评分
            └── 建议的下一步
```

## 五维度评估

| 维度 | 权重 | 关键问题 |
|------|------|----------|
| Problem | 25% | 要解决什么问题？为什么重要？ |
| Solution | 25% | 可能的解决方案是什么？有什么直觉？ |
| Contribution | 20% | 想做出什么类型的贡献？成功标准是什么？ |
| Constraints | 15% | 有什么时间、资源、目标期刊约束？ |
| Novelty | 15% | 与现有工作的区别是什么？关键洞察是什么？ |

## 输出示例

```
💡 意图澄清助手
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

当前研究想法:
"我想研究时间序列预测的优化方法"

清晰度评估: 0.35/1.0 (需要进一步澄清)

维度评分:
  Problem:      0.3 ████████░░░░░░░░░░░░
  Solution:     0.2 ██████░░░░░░░░░░░░░░
  Contribution: 0.4 ████████████░░░░░░░░
  Constraints:  0.3 ████████░░░░░░░░░░░░
  Novelty:      0.5 ███████████████░░░░░

让我问您几个问题:

Q1: 您试图解决的具体问题是什么?
    (例如: 长序列预测精度低? 计算效率低? 泛化能力差?)

> 长序列预测的精度问题，特别是预测窗口超过100步时精度下降明显

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

澄清后的研究想法:
"针对长序列时间序列预测(>100步)中精度下降的问题，
提出一种改进的注意力机制，增强模型对长期依赖的捕获能力。
目标投稿ICML 2026 (截止: 2026年5月)"

清晰度评分: 0.78/1.0 ✅

维度评分:
  Problem:      0.8 ████████████████████░
  Solution:     0.7 ██████████████████░░░
  Contribution: 0.8 ████████████████████░
  Constraints:  0.9 ████████████████████░
  Novelty:      0.6 █████████████████░░░░

建议下一步:
1. 运行 /init-research 初始化项目
2. 或继续细化特定方面 (输入: /insight --focus novelty)
```

## 清晰度阈值

| 分数 | 状态 | 建议 |
|------|------|------|
| >= 0.7 | 清晰 | 可以开始研究 |
| 0.4-0.7 | 需澄清 | 继续问答循环 |
| < 0.4 | 模糊 | 建议brainstorming |

## 与其他命令的关系

- **`/init-research`** - 内部集成了insight功能
- **`/configure`** - 可修改澄清后的idea
- **research-ideation技能** - 清晰度过低时触发