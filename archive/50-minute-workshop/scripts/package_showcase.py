"""Package tracked deliverables and recorded synthetic evidence, never local credentials."""
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
tracked = subprocess.run(
    ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
).stdout.decode().split("\0")
paths = [ROOT / path for path in tracked if path]
paths += [p for p in (ROOT / "evidence").rglob("*")
          if p.is_file() and p.suffix in (".json", ".jsonl", ".txt")]
for path in paths:
    parts = path.relative_to(ROOT).parts
    if any(p in (".azure", ".venv", ".git", ".runtime") for p in parts) or path.name == ".env":
        raise ValueError(f"Local-only file unexpectedly selected: {path}")
    if path.suffix in (".json", ".jsonl", ".txt", ".md", ".py", ".yml", ".yaml", ".ps1", ".html"):
        content = path.read_text(encoding="utf-8-sig")
        for pattern in [r"InstrumentationKey=[0-9a-fA-F-]{36}",
                        r"\bgh[pousr]_[A-Za-z0-9]{30,}",
                        r"\bgithub_pat_[A-Za-z0-9_]{40,}"]:
            if re.search(pattern, content):
                raise ValueError(f"Potential live credential in package input: {path.name}")
out = ROOT.parent / "deliverables"
out.mkdir(exist_ok=True)
archive = out / "Foundry showcase - presentation and demo.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for path in sorted(set(paths)):
        if path.is_file():
            z.write(path, "foundry-showcase/" + path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:
        raise RuntimeError("Archive verification failed")
print(f"{archive} ({archive.stat().st_size:,} bytes)")
