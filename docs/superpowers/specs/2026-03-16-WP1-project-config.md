# Work Package 1: 项目配置修复

**目标**: 修复项目打包配置，确保项目可正确安装

**预估工作量**: 小 (30分钟)

---

## 修改文件清单

| 文件 | 操作 |
|------|------|
| `scripts/__init__.py` | 新建 |
| `pyproject.toml` | 修改 |
| `requirements.txt` | 修改 |
| `.gitignore` | 检查/修改 |

---

## 具体任务

### 1.1 创建 `scripts/__init__.py`

在 `scripts/` 目录下创建空的 `__init__.py` 文件：

```python
# AI Research Orchestrator Scripts Package
```

**原因**: pyproject.toml 配置将 scripts 作为包，需要 `__init__.py` 使其成为合法的 Python 包。

---

### 1.2 修复 pyproject.toml 资源文件路径

**当前配置** (第 68 行):
```toml
scripts = ["../assets/templates/**/*", "../assets/prompts/**/*"]
```

**问题**: 使用了 `../` 相对路径，可能导致打包时资源文件缺失。

**修复方案**:
```toml
[tool.setuptools.package-data]
"*" = ["assets/templates/**/*", "assets/prompts/**/*"]
```

或者确保路径相对于项目根目录正确。

---

### 1.3 统一 GitHub URL

**文件**: `pyproject.toml` 第 58-61 行

**当前**:
```toml
Homepage = "https://github.com/example/ai-research-orchestrator"
```

**修改为**:
```toml
Homepage = "https://github.com/jacazjx/AI-Research-Orchestrator"
```

确保与 `marketplace.json` 中的 URL 一致。

---

### 1.4 完善 requirements.txt

**当前内容**:
```
# AI Research Orchestrator
# Core dependencies
PyYAML>=6.0

# Development dependencies (install with: pip install -e ".[dev]")
# See pyproject.toml for the full list
```

**建议修改**:
```
# AI Research Orchestrator
# Core dependencies
PyYAML>=6.0

# Development dependencies
# Install with: pip install -e ".[dev]"
# Or manually install:
# pytest>=7.0
# black>=23.0
# isort>=5.0
# flake8>=6.0
# mypy>=1.0
# pre-commit>=3.0
```

---

### 1.5 检查 .gitignore 和 .coverage

**检查项**:
1. `.gitignore` 第 39 行已有 `.coverage` 规则
2. 如果项目根目录存在 `.coverage` 文件，需要从 git 中移除：
   ```bash
   git rm --cached .coverage
   ```

---

## 验收标准

- [ ] `pip install -e .` 成功执行
- [ ] `python -c "from scripts.orchestrator_common import load_state"` 不报错
- [ ] `pyproject.toml` 和 `marketplace.json` 的 GitHub URL 一致
- [ ] `requirements.txt` 包含完整的开发依赖说明
- [ ] `.coverage` 文件不在 git 追踪中

---

## 注意事项

- 此工作包与其他工作包无文件冲突，可安全并行
- 修改后请运行 `python -m pytest tests/ -v` 确保测试通过