import ast
from pathlib import Path
from collections import defaultdict

ROOT = Path(".")
OUTPUT = Path("module_dependency.mmd")

edges = defaultdict(set)

def get_module_path(py_file: Path) -> str:
    return py_file.with_suffix("").as_posix().replace("/", ".")

for py_file in ROOT.rglob("*.py"):
    if any(p in py_file.parts for p in [".env", "venv", "site-packages", "__pycache__"]) or py_file.name.startswith("."):
        continue
    module = get_module_path(py_file.relative_to(ROOT))
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"⚠️ 無法解析 {py_file}: {e}")
        continue

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                edges[module].add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                edges[module].add(node.module)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("```mermaid\ngraph TD\n")
    for src, tgts in edges.items():
        for tgt in tgts:
            if tgt.startswith(("ui", "core", "data", "agent")):
                f.write(f'  "{src}" --> "{tgt}"\n')
    f.write("```")

print(f"✅ Mermaid 模組相依圖已輸出至：{OUTPUT.resolve()}")
