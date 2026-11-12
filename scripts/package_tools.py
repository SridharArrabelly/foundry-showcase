"""Package only authored tool code and the existing canonical Volt fixtures."""

import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DOMAIN = ROOT / "tools" / "volt"


def main() -> None:
    artifact = ROOT / ".runtime" / "volt-tools.zip"
    artifact.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(artifact, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in ("function_app.py", "support.py", "host.json", "requirements.txt"):
            archive.write(TOOLS / name, name)
        for name in ("__init__.py", "domain.py", "data.json"):
            archive.write(DOMAIN / name, f"volt/{name}")
    print(f"{artifact}\nsha256:{hashlib.sha256(artifact.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
