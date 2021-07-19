import sys
from pathlib import Path
import runpy

sys.path.append(str(Path().absolute()))

for f in Path("nix").rglob("*"):
	if f.is_file() and f.name.endswith("nox.py"):
		runpy.run_path(str(f))