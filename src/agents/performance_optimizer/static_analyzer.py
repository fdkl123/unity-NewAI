from __future__ import annotations

import json
import re
from pathlib import Path


def analyze_project(root: Path) -> list[dict]:
    assets = root / "Assets"
    if not assets.exists():
        return []
    findings: list[dict] = []
    for script in assets.rglob("*.cs"):
        findings.extend(analyze_csharp_file(script, root))
    return findings


def write_performance_report(root: Path, output_path: Path | None = None) -> list[dict]:
    findings = analyze_project(root)
    output_path = output_path or root / ".orchestrator" / "reports" / "performance-findings.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"findings": findings}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return findings


def analyze_csharp_file(path: Path, root: Path | None = None) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    relative = str(path.relative_to(root)) if root else str(path)
    findings: list[dict] = []
    hot_ranges = _method_ranges(lines, {"Update", "FixedUpdate", "LateUpdate"})

    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        in_hot_path = any(start <= line_no <= end for start, end in hot_ranges)
        if in_hot_path and re.search(r"\b(GetComponent|FindObjectOfType|GameObject\.Find|FindWithTag)\b", stripped):
            findings.append(_finding("cpu", "high", relative, line_no, "Expensive lookup in Unity hot path.", "Cache references in Awake/Start or inject dependencies."))
        if in_hot_path and re.search(r"\bnew\s+(List|Dictionary|HashSet|StringBuilder|WaitForSeconds)\b", stripped):
            findings.append(_finding("gc", "high", relative, line_no, "Managed allocation in Unity hot path.", "Reuse collections or cache yield instructions outside Update-like methods."))
        if in_hot_path and ("+" in stripped and "text" in stripped.lower()):
            findings.append(_finding("gc", "medium", relative, line_no, "Possible per-frame UI string concatenation.", "Update UI only on value changes and cache formatted strings."))
        if re.search(r"\bInstantiate\s*\(", stripped):
            findings.append(_finding("object_lifecycle", "medium", relative, line_no, "Instantiate call can create frame spikes if used during gameplay.", "Use prewarmed object pools for repeated runtime objects."))
        if re.search(r"\bDestroy\s*\(", stripped):
            findings.append(_finding("object_lifecycle", "medium", relative, line_no, "Destroy call can create lifecycle and GC pressure.", "Return reusable gameplay objects to pools where behavior allows."))
        if in_hot_path and re.search(r"\bPhysics\.(Raycast|SphereCast|OverlapSphere|OverlapBox)\b", stripped) and "LayerMask" not in stripped:
            findings.append(_finding("physics", "medium", relative, line_no, "Physics query in hot path without visible layer mask.", "Cache layer masks and reduce query frequency."))
        if re.search(r"\bResources\.Load\b", stripped):
            findings.append(_finding("asset_pipeline", "medium", relative, line_no, "Resources.Load makes asset dependencies implicit.", "Prefer serialized references or Addressables when content scale grows."))
    return findings


def _method_ranges(lines: list[str], names: set[str]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    pattern = re.compile(r"\b(?:void|IEnumerator)\s+(" + "|".join(names) + r")\s*\(")
    for index, line in enumerate(lines):
        if not pattern.search(line):
            continue
        depth = 0
        started = False
        for cursor in range(index, len(lines)):
            depth += lines[cursor].count("{")
            if "{" in lines[cursor]:
                started = True
            depth -= lines[cursor].count("}")
            if started and depth <= 0:
                ranges.append((index + 1, cursor + 1))
                break
    return ranges


def _finding(category: str, severity: str, path: str, line: int, evidence: str, recommendation: str) -> dict:
    return {
        "category": category,
        "severity": severity,
        "location": f"{path}:{line}",
        "evidence": evidence,
        "recommendation": recommendation,
    }
