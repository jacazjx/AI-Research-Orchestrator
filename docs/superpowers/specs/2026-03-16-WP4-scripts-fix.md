# Work Package 4: Python 脚本修复

**目标**: 修复代码中的 bug、统一阶段名称、提取重复代码、改进错误处理

**预估工作量**: 大 (2-3小时)

---

## 修改文件清单

| 文件 | 修复类型 |
|------|---------|
| `scripts/run_stage_loop.py` | CRITICAL bug |
| `scripts/pivot_manager.py` | CRITICAL bug |
| `scripts/orchestrator_common.py` | 新增公共函数 |
| `scripts/run_remote_job.py` | 硬编码路径 |
| `scripts/sentinel.py` | 错误处理 |
| `scripts/quality_gate.py` | 重复代码 |
| `scripts/generate_statusline.py` | 重复代码 |
| 其他 17 个脚本 | 次要修复 |

---

## 具体任务

### 4.1 修复 CRITICAL: KeyError 风险 (run_stage_loop.py)

**文件**: `scripts/run_stage_loop.py`
**位置**: 第 351-365 行

**当前代码**:
```python
def _completion_percent(phase_name: str) -> int:
    return {
        "survey": 20,
        "pilot": 40,
        "experiments": 60,
        "paper": 80,
        "reflection": 100,
    }[phase_name]  # KeyError 风险
```

**修复方案**:
```python
def _completion_percent(phase_name: str) -> int:
    phase_progress = {
        "survey": 20,
        "pilot": 40,
        "experiments": 60,
        "paper": 80,
        "reflection": 100,
        # Legacy names for backward compatibility
        "01-survey": 20,
        "02-pilot-analysis": 40,
        "03-experiments": 60,
        "04-paper": 80,
        "05-reflection": 100,
    }
    if phase_name not in phase_progress:
        raise ValueError(f"Unknown phase name: {phase_name}")
    return phase_progress[phase_name]
```

---

### 4.2 修复 CRITICAL: 阶段名称不一致 (pivot_manager.py)

**文件**: `scripts/pivot_manager.py`
**位置**: 第 108-119 行

**当前代码**:
```python
if pivot_type == "downgrade_to_pilot":
    state["current_phase"] = "02-pilot-analysis"  # Legacy name
    state["phase"] = "02-pilot-analysis"
```

**修复方案**:
```python
if pivot_type == "downgrade_to_pilot":
    state["current_phase"] = "pilot"  # Semantic name
    state["phase"] = "pilot"
```

检查文件中所有使用 legacy 阶段名称的地方并统一改为语义名称。

---

### 4.3 提取公共函数: 阶段名称映射 (orchestrator_common.py)

**问题**: 阶段名称映射在以下 4 个文件中重复定义：
- `generate_statusline.py` 第 57-69, 72-84 行
- `pivot_manager.py` 第 124-138 行
- `quality_gate.py` 第 107-120 行
- `run_stage_loop.py` 第 39-52 行

**修复方案**: 在 `orchestrator_common.py` 中添加公共函数：

```python
# Phase name mapping (legacy to semantic)
LEGACY_TO_SEMANTIC_PHASE = {
    "01-survey": "survey",
    "02-pilot-analysis": "pilot",
    "03-experiments": "experiments",
    "04-paper": "paper",
    "05-reflection": "reflection",
}

SEMANTIC_TO_LEGACY_PHASE = {v: k for k, v in LEGACY_TO_SEMANTIC_PHASE.items()}

def normalize_phase_name(phase_name: str) -> str:
    """Convert legacy phase name to semantic name."""
    return LEGACY_TO_SEMANTIC_PHASE.get(phase_name, phase_name)

def get_legacy_phase_name(phase_name: str) -> str:
    """Convert semantic phase name to legacy name."""
    return SEMANTIC_TO_LEGACY_PHASE.get(phase_name, phase_name)

def get_all_phase_aliases(phase_name: str) -> list[str]:
    """Get all valid names for a phase (semantic + legacy)."""
    semantic = normalize_phase_name(phase_name)
    legacy = get_legacy_phase_name(semantic)
    if semantic == legacy:
        return [semantic]
    return [semantic, legacy]
```

然后修改其他 4 个文件，导入并使用这些函数。

---

### 4.4 修复硬编码路径 (run_remote_job.py)

**文件**: `scripts/run_remote_job.py`
**位置**: 第 73-76 行

**当前代码**:
```python
log_dir = project_root / "00-admin/runtime/logs"
```

**修复方案**:
```python
log_dir = project_root / ".autoresearch/runtime/logs"
```

同时检查文件中是否有其他硬编码的旧路径。

---

### 4.5 改进错误处理 (sentinel.py)

**文件**: `scripts/sentinel.py`
**位置**: 第 36-48 行

**当前代码**:
```python
registry = read_yaml(registry_path)
```

**修复方案**:
```python
try:
    registry = read_yaml(registry_path)
except yaml.YAMLError as e:
    print(json.dumps({
        "status": "error",
        "error": f"Invalid YAML in registry: {e}",
        "registry_path": str(registry_path)
    }))
    return
except FileNotFoundError:
    print(json.dumps({
        "status": "error",
        "error": "Registry file not found",
        "registry_path": str(registry_path)
    }))
    return
```

---

### 4.6 提取魔法数字为常量 (sentinel.py)

**文件**: `scripts/sentinel.py`
**位置**: 第 27 行

**当前代码**:
```python
stale_after = stale_after_minutes or int(config["runtime"].get("stale_after_minutes", 30))
```

**修复方案**: 在文件顶部添加常量：
```python
# Default stale threshold in minutes
DEFAULT_STALE_AFTER_MINUTES = 30
```

然后使用：
```python
stale_after = stale_after_minutes or int(config["runtime"].get("stale_after_minutes", DEFAULT_STALE_AFTER_MINUTES))
```

---

### 4.7 统一 JSON 输出格式

检查所有脚本中 `json.dumps()` 的使用，统一格式：

```python
# 标准 JSON 输出格式
print(json.dumps(result, ensure_ascii=False, indent=2))
```

需要修改的文件：
- `analyze_project.py`
- `audit_system.py`
- 其他使用 JSON 输出的脚本

---

### 4.8 修复异常消息访问 (run_remote_job.py)

**文件**: `scripts/run_remote_job.py`
**位置**: 第 95 行

**当前代码**:
```python
stderr_text = f"{type(exc).__name__}: {exc.message}"
```

**修复方案**:
```python
stderr_text = f"{type(exc).__name__}: {str(exc)}"
```

---

### 4.9 添加输入验证 (schedule_jobs.py)

**文件**: `scripts/schedule_jobs.py`
**位置**: `schedule_job` 函数

**修复方案**:
```python
def schedule_job(command: str, cwd: str | None = None, ...) -> dict[str, object]:
    # Input validation
    if not command or not command.strip():
        return {"status": "error", "error": "Command cannot be empty"}

    if cwd and not Path(cwd).exists():
        return {"status": "error", "error": f"Working directory does not exist: {cwd}"}

    # ... rest of function
```

---

## 验收标准

- [ ] `_completion_percent()` 不再有 KeyError 风险
- [ ] `pivot_manager.py` 使用语义阶段名称
- [ ] `orchestrator_common.py` 包含阶段名称映射函数
- [ ] 4 个重复定义阶段映射的文件已重构
- [ ] `run_remote_job.py` 使用新目录结构
- [ ] `sentinel.py` 有完善的错误处理
- [ ] 魔法数字已提取为常量
- [ ] JSON 输出格式统一
- [ ] 所有测试通过: `python -m pytest tests/ -v`

---

## 注意事项

- 修改 `orchestrator_common.py` 后，其他脚本需要更新导入
- 运行 `python -m mypy scripts/ --ignore-missing-imports` 检查类型
- 运行 `python -m pytest tests/ -v` 确保测试通过
- 此工作包与 WP-1 有文件重叠 (`orchestrator_common.py`)，但修改不同区域